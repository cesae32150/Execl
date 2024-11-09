import paramiko
import os
import getpass
from flask import Flask, send_file, abort
from io import BytesIO  # Usamos BytesIO para enviar el archivo en memoria
from pathlib import Path

app = Flask(__name__)

# Configuración SSH
hostname = 'ssh-natureza.alwaysdata.net'
port = 22
username = 'natureza_anon'
password = os.getenv('SSH_PASSWORD', '123456')  # Obtener la contraseña de una variable de entorno

# Ruta del archivo en el servidor remoto
archivo_remoto = '72553563.xlsx'  # Asegúrate de que esta ruta sea correcta en el servidor

def descargar_archivo_remoto():
    """Función que descarga el archivo desde el servidor remoto usando SFTP y lo devuelve en memoria."""
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

        # Crear un objeto en memoria donde almacenaremos el archivo descargado
        archivo_memoria = BytesIO()

        # Descargar el archivo desde el servidor remoto directamente a memoria
        sftp.getfo(archivo_remoto, archivo_memoria)

        # Cerrar la conexión SFTP y SSH
        sftp.close()
        client.close()

        # Volver al inicio del archivo en memoria para enviarlo
        archivo_memoria.seek(0)

        return archivo_memoria

    except Exception as e:
        print(f"Error al conectar o descargar el archivo: {e}")
        return None

@app.route('/descargar')
def descargar():
    """Ruta para descargar el archivo desde el servidor remoto y enviarlo al cliente."""
    archivo_memoria = descargar_archivo_remoto()

    if archivo_memoria:
        # Retornar el archivo descargado directamente al navegador del cliente
        return send_file(archivo_memoria, as_attachment=True, download_name='72553563.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        # Si hubo un error al descargar el archivo
        abort(404, description="Archivo no encontrado en el servidor remoto")

if __name__ == '__main__':
    # Iniciar el servidor HTTP en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
