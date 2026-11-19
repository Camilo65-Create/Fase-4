from Clientes import Cliente
from servicios import Servicio
from Reservas import Reserva
from Excepciones import ErrorDatos
from Logs import registro


class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorDatos("El cliente no es válido.")

        if any(c.documento == cliente.documento for c in self.clientes):
            raise ErrorDatos("El cliente ya está registrado.")

        self.clientes.append(cliente)
        registro.info(f"Cliente registrado: {cliente.nombre}")

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorDatos("El servicio no es válido.")

        self.servicios.append(servicio)
        registro.info(f"Servicio registrado: {servicio.nombre}")

    def crear_reserva(self, cliente, servicio, duracion):
        if cliente not in self.clientes:
            raise ErrorDatos("El cliente no está registrado en el sistema.")

        if servicio not in self.servicios:
            raise ErrorDatos("El servicio no está registrado en el sistema.")

        reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(reserva)

        registro.info(
            f"Reserva creada para el cliente {cliente.nombre}."
        )

        return reserva

    def buscar_cliente(self, documento):
        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente

        return None

    def buscar_servicio(self, id_servicio):
        for servicio in self.servicios:
            if servicio.id == id_servicio:
                return servicio

        return None

    def buscar_reserva(self, posicion):
        if not isinstance(posicion, int) or isinstance(posicion, bool):
            raise ErrorDatos("La posición debe ser un número entero.")

        if posicion < 1 or posicion > len(self.reservas):
            raise ErrorDatos("No existe una reserva en esa posición.")

        return self.reservas[posicion - 1]

    def mostrar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for cliente in self.clientes:
            print(cliente.describir())

    def mostrar_servicios(self):
        if not self.servicios:
            print("No hay servicios registrados.")
            return

        for servicio in self.servicios:
            print(servicio.describir())

    def mostrar_reservas(self):
        if not self.reservas:
            print("No hay reservas registradas.")
            return

        for posicion, reserva in enumerate(self.reservas, start=1):
            print(f"{posicion}. {reserva.describir()}")
