# Software-FJ

# Estas librerías permiten validar los datos y guardar los errores.
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4

carpeta = Path(__file__).resolve().parent / "logs"
carpeta.mkdir(exist_ok=True)
registro = logging.getLogger("software_fj_entrega")

if not registro.handlers:
    archivo = logging.FileHandler(
        carpeta / "eventos.log", encoding="utf-8"
    )
    archivo.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )
    registro.addHandler(archivo)

registro.setLevel(logging.INFO)
registro.propagate = False


# Los errores propios se registran cuando se detectan.
class ErrorFJ(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        registro.error(
            "%s: %s", type(self).__name__, mensaje
        )


class ErrorDatos(ErrorFJ):
    """Un dato no cumple las reglas."""


class ErrorEstado(ErrorFJ):
    """La operación no corresponde al estado actual."""


class ErrorProceso(ErrorFJ):
    """No se pudo terminar una reserva."""


# Todos los registros tienen un identificador y una descripción.
class Entidad(ABC):
    def __init__(self):
        self.__id = uuid4().hex[:12]

    @property
    def id(self):
        return self.__id

    @abstractmethod
    def describir(self):
        """Cada clase presenta sus propios datos."""


# Esta función revisa los nombres y otros textos.
def validar_texto(valor, campo):
    if (
        not isinstance(valor, str)
        or not 2 <= len(valor.strip()) <= 120
    ):
        raise ErrorDatos(
            f"{campo}: escribe un texto de 2 a 120 caracteres."
        )
    return valor.strip()


# Los datos se validan antes de guardarlos en atributos privados.
class Cliente(Entidad):
    def __init__(self, documento, nombre, correo, telefono):
        super().__init__()

        datos = (documento, nombre, correo, telefono)

        if not all(isinstance(dato, str) for dato in datos):
            raise ErrorDatos(
                "Los datos del cliente deben ser textos."
            )

        documento = documento.strip()
        correo = correo.strip().lower()
        telefono = telefono.strip()
        nombre = validar_texto(nombre, "Nombre")

        if not re.fullmatch(r"[0-9]{5,15}", documento):
            raise ErrorDatos(
                "Documento: debe tener entre 5 y 15 dígitos."
            )

        if (
            not any(letra.isalpha() for letra in nombre)
            or not all(
                letra.isalpha() or letra in " '-"
                for letra in nombre
            )
        ):
            raise ErrorDatos(
                "Nombre: solo se permiten letras, espacios, "
                "apóstrofes y guiones."
            )

        if (
            len(correo) > 120
            or not re.fullmatch(
                r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", correo
            )
        ):
            raise ErrorDatos("El correo no es válido.")

        if not re.fullmatch(r"\+?[0-9]{7,15}", telefono):
            raise ErrorDatos(
                "Teléfono: debe tener entre 7 y 15 dígitos."
            )

        self.__documento = documento
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        registro.info("Cliente creado: %s", self.id)

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return f"Cliente {self.id} | {self.nombre}"


# Prueba
if __name__ == "__main__":
    print("Software FJ — Prueba de clientes")

    cliente = Cliente(
        "100001", "Ana Perez", "ana@example.com", "3001234567"
    )
    print(cliente.describir())

    try:
        Cliente("12", "Ana Perez", "sin-correo", "123")
    except ErrorDatos as error:
        print("Error controlado:", error)
