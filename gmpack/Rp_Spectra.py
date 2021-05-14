import numpy as np
import math as m


class RpSpectra(object):
    def __init__(self, record_name, sampling_frequency, unit='g', tf=10, step=0.01, ksi=0.05, rs_type='acc'):
        # initialize response spectrum
        self.mass = 1
        self.convert_to_g = 1
        self.T_final = tf
        self.step = step
        self.damping = ksi
        self.new_name = record_name
        self.new_name = "data#" + record_name
        self.n_steps = int(tf / step)
        self.data = np.zeros([2, self.n_steps])
        self.type = rs_type

        # fill periods
        self.fill_period(tf, step)
        # handle units
        self.unit_conversion(unit)
        # read the record
        self.rec_step = 0.0
        self.rec_size = 0
        self.rec_time = 0.0
        self.record = np.zeros([1, 1])
        self.read(record_name, sampling_frequency)

        # compute the response spectrum
        self.compute()

    def fill_period(self, tf, step):
        range_1 = 3 * int(self.n_steps / 10)
        step_1 = (3 * step) / range_1
        limit_1 = step_1 * range_1
        range_2 = int(self.n_steps / 2)
        step_2 = (step * 10 - limit_1) / (range_2 - range_1)
        limit_2 = limit_1 + step_2 * (range_2 - range_1)
        range_3 = self.n_steps
        step_3 = (int(tf) - limit_2) / (range_3 - range_2)

        i = 0
        self.data[0, i] = step_1
        for j in range(range_1 - 1):
            self.data[0, i + 1] = self.data[0, i] + step_1
            i += 1

        for j in range(range_2 - range_1):
            self.data[0, i + 1] = self.data[0, i] + step_2
            i += 1

        for j in range(range_3 - range_2):
            self.data[0, i + 1] = self.data[0, i] + step_3
            i += 1

    def unit_conversion(self, unit):
        if unit == 'mm':
            self.convert_to_g = 1.0 / 9806.65
        elif unit == 'cm':
            self.convert_to_g = 1.0 / 980.665
        elif unit == 'm':
            self.convert_to_g = 1.0 / 9.80665
        elif unit == 'g':
            self.convert_to_g = 1.0

    def read(self, record_name, sampling_frequency):
        file = open(record_name, "r")
        lines = file.readlines()
        i = 0
        list_record = []
        for line in lines:
            list_record.append(float(line.strip()))
            i += 1

        file.close()
        self.rec_size = i
        self.rec_step = float(sampling_frequency)
        self.rec_time = self.rec_size * self.rec_step
        self.record = np.zeros([1, self.rec_size])
        for i in range(self.rec_size):
            self.record[0, i] = list_record[i] * self.convert_to_g

    def compute(self):
        for i in range(self.n_steps):
            acc = np.zeros([1, self.rec_size])
            vel = np.zeros([1, self.rec_size])
            disp = np.zeros([1, self.rec_size])

            # S.D.O.F. solution with Newmark method
            # constant acceleration
            gamma = 0.5
            beta = 0.25
            # S.D.O.F. parameters
            omega = (2 * m.pi) / self.data[0, i]
            k = omega * omega * self.mass
            c = self.damping * 2 * self.mass * omega
            dt = self.rec_step
            kb = (1 / (beta * dt * dt) * self.mass) + ((gamma / (beta * dt)) * c) + k
            # Solve
            acc[0, 0] = (1 / self.mass) * ((self.mass * -self.record[0, 0]) - c * vel[0, 0] - k * disp[0, 0])
            for j in range(self.rec_size - 1):
                vel_tilda = vel[0, j] + (1 - gamma) * dt * acc[0, j]
                disp_tilda = disp[0, j] + vel[0, j] * dt + \
                             0.5 * (1 - 2 * beta) * dt * dt * acc[0, j]
                pb = (self.mass * -self.record[0, j + 1]) + self.mass * ((1 / (beta * dt * dt)) * disp_tilda) + \
                     c * (((gamma / (beta * dt)) * disp_tilda) - vel_tilda)
                disp[0, j + 1] = pb / kb
                vel[0, j + 1] = vel_tilda + (gamma / (beta * dt)) * (disp[0, j + 1] - disp_tilda)
                acc[0, j + 1] = self.record[0, j + 1] + (1 / (beta * dt * dt)) * (disp[0, j + 1] - disp_tilda)

            if self.type == 'disp':
                self.data[1, i] = 2 * np.max(np.abs(disp))
            elif self.type == 'vel':
                self.data[1, i] = 2 * np.max(np.abs(vel))
            elif self.type == 'acc':
                self.data[1, i] = 2 * np.max(np.abs(acc))
            else:
                raise Exception("compute: Unknown response spectra type string! Can be either 'disp', 'vel' or 'acc'.")

    def write(self):
        file = open(self.new_name, "w")
        for i in range(self.n_steps):
            file.write("{:.8f}\t{:.8f}\n".format(self.data[0, i], self.data[1, i]))

        file.close()

    def get_name(self):
        return self.new_name
