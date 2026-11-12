#Importaciones necesarias
from abc import abstractmethod

from Clientes import Entidad, validar_texto

#Clase abstracta que representa los servicios de Software FJ
class Servicio(Entidad):

    def __init__(self,nombre, descripcion,tarifa):
        super().__init__()

        self.nombre = validar_texto(nombre, "Nombre de serivicio")
        self.descripcion = validar_texto(descripcion, "Descripción")
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass
