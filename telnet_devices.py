from telnetlib import Telnet
from datetime import datetime
from os import walk
import ftplib


def create_config_file(username, password):
    router_telnet = Telnet()

    router_telnet.read_until(b'Username: ')
    router_telnet.write(username.encode('ascii') + b'\n')

    router_telnet.read_until(b'Password: ')
    router_telnet.write(password.encode('ascii') + b'\n')

    router_telnet.read_until(b'#')
    router_telnet.write('configure'.encode('ascii') + b'\n')

    router_telnet.read_until(b'(configure)')
    router_telnet.write('copy running-config startup-config'.encode('ascii') + b'\n')


def get_config_file(ip_address, username, password):
    now = datetime.now()
    ftp_server = ftplib.FTP(ip_address, username, password)
    with open('devices_files/' + ip_address + '/startup-config-' + now.strftime("%d%m%Y%H%M%S"), 'wb') as file:
        ftp_server.retrbinary(f"RETR startup-config", file.write)


def set_config_file(ip_address, username, password):
    filenames = next(walk('devices_files/' + ip_address + '/'), (None, None, []))[2]
    ftp_server = ftplib.FTP(ip_address, username, password)
    if len(filenames) > 0:
        print('Selecciona el archivo que deseas mandar al router: ')
        for i in range(len(filenames)):
            print('\n' + filenames[i])
        file_name = input('Ingresa el nombre del archivo: ')
        # Read file in binary mode
        with open('devices_files/' + ip_address + '/' + file_name, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR startup-config", file_name)