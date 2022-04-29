import time

import numpy as np
import pandas as pd


def main():
    start = time.time()

    data = get_file()
    if data.empty:
        print('File format is wrong, only accept CSV, XLSX or ODS formats with HEADER or skip first line!')
        return
    
    qnt_bus = get_qnt_bus(data)

    bus = np.zeros((qnt_bus, qnt_bus))

    code = time.time()

    final_bus = model_bus(bus, data, qnt_bus)

    end = time.time()

    print(final_bus)


    print(f'\nExecution Time without reading_file = {end - code} seconds')
    print(f'\nExecution Time with reading_file = {end - start} seconds\n')


def model_bus(bus, data, qnt_bus):
    for _row in data.iterrows():
        row = _row[1]

        if int(row[0]) == 1:
            bus = tipo_1(row[1], bus, row[3])
        elif int(row[0]) == 2:
            bus = tipo_2(row[1], row[2], bus, row[3])
        elif int(row[0]) == 3:
            bus = tipo_3(row[1], row[2], bus, row[3], qnt_bus)
        else:
            print(f'Wrong type in line {_row[0] + 1}, please fix it!')
    
    return bus




def tipo_1(new_bus, bus, z):
    bus[new_bus - 1][new_bus - 1] = z

    return bus


def tipo_2(new_bus, old_bus, bus, z):
    bus[new_bus - 1] = bus[old_bus - 1]
    bus[:, new_bus - 1] = bus[:, old_bus - 1]
    bus[new_bus - 1, new_bus - 1] = bus[old_bus - 1, old_bus - 1] + z

    return bus


def tipo_3(bus2, bus1, bus, z, qnt_bus):
    new_column = bus[:, bus2 - 1] - bus[:, bus1 - 1]
    bus = np.hstack([bus, np.atleast_2d(new_column).T])

    new_row = bus[bus2 - 1] - bus[bus1 - 1]
    bus = np.vstack([bus, new_row])

    in_line = len(bus) - 1

    bus[in_line, in_line] = (
        bus[bus1 - 1, bus1 - 1] +
        bus[bus2 - 1, bus2 - 1] -
        bus[bus1 - 1, bus2 - 1] -
        bus[bus2 - 1, bus1 - 1] +
        z
    )

    bus = (
        bus[:qnt_bus, :qnt_bus] -
        bus[:qnt_bus, qnt_bus:].dot(
            np.linalg.inv(bus[qnt_bus:len(bus), qnt_bus:len(bus)])
        ).dot(
            bus[qnt_bus:, :qnt_bus]
        )
    )
    
    return bus


def get_file():
    # file = '/home/nomura/Documents/Github/Python/utfpr/SEP2_zbus/files/exemplo_1_zbus.ods'
    file = '/home/guilherme.leite/Documents/Github/Python/zbus/files/exercicio_fixacao.ods'

    if not file:
        file = input('Insert file directory: ')

    if '.csv' in file:
        delimiter = input('Insert csv delimiter: ')
        data = pd.read_csv(file, delimiter=delimiter)
    elif '.xlsx' in file:
        data = pd.read_excel(file)
    elif '.ods' in file:
        data = pd.read_excel(file, engine='odf')
    else:
        return pd.Series()
    
    return data


def get_qnt_bus(data):
    qnt_bus = set()
    for row in data.iterrows():
        if row[1][1] == 'ref' or row[1][2] == 'ref':
            continue
        qnt_bus.add(row[1][1])
        qnt_bus.add(row[1][2])
    
    return len(qnt_bus)


if __name__ == '__main__':
    main()