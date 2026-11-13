from servicios import ReservaSala, AlquilerEquipo, Asesoria

sala1 = ReservaSala(
    "Reserva de salas",
    "Alquiler de salas para reuniones",
    50000,
    20
)

print(sala1.describir())
print("Costo:", sala1.calcular_costo(3))

