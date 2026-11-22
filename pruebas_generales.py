# Herramienta incluida en Python para realizar pruebas automáticas.
import unittest

# Clases que se utilizarán durante las pruebas.
from Clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from Reservas import Reserva
from Sistema import Sistema

# Excepciones propias y registro de eventos.
from Excepciones import ErrorDatos, ErrorEstado, ErrorProceso
from Logs import registro


# Servicio de prueba que provoca un fallo durante el cálculo.
class SalaConError(ReservaSala):

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Simula un error para comprobar su manejo."""
        raise ValueError("Fallo de cálculo provocado por la prueba.")


# Agrupa las pruebas del programa.
class PruebasSoftwareFJ(unittest.TestCase):

    def setUp(self):
        """Prepara datos nuevos antes de cada prueba."""
        self.sistema = Sistema()

        self.cliente = Cliente(
            "12345678",
            "Carlos Vasquez",
            "carlos@gmail.com",
            "3001234567"
        )

        self.sala = ReservaSala(
            "Sala de reuniones",
            "Sala para reuniones empresariales",
            50000,
            20
        )

    def comprobar_error(self, tipo_error, operacion, *args, **kwargs):
        """Verifica un error esperado y lo guarda en el log."""
        try:
            operacion(*args, **kwargs)

        except tipo_error as error:
            # Registra el error esperado con su detalle.
            registro.exception(
                "Error esperado en %s",
                self._testMethodName
            )
            return error

        else:
            # La prueba falla si la operación no rechaza el dato.
            self.fail(
                f"Se esperaba una excepción {tipo_error.__name__}."
            )

    def test_01_cliente_valido(self):
        """Registrar un cliente válido."""
        self.sistema.registrar_cliente(self.cliente)

        # Comprueba que el cliente quedó guardado.
        self.assertIn(self.cliente, self.sistema.clientes)

    def test_02_correo_invalido(self):
        """Rechazar un cliente con correo incorrecto."""
        self.comprobar_error(
            ErrorDatos,
            Cliente,
            "87654321",
            "Ana Perez",
            "correo-invalido",
            "3007654321"
        )

    def test_03_cliente_duplicado(self):
        """Rechazar dos clientes con el mismo documento."""
        self.sistema.registrar_cliente(self.cliente)

        # Crea otro objeto con el mismo documento.
        duplicado = Cliente(
            "12345678",
            "Carlos Perez",
            "otro@gmail.com",
            "3007654321"
        )

        self.comprobar_error(
            ErrorDatos,
            self.sistema.registrar_cliente,
            duplicado
        )

        # El registro rechazado no debe aumentar la lista.
        self.assertEqual(len(self.sistema.clientes), 1)

    def test_04_tres_servicios_validos(self):
        """Crear y registrar los tres tipos de servicio."""
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

        # Usa los servicios mediante su interfaz común.
        for servicio in (self.sala, equipo, asesoria):
            self.sistema.registrar_servicio(servicio)
            self.assertGreater(servicio.calcular_costo(2), 0)

        self.assertEqual(len(self.sistema.servicios), 3)

    def test_05_tarifa_negativa(self):
        """Rechazar una sala con tarifa negativa."""
        self.comprobar_error(
            ValueError,
            ReservaSala,
            "Sala invalida",
            "Sala para reuniones",
            -50000,
            20
        )

    def test_06_equipo_sin_cantidad(self):
        """Rechazar un servicio con cero equipos."""
        self.comprobar_error(
            ValueError,
            AlquilerEquipo,
            "Alquiler de equipos",
            "Alquiler de computadores",
            30000,
            "Computador",
            0
        )

    def test_07_duraciones_invalidas(self):
        """Rechazar duraciones incorrectas."""
        duraciones = (0, -2, float("nan"), float("inf"), True)

        # Revisa cada duración por separado.
        for duracion in duraciones:
            with self.subTest(duracion=duracion):
                self.comprobar_error(
                    ErrorDatos,
                    Reserva,
                    self.cliente,
                    self.sala,
                    duracion
                )

    def test_08_cliente_no_registrado(self):
        """Rechazar una reserva con cliente no registrado."""
        self.sistema.registrar_servicio(self.sala)

        self.comprobar_error(
            ErrorDatos,
            self.sistema.crear_reserva,
            self.cliente,
            self.sala,
            2
        )

        self.assertEqual(len(self.sistema.reservas), 0)

    def test_09_servicio_no_registrado(self):
        """Rechazar una reserva con servicio no registrado."""
        self.sistema.registrar_cliente(self.cliente)

        self.comprobar_error(
            ErrorDatos,
            self.sistema.crear_reserva,
            self.cliente,
            self.sala,
            2
        )

        self.assertEqual(len(self.sistema.reservas), 0)

    def test_10_reserva_completa(self):
        """Crear, confirmar y procesar una reserva válida."""
        self.sistema.registrar_cliente(self.cliente)
        self.sistema.registrar_servicio(self.sala)

        reserva = self.sistema.crear_reserva(
            self.cliente,
            self.sala,
            2
        )

        self.assertEqual(reserva.estado, "Pendiente")

        reserva.confirmar()
        self.assertEqual(reserva.estado, "Confirmada")

        costo = reserva.procesar()

        # Dos horas a 50.000 deben costar 100.000.
        self.assertEqual(costo, 100000)
        self.assertEqual(reserva.estado, "Procesada")

    def test_11_reserva_cancelada(self):
        """Impedir el procesamiento de una reserva cancelada."""
        reserva = Reserva(self.cliente, self.sala, 2)
        reserva.cancelar()

        self.comprobar_error(
            ErrorEstado,
            reserva.procesar
        )

        self.assertEqual(reserva.estado, "Cancelada")

    def test_12_parametro_faltante(self):
        """Controlar la ausencia del teléfono obligatorio."""
        self.comprobar_error(
            TypeError,
            Cliente,
            "87654321",
            "Ana Perez",
            "ana@gmail.com"
        )

    def test_13_error_encadenado(self):
        """Comprobar ErrorProceso y su excepción original."""
        sala_con_error = SalaConError(
            "Sala de prueba",
            "Servicio que simula un fallo",
            50000,
            10
        )

        reserva = Reserva(
            self.cliente,
            sala_con_error,
            2
        )
        reserva.confirmar()

        error = self.comprobar_error(
            ErrorProceso,
            reserva.procesar
        )

        # Comprueba que 'raise ... from error' conservó la causa.
        self.assertIsInstance(error.__cause__, ValueError)

        # Una reserva cuyo procesamiento falla no debe quedar procesada.
        self.assertEqual(reserva.estado, "Confirmada")

    def test_14_impuesto_y_descuento(self):
        """Comprobar el cálculo con porcentajes opcionales."""
        costo = self.sala.calcular_costo(
            3,
            impuesto=10,
            descuento=5
        )

        # 150.000 menos 5 %, y luego más 10 %.
        self.assertAlmostEqual(costo, 156750)

    def test_15_continuar_despues_de_error(self):
        """Completar una operación válida después de un error."""
        self.sistema.registrar_cliente(self.cliente)
        self.sistema.registrar_servicio(self.sala)

        # Primero provoca un error controlado.
        self.comprobar_error(
            ErrorDatos,
            self.sistema.crear_reserva,
            self.cliente,
            self.sala,
            0
        )

        # Después realiza una reserva válida en el mismo sistema.
        reserva = self.sistema.crear_reserva(
            self.cliente,
            self.sala,
            1
        )

        reserva.confirmar()
        costo = reserva.procesar()

        self.assertEqual(costo, 50000)
        self.assertEqual(reserva.estado, "Procesada")
        self.assertEqual(len(self.sistema.reservas), 1)


# Ejecuta las pruebas solo al iniciar directamente este archivo.
if __name__ == "__main__":
    unittest.main(verbosity=2)
