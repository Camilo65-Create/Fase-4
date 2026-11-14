from servicios import ReservaSala, AlquilerEquipo, Asesoria
from Excepciones import ErrorEstado, ErrorProceso
from Clientes import Cliente
from Reservas import Reserva

sala1 = ReservaSala(
    "Reserva de salas",
    "Alquiler de salas para reuniones",
    50000,
    20
)

print(sala1.describir())
print("Costo:", sala1.calcular_costo(3))

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

# Crear servicio de alquiler de equipo
equipo1 = AlquilerEquipo(
    "Alquiler de equipos",
    "Alquiler de computadores",
    30000,
    "Computador",
    5
)

print("\nPrueba de alquiler de equipo:")
print(equipo1.describir())
print("Costo por 3 horas:", equipo1.calcular_costo(3))

# Crear servicio de asesoría
asesoria1 = Asesoria(
    "Asesoría empresarial",
    "Consultoría para empresas",
    80000,
    "Administración",
    "Juan Pérez"
)

print("\nPrueba de asesoría:")
print(asesoria1.describir())
print("Costo por 3 horas:", asesoria1.calcular_costo(3))

# Prueba de validación de alquiler de equipos
try:
    equipo_invalido = AlquilerEquipo(
        "Alquiler de equipos",
        "Alquiler de computadores",
        30000,
        "Computador",
        0
    )

    equipo_invalido.validar_parametros()

except ValueError as error:
    print("\nError controlado:", error)

try:
    sala_invalida = ReservaSala(
        "Sala de reuniones",
        "Sala para eventos",
        -50000,
        20
    )

    sala_invalida.validar_parametros()

except ValueError as error:
    print("\nError controlado:", error)

print("\nPrueba de impuesto y descuento:")
print(
    "Costo con impuesto del 10% y descuento del 5%:",
    sala1.calcular_costo(3, impuesto=10, descuento=5)
)