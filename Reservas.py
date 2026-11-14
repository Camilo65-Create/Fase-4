from Clientes import Cliente
from servicios import Servicio
from Excepciones import ErrorDatos, ErrorEstado, ErrorProceso
from Logs import registro

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if not isinstance(cliente, Cliente):
            raise ErrorDatos("El cliente proporcionado no es válido.")

        if not isinstance(servicio, Servicio):
            raise ErrorDatos("El servicio proporcionado no es válido.")

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ErrorDatos("La duración debe ser un número mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

        def calcular_costo(self):
            return self.servicio.calcular_costo(self.duracion)

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ErrorEstado("Solo se pueden confirmar reservas pendientes.")

        self.estado = "Confirmada"
        registro.info(f"Reserva confirmada para el cliente {self.cliente.id}")        

    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise ErrorEstado("No se puede cancelar esta reserva.")

        self.estado = "Cancelada"
        registro.info(f"Reserva cancelada para el cliente {self.cliente.id}")

    def procesar(self):
        if self.estado != "Confirmada":
            raise ErrorEstado("Solo se pueden procesar reservas confirmadas.")

        try:
            costo = self.calcular_costo()

        except Exception as error:
            registro.exception("Error al procesar la reserva.")
            raise ErrorProceso(
                "No se pudo completar el procesamiento de la reserva."
            ) from error

        else:
            self.estado = "Procesada"

            registro.info(
                f"Reserva procesada para el cliente {self.cliente.id}. "
                f"Costo total: {costo}"
            )

            return costo

        finally:
            registro.info(
                f"Finalizó el intento de procesamiento de la reserva "
                f"del cliente {self.cliente.id}."
            )

    def describir(self):
        return (
            f"Reserva del cliente: {self.cliente.nombre}. "
            f"Servicio: {self.servicio.nombre}. "
            f"Duración: {self.duracion} horas. "
            f"Estado: {self.estado}."
        )