# Software-FJ

# Se usan herramientas estándar para validar datos y crear identificadores.
import re
from abc import ABC, abstractmethod
from uuid import uuid4
from Excepciones import ErrorDatos

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

# Esta función sirve para revisar nombres y otros textos.
def validar_texto(valor, campo):
    if not isinstance(valor, str) or not 2 <= len(valor.strip()) <= 120:
        raise ErrorDatos(f"{campo}: escribe un texto de 2 a 120 caracteres.")
    return valor.strip()

# Los datos personales se validan antes de guardarlos como atributos privados.
class Cliente(Entidad):
    def __init__(self, documento, nombre, correo, telefono):
        super().__init__()
        if not all(isinstance(dato, str) for dato in (documento, nombre, correo, telefono)):
            raise ErrorDatos("Los datos del cliente deben ser textos.")
        documento, correo, telefono = documento.strip(), correo.strip().lower(), telefono.strip()
        nombre = validar_texto(nombre, "Nombre")
        if not re.fullmatch(r"[0-9]{5,15}", documento):
            raise ErrorDatos("Documento: debe tener entre 5 y 15 dígitos.")
        if not any(letra.isalpha() for letra in nombre) or not all(letra.isalpha() or letra in " '-" for letra in nombre):
            raise ErrorDatos("Nombre: solo se permiten letras, espacios, apóstrofes y guiones.")
        if len(correo) > 120 or not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", correo):
            raise ErrorDatos("El correo no es válido.")
        if not re.fullmatch(r"\+?[0-9]{7,15}", telefono):
            raise ErrorDatos("Teléfono: debe tener entre 7 y 15 dígitos.")
        self.__documento, self.__nombre = documento, nombre
        self.__correo, self.__telefono = correo, telefono

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
