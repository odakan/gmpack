from matplotlib import pyplot as plt
import numpy as np


def count(list_names):
    n_rows = 0
    n_col = 0
    for name in list_names:
        file_1 = open(name, "r")
        lines = file_1.readlines()
        i = 0
        for line in lines:
            i += 1

        file_1.close()
        n_rows += 1
        if i > n_col:
            n_col = i

    return [n_rows, n_col]


def read(name):
    file_1 = open(name, "r")
    lines = file_1.readlines()
    i = 0
    spectra = []
    period = []
    for line in lines:
        spectra.append(float(line.strip().split()[0]))
        period.append(float(line.strip().split()[1]))
        i += 1

    file_1.close()
    data = np.zeros([2, len(spectra)])
    for i in range(len(spectra)):
        data[0, i] = spectra[i]
        data[1, i] = period[i]

    return data


class PlotSpectra(object):
    def __init__(self, list_names):
        self.size = count(list_names)
        self.x_data = np.zeros([self.size[0], self.size[1]])
        self.y_data = np.zeros([self.size[0], self.size[1]])
        self.fill(list_names)
        self.plot(list_names)

    def fill(self, list_names):
        i = 0
        for name in list_names:
            k = 0
            data = read(name)
            for j in range(len(data[0, :])):
                self.x_data[i, k] = data[0, k]
                self.y_data[i, k] = data[1, k]
                k += 1

            last_idx = k - 1
            for j in range(self.size[1] - last_idx - 1):
                self.x_data[i, k] = data[0, last_idx]
                self.y_data[i, k] = data[1, last_idx]
                k += 1

            i += 1

    def plot(self, list_names):
        for i in range(self.size[0]):
            plt.plot(self.x_data[i, :], self.y_data[i, :])
            list_names[i] = list_names[i].split("#")[-1]
            # list_names[i] = list_names[i].split(".")[0]

        plt.legend(list_names, loc='lower left')
        plt.semilogx()
        plt.semilogy()
        plt.grid()
        plt.show()
