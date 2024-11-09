import paramiko
import os
from flask import Flask, send_file, after_this_request
from pathlib import Path

app = Flask(__name__)

# Configuración SSH
hostname = 'ssh-natureza.alwaysdata.net'
port = 22
username = 'natureza_anon'
password = '(123456)'

# Obtener la ruta de la carpeta "Descargas" de forma más general
descargas_path = str(Path.home() / 'Downloads')  # Usamos Path.home() para obtener la ruta del directorio home

# Si no existe la carpeta "Downloads", usar una ruta por defecto en el servidor
if not os.path.exists(descargas_path):
    descargas_path = '/tmp'  # Ruta alternativa en servidores tipo Linux

# Ruta donde se guardará el archivo localmente en la carpeta "Descargas"
archivo_local = os.path.join(descargas_path, 'JSalazar.xlsx')  # Guardar en "Descargas"

# Ruta del archivo en el servidor remoto
archivo_remoto = 'JSalazar.xlsx'

def descargar_archivo_remoto():
    """Función para descargar el archivo desde el servidor SSH al equipo local"""
    try:
        # Crear el cliente SSH
        client = paramiko.SSHClient()

        # Cargar las claves del sistema
        client.load_system_host_keys()

        # Auto-aceptar claves de hosts desconocidos
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor SSH
        client.connect(hostname, username=username, password=password, port=port)

        # Crear el cliente SFTP para la transferencia de archivos
        sftp = client.open_sftp()

        # Descargar el archivo desde el servidor remoto
        sftp.get(archivo_remoto, archivo_local)
        print(f'Archivo {archivo_remoto} descargado correctamente.')

        # Cerrar la conexión SFTP y SSH
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error al conectar o descargar el archivo: {e}")

@app.route('/api/descargar')
def descargar():
    """Ruta para manejar la descarga del archivo"""
    # Solo intentamos descargar el archivo remoto una vez si no existe localmente
    if not os.path.exists(archivo_local):
        descargar_archivo_remoto()

    # Aseguramos que la respuesta no sea cacheada por el navegador
    @after_this_request
    def no_cache(response):
        response.cache_control.no_store = True
        return response

    # Retornamos el archivo como adjunto para descarga
    return send_file(archivo_local, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)