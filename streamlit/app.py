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
    initial_sidebar_state="expanded"
)

catalog = "iceberg"
schema = "bronze"

def create_trino_connection() -> dbapi.Connection:
    """Create a Trino db connection"""
    try:
        conn = connect(
            host="localhost",
            port=1080,
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
        raise Exception(f"Query {qry} failed: {e}")
    cols = [col.name for col in cur.description]
    df = pd.DataFrame(cur.fetchall(), columns=cols)
    return df

conn = create_trino_connection()
alltime_count_issues = f"""
                    select
                        repo,
                        created_at,
                        num_issues
                    from
                        {catalog}.{schema}.all_time_issues_trend
                    """
result_set1 = execute_query(alltime_count_issues)

last_7_days = f"""
        select 
            repo,
            created_at,
            issue_count
        from 
            {catalog}.{schema}.last_7_days_fct_issues 
        """
result_set2 = execute_query(last_7_days)

update_count_issues = f"""
                    select
                        repo,
                        num_days,
                        num_issues
                    from
                        {catalog}.{schema}.num_update_issues
                    """
result_set3 = execute_query(update_count_issues)

num_labels_issues = f"""
                    select
                        repo,
                        label,
                        num_labels
                    from
                        {catalog}.{schema}.num_labels_per_repo
                    """
result_set4 = execute_query(num_labels_issues)

alltime_count_commits = f"""
                    select
                        repo,
                        commit_author_date,
                        num_commits
                    from
                        {catalog}.{schema}.all_time_author_commits_trend
                    """
result_set5 = execute_query(alltime_count_commits)

alltime_count_committer_commits = f"""
                    select
                        repo,
                        committer_commit_date,
                        num_commits
                    from
                        {catalog}.{schema}.all_time_committer_commits_trend
                    """
result_set6 = execute_query(alltime_count_committer_commits)

author_commits_by_repo = f"""
                    select
                        repo,
                        author_name,
                        num_commits
                    from
                        {catalog}.{schema}.num_author_commits_by_repo
                    """
result_set7 = execute_query(author_commits_by_repo)

committer_commits_by_repo = f"""
                    select
                        repo,
                        committer_name,
                        num_commits
                    from
                        {catalog}.{schema}.num_committer_commits_by_repo
                    """
result_set8 = execute_query(committer_commits_by_repo)


# Line chart
def make_linechart1(
        input_df, 
        input_x=None, 
        input_y=None, 
        input_color=None,
        label_x=None,
        label_y=None
    ):
    # https://stackoverflow.com/questions/53287928/tooltips-in-altair-line-charts
    highlight = alt.selection_point(on='pointerover', fields=[input_color], nearest=True)
    linechart = alt.Chart(input_df).mark_line().encode(
            alt.X(f"{input_x}:T", axis=alt.Axis(title=label_x, titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            alt.Y(f"{input_y}:Q", axis=alt.Axis(title=label_y, titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            color=f"{input_color}:N", #alt.value('gold'),
            tooltip=[alt.Tooltip(f"{input_y}:Q", title=label_y, format=",d"), alt.Tooltip(f'yearmonthdate({input_x}):Q', title=label_x)]
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

def make_linechart2(input_df, input_x=None, input_y=None, input_color=None):
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

def make_linechart3(input_df, input_x=None, input_y=None, input_color=None):
    # https://stackoverflow.com/questions/53287928/tooltips-in-altair-line-charts
    highlight = alt.selection_point(on='pointerover', fields=[input_color], nearest=True)
    linechart = alt.Chart(input_df).mark_line().encode(
            alt.X(f"{input_x}:Q", axis=alt.Axis(title="Num days to update", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            alt.Y(f"{input_y}:Q", axis=alt.Axis(title="Count of issues", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            color=f"{input_color}:N", #alt.value('gold'),
            tooltip=[alt.Tooltip(f"{input_y}:Q", title="Issue count", format=",d"), alt.Tooltip(f'{input_x}:Q', title="Num days")]
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

# Table
def make_table1(input_df, bar_style_col=None, cols=None):
    # input_df.set_index(input_df.columns[0], inplace=True)
    input_df_style =  input_df.style
    input_df_style = input_df_style \
        .hide(axis='index') \
        .bar(subset=[bar_style_col], color='brown') \
        .set_table_styles(
            {col: [{'selector': 'th', 'props': [('background-color', 'gray'), ('color', 'white'), ('font-weight', 'bold')]}]
             for col in cols
            },
        # {
        #     'repo': [{'selector': 'th', 'props': [('background-color', 'gray'), ('color', 'white'), ('font-weight', 'bold')]}],
        #     'label': [{'selector': 'th', 'props': [('background-color', 'gray'), ('color', 'white'), ('font-weight', 'bold')]}],
        #     'num_labels': [{'selector': 'th', 'props': [('background-color', 'gray'), ('color', 'white'), ('font-weight', 'bold')]}],
        # },
        overwrite=False
    )
    # st.dataframe(
    #     input_df.bar(subset=["num_labels"], color='gray'),
    #     column_order=("repo", "label", "num_labels"),
    #     hide_index=True,
    #     width=None,
    # )
    st.write(input_df_style.to_html(escape=False), unsafe_allow_html=True)


with st.sidebar:
    st.title(f'''
    🐙{page_title}
''')

tab1, tab2 = st.tabs(["Commits", "Issues"])
with tab1:
#    st.header("Commits trends")
   st.markdown("<h1 style='text-align: center; color: gold;'>Commits trends</h1>", unsafe_allow_html=True)
   col = st.columns((3.5, 10.5), gap='small')
   with col[0]:
        st.markdown("Top 3 authors by repo commits")
        cols = ["repo", "author_name", "num_commits"]
        make_table1(result_set7, bar_style_col="num_commits", cols=cols)

        st.markdown("Top 3 committers by repo commits")
        cols = ["repo", "committer_name", "num_commits"]
        make_table1(result_set8, bar_style_col="num_commits", cols=cols)

   with col[1]:
    st.markdown("Count of author commits - all time")
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
    
    st.markdown("Count of committer commits - all time")
    linechart = make_linechart1(
        result_set6, 
        input_x="committer_commit_date", 
        input_y="num_commits", 
        input_color="repo",
        label_x="Committer commit date",
        label_y="# of commits"
    )
    if linechart:
        st.altair_chart(linechart, use_container_width=True)

with tab2:
    # st.header("Issues trends")
    st.markdown("<h1 style='text-align: center; color: gold;'>Issues trends</h1>", unsafe_allow_html=True)
    col = st.columns((3.5, 10.5), gap='small')
    with col[0]:
        st.markdown("Top 3 labels by repo")
        cols =[ "repo", "label", "num_labels"]
        make_table1(result_set4, bar_style_col="num_labels", cols=cols)
    with col[1]:
        st.markdown("Count of issues - all time")
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

        st.markdown("Cumulative count of issues - last 7 days")
        linechart = make_linechart2(result_set2, input_x="created_at", input_y="issue_count", input_color="repo")
        if linechart:
            st.altair_chart(linechart, use_container_width=True)
        
        st.markdown("Days taken to update issues")
        linechart = make_linechart3(result_set3, input_x="num_days", input_y="num_issues", input_color="repo")
        if linechart:
            st.altair_chart(linechart, use_container_width=True)

        
    