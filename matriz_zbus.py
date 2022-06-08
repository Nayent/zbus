import os
import time

import numpy as np

from model import de_para
from functions import (
    bifasica_terra, get_file, model_bus, monofasica, bifasica, trifasico
)

def main():
    start = time.time()

    data = get_file()

    code = time.time()

    pos_neg, zero = model_bus(data)

    end = time.time()

    # print(final_bus)

    # print(f'\nExecution Time without reading_file = {end - code} seconds')
    # print(f'\nExecution Time with reading_file = {end - start} seconds\n')

    while True:
        falta = input(
            'Escolha o tipo de falta:\n'
            'Monofasica     (m)\n'
            'Bifasica       (b)\n'
            'Bifasica Terra (bt)\n'
            'Trifasica      (t)\n'
            'Exit           (e)\n\n'
            '-> '
        )

        if falta == 'e':
            break

        barra_falta = int(input('\nBarra na qual ocorreu a falta: '))

        if falta == 'm':
            i_fase, tensoes_fase = monofasica(pos_neg, zero, barra_falta)
        elif falta == 'b':
            i_fase, tensoes_fase = bifasica(pos_neg, barra_falta)
        elif falta == 'bt':
            i_fase, tensoes_fase = bifasica_terra(pos_neg, zero, barra_falta)
        elif falta == 't':
            i_fase, tensoes_fase = trifasico(pos_neg, barra_falta)
        else:
            print('Value Error')
            continue

        print('\n', i_fase, '\n')
        print(tensoes_fase, '\n')


if __name__ == '__main__':
    main()