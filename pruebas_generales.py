from servicios import ReservaSala, AlquilerEquipo, Asesoria
from Excepciones import ErrorEstado
from Clientes import Cliente
from Reservas import Reserva

# sala1 = ReservaSala(
#     "Reserva de salas",
#     "Alquiler de salas para reuniones",
#     50000,
#     20
# )

# print(sala1.describir())
# print("Costo:", sala1.calcular_costo(3))

# Crear un cliente
cliente1 = Cliente(
    "12345678",
    "Carlos Vasquez",
    "carlos@gmail.com",
    "3001234567"
)

# Crear un servicio
sala1 = ReservaSala(
    "Reserva de salas",
    "Alquiler de salas para reuniones",
    50000,
    20
)

# Crear una reserva
reserva1 = Reserva(cliente1, sala1, 3)

# Mostrar información
print(reserva1.describir())
print("Costo:", reserva1.calcular_costo())

# Confirmar la reserva
reserva1.confirmar()

# Procesar la reserva
print("Costo final:", reserva1.procesar())

try:
    reserva1.confirmar()

except ErrorEstado as error:
    print("Error controlado:", error)


# Crear una segunda reserva
reserva2 = Reserva(cliente1, sala1, 2)

# Cancelar la reserva
reserva2.cancelar()

print("\nSegunda reserva:")
print(reserva2.describir())


# Intentar procesar una reserva cancelada
try:
    reserva2.procesar()

except ErrorEstado as error:
    print("Error controlado:", error)