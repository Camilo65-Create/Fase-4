# Software FJ

# Se preparan las herramientas para guardar eventos en un archivo de texto.
import logging
from pathlib import Path

# El archivo de registro queda dentro de una carpeta junto a los módulos.
carpeta = Path(__file__).resolve().parent / "logs"
carpeta.mkdir(exist_ok=True)
archivo_log = carpeta / "eventos.log"

# Todos los módulos usan el mismo registro para evitar archivos duplicados.
registro = logging.getLogger("software_fj_entrega")
if not registro.handlers:
    archivo = logging.FileHandler(archivo_log, encoding="utf-8")
    archivo.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    registro.addHandler(archivo)
registro.setLevel(logging.INFO)
registro.propagate = False

# Esta prueba confirma que el registro puede guardar un evento.
if __name__ == "__main__":
    registro.info("Prueba del archivo de registro")
    print("Registro preparado:", archivo_log)
