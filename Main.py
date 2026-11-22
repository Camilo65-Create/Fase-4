# Importaciones necesarias
from Logs import registro, formatear_pesos
from Sistema import Sistema
from Clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from Excepciones import ErrorFJ


# Registra los servicios disponibles al iniciar el sistema.
def cargar_servicios(sistema):
    """Crea los servicios iniciales y los registra en el sistema."""

    # Servicio de alquiler de salas.
    sala = ReservaSala(
        "Reserva de salas",
        "Alquiler de salas para reuniones",
        50000,
        20
    )

    # Servicio de alquiler de equipos.
    equipo = AlquilerEquipo(
        "Alquiler de equipos",
        "Alquiler de computadores",
        30000,
        "Computador",
        5
    )

    # Servicio de asesoría empresarial.
    asesoria = Asesoria(
        "Asesoria empresarial",
        "Consultoria para empresas",
        80000,
        "Administracion",
        "Juan Perez"
    )

    # Agrega los tres servicios a la lista del sistema.
    sistema.registrar_servicio(sala)
    sistema.registrar_servicio(equipo)
    sistema.registrar_servicio(asesoria)


# Presenta las opciones disponibles para el usuario.
def mostrar_menu():
    """Muestra el menú principal de Software FJ."""

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


# Permite seleccionar una reserva existente.
def seleccionar_reserva(sistema):
    """Muestra las reservas y permite elegir una por su posición."""

    sistema.mostrar_reservas()

    # Comprueba si existen reservas registradas.
    if not sistema.reservas:
        return None

    posicion = int(input("Ingrese el numero de la reserva: "))
    return sistema.buscar_reserva(posicion)


# Función principal que controla la ejecución del programa.
def ejecutar():
    """Inicia el sistema y controla las operaciones del menú."""

    # Crea el sistema y carga los servicios disponibles.
    sistema = Sistema()
    cargar_servicios(sistema)

    # Mantiene el menú activo hasta que el usuario decida salir.
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ")

        try:
            # Opción 1: registrar un nuevo cliente.
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

            # Opción 2: mostrar los clientes registrados.
            elif opcion == "2":
                sistema.mostrar_clientes()

            # Opción 3: mostrar los servicios disponibles.
            elif opcion == "3":
                sistema.mostrar_servicios()

            # Opción 4: crear una reserva.
            elif opcion == "4":

                # Verifica que exista al menos un cliente registrado.
                if not sistema.clientes:
                    print("Primero debe registrar un cliente.")
                    continue

                # Muestra los clientes para seleccionar uno.
                print("\nClientes disponibles:")
                for i, cliente in enumerate(sistema.clientes, start=1):
                    print(f"{i}. {cliente.describir()}")

                numero_cliente = int(input("Seleccione el cliente: "))
                # Valida la selección antes de acceder a la lista.
                if not 1 <= numero_cliente <= len(sistema.clientes):
                    raise ValueError("Seleccione un número de cliente válido.")
                cliente = sistema.clientes[numero_cliente - 1]

                # Muestra los servicios disponibles para seleccionar uno.
                print("\nServicios disponibles:")
                for i, servicio in enumerate(sistema.servicios, start=1):
                    print(f"{i}. {servicio.describir()}")

                numero_servicio = int(input("Seleccione el servicio: "))
                # Rechaza posiciones inexistentes, cero y números negativos.
                if not 1 <= numero_servicio <= len(sistema.servicios):
                    raise ValueError("Seleccione un número de servicio válido.")
                servicio = sistema.servicios[numero_servicio - 1]

                # Solicita la duración de la reserva.
                duracion = float(input("Duracion en horas: "))

                # Crea la reserva y muestra su información.
                reserva = sistema.crear_reserva(
                    cliente, servicio, duracion
                )

                print("Reserva creada correctamente.")
                print(reserva.describir())

            # Opción 5: mostrar todas las reservas.
            elif opcion == "5":
                sistema.mostrar_reservas()

            # Opción 6: confirmar una reserva.
            elif opcion == "6":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    reserva.confirmar()
                    print("Reserva confirmada.")

            # Opción 7: cancelar una reserva.
            elif opcion == "7":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    reserva.cancelar()
                    print("Reserva cancelada.")

            # Opción 8: procesar una reserva confirmada.
            elif opcion == "8":
                reserva = seleccionar_reserva(sistema)

                if reserva:
                    costo = reserva.procesar()
                    print(
                        "Reserva procesada. Costo total: "
                        f"{formatear_pesos(costo)}"
                    )
            # Opción 0: finalizar la ejecución.
            elif opcion == "0":
                print("Gracias por utilizar Software FJ.")
                break

            # Informa cuando el usuario selecciona una opción inexistente.
            else:
                print("Opcion no valida. Intente nuevamente.")

        # Controla errores propios del sistema y errores de entrada.
        except (ErrorFJ, ValueError, IndexError, TypeError) as error:
            # Guarda el error y su detalle técnico en el archivo de logs.
            registro.exception("Error durante una operación del menú.")
            # Informa al usuario sin cerrar la aplicación.
            print("No se pudo completar la operación:", error)


# Ejecuta el programa únicamente cuando este archivo se inicia directamente.
if __name__ == "__main__":
    ejecutar()
