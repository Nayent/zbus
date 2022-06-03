import os
import pandas as pd
import numpy as np

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