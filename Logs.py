# Herramientas para registrar eventos y manejar carpetas.
import logging
from pathlib import Path


# Define la presentación del archivo de eventos.
class FormatoEventos(logging.Formatter):

    def format(self, evento):
        """Organiza cada evento en un bloque legible."""

        # Presenta la fecha sin milisegundos.
        fecha = self.formatTime(evento, "%d/%m/%Y %H:%M:%S")

        # Traduce los niveles utilizados por el programa.
        niveles = {
            "DEBUG": "DEPURACIÓN",
            "INFO": "INFORMACIÓN",
            "WARNING": "ADVERTENCIA",
            "ERROR": "ERROR",
            "CRITICAL": "CRÍTICO"
        }

        nivel = niveles.get(evento.levelname, evento.levelname)

        # Construye el bloque principal del evento.
        lineas = [
            "=" * 65,
            f"FECHA   : {fecha}",
            f"NIVEL   : {nivel}",
            f"EVENTO  : {evento.getMessage()}"
        ]

        # Muestra una explicación corta cuando existe una excepción.
        if evento.exc_info:
            tipo, error, _ = evento.exc_info
            lineas.append(f"DETALLE : {tipo.__name__}: {error}")
            lineas.append(
                "CONSULTA: errores_tecnicos.log para el detalle completo."
            )

        lineas.append("=" * 65)

        return "\n".join(lineas) + "\n"


# Crea la carpeta de registros junto a los módulos.
carpeta = Path(__file__).resolve().parent / "logs"
carpeta.mkdir(exist_ok=True)

# Define los archivos de salida.
archivo_log = carpeta / "eventos.log"
archivo_tecnico = carpeta / "errores_tecnicos.log"

# Mantiene el mismo nombre de registro usado en el proyecto.
registro = logging.getLogger("software_fj_entrega")
registro.setLevel(logging.INFO)
registro.propagate = False

# Evita agregar manejadores duplicados.
if not registro.handlers:

    # Archivo legible con eventos y resúmenes de errores.
    eventos = logging.FileHandler(
        archivo_log,
        encoding="utf-8"
    )
    eventos.setLevel(logging.INFO)
    eventos.setFormatter(FormatoEventos())
    registro.addHandler(eventos)

    # Archivo técnico: guarda errores y sus trazas completas.
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


# Permite comprobar este módulo ejecutándolo directamente.
if __name__ == "__main__":
    registro.info("Prueba del sistema de registros.")
    print("Registro de eventos:", archivo_log)
    print("Registro técnico:", archivo_tecnico)
