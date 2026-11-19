
from Sistema import Sistema
from Clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from Excepciones import ErrorFJ


def cargar_servicios(sistema):
    sala = ReservaSala(
        "Reserva de salas",
        "Alquiler de salas para reuniones",
        50000,
        20
    )

    equipo = AlquilerEquipo(
        "Alquiler de equipos",
        "Alquiler de computadores",
        30000,
        "Computador",
        5
    )

    asesoria = Asesoria(
        "Asesoria empresarial",
        "Consultoria para empresas",
        80000,
        "Administracion",
        "Juan Perez"
    )

    sistema.registrar_servicio(sala)
    sistema.registrar_servicio(equipo)
    sistema.registrar_servicio(asesoria)


def mostrar_menu():
    print("\n========== SOFTWARE FJ ==========")
    print("1. Registrar cliente")
    print("2. Mostrar clientes")
    print("3. Mostrar servicios")
    print("4. Crear reserva")
    print("5. Mostrar reservas")
    print("6. Confirmar reserva")
    print("7. Cancelar reserva")
    print("8. Procesar reserva")
    print("0. Salir")
    print("=================================")


def seleccionar_reserva(sistema):
    sistema.mostrar_reservas()

    if not sistema.reservas:
        return None

    posicion = int(input("Ingrese el numero de la reserva: "))
    return sistema.buscar_reserva(posicion)


def ejecutar():
    sistema = Sistema()
    cargar_servicios(sistema)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ")

        try:
            if opcion == "1":
                documento = input("Documento: ")
                nombre = input("Nombre completo: ")
                correo = input("Correo electronico: ")
                telefono = input("Telefono: ")

                cliente = Cliente(
                    documento, nombre, correo, telefono
                )

                sistema.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")

            elif opcion == "2":
                sistema.mostrar_clientes()

            elif opcion == "3":
                sistema.mostrar_servicios()

            elif opcion == "4":
                if not sistema.clientes:
                    print("Primero debe registrar un cliente.")
                    continue

                print("\nClientes disponibles:")
                for i, cliente in enumerate(sistema.clientes, start=1):
                    print(f"{i}. {cliente.describir()}")

                numero_cliente = int(input("Seleccione el cliente: "))
                cliente = sistema.clientes[numero_cliente - 1]

                print("\nServicios disponibles:")
                for i, servicio in enumerate(sistema.servicios, start=1):
                    print(f"{i}. {servicio.describir()}")

                numero_servicio = int(input("Seleccione el servicio: "))
                servicio = sistema.servicios[numero_servicio - 1]

                duracion = float(input("Duracion en horas: "))

                reserva = sistema.crear_reserva(
                    cliente, servicio, duracion
                )

                print("Reserva creada correctamente.")
                print(reserva.describir())

            elif opcion == "5":
                sistema.mostrar_reservas()

            elif opcion == "6":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    reserva.confirmar()
                    print("Reserva confirmada.")

            elif opcion == "7":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    reserva.cancelar()
                    print("Reserva cancelada.")

            elif opcion == "8":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    costo = reserva.procesar()
                    print(f"Reserva procesada. Costo total: ${costo:,.2f}")

            elif opcion == "0":
                print("Gracias por utilizar Software FJ.")
                break

            else:
                print("Opcion no valida. Intente nuevamente.")

        except (ErrorFJ, ValueError, IndexError) as error:
            print("No se pudo completar la operacion:", error)


if __name__ == "__main__":
    ejecutar()
