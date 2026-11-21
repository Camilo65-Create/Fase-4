# Importaciones necesarias
from Clientes import Cliente
from servicios import Servicio
from Excepciones import ErrorDatos, ErrorEstado, ErrorProceso
from Logs import registro


# Clase que representa una reserva realizada por un cliente.
class Reserva:

    def __init__(self, cliente, servicio, duracion):
        """Inicializa una reserva con su cliente, servicio y duración."""

        # Comprueba que el cliente sea un objeto de la clase Cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorDatos("El cliente proporcionado no es válido.")

        # Comprueba que el servicio pertenezca a la clase Servicio.
        if not isinstance(servicio, Servicio):
            raise ErrorDatos("El servicio proporcionado no es válido.")

        # Verifica que la duración sea un número positivo.
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ErrorDatos("La duración debe ser un número mayor que cero.")

        # Almacena los datos de la reserva y establece su estado inicial.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def calcular_costo(self):
        """Calcula el costo de la reserva utilizando el servicio seleccionado."""
        return self.servicio.calcular_costo(self.duracion)

    def confirmar(self):
        """Confirma una reserva que se encuentre en estado pendiente."""

        # Solo se pueden confirmar las reservas pendientes.
        if self.estado != "Pendiente":
            registro.error(
                "Intento de confirmar una reserva que no está pendiente."
            )
            raise ErrorEstado("Solo se pueden confirmar reservas pendientes.")

        # Actualiza el estado y registra la confirmación.
        self.estado = "Confirmada"
        registro.info(f"Reserva confirmada para el cliente {self.cliente.id}")

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        # Comprueba que la reserva pueda ser cancelada.
        if self.estado not in ("Pendiente", "Confirmada"):
            registro.error(
                "Intento de cancelar una reserva que no puede cancelarse."
            )
            raise ErrorEstado("No se puede cancelar esta reserva.")

        # Actualiza el estado y registra la cancelación.
        self.estado = "Cancelada"
        registro.info(f"Reserva cancelada para el cliente {self.cliente.id}")

    def procesar(self):
        """Procesa una reserva confirmada y devuelve el costo final."""

        # Verifica que la reserva haya sido confirmada previamente.
        if self.estado != "Confirmada":
            registro.error("Intento de procesar una reserva que no está confirmada.")
            raise ErrorEstado("Solo se pueden procesar reservas confirmadas.")

        try:
            # Calcula el costo de la reserva.
            costo = self.calcular_costo()

        except Exception as error:
            # Registra el error y genera una excepción propia del sistema.
            registro.exception("Error al procesar la reserva.")
            raise ErrorProceso(
                "No se pudo completar el procesamiento de la reserva."
            ) from error

        else:
            # Si el cálculo es correcto, cambia el estado de la reserva.
            self.estado = "Procesada"

            registro.info(
                f"Reserva procesada para el cliente {self.cliente.id}. "
                f"Costo total: {costo}"
            )

            return costo

        finally:
            # Registra la finalización del intento de procesamiento,
            # independientemente de si ocurrió un error.
            registro.info(
                f"Finalizó el intento de procesamiento de la reserva "
                f"del cliente {self.cliente.id}."
            )

    def describir(self):
        """Devuelve un resumen con la información y el estado de la reserva."""
        return (
            f"Reserva del cliente: {self.cliente.nombre}. "
            f"Servicio: {self.servicio.nombre}. "
            f"Duración: {self.duracion} horas. "
            f"Estado: {self.estado}."
        )
