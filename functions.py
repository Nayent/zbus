import os
import pandas as pd
import numpy as np

from model import de_para

qnt_bus = 37


def get_file():
    file_names = [
        os.path.join(os.getcwd(), 'files', 'data', 'barras_tipo_1.xlsx'),
        os.path.join(os.getcwd(), 'files', 'data', 'dados_de_linha.xlsx'),
    ]

    all_data = []

    for file in file_names:
        if '.xlsx' in file:
            data = pd.read_excel(file)
        elif '.ods' in file:
            data = pd.read_excel(file, engine='odf')
        else:
            print("ERROR file")
            continue

        all_data.append(data)
    
    return all_data


def tipo_1(new_bus, bus, z):
    bus[new_bus - 1][new_bus - 1] = z

    return bus


def tipo_2(new_bus, old_bus, bus, z):
    bus[new_bus - 1] = bus[old_bus - 1]
    bus[:, new_bus - 1] = bus[:, old_bus - 1]
    bus[new_bus - 1, new_bus - 1] = bus[old_bus - 1, old_bus - 1] + z

    return bus


def tipo_3(bus2, bus1, bus, z):
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

    bus = kron_reduc(bus)
    
    return bus


def kron_reduc(zbus):
    zbus = (
        zbus[:qnt_bus, :qnt_bus] -
        zbus[:qnt_bus, qnt_bus:].dot(
            np.linalg.inv(zbus[qnt_bus:len(zbus), qnt_bus:len(zbus)])
        ).dot(
            zbus[qnt_bus:, :qnt_bus]
        )
    )

    return zbus


def model_bus(data):
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

    np.savetxt("bus_postiva.csv", bus, delimiter="|")
    np.savetxt("bus_zero.csv", bus_zero, delimiter="|")
    return bus, bus_zero


# Faltas
def equilibrado(zbus, ref_bus):
    pass


def monofasica(zbus, ref_bus):
    pass


def bifasica(zbus, ref_bus):
    pass


def bifasica_terra(zbus, ref_bus):
    pass