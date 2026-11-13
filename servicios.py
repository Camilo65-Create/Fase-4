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

class ReservaSala(Servicio):

    def __init__(self, nombre, descripcion, tarifa, capacidad):
        super().__init__(nombre, descripcion, tarifa)

        self.capacidad = capacidad

    def describir(self):
        return f"{self.nombre}: {self.descripcion}. Capacidad: {self.capacidad} personas."

    def validar_parametros(self):
        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo.")

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_parametros()

        if horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total    

class AlquilerEquipo(Servicio):

    def __init__(self, nombre, descripcion, tarifa, equipo, cantidad):
        super().__init__(nombre, descripcion, tarifa)

        self.equipo = validar_texto(equipo, "Nombre del equipo")
        self.cantidad = cantidad

    def validar_parametros(self):
        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

    def describir(self):
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Equipo: {self.equipo}. Cantidad disponible: {self.cantidad}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_parametros()

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total

class Asesoria(Servicio):

    def __init__(self, nombre, descripcion, tarifa, especialidad, asesor):
        super().__init__(nombre, descripcion, tarifa)

        self.especialidad = validar_texto(especialidad, "Especialidad")
        self.asesor = validar_texto(asesor, "Nombre del asesor")

    def validar_parametros(self):
        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

    def describir(self):
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Especialidad: {self.especialidad}. Asesor: {self.asesor}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar_parametros()

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total

