# Software FJ

# Esta clase permite reconocer juntos los errores propios del programa.
class ErrorFJ(Exception):
    """Clase base para los errores propios de Software FJ."""

# Se utiliza cuando un dato ingresado no cumple las validaciones.
class ErrorDatos(ErrorFJ):
    """Indica que un dato ingresado no cumple las reglas del sistema."""

# Se utiliza cuando una acción no es válida para el estado actual.
class ErrorEstado(ErrorFJ):
    """Indica que una operación no corresponde al estado actual."""

# Se utiliza cuando una reserva no puede completar su procesamiento.
class ErrorProceso(ErrorFJ):
    """Indica que no se pudo completar un proceso del sistema."""

# Esta prueba revisa que las tres clases puedan reconocerse como errores propios.
def probar_excepciones():
    tipos_error = (ErrorDatos, ErrorEstado, ErrorProceso)
    for tipo_error in tipos_error:
        try:
            raise tipo_error(f"Prueba de {tipo_error.__name__}.")
        except ErrorFJ as error:
            print("Error controlado:", error)

# Al ejecutar este archivo directamente, se prueban las clases de error.
if __name__ == "__main__":
    probar_excepciones()
