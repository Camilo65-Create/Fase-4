# Herramientas para registrar eventos y manejar carpetas.
import logging
from pathlib import Path


class FormatoEventos(logging.Formatter):
    """Presenta cada evento en un bloque organizado."""

    def format(self, evento):
        # Presenta la fecha sin milisegundos.
        fecha = self.formatTime(evento, "%d/%m/%Y %H:%M:%S")

        # Traduce los niveles del registro.
        niveles = {
            "DEBUG": "DEPURACIÓN",
            "INFO": "INFORMACIÓN",
            "WARNING": "ADVERTENCIA",
            "ERROR": "ERROR",
            "CRITICAL": "CRÍTICO"
        }

        nivel = niveles.get(evento.levelname, evento.levelname)

        # Construye el encabezado y el mensaje del evento.
        lineas = [
            "=" * 75,
            f"FECHA   : {fecha}",
            f"NIVEL   : {nivel}",
            f"ORIGEN  : {evento.filename} / {evento.funcName}",
            "-" * 75,
            f"EVENTO  : {evento.getMessage()}"
        ]

        # Agrega la excepción y su traza cuando están disponibles.
        if evento.exc_info:
            tipo, error, _ = evento.exc_info

            lineas.extend([
                "-" * 75,
                f"ERROR   : {tipo.__name__}",
                f"MOTIVO  : {error}",
                "DETALLE TÉCNICO:"
            ])

            # Conserva también las excepciones encadenadas.
            detalle = self.formatException(evento.exc_info)

            for linea in detalle.splitlines():
                lineas.append(f"    {linea}")

        lineas.append("=" * 75)

        return "\n".join(lineas) + "\n"


# Crea la carpeta junto a los archivos del proyecto.
carpeta = Path(__file__).resolve().parent / "logs"
carpeta.mkdir(exist_ok=True)

# Define los archivos de registro.
archivo_log = carpeta / "eventos.log"
archivo_tecnico = carpeta / "errores_tecnicos.log"

# Todos los módulos utilizan el mismo registro.
registro = logging.getLogger("software_fj_entrega")
registro.setLevel(logging.INFO)
registro.propagate = False

# Evita duplicar los manejadores al importar el módulo.
if not registro.handlers:

    # Guarda todos los eventos con presentación organizada.
    eventos = logging.FileHandler(
        archivo_log,
        encoding="utf-8"
    )
    eventos.setLevel(logging.INFO)
    eventos.setFormatter(FormatoEventos())
    registro.addHandler(eventos)

    # Guarda una copia técnica de los errores.
    errores = logging.FileHandler(
        archivo_tecnico,
        encoding="utf-8"
    )
    errores.setLevel(logging.ERROR)
    errores.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S"
        )
    )
    registro.addHandler(errores)


# Permite probar directamente la creación de registros.
if __name__ == "__main__":
    registro.info("Prueba del sistema de registros.")

    print("Archivo de eventos:", archivo_log)
    print("Archivo técnico:", archivo_tecnico)
