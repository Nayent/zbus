import os
# import unicodecsv
import time
import numpy as np

from model import Linha
from functions import get_file, get_qnt_bus

def main():
    start = time.time()

    data, file_name = get_file()
    if data.empty:
        print('File format is wrong, only accept CSV, XLSX and ODS formats with HEADER or skip first line!')
        return
    
    linha = Linha(data)

if __name__ == '__main__':
    main()