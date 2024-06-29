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
from streamlit_app.streamlit_queries import *
from streamlit_app.streamlit_charts import *

page_title = "GitHub repository trends"
st.set_page_config(
    page_title=page_title,
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title(f'''
    🐙{page_title}
''')

# catalog = "iceberg"
# schema = "bronze"

def create_trino_connection() -> dbapi.Connection:
    """Create a Trino db connection
    From host machine use localhost:1080
    """
    try:
        conn = connect(
            host="trino",
            port=8080,
            user="admin",
            catalog=f"{catalog}",
            schema=f"{schema}",
        )
    except exceptions.TrinoConnectionError as e:
        raise Exception(f"Trino connection to iceberg failed: {e}")
    return conn

@st.cache_data(ttl=600)
def execute_query(qry: str) -> pd.DataFrame:
    cur = conn.cursor()
    try:
        cur.execute(qry)
    except exceptions.TrinoQueryError as e:
        print(f"Query {qry} failed: {e}")
        return
    cols = [col.name for col in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    return df

conn = create_trino_connection()

result_set1 = execute_query(all_time_issues_trend)

result_set2 = execute_query(last_7_days_fct_issues)

result_set3 = execute_query(num_updated_issues)

result_set4 = execute_query(num_labels_per_repo)

result_set5 = execute_query(all_time_author_commits_trend)

result_set6 = execute_query(all_time_committer_commits_trend)

result_set7 = execute_query(num_author_commits_by_repo)

result_set8 = execute_query(num_committer_commits_by_repo)

result_set9 = execute_query(summary_stats_base_repo)


tab1, tab2, tab3 = st.tabs(["Summary", "Commits", "Issues"])
with tab1:
    st.markdown("<h1 style='text-align: center; color: gold;'>Summary stats of the repo</h1>", unsafe_allow_html=True)
    st.markdown("All time summary sats")
    if result_set9 is not None:
        cols = result_set9.columns.tolist()
        input_df_style = make_table1(result_set9, bar_style_col=cols[2:], cols=cols)
        st.write(input_df_style.to_html(escape=False), unsafe_allow_html=True)
    else:
        print("Table `num_author_commits_by_repo` not ready. Check Trino dashboard")

with tab2:
#    st.header("Commits trends")
   st.markdown("<h1 style='text-align: center; color: gold;'>Commits trends</h1>", unsafe_allow_html=True)
   col = st.columns((3.5, 8.5), gap='small')
   with col[0]:
        st.markdown("Top 3 authors by repo commits")
        if result_set7 is not None:
            cols = result_set7.columns.tolist()
            input_df_style = make_table1(result_set7, bar_style_col=["num_commits"], cols=cols)
            st.write(input_df_style.to_html(escape=False), unsafe_allow_html=True)
        else:
            print("Table `num_author_commits_by_repo` not ready. Check Trino dashboard")

        st.markdown("Top 3 committers by repo commits")
        if  result_set8 is not None:
            cols = result_set8.columns.tolist()
            input_df_style = make_table1(result_set8, bar_style_col=["num_commits"], cols=cols)
            st.write(input_df_style.to_html(escape=False), unsafe_allow_html=True)
        else:
            print("Table `num_committer_commits_by_repo` not ready. Check Trino dashboard")
        
        st.markdown('Note - when GitHub is the committer the commit author date and commit committer dates are identical. Hence the almost identical charts')

   with col[1]:
    st.markdown("Count of author commits - all time")
    if result_set5 is not None:
        linechart = make_linechart1(
            result_set5, 
            input_x="commit_author_date", 
            input_y="num_commits", 
            input_color="repo",
            label_x="Author commit date",
            label_y="# of commits"
        )
        if linechart:
            st.altair_chart(linechart, use_container_width=True)
    else:
        print("Table `all_time_author_commits_trend` not ready. Check Trino dashboard")
    
    st.markdown("Count of committer commits - all time")
    if result_set6 is not None:
        linechart = make_linechart1(
            result_set6, 
            input_x="commit_committer_date", 
            input_y="num_commits", 
            input_color="repo",
            label_x="Committer commit date",
            label_y="# of commits"
        )
        if linechart:
            st.altair_chart(linechart, use_container_width=True)
    else:
        print("Table `all_time_committer_commits_trend` not ready. Check Trino dashboard")

with tab3:
    # st.header("Issues trends")
    st.markdown("<h1 style='text-align: center; color: gold;'>Issues trends</h1>", unsafe_allow_html=True)
    col = st.columns((3.5, 10.5), gap='small')
    with col[0]:
        st.markdown("Top 3 labels by repo")
        if result_set4 is not None:
            cols = result_set4.columns.tolist()
            input_df_style = make_table1(result_set4, bar_style_col=["num_labels"], cols=cols)
            st.write(input_df_style.to_html(escape=False), unsafe_allow_html=True)
        else:
            print("Table `num_labels_per_repo` not ready. Check Trino dashboard")
    with col[1]:
        st.markdown("Count of issues - all time")
        if result_set1 is not None:
            linechart = make_linechart1(
                result_set1, 
                input_x="created_at", 
                input_y="num_issues", 
                input_color="repo",
                label_x="Creation date",
                label_y="# of issues"
            )
            if linechart:
                st.altair_chart(linechart, use_container_width=True)
        else:
            print("Table `all_time_issues_trend` not ready. Check Trino dashboard")

        st.markdown("Cumulative count of issues - last 7 days")
        if result_set2 is not None:
            linechart = make_linechart2(result_set2, input_x="created_at", input_y="issue_count", input_color="repo")
            if linechart:
                st.altair_chart(linechart, use_container_width=True)
        else:
            print("Table `last_7_days_fct_issues` not ready. Check Trino dashboard")
        
        st.markdown("Days taken to update issues")
        if result_set3 is not None:
            linechart = make_linechart3(result_set3, input_x="num_days", input_y="num_issues", input_color="repo")
            if linechart:
                st.altair_chart(linechart, use_container_width=True)
        else:
            print("Table `num_updated_issues` not ready. Check Trino dashboard")

        
    