import os
import time

import numpy as np

from model import de_para, index_name
from functions import (
    bifasica_terra, get_file, model_bus, monofasica, bifasica, round_, trifasico
)

def main():
    start = time.time()

    impedancias, data = get_file()

    code = time.time()

    pos_neg, zero = model_bus(data)

    end = time.time()

    # print(final_bus)

    # print(f'\nExecution Time without reading_file = {end - code} seconds')
    # print(f'\nExecution Time with reading_file = {end - start} seconds\n')

    while True:
        falta = input(
            '\nEscolha o tipo de falta:\n'
            '- Monofasica     (m)\n'
            '- Bifasica       (b)\n'
            '- Bifasica Terra (bt)\n'
            '- Trifasica      (t)\n'
            '- Exit           (e)\n\n'
            '-> '
        )

        if falta == 'e':
            break

        barra_falta = int(input('\nBarra na qual ocorreu a falta: '))

        if falta == 'm':
            print('Para a falta do tipo Monofásica')
            i_fase, tensoes_fase, correntes = monofasica(pos_neg, zero, barra_falta, impedancias)
        elif falta == 'b':
            print('Para a falta do tipo Bifásico')
            i_fase, tensoes_fase, correntes = bifasica(pos_neg, barra_falta, impedancias)
        elif falta == 'bt':
            print('Para a falta do tipo Bifásico-Terra')
            i_fase, tensoes_fase, correntes = bifasica_terra(pos_neg, zero, barra_falta, impedancias)
        elif falta == 't':
            print('Para a falta do tipo Trifásico')
            i_fase, tensoes_fase, correntes = trifasico(pos_neg, barra_falta, impedancias)
            print(f'\nCorrente de falta na barra {barra_falta}:\n', i_fase, '\n')
            print('Tensões nas barras:\n')
            for index in range(len(tensoes_fase)):
                print('{:<25} {}'.format(index_name[index]+':', round_(tensoes_fase[index][0])))
            print('\nCorrentes entre barras:\n')
            for key, item in correntes.items():
                print('{:<9} {}'.format(key+':', round_(item)))
            continue
        else:
            print('Value Error')
            continue
        
        print(f'\nCorrente de falta na barra {barra_falta}:\n', i_fase, '\n')
        print('Tensões nas barras:\n')
        for index in range(len(tensoes_fase)):
            print('{:<25} {}'.format(index_name[index]+':', list(map(round_, tensoes_fase[index]))))
        print('\nCorrentes entre barras:\n')
        for key, item in correntes.items():
            print('{:<9} {}'.format(key+':', list(map(round_, item))))


if __name__ == '__main__':
    main()