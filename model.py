import numpy as np

from matriz_zbus import get_qnt_bus

class Linha:
    def __init__(self, data):
        self.data = data
        self.distinct_bus = set()
        self.get_qnt_bus()
        self.zbus = np.zeros((self.qnt_bus, self.qnt_bus))
        self.model_zbus()
    
    def get_qnt_bus(self):
        qnt_bus = set()
        for row in self.data.iterrows():
            # Create get_qnt_bus for the template
            pass
        
        self.qnt_bus = qnt_bus
    
    def model_zbus(self):
        for row in self.data.iterrows():
            
            if row[''] :
                self.tipo_1(row[1], row[3])
            elif row[''] == 2:
                self.tipo_2(row[1], row[2], row[3])
            elif row[''] == 3:
                self.tipo_3(row[1], row[2], row[3])
        
    def tipo_1(self, bus, z):
        self.zbus[bus - 1][bus - 1] = z


    def tipo_2(self, new_bus, old_bus, z):
        self.zbus[new_bus - 1] = self.zbus[old_bus - 1]
        self.zbus[:, new_bus - 1] = self.zbus[:, old_bus - 1]
        self.zbus[new_bus - 1, new_bus - 1] = self.zbus[old_bus - 1, old_bus - 1] + z


    def tipo_3(self, bus2, bus1, z):
        new_column = self.bus[:, bus2 - 1] - self.bus[:, bus1 - 1]
        self.bus = np.hstack([self.bus, np.atleast_2d(new_column).T])

        new_row = self.bus[bus2 - 1] - self.bus[bus1 - 1]
        self.bus = np.vstack([self.bus, new_row])

        in_line = len(self.bus) - 1

        self.bus[in_line, in_line] = (
            self.bus[bus1 - 1, bus1 - 1] +
            self.bus[bus2 - 1, bus2 - 1] -
            self.bus[bus1 - 1, bus2 - 1] -
            self.bus[bus2 - 1, bus1 - 1] +
            z
        )

        
        
    def kron_reduc(self):

        zbus = (
            zbus[:size_zbus, :size_zbus] -
            zbus[:size_zbus, size_zbus:].dot(
                np.linalg.inv(zbus[size_zbus:len(zbus), size_zbus:len(zbus)])
            ).dot(
                zbus[size_zbus:, :size_zbus]
            )
        )
