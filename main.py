import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

df = pd.read_csv('data/cicada_survey2.csv')

print(list(df.columns))


df = df[df['test_type'] == 'main']


def show_data(df, field, split_by):

    options = list(set(df[split_by]))
    fig = go.Figure()
    for option in options:
        fig.add_trace(go.Histogram(x=df[df[split_by] == option][field], name=option))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', title=field)
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()


def show_data_dif(df, field, split_by):
    pids = list(set(df['Random PID']))
    fig = go.Figure()
    options = list(set(df[split_by]))
    df1 = df[df[split_by] == options[1]]
    df0 = df[df[split_by] == options[0]]
    xx = []
    for pid in pids:
        xx.append(
            df1[df1['Random PID'] == pid][field].item()
            - df0[df0['Random PID'] == pid][field].item()
        )

    if np.abs(np.sum(xx)) >= 15:  # Only show interesting ones
        fig.add_trace(
            go.Histogram(
                x=xx, xbins=dict(start=-6.5, end=6.5, size=1)  # bins used for histogram
            )
        )
        # Overlay both histograms
        fig.update_layout(
            barmode='overlay',
            title=f'{field},       {options[0]} <---> {options[1]}',
            xaxis_range=[-7, 7],
            bargap=0.2,
        )
        # Reduce opacity to see both histograms
        # fig.update_layout(scene={'XAxis':dict(tickmode="array", tickvals=list(range(-7,8)))})
        fig.update_traces(opacity=0.75)
        fig.show()


def show_data_corrected(df, field, split_by, correct_by):
    options = list(set(df[split_by]))
    conditionals = list(set(df[correct_by]))
    fig = make_subplots(
        rows=len(conditionals),
        cols=1,
        subplot_titles=[f'{field} | {conditional}' for conditional in conditionals],
    )
    for c, conditional in enumerate(conditionals):
        df_cond = df[df[correct_by] == conditional]
        for option in options:
            fig.add_trace(
                go.Histogram(
                    x=df_cond[df_cond[split_by] == option][field],
                    name=option,
                    xbins=dict(start=0.5, end=7.5, size=1),  # bins used for histogram
                ),
                row=c + 1,
                col=1,
            )
        # Overlay both histograms
        # Reduce opacity to see both histograms
        # fig.update_layout(scene={'XAxis':dict(tickmode="array", tickvals=list(range(-7,8)))})
    fig.update_traces(opacity=0.75)
    fig.update_layout(barmode='overlay')
    fig.show()


def show_data_corrected_many_fields(df, fields, split_by, correct_by):
    options = list(set(df[split_by]))
    conditionals = list(set(df[correct_by]))
    titles = [
        f'{field[:30]} | {conditional}'
        for conditional in conditionals
        for field in fields
    ]
    fig = make_subplots(rows=len(conditionals), cols=len(fields), subplot_titles=titles)
    for f, field in enumerate(fields):
        for c, conditional in enumerate(conditionals):
            df_cond = df[df[correct_by] == conditional]
            for option in options:
                fig.add_trace(
                    go.Histogram(
                        x=df_cond[df_cond[split_by] == option][field],
                        name=option,
                        xbins=dict(  # bins used for histogram
                            start=0.5, end=7.5, size=1
                        ),
                    ),
                    row=c + 1,
                    col=f + 1,
                )
    fig.update_traces(opacity=0.75)
    fig.update_layout(barmode='group')
    fig.show()


# splitters = ['The task I just completed was...', 'This is your first or second survey', 'The system was setup...']
fields = [
    'I made the sketch vs The system made the sketch',
    "I'm very unsatisfied with the sketch vs I'm very satisfied with the sketch",
    'The sketch was what I was aiming for vs The sketch outcome was unexpected',
    'The sketch is a very typical vs The sketch is a very novel',
    'I was able to effectively communicate what I wanted to the system.',
    'I was able to steer the system towards output that was aligned with my goals.',
    'At times, I felt that the system was steering me towards its own goals.',
    'At times, it felt like the system and I were collaborating as equals.',
    'I would be happy to use this system or tool on a regular basis.',
    'I enjoyed using the system or tool.',
    ' It was easy for me to explore many different ideas, options, designs, or outcomes, using this system or tool.',
    ' The system or tool was helpful in allowing me to track different ideas, outcomes, or possibilities',
    'I was able to be very creative while doing the activity inside this system or tool.',
    ' The system or tool allowed me to be very expressive.',
    ' My attention was fully tuned to the activity, and I forgot about the system or tool that I was using.',
    'I became so absorbed in the activity that I forgot about the system or tool that I was using.',
    'I was satisfied with what I got out of the system or tool.',
    'What I was able to produce was worth the effort I had to exert to produce it.',
]
# for splitter in splitters:
#     for field in fields:
# show_data(df,field, splitter)
# show_data_dif(df,field, splitter)


# conditioners = ['The task I just completed was...', 'This is your first or second survey']
# for conditioner in conditioners:
#     for field in fields:
#         show_data_corrected(df, field, 'The system was setup...', conditioner)

conditioners = [
    'The task I just completed was...',
    'This is your first or second survey',
]
N = len(fields)
for conditioner in conditioners:
    for k in range(4):
        show_data_corrected_many_fields(
            df,
            fields[round(k / 4 * N) : round((k + 1) / 4 * N)],
            'The system was setup...',
            conditioner,
        )
