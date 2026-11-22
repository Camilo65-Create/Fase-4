# Herramientas para registrar eventos y administrar carpetas.
import logging
from pathlib import Path

def formatear_pesos(valor):
    """Presenta un valor con signo pesos y separadores colombianos."""
    texto = f"${valor:,.2f}"
    return (
        texto.replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

class FormatoEventos(logging.Formatter):
    """Organiza la información recibida en bloques legibles."""

    def format(self, evento):
        # Obtiene la fecha y hora del evento.
        fecha = self.formatTime(evento, "%d/%m/%Y")
        hora = self.formatTime(evento, "%H:%M:%S")

        # Traduce los niveles del registro.
        niveles = {
            "DEBUG": "DEPURACIÓN",
            "INFO": "INFORMACIÓN",
            "WARNING": "ADVERTENCIA",
            "ERROR": "ERROR",
            "CRITICAL": "CRÍTICO"
        }

        nivel = niveles.get(evento.levelname, evento.levelname)

        # Conserva el mensaje completo, incluso si tiene varias líneas.
        mensaje = evento.getMessage()

        # Construye el encabezado del registro.
        lineas = [
            "=" * 78,
            "                         SOFTWARE FJ",
            "                    REGISTRO DE ACTIVIDADES",
            "-" * 78,
            f"FECHA          : {fecha}",
            f"HORA           : {hora}",
            f"NIVEL          : {nivel}",
            f"ARCHIVO ORIGEN : {evento.filename}",
            f"FUNCIÓN        : {evento.funcName}",
            f"LÍNEA          : {evento.lineno}",
            "-" * 78,
            "DESCRIPCIÓN DEL EVENTO",
            "-" * 78,
            mensaje
        ]

        # Agrega los detalles de la excepción cuando se adjuntaron.
        if evento.exc_info:
            tipo, error, traza = evento.exc_info

            lineas.extend([
                "",
                "-" * 78,
                "INFORMACIÓN DEL ERROR",
                "-" * 78,
                f"TIPO DE ERROR  : {tipo.__name__}",
                f"MOTIVO         : {error}"
            ])

            # Localiza el punto donde se originó la excepción final.
            if traza is not None:
                origen = traza

                while origen.tb_next is not None:
                    origen = origen.tb_next

                archivo_origen = Path(
                    origen.tb_frame.f_code.co_filename
                ).name

                funcion_origen = origen.tb_frame.f_code.co_name

                lineas.extend([
                    f"ARCHIVO ERROR  : {archivo_origen}",
                    f"FUNCIÓN ERROR  : {funcion_origen}",
                    f"LÍNEA ERROR    : {origen.tb_lineno}"
                ])

            # Incluye la traza completa y las excepciones encadenadas.
            lineas.extend([
                "",
                "-" * 78,
                "DETALLE TÉCNICO COMPLETO",
                "-" * 78
            ])

            detalle = self.formatException(evento.exc_info)

            for linea in detalle.splitlines():
                lineas.append(f"    {linea}")

        # Conserva información de pila adicional si fue enviada.
        if evento.stack_info:
            lineas.extend([
                "",
                "PILA ADICIONAL:",
                evento.stack_info
            ])

        # Cierra el bloque del evento.
        lineas.extend([
            "=" * 78,
            ""
        ])

        return "\n".join(lineas)


# Crea la carpeta de registros junto a los módulos del programa.
carpeta = Path(__file__).resolve().parent / "logs"
carpeta.mkdir(exist_ok=True)

# Conserva los dos archivos de registro.
archivo_log = carpeta / "eventos.log"
archivo_tecnico = carpeta / "errores_tecnicos.log"

# Conserva el nombre del registro utilizado por el proyecto.
registro = logging.getLogger("software_fj_entrega")
registro.setLevel(logging.INFO)

# Evita enviar los mismos mensajes al registro general de Python.
registro.propagate = False

# Agrega los manejadores una sola vez.
if not registro.handlers:

    # Guarda todos los eventos con el formato organizado.
    eventos = logging.FileHandler(
        archivo_log,
        mode="a",
        encoding="utf-8"
    )
    eventos.setLevel(logging.INFO)
    eventos.setFormatter(FormatoEventos())
    registro.addHandler(eventos)

    # Guarda una copia de los errores con presentación técnica.
    errores = logging.FileHandler(
        archivo_tecnico,
        mode="a",
        encoding="utf-8"
    )
    errores.setLevel(logging.ERROR)

    formato_tecnico = logging.Formatter(
        (
            "%(asctime)s | %(levelname)s\n"
            "Archivo: %(filename)s | "
            "Función: %(funcName)s | "
            "Línea: %(lineno)d\n"
            "Mensaje: %(message)s"
        ),
        datefmt="%d/%m/%Y %H:%M:%S"
    )

    errores.setFormatter(formato_tecnico)
    registro.addHandler(errores)


# Prueba sencilla al ejecutar este archivo directamente.
if __name__ == "__main__":
    registro.info("Prueba del registro de actividades.")

    print("Registro de actividades:", archivo_log)
    print("Registro técnico:", archivo_tecnico)
