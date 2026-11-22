# Importaciones necesarias
from Clientes import Cliente
from servicios import Servicio
from Reservas import Reserva
from Excepciones import ErrorDatos
from Logs import registro


# Clase encargada de administrar los clientes, servicios y reservas.
class Sistema:

    def __init__(self):
        """Inicializa las listas donde se almacenan los datos del sistema."""
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        """Registra un cliente después de comprobar que sea válido."""

        # Verifica que el objeto recibido pertenezca a la clase Cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorDatos("El cliente no es válido.")

        # Evita registrar dos clientes con el mismo documento.
        if any(c.documento == cliente.documento for c in self.clientes):
            raise ErrorDatos("El cliente ya está registrado.")

        self.clientes.append(cliente)

        # Registra la operación realizada.
        registro.info(f"Cliente registrado: {cliente.nombre}")

        def registrar_servicio(self, servicio):
        """Valida un servicio antes de incorporarlo al sistema."""
        try:
            # Comprueba que el objeto pertenezca a la clase Servicio.
            if not isinstance(servicio, Servicio):
                raise ErrorDatos("El servicio no es válido.")

            # Rechaza servicios con tarifas, capacidades o cantidades inválidas.
            servicio.validar_parametros()

        except (ErrorDatos, ValueError, TypeError):
            # Registra el error y lo comunica al código que llamó al método.
            registro.exception("No se pudo registrar el servicio.")
            raise

        else:
            # Solo incorpora el servicio cuando todas las validaciones pasan.
            self.servicios.append(servicio)
            registro.info(f"Servicio registrado: {servicio.nombre}")

    def crear_reserva(self, cliente, servicio, duracion):
        """Crea una reserva utilizando un cliente y un servicio registrados."""

        # Comprueba que el cliente pertenezca al sistema.
        if cliente not in self.clientes:
            raise ErrorDatos("El cliente no está registrado en el sistema.")

        # Comprueba que el servicio esté disponible en el sistema.
        if servicio not in self.servicios:
            raise ErrorDatos("El servicio no está registrado en el sistema.")

        # Crea la reserva y la almacena en la lista correspondiente.
        reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(reserva)

        registro.info(
            f"Reserva creada para el cliente {cliente.nombre}."
        )

        return reserva

    def buscar_cliente(self, documento):
        """Busca un cliente mediante su número de documento."""

        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente

        # Devuelve None cuando no encuentra coincidencias.
        return None

    def buscar_servicio(self, id_servicio):
        """Busca un servicio utilizando su identificador."""

        for servicio in self.servicios:
            if servicio.id == id_servicio:
                return servicio

        return None

    def buscar_reserva(self, posicion):
        """Busca una reserva según su posición dentro de la lista."""

        # Verifica que la posición recibida sea un número entero.
        if not isinstance(posicion, int) or isinstance(posicion, bool):
            raise ErrorDatos("La posición debe ser un número entero.")

        # Comprueba que la posición corresponda a una reserva existente.
        if posicion < 1 or posicion > len(self.reservas):
            raise ErrorDatos("No existe una reserva en esa posición.")

        # Resta uno porque las listas comienzan en la posición cero.
        return self.reservas[posicion - 1]

    def mostrar_clientes(self):
        """Muestra la información de todos los clientes registrados."""

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for cliente in self.clientes:
            print(cliente.describir())

    def mostrar_servicios(self):
        """Muestra la información de los servicios registrados."""

        if not self.servicios:
            print("No hay servicios registrados.")
            return

        for servicio in self.servicios:
            print(servicio.describir())

    def mostrar_reservas(self):
        """Muestra las reservas registradas y su posición en la lista."""

        if not self.reservas:
            print("No hay reservas registradas.")
            return

        for posicion, reserva in enumerate(self.reservas, start=1):
            print(f"{posicion}. {reserva.describir()}")
