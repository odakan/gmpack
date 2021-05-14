import numpy as np


class FlattenRecord(object):
    def __init__(self, name, skip=0, output='acc', dt=1.0, unit='g'):
        # initialize internal variables
        self.name = name
        self.step = dt
        self.output = output
        self.skip_lines = int(skip)
        self.new_name = ''
        self.convert_to_g = 0.0
        self.length = 1
        # initialize data arrays
        self.data = np.zeros([1])

        # set unit conversion
        self.unit_conversion(unit)

        # read by flattening the record
        self.new_name = self.name
        self.flatten()

        # compute velocity or displacement history
        if output == 'acc':
            self.new_name = 'Acc#' + self.new_name
        elif output == 'vel':
            if dt == 1.0:
                print("integrate: Record sampling frequency is dt = 1.0 by default!!! Please check!")

            self.new_name = 'Vel#' + self.new_name
            self.integrate(self.step)
        elif output == 'disp':
            if dt == 1.0:
                print("integrate: Record sampling frequency is dt = 1.0 by default!!! Please check!")

            self.new_name = 'Disp#' + self.new_name
            self.integrate(self.step)
            self.integrate(self.step)
        else:
            raise Exception("integrate: Desired output is unknown! Can be either output='acc', 'vel' or 'disp'...")

    def unit_conversion(self, unit):
        if unit == 'mm':
            self.convert_to_g = 1.0 / 9806.65
        elif unit == 'cm':
            self.convert_to_g = 1.0 / 980.665
        elif unit == 'm':
            self.convert_to_g = 1.0 / 9.80665
        elif unit == 'g':
            self.convert_to_g = 1.0

    def flatten(self):
        file = open(self.name, "r")
        lines = file.readlines()
        counter = 0
        record = []
        skip = self.skip_lines
        for line in lines:
            if skip > 0:
                pass
            else:
                for data in line.split():
                    record.append(data.strip())
                    counter += 1
            skip -= 1

        file.close()
        self.length = counter
        self.data = np.zeros(self.length)
        for i in range(self.length):
            self.data[i] = float(record[i]) * self.convert_to_g

    def integrate(self, dt):
        new_data = np.zeros(self.length)
        new_data[0] = (0 + self.data[0]) * 0.5 * dt
        for i in range(self.length - 1):
            new_data[i + 1] = new_data[i] + (self.data[i] + self.data[i + 1]) * 0.5 * dt

        self.data = new_data.copy()

    def write(self):
        file = open(self.new_name, "w")
        for i in range(self.length):
            file.write("{:.8f}\n".format(self.data[i]))

        file.close()

    def get_name(self):
        return self.new_name
