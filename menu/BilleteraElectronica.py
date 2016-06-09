'''
Created on May 10, 2016

@author: nek
'''

from menu.Transaccion import *;
import sys

class BilleteraElectronica(object):
    '''
    classdocs
    '''
    
    # Metodo constructor de la billetera
    def __init__(self, ident, nombres, apellidos, pin, saldoIni = 0):
        
        self.identificador = ident;
        self.nombres = nombres;
        self.apellidos = apellidos;
        self.pin = pin;
        
        self.histCreditos = [];
        self.histDebitos = [];
        
        self.balance = saldoIni;
    
    
    def __new__(cls,  ident, nombres, apellidos, pin, saldoIni = 0):
        if(type(nombres) == str and type(apellidos) == str and
           type(pin) == str and type(saldoIni) == float and saldoIni >= 0 ):
            return super(BilleteraElectronica, cls).__new__(cls);
        else:
            return None;
    
    # Metodo que devuelve el saldo de la billetera
    def saldo(self):
        
        return self.balance;
    
    # Metodo que registra y realiza una recarga a la billetera
    # retorna:
    # 0 en caso de hacer la opercion
    # 1 en caso de fallo por monto invalido
    # 2 en caso de fallo por fecha invalida
    # 3 en caso de pin incorrecto
    def recargar(self, pin, ident, ano, mes, dia, monto):
        
        if(pin == self.pin and monto > 0 and monto <= sys.float_info.max):
            
            if(self.balance + monto > sys.float_info.max):
                print("Balance excede maximo de almacenado")
                return 1;
            else:
                self.balance += monto;
                aux = Transaccion(ident, ano, mes, dia, monto);
            
            if(aux != None):
                self.histCreditos.append(aux);
                return 0;
            else:
                print("Fecha invalida.")
                return 2;
            
        elif(monto <= 0 or monto > sys.float_info.max):
            print("Monto invalido");
            return 1;
            
        else:
            print("Pin incorrecto.");
            return 3;
        
    # Metodoque registra y realiza un consumo de la billetera
    # retorna:
    # 0 en caso de realizar la operacion
    # 1 en caso de error de fecha invalida
    # 2 en caso de tener saldo insuficiente
    # 3 en caso de error de monto invalido
    # 4 en caso de pin incorrecto   
    def consumir(self, pin, ident, ano, mes, dia, monto):
        
        if(pin == self.pin and self.balance >= monto and monto >= 0 and monto < sys.float_info.max):
            
            self.balance -= monto;
            aux = Transaccion(ident, ano, mes, dia, monto);
            
            if(aux != None):
                self.histDebitos.append(aux);
                return 0;
            else:
                print("Fecha invalida.")
                return 1;

        elif(self.pin != pin):
            return 4;

        elif(self.balance < monto):
            
            print("Saldo insuficiente.");
            return 2;
            
        elif(monto < 0):
            
            print("Monto invalido.");
            return 3;
        else:
            print("Pin incorrecto.");
            return 4;
            
    
    
