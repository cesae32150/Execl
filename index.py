import paramiko
import os
import getpass
from flask import Flask, send_file
from pathlib import Path

app = Flask(__name__)

# Configuración SSH
hostname = 'ssh-natureza.alwaysdata.net'
port = 22
username = 'natureza_anon'
password = os.getenv('SSH_PASSWORD', '123456')  # Obtener la contraseña de una variable de entorno

# Ruta donde se guardará el archivo en el entorno de Render (por ejemplo, /tmp)
archivo_local = Path('/tmp/72553563.xlsx')  # Usamos /tmp para almacenamiento temporal en el contenedor

# Ruta del archivo en el servidor remoto
archivo_remoto = '72553563.xlsx'  # Asegúrate de que esta ruta sea correcta en el servidor

def descargar_archivo_remoto():
    """Función que descarga el archivo desde el servidor remoto usando SFTP."""
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
        sftp.get(archivo_remoto, str(archivo_local))  # Usamos str() para convertir la ruta a string
        print(f'Archivo {archivo_remoto} descargado correctamente en {archivo_local}')

        # Cerrar la conexión SFTP y SSH
        sftp.close()
        client.close()

        # Verifica si el archivo fue descargado correctamente
        if archivo_local.exists():
            print(f"El archivo fue descargado con éxito: {archivo_local}")
        else:
            print(f"El archivo no fue encontrado en la ruta {archivo_local}")

    except Exception as e:
        print(f"Error al conectar o descargar el archivo: {e}")

@app.route('/descargar')
def descargar():
    """Ruta para descargar el archivo desde el servidor remoto y enviarlo al cliente."""
    # Descargar el archivo desde el servidor remoto
    descargar_archivo_remoto()

    # Verificar si el archivo ha sido descargado antes de intentar enviarlo
    if archivo_local.exists():
        # Retornar el archivo descargado para que se pueda descargar vía HTTP
        return send_file(archivo_local, as_attachment=True)
    else:
        return f"Error: El archivo {archivo_local} no se encontró", 404

if __name__ == '__main__':
    # Iniciar el servidor HTTP en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
