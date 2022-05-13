import os
import pandas as pd

def get_file():
    file_name = None

    if not file_name:
        home_path = os.path.join(os.getcwd(), 'files', 'data')
        file_name = input('Insert file name(with extension): ')
    file = os.path.join(home_path, file_name)

    if '.csv' in file:
        delimiter = input('Insert csv delimiter: ')
        data = pd.read_csv(file, delimiter=delimiter)
    elif '.xlsx' in file:
        data = pd.read_excel(file)
    elif '.ods' in file:
        data = pd.read_excel(file, engine='odf')
    # Missing the default type...
    elif 'OTHER TYPE' in file:
        pass
    else:
        return pd.Series()
    
    return data, file_name
