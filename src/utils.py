def plot4paper(
    fig, filename, title=None, height=None, two_column_size=False, fontsize=28
):
    fig.update_layout(
        margin={'l': 0, 'r': 0, 't': 60 if title else 0, 'b': 0},
        title=title,
        width=2082 if two_column_size else 1024,
        height=height,
        font={'size': fontsize, 'color': 'black'},
    )
    fig.write_image(filename)
    return
