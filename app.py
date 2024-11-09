import paramiko

# Datos de conexión SSH
hostname = 'ssh-natureza.alwaysdata.net'  # Dirección IP o nombre de dominio del servidor
port = 22  # Puerto del servidor SSH (por lo general es 22)
username = 'natureza_anon'
password = '(123456)'

# Ruta del archivo Excel a subir
archivo_local = '"E:\Documento Para Subir.xlsx"'

# Ruta en el servidor donde se guardará el archivo
archivo_remoto = 'ssh-natureza.alwaysdata.net/72553563/'

# Establecer la conexión SSH
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

    # Subir el archivo al servidor
    sftp.put(archivo_local, archivo_remoto)
    print(f'Archivo {archivo_local} subido correctamente a {archivo_remoto}')

    # Cerrar la conexión SFTP y SSH
    sftp.close()
    client.close()

except Exception as e:
    print(f"Error al conectar o subir el archivo: {e}")
