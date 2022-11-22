import matplotlib.pyplot as plt
import numpy as np


def plotting(all_data_np, train_data_np, test_data_np, bins, title, filename):
    fig, ax = plt.subplots()
    plt.hist([all_data_np,
              train_data_np,
              test_data_np], bins, label=[
        'Total data',
        'Train',
        'Test'], density=True)

    plt.title(title)
    plt.legend(loc='upper right')
    ax.plot()
    plt.savefig(filename)


def get_histograms(_train_data, _test_data, _all_data):
    plt.style.use('seaborn-deep')

    train_data_np = np.array(_train_data)
    test_data_np = np.array(_test_data)
    all_data_np = np.array(_all_data)

    train_data_np = train_data_np[train_data_np < 30]
    test_data_np = test_data_np[test_data_np < 30]
    all_data_np = all_data_np[all_data_np < 30]
    bins = np.linspace(0, 20, 10)

    plotting(all_data_np, train_data_np, test_data_np, bins,
             'Node degree 0-20',
             r'outputs/hist_0_20.png')

    all_data_np_12 = all_data_np[all_data_np > 12]
    train_data_np_12 = train_data_np[train_data_np > 12]
    test_data_np_12 = test_data_np[test_data_np > 12]

    bins_12 = np.linspace(0, 30, 15)

    plotting(train_data_np_12, test_data_np_12, all_data_np_12, bins_12,
             'Node degree 12+',
             r'outputs/hist_12_.png')


# plotting([1, 2, 3], [4, 5, 6], [7, 8, 9], [_ for _ in range(100)], '', '1.png')
# plotting([10, 20, 30], [40, 50, 60], [70, 80, 90], [_ for _ in range(100)], '', '2.png')
