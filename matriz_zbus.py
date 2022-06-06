import os
# import unicodecsv
import time

import numpy as np

from model import de_para
from functions import (
    get_file, model_bus
)

def main():
    start = time.time()

    data = get_file()

    code = time.time()

    pos_neg, zero = model_bus(data)

    end = time.time()

    # print(final_bus)

    print(f'\nExecution Time without reading_file = {end - code} seconds')
    print(f'\nExecution Time with reading_file = {end - start} seconds\n')


if __name__ == '__main__':
    main()