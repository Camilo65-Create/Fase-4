# Importaciones necesarias
from abc import abstractmethod
from Clientes import Entidad, validar_texto


# Clase abstracta que representa los servicios de Software FJ.
# Hereda de Entidad y establece los métodos que deben implementar
# las clases de servicios especializados.
class Servicio(Entidad):

    def __init__(self, nombre, descripcion, tarifa):
        """Inicializa los datos generales de un servicio."""
        super().__init__()

        # Valida y almacena la información básica del servicio.
        self.nombre = validar_texto(nombre, "Nombre de serivicio")
        self.descripcion = validar_texto(descripcion, "Descripción")
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo del servicio según su duración."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Verifica que los datos del servicio sean válidos."""
        pass


# Servicio especializado para el alquiler de salas.
class ReservaSala(Servicio):

    def __init__(self, nombre, descripcion, tarifa, capacidad):
        """Inicializa una sala con su información y capacidad."""
        super().__init__(nombre, descripcion, tarifa)
        self.capacidad = capacidad

    def describir(self):
        """Devuelve una descripción de la sala y su capacidad."""
        return f"{self.nombre}: {self.descripcion}. Capacidad: {self.capacidad} personas."

    def validar_parametros(self):
        """Comprueba que la tarifa y la capacidad sean válidas."""

        # La tarifa debe ser un número positivo.
        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

        # La capacidad debe ser un entero positivo.
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo.")

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de alquiler de la sala."""

        self.validar_parametros()

        if horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        # Verifica que el impuesto y el descuento sean porcentajes válidos.
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        # Calcula el subtotal, aplica el descuento y después el impuesto.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total


# Servicio especializado para el alquiler de equipos.
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, descripcion, tarifa, equipo, cantidad):
        """Inicializa el servicio con el tipo y cantidad de equipos."""
        super().__init__(nombre, descripcion, tarifa)

        self.equipo = validar_texto(equipo, "Nombre del equipo")
        self.cantidad = cantidad

    def validar_parametros(self):
        """Comprueba que la tarifa y la cantidad de equipos sean válidas."""

        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

    def describir(self):
        """Devuelve la información del equipo y su cantidad disponible."""
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Equipo: {self.equipo}. Cantidad disponible: {self.cantidad}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo del alquiler de equipos según las horas."""

        self.validar_parametros()

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        # Comprueba que los porcentajes estén dentro del rango permitido.
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        # Aplica primero el descuento y luego el impuesto al subtotal.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total


# Servicio especializado que ofrece asesorías profesionales.
class Asesoria(Servicio):

    def __init__(self, nombre, descripcion, tarifa, especialidad, asesor):
        """Inicializa la asesoría con su especialidad y responsable."""
        super().__init__(nombre, descripcion, tarifa)

        self.especialidad = validar_texto(especialidad, "Especialidad")
        self.asesor = validar_texto(asesor, "Nombre del asesor")

    def validar_parametros(self):
        """Comprueba que la tarifa de la asesoría sea válida."""

        if not isinstance(self.tarifa, (int, float)) or self.tarifa <= 0:
            raise ValueError("La tarifa debe ser un número mayor que cero.")

    def describir(self):
        """Devuelve la información de la asesoría y del asesor."""
        return (
            f"{self.nombre}: {self.descripcion}. "
            f"Especialidad: {self.especialidad}. Asesor: {self.asesor}."
        )

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo de la asesoría según su duración."""

        self.validar_parametros()

        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        # Verifica que los porcentajes del impuesto y descuento sean válidos.
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise ValueError("El impuesto y el descuento deben estar entre 0 y 100.")

        # Calcula el valor final aplicando descuento e impuesto.
        subtotal = self.tarifa * horas
        subtotal -= subtotal * (descuento / 100)
        total = subtotal + subtotal * (impuesto / 100)

        return total