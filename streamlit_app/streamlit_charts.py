import altair as alt
import plotly.express as px

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

def make_linechart4(input_df, input_x=None, input_y=None, input_color=None):
    # https://stackoverflow.com/questions/53287928/tooltips-in-altair-line-charts
    highlight = alt.selection_point(on='pointerover', fields=[input_color], nearest=True)
    linechart = alt.Chart(input_df).mark_line().encode(
            alt.X(f"{input_x}:T", axis=alt.Axis(title="Download date", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            alt.Y(f"{input_y}:Q", axis=alt.Axis(title="Percent change in downloads", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0, format=".0%")),
            color=f"{input_color}:N", #alt.value('gold'),
            tooltip=[alt.Tooltip(f"{input_y}:Q", title="Issue count", format=".0%"), alt.Tooltip(f'{input_x}:T', title="Download date")]
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
        .bar(subset=bar_style_col, color='brown') \
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
    return input_df_style