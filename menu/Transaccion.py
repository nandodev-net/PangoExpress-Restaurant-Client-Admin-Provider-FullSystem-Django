'''
Created on May 10, 2016

@author: nek
'''

import datetime;

class Transaccion(object):

    # Se tiene como precondicion que todos los valores sean validos
    def __init__(self, ident, ano, mes, dia, monto):
        
        try:
            self.id = ident;
            self.fecha = datetime.date(ano, mes, dia);
            self.monto = monto;
            
        except:
            
            return None;
        
    def __str__(self):
        
        return "%i - %i - %i, at %i, for %i Bs." % (self.fecha.year, self.fecha.month, self.fecha.day, self.id, self.monto)