import math
import os
import pandas as pd
import numpy as np

from model import de_para

qnt_bus = 37

a = (-0.5 + 0.8660254037844386j)
matrix_t = np.array((
    [1, 1, 1],
    [1, a**2, a],
    [1, a, a**2]
))

linhas = 0


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
def trifasico(pos_neg, ref_bus):
    index_zbus = de_para[ref_bus]['n_bar']

    icc = 1 / (pos_neg[index_zbus][index_zbus])

    tensoes = np.zeros((qnt_bus, 1))

    for t in range(qnt_bus):
        tensoes[t][0] = 1 - (pos_neg[t][index_zbus] / pos_neg[index_zbus][index_zbus])

    return icc, tensoes


def monofasica(pos_neg, zero, ref_bus, zf=0):
    index_zbus = de_para[ref_bus]['n_bar']

    ia_seq = 1/(
        2 * pos_neg[index_zbus][index_zbus] + zero[index_zbus][index_zbus] + 3 * zf
    )

    ia_fase = ia_seq * 3

    tensoes = np.zeros((qnt_bus, 3))

    for t in range(qnt_bus):
        tensoes[t][0] = 1 - (pos_neg[t][index_zbus] * ia_seq) # Positivo
        tensoes[t][1] = - pos_neg[t][index_zbus] * ia_seq # negativo
        tensoes[t][2] = - zero[t][index_zbus] * ia_seq # Zero

    tensoes_fase = fortescue(tensoes)

    return ia_fase, tensoes_fase


def bifasica(pos_neg, ref_bus, zf=0):
    index_zbus = de_para[ref_bus]['n_bar']

    ia_seq = 1/(
        2 * pos_neg[index_zbus][index_zbus] + zf
    )

    i_fase = [
        0,
        - ia_seq * math.sqrt(3),
        ia_seq * math.sqrt(3)
    ]

    tensoes = np.zeros((qnt_bus, 3))

    for t in range(qnt_bus):
        tensoes[t][0] = 1 - (pos_neg[t][index_zbus] * ia_seq) # Positivo
        tensoes[t][1] = - pos_neg[t][index_zbus] * ia_seq # negativo

    tensoes_fase = fortescue(tensoes)

    return i_fase, tensoes_fase


def bifasica_terra(pos_neg, zero, ref_bus, zf=0):
    index_zbus = de_para[ref_bus]['n_bar']

    zkk_p = pos_neg[index_zbus][index_zbus]
    zkk_z = zero[index_zbus][index_zbus]

    zeq = zkk_p + (zkk_p * (zkk_z + 3*zf))/(zkk_p + zkk_z + 3*zf)

    ia_seq = 1 / zeq


    tensoes = np.zeros((qnt_bus, 3))

    for t in range(qnt_bus):
        tensoes[t][0] = 1 - (pos_neg[t][index_zbus] * ia_seq) # Positivo
        tensoes[t][1] = tensoes[t][0] # Negativo
        tensoes[t][2] = tensoes[t][0] # Zero

    i_seq = [
        - tensoes[index_zbus][index_zbus] / (zero[index_zbus][index_zbus] + 3*zf),
        ia_seq,
        - tensoes[index_zbus][index_zbus] / pos_neg[index_zbus][index_zbus],
    ]

    i_fase = abs(np.dot(matrix_t, i_seq))

    tensoes_fase = fortescue(tensoes)

    return i_fase, tensoes_fase


def fortescue(tensoes):
    tensoes_fase = np.zeros((qnt_bus, 3))

    for t in range(qnt_bus):
        temp_tensoes = np.array((
            [tensoes[t][2]],
            [tensoes[t][0]],
            [tensoes[t][1]],
        ))

        tensoes_fase[t][0] = abs(np.dot(matrix_t, temp_tensoes)[0][0])
        tensoes_fase[t][1] = abs(np.dot(matrix_t, temp_tensoes)[1][0])
        tensoes_fase[t][2] = abs(np.dot(matrix_t, temp_tensoes)[2][0])

    return tensoes_fase


def correntes(tensoes_fase):
    correntes = {}
    for l in range(len(linhas)):
        cdp = '-'.join(str(linhas[l]), str(linhas[l]['Para']))

        de = de_para[linhas[l]['De']]['n_bar']
        para = de_para[linhas[l]['Para']]['n_bar']

        correntes[cdp] = [
            (tensoes_fase[de][0] - tensoes_fase[para][0]) / linhas[l]['impedancia'],
            (tensoes_fase[de][1] - tensoes_fase[para][1]) / linhas[l]['impedancia'],
            (tensoes_fase[de][2] - tensoes_fase[para][2]) / linhas[l]['impedancia'],
        ]

    return correntes