# Herramientas para definir métodos abstractos y validar números.
from abc import abstractmethod
from math import isfinite

# Importa la entidad general y la validación de textos.
from Clientes import Entidad, validar_texto


def es_numero_valido(valor):
    """Acepta números finitos y rechaza booleanos."""
    return (
        isinstance(valor, (int, float))
        and not isinstance(valor, bool)
        and isfinite(valor)
    )


# Clase abstracta de la que heredan los servicios especializados.
class Servicio(Entidad):

    def __init__(self, nombre, descripcion, tarifa):
        """Guarda los datos generales del servicio."""
        super().__init__()

        self.nombre = validar_texto(nombre, "Nombre del servicio")
        self.descripcion = validar_texto(descripcion, "Descripción")
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Cada servicio debe implementar su cálculo."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Cada servicio debe validar sus datos."""
        pass

    def validar_tarifa(self):
        """Comprueba que la tarifa sea un número positivo."""
        if not es_numero_valido(self.tarifa) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número positivo.")

    def validar_calculo(self, horas, impuesto, descuento):
        """Revisa los datos utilizados para calcular un costo."""
        if not es_numero_valido(horas) or horas <= 0:
            raise ValueError("Las horas deben ser un número positivo.")

        if not es_numero_valido(impuesto) or not 0 <= impuesto <= 100:
            raise ValueError("El impuesto debe estar entre 0 y 100.")

        if not es_numero_valido(descuento) or not 0 <= descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")


# Servicio especializado para reservar salas.
class ReservaSala(Servicio):

    def __init__(self, nombre, descripcion, tarifa, capacidad):
        """Crea una sala y comprueba que sus datos sean válidos."""
        super().__init__(nombre, descripcion, tarifa)

        self.capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self):
        """Valida la tarifa y la capacidad de la sala."""
        self.validar_tarifa()

        # Exige un entero positivo y rechaza booleanos.
        if type(self.capacidad) is not int or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo.")

    def describir(self):
        """Devuelve la descripción de la sala."""
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Capacidad: {self.capacidad} personas."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de la sala con porcentajes opcionales."""
        self.validar_parametros()
        self.validar_calculo(horas, impuesto, descuento)

        # Aplica primero el descuento y después el impuesto.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total


# Servicio especializado para alquilar equipos.
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, descripcion, tarifa, equipo, cantidad):
        """Crea un servicio de equipos y valida sus datos."""
        super().__init__(nombre, descripcion, tarifa)

        self.equipo = validar_texto(equipo, "Nombre del equipo")
        self.cantidad = cantidad
        self.validar_parametros()

    def validar_parametros(self):
        """Valida la tarifa y la cantidad de equipos."""
        self.validar_tarifa()

        # Solo acepta cantidades enteras positivas.
        if type(self.cantidad) is not int or self.cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

    def describir(self):
        """Devuelve la información de los equipos."""
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Equipo: {self.equipo}. "
            f"Cantidad disponible: {self.cantidad}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el alquiler según las horas contratadas."""
        self.validar_parametros()
        self.validar_calculo(horas, impuesto, descuento)

        # Conserva la fórmula original de tarifa por hora.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total


# Servicio especializado para ofrecer asesorías.
class Asesoria(Servicio):

    def __init__(self, nombre, descripcion, tarifa, especialidad, asesor):
        """Crea una asesoría y comprueba sus datos."""
        super().__init__(nombre, descripcion, tarifa)

        self.especialidad = validar_texto(especialidad, "Especialidad")
        self.asesor = validar_texto(asesor, "Nombre del asesor")
        self.validar_parametros()

    def validar_parametros(self):
        """Comprueba que la tarifa de la asesoría sea válida."""
        self.validar_tarifa()

    def describir(self):
        """Devuelve la especialidad y el asesor responsable."""
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Especialidad: {self.especialidad}. "
            f"Asesor: {self.asesor}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de la asesoría."""
        self.validar_parametros()
        self.validar_calculo(horas, impuesto, descuento)

        # Aplica descuento e impuesto al valor de las horas.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total
