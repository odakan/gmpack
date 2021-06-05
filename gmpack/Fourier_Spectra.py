import numpy as np
from scipy.fft import fft, fftfreq


class FSpectra(object):
    def __init__(self, record_name, sampling_frequency):
        # read the record
        self.sampling_frequency = sampling_frequency
        self.step = sampling_frequency
        self.new_name = "FrqS#" + record_name
        self.rec_step = 0.0
        self.rec_size = 0
        self.rec_time = 0.0
        self.number_of_records = 1;
        self.record = np.zeros([1, 1])
        self.read(record_name, sampling_frequency)

        # initialize frequency spectrum
        self.data = np.zeros([self.number_of_records + 1, self.rec_size // 2])

        # compute the frequency spectrum
        self.data[0, :] = self.frequency()[0:self.rec_size // 2]
        for i in range(self.number_of_records):
            self.data[i + 1, :] = self.amplitude(i)[0:self.rec_size // 2]

    def frequency(self):
        return fftfreq(self.rec_size, self.sampling_frequency)

    def amplitude(self, index):
        return np.abs(fft(self.record[index, :]))


    def read(self, record_name, sampling_frequency):
        file = open(record_name, "r")
        lines = file.readlines()
        self.rec_size = len(lines)
        self.number_of_records = len(lines[0].strip().split())
        self.rec_step = float(sampling_frequency)
        self.rec_time = self.rec_size * self.rec_step
        self.record = np.zeros([self.number_of_records, self.rec_size])
        for i in range(self.number_of_records):
            for line, j in zip(lines, range(self.rec_size)):
                self.record[i, j] = float(line.strip().split()[i])

        file.close()

    def write(self):
        file = open(self.new_name, "w")
        for i in range(self.rec_size // 2):
            for j in range(self.number_of_records + 1):
                file.write("{:.4f}".format(self.data[j, i]))
                if j < self.number_of_records:
                    file.write("\t")

            if i < (self.rec_size - 1):
                file.write("\n")

        file.close()

    def get_name(self):
        return self.new_name

    def how_many(self):
        return self.number_of_records
