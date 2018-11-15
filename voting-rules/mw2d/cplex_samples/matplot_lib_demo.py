




def draw_bar_graph(values, output_file_name=None):
    # https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
    # https://plot.ly/matplotlib/bar-charts/

    import matplotlib.pyplot as plt
    import numpy as np

    values_len = len(values)
    x = np.arange(values_len)
    plt.bar(x, height= values)
    plt.xticks(x + .5, range(values_len))
    plt.show()
    if output_file_name is not None:
        # https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
        # https://stackoverflow.com/a/9890599/554036
        plt.savefig(output_file_name, bbox_inches='tight')

def demo():
    list_of_floats = [1.123, 1.155, 2.4124, 0.1232]
    draw_bar_graph(list_of_floats)


if __name__ == '__main__':
    demo()