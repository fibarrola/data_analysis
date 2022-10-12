import pandas as pd
import plotly.graph_objects as go
from src.utils import plot4paper

df = pd.read_csv('data/cicada_survey2.csv')
df = df[df['test_type'] == 'main']

question_groups = {
    'I made the sketch vs The system made the sketch': [
        'I made the sketch vs The system made the sketch'
    ],
    "I'm very unsatisfied vs I'm very satisfied with the sketch": [
        "I'm very unsatisfied with the sketch vs I'm very satisfied with the sketch"
    ],
    'The sketch was: what I was aiming for vs unexpected': [
        'The sketch was what I was aiming for vs The sketch outcome was unexpected'
    ],
    'The sketch is a very typical vs The sketch is a very novel': [
        'The sketch is a very typical vs The sketch is a very novel'
    ],
    'I was able to effectively communicate what I wanted to the system.': [
        'I was able to effectively communicate what I wanted to the system.'
    ],
    'I was able to steer the system towards an output aligned with my goals.': [
        'I was able to steer the system towards output that was aligned with my goals.'
    ],
    'At times, I felt that the system was steering me towards its own goals.': [
        'At times, I felt that the system was steering me towards its own goals.'
    ],
    'At times, it felt like the system and I were collaborating as equals.': [
        'At times, it felt like the system and I were collaborating as equals.'
    ],
    'ENJOYMENT': [
        'I would be happy to use this system or tool on a regular basis.',
        'I enjoyed using the system or tool.',
    ],
    'EXPLORATION': [
        ' It was easy for me to explore many different ideas, options, designs, or outcomes, using this system or tool.',
        ' The system or tool was helpful in allowing me to track different ideas, outcomes, or possibilities',
    ],
    'EXPRESSIVENESS': [
        'I was able to be very creative while doing the activity inside this system or tool.',
        ' The system or tool allowed me to be very expressive.',
    ],
    'IMMERSIVENESS': [
        ' My attention was fully tuned to the activity, and I forgot about the system or tool that I was using.',
        'I became so absorbed in the activity that I forgot about the system or tool that I was using.',
    ],
    'WORTH': [
        'I was satisfied with what I got out of the system or tool.',
        'What I was able to produce was worth the effort I had to exert to produce it.',
    ],
    'HUMAN-MACHINE COLLABORATION': [
        'I was able to effectively communicate what I wanted to the system.',
        'I was able to steer the system towards output that was aligned with my goals.',
    ],
}

splitters = {
    'The task I just completed was...': ['B', 'A'],
    'This is your first or second survey': ['Second Survey', 'First Survey'],
    'The system was setup...': ['With the tool', 'Without the tool'],
}
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

M0 = 0
for question_group in question_groups:
    fig = go.Figure()
    for splitter in splitters:
        for option in splitters[splitter]:
            df_filt = df[df[splitter] == option]
            if option in ['A', 'B']:  # these are not self explanatory
                option = 'Task ' + option
            data = []
            for question in question_groups[question_group]:
                data += list(df_filt[question])
            counts = [0 for k in range(8)]
            # count[0] is for spacing
            for d in data:
                counts[d] += 1
            M0 = max(counts[5] + counts[6] + counts[7], M0)


for qg, question_group in enumerate(question_groups):
    fig = go.Figure()
    M = M0 * len(question_groups[question_group]) // 2
    for splitter in splitters:
        for option in splitters[splitter]:
            df_filt = df[df[splitter] == option]
            if option in ['A', 'B']:  # these are not self explanatory
                option = 'Task ' + option
            data = []
            for question in question_groups[question_group]:
                data += list(df_filt[question])
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
                )
            )
        # a = go.bar.Marker
        # print(a.color)
        # print(dir(a.color.setter))
        # sdadsa
        # break

        fig.add_trace(
            go.Bar(
                x=[0],
                y=[' ' if option == splitters[splitter][1] else ''],
                orientation='h',
                marker={'color': colors},
            )
        )

    fig.add_vline(x=M)
    fig.update_xaxes(range=[0, 2 * M], showgrid=False, visible=False)
    fig.update_layout(
        barmode='stack',
        showlegend=False,
        # plot_bgcolor='hsla(0,0,0,0)',
        # paper_bgcolor='hsla(0,0,0,0)',
    )
    plot4paper(fig, f'out/q{qg+1}.png', title=question_group, fontsize=22, height=300)
