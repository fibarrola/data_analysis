import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('data/cicada_survey2.csv')

# print(list(df.columns))


df = df[df['test_type'] == 'main']
M = 30
N_COLS = 2
H = 2048

splitters = [
    'The task I just completed was...',
    'This is your first or second survey',
    'The system was setup...',
]
questions = [
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
questions = questions[:13]
colors = [
    'hsla(118,0,50,0)',
    'hsla(0,90,50,1)',
    'hsla(0,60,50,1)',
    'hsla(0,30,50,1)',
    'hsla(150,0,50,1)',
    'hsla(150,30,50,1)',
    'hsla(150,60,50,1)',
    'hsla(150,90,50,1)',
]


# question = questions[4]
# fig = go.Figure()
# for splitter in splitters:
#     options = list(set(df[splitter]))
#     for option in options:
#         df_filt = df[df[splitter]==option]
#         if option in ['A', 'B']: # these are not self explanatory
#             option = 'Task '+option
#         data = list(df_filt[question])
#         counts = [0 for k in range(8)]
#         # count[0] is for spacing
#         for d in data:
#             counts[d] += 1
#         counts[0] = M-counts[1]-counts[2]-counts[3]-counts[4]/2
#         fig.add_trace(go.Bar(x=counts, y=[option for i in range(8)], orientation='h', marker={'color':colors}))

# fig.update_layout( barmode='stack', title=question)
# fig.update_xaxes(tickvals=[10*x for x in range(7)], showgrid=False)
# fig.show()

## BY QUESTION
fig = make_subplots(
    rows=18 // N_COLS + 1, cols=N_COLS, subplot_titles=questions, vertical_spacing=0.03
)
for q, question in enumerate(questions):
    for splitter in splitters:
        options = list(set(df[splitter]))
        for option in options:
            df_filt = df[df[splitter] == option]
            if option in ['A', 'B']:  # these are not self explanatory
                option = 'Task ' + option
            data = list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            counts[0] = M - counts[1] - counts[2] - counts[3] - counts[4] / 2
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=[option for i in range(8)],
                    orientation='h',
                    marker={'color': colors},
                ),
                row=q // N_COLS + 1,
                col=q % N_COLS + 1,
            )

fig.add_vline(x=M)
fig.update_layout(barmode='stack', showlegend=False, height=H)
fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
fig.show()

## BY SPLITTER
all_options = []
for splitter in splitters:
    for option in list(set(df[splitter])):
        if option in ['A', 'B']:  # these are not self explanatory
            option = 'Task ' + option
        all_options.append(option)
fig = make_subplots(rows=3, cols=2, subplot_titles=all_options, vertical_spacing=0.03)

for s, splitter in enumerate(splitters):
    options = list(set(df[splitter]))
    for o, option in enumerate(options):
        for q, question in enumerate(questions):
            df_filt = df[df[splitter] == option]
            data = list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            counts[0] = M - counts[1] - counts[2] - counts[3] - counts[4] / 2
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=[f'Q{q+1}' for i in range(8)],
                    orientation='h',
                    marker={'color': colors},
                ),
                row=s + 1,
                col=o + 1,
            )
            # fig.add_trace(go.Bar(x=counts, y=[question for i in range(8)], orientation='h', marker={'color':colors}), row=s+1, col=o+1)

fig.add_vline(x=M)
fig.update_layout(barmode='stack', showlegend=False, height=1280)
fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
fig.show()


## MODIFIED

## BY QUESTION
tick_positions = [1, 3, 6, 8, 11, 13]
fig = make_subplots(
    rows=18 // N_COLS + 1, cols=N_COLS, subplot_titles=questions, vertical_spacing=0.03
)
for q, question in enumerate(questions):
    for s, splitter in enumerate(splitters):
        options = list(set(df[splitter]))
        for o, option in enumerate(options):
            df_filt = df[df[splitter] == option]
            if option in ['A', 'B']:  # these are not self explanatory
                option = 'Task ' + option
            data = list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            counts[0] = M - counts[1] - counts[2] - counts[3] - counts[4] / 2
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=[option for i in range(8)],
                    orientation='h',
                    marker={'color': colors},
                ),
                row=q // N_COLS + 1,
                col=q % N_COLS + 1,
            )
            # fig.add_trace(go.Bar(x=counts, y=[tick_positions[2*s+o] for i in range(8)], orientation='h', marker={'color':colors}), row=q//N_COLS+1, col=q%N_COLS+1)
        fig.add_trace(
            go.Bar(
                x=[0],
                y=[' ' if splitter == splitters[1] else ''],
                orientation='h',
                marker={'color': colors},
            ),
            row=q // N_COLS + 1,
            col=q % N_COLS + 1,
        )

fig.add_vline(x=M)
fig.update_layout(
    barmode='stack', showlegend=False, height=H, margin=dict(l=20, r=20, t=20, b=20)
)
fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
fig.show()

## BY SPLITTER
all_options = []
for splitter in splitters:
    for option in list(set(df[splitter])):
        if option in ['A', 'B']:  # these are not self explanatory
            option = 'Task ' + option
        all_options.append(option)
fig = make_subplots(rows=3, cols=2, subplot_titles=all_options, vertical_spacing=0.03)

for s, splitter in enumerate(splitters):
    options = list(set(df[splitter]))
    for o, option in enumerate(options):
        for q, question in enumerate(questions):
            df_filt = df[df[splitter] == option]
            data = list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            counts[0] = M - counts[1] - counts[2] - counts[3] - counts[4]
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=[f'Q{q+1}' for i in range(8)],
                    orientation='h',
                    marker={'color': colors},
                ),
                row=s + 1,
                col=o + 1,
            )
            # fig.add_trace(go.Bar(x=counts, y=[question for i in range(8)], orientation='h', marker={'color':colors}), row=s+1, col=o+1)

fig.add_vline(x=M)
fig.update_layout(barmode='stack', showlegend=False, height=1280)
fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
fig.show()


## BY QUESTION
tick_positions = [1, 3, 6, 8, 11, 13]
fig = make_subplots(
    rows=18 // N_COLS + 1, cols=N_COLS, subplot_titles=questions, vertical_spacing=0.03
)
for q, question in enumerate(questions):
    for s, splitter in enumerate(splitters):
        options = list(set(df[splitter]))
        for o, option in enumerate(options):
            df_filt = df[df[splitter] == option]
            if option in ['A', 'B']:  # these are not self explanatory
                option = 'Task ' + option
            data = list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            counts[0] = M - counts[1] - counts[2] - counts[3] - counts[4]
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=[option for i in range(8)],
                    orientation='h',
                    marker={'color': colors},
                ),
                row=q // N_COLS + 1,
                col=q % N_COLS + 1,
            )
            # fig.add_trace(go.Bar(x=counts, y=[tick_positions[2*s+o] for i in range(8)], orientation='h', marker={'color':colors}), row=q//N_COLS+1, col=q%N_COLS+1)
        fig.add_trace(
            go.Bar(
                x=[0],
                y=[' ' if splitter == splitters[1] else ''],
                orientation='h',
                marker={'color': colors},
            ),
            row=q // N_COLS + 1,
            col=q % N_COLS + 1,
        )

fig.add_vline(x=M)
fig.update_layout(
    barmode='stack', showlegend=False, height=H, margin=dict(l=20, r=20, t=20, b=20)
)
fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
fig.show()
