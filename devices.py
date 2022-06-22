from termcolor import colored, cprint
from snmp_requests import *
from database import DataBase
from telnet_devices import *
import os


def print_colored(description, text, color, args):
    print('\t', description, ': ', end='')
    cprint(text, color, attrs=args)


class Devices:

    def __init__(self):
        self.devices_database = DataBase()

    def list_devices(self, show_info):
        devices_status = {}
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            for device in devices:
                response = snmp_get(devices[device]['community'], devices[device]['ip_address'], '1.3.6.1.2.1.1.1.0')
                devices_status[device] = response

            counter = 0
            for device in devices:
                print("_______________________________________________________________")
                print(str(counter) + ".-")
                counter += 1
                print_colored('Dispositivo', devices[device]['host_name'], 'green', ['bold'])
                print_colored('Dirección IP', devices[device]['ip_address'], 'green', ['bold'])

                if show_info:
                    if devices_status[device] is not None:
                        print_colored('Estado', 'UP', 'green', ['bold'])
                        num_interfaces = snmp_get(devices[device]['community'], devices[device]['ip_address'],
                                                  '1.3.6.1.2.1.2.1.0')
                        print_colored('No. interfaces', num_interfaces, 'green', ['bold'])
                        interfaces_name = snmp_walk(devices[device]['community'], devices[device]['ip_address'],
                                                    '1.3.6.1.2.1.2.2.1.2')
                        for name in interfaces_name:
                            print_colored('\tInterface', name, 'green', ['bold'])

                        print_colored('Router info', snmp_walk(devices[device]['community'], devices[device]['ip_address'], '1.3.6.1.2.1.1.1')[0])
                    else:
                        print_colored('Estado', 'DOWN', 'red', ['bold'])
                        print_colored('No. interfaces', 'Desconocido', 'red', ['bold'])

    def add_devices(self):
        print()
        host_name = input('Ingresa el nombre del dispositivo: ')
        ip_address = input('Ingresa la dirección ip del dispositivo: ')
        snmp_version = input('Ingresa la version de SNMP configurada en el dispositivo: ')
        community = input('Ingresa la comunidad configurada en el dispositivo: ')
        telnet_user = input('Ingresa el usuario de telnet del dispositivo: ')
        telnet_pass = input('Ingresa la contraseña de telnet del dispositivo: ')

        os.system('mkdir devices_files/' + ip_address)

        self.devices_database.insert(host_name, ip_address, snmp_version, community, telnet_user, telnet_pass)

        print(colored('\nDispositivo agregado exitosamente.', 'green'))

    def delete_devices(self):
        ip_address = input('Ingresa la dirección ip del dispositivo que desea eliminar: ')
        os.system('rm -r devices_files/' + ip_address)
        self.devices_database.delete(ip_address)
        print(colored('\nDispositivo eliminado exitosamente.', 'green'))

    def generate_config_file(self):
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            self.list_devices(False)
            ip_address = input('Ingresa la dirección ip del dispositivo que desea que genere su archivo de configuracion: ')
            create_config_file(devices[ip_address]['telnet_user'], devices[ip_address]['telnet_pass'])

    def get_config_file(self):
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            self.list_devices(False)
            ip_address = input('Ingresa la dirección ip del dispositivo que desea obtener su archivo de configuracion: ')

    def set_config_file(self):
        devices = self.devices_database.read()
        if devices == {}:
            cprint('No hay dispositivos agregados', 'yellow', attrs=['bold'])
        else:
            self.list_devices(False)
            ip_address = input('Ingresa la dirección ip del dispositivo que desea establecer su archivo de configuracion: ')
