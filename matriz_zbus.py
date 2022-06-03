import os
# import unicodecsv
import time

import numpy as np

from model import de_para
from functions import (
    get_file, tipo_1, tipo_2, tipo_3
)

def main():
    start = time.time()

    data = get_file()

    qnt_bus = 37

    code = time.time()

    final_bus = model_bus(data, qnt_bus)

    end = time.time()

    # print(final_bus)

    print(f'\nExecution Time without reading_file = {end - code} seconds')
    print(f'\nExecution Time with reading_file = {end - start} seconds\n')


def model_bus(data, qnt_bus):
    bus = np.zeros((qnt_bus, qnt_bus))
    already_bars = set()
    file_aux = 0

    for data_ in data:
        for index, row in data_.iterrows():
            if row.get('Barras tipo 1'):
                num_bar = de_para[int(row['Barras tipo 1'])]['n_bar']
                bus = tipo_1(num_bar, bus, row['X+'])
                already_bars.add(int(row['Barras tipo 1']))
            elif int(row['De']) in already_bars and int(row['Para']) in already_bars:
                num_bar1 = de_para[int(row['De'])]['n_bar']
                num_bar2 = de_para[int(row['Para'])]['n_bar']
                bus = tipo_3(num_bar1, num_bar2, bus, row['X+  pu'])
                bus_zero = tipo_3(num_bar1, num_bar2, bus_zero, row['X0  pu'])
            else:
                if int(row['De']) in already_bars:
                    num_bar1 = de_para[int(row['De'])]['n_bar']
                    num_bar2 = de_para[int(row['Para'])]['n_bar']
                else:
                    num_bar1 = de_para[int(row['Para'])]['n_bar']
                    num_bar2 = de_para[int(row['De'])]['n_bar']
                bus = tipo_2(num_bar2, num_bar1, bus, row['X+  pu'])
                bus_zero = tipo_2(num_bar2, num_bar1, bus_zero, row['X0  pu'])
                already_bars.add(int(row['De']))
                already_bars.add(int(row['Para']))

        file_aux += 1
        if file_aux == 1:
            bus_zero = bus
    import ipdb
    ipdb.set_trace()
    return bus


if __name__ == '__main__':
    main()