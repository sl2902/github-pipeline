import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from trino import dbapi
from trino.dbapi import connect
from trino import exceptions
# from google.oauth2 import service_account
# from google.cloud import bigquery
import os, sys
import json
from dotenv import load_dotenv

page_title = "GitHub repository trends"
st.set_page_config(
    page_title=page_title,
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

def create_trino_connection() -> dbapi.Connection:
    """Create a Trino db connection"""
    try:
        conn = connect(
            host="localhost",
            port=1080,
            user="admin",
            catalog="iceberg",
            schema="bronze",
        )
    except exceptions.TrinoConnectionError as e:
        raise(f"Trino connection to iceberg failed: {e}")
    return conn

@st.cache_data(ttl=600)
def execute_query(qry: str) -> pd.DataFrame:
    cur = conn.cursor()
    try:
        cur.execute(qry)
    except exceptions.TrinoQueryError as e:
        raise(f"Query {qry} failed: {e}")
    cols = [col.name for col in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    return df

conn = create_trino_connection()
last_7_days = """
        select 
            repo,
            created_at,
            issue_count
        from 
            iceberg.bronze.last_7_days_fct_issues 
        """
result_set = execute_query(last_7_days)
# print(pd.DataFrame(result_set).head())


# Line chart
def make_linechart(input_df, input_x=None, input_y=None, input_color=None):
    # https://stackoverflow.com/questions/53287928/tooltips-in-altair-line-charts
    highlight = alt.selection_point(on='pointerover', fields=[input_color], nearest=True)
    linechart = alt.Chart(input_df).mark_line().encode(
            alt.X(f"yearmonthdate({input_x}):T", axis=alt.Axis(title="Creation date", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            alt.Y(f"{input_y}:Q", axis=alt.Axis(title="Count of issues", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            color=f"{input_color}:N", #alt.value('gold'),
            tooltip=[alt.Tooltip(f"{input_y}:Q", title="Issue count", format=",d"), alt.Tooltip(f'yearmonthdate({input_x}):T', title="Created at")]
        )
    # tt = linechart.mark_line(strokeWidth=30, opacity=0.01)
    points = linechart.mark_circle().encode(
                    opacity=alt.value(0)
                            ).add_params(
                                highlight
                            ).properties(
                                width=600
                    )
    return linechart + points


with st.sidebar:
    st.title(f'🏂 {page_title}')

tab1, tab2 = st.tabs(["Commits", "Issues"])
with tab1:
   st.header("Commits trends")

with tab2:
    st.header("Issues trends")
    col = st.columns((1.5, 4.5, 2), gap='medium')
    with col[1]:
        st.markdown("Cumulative count of issues - last 7 days")
        linechart = make_linechart(result_set, input_x="created_at", input_y="issue_count", input_color="repo")
        if linechart:
            st.altair_chart(linechart, use_container_width=True)


        
    