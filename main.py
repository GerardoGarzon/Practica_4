from devices import Devices
import os


def main():
    devices = Devices()

    while True:
        os.system('clear')
        selection = 0

        while selection < 1 or selection > 6:
            print("Administración de configuración - Practica 4 \n"
                  "\t1.- Agregar router.\n"
                  "\t2.- Listar información de routers.\n"
                  "\t3.- Generar archivo de configuración.\n"
                  "\t4.- Obtener archivo de configuración.\n"
                  "\t5.- Establecer archivo de configuración.\n"
                  "\t6.- Salir.\n")
            selection = int(input("Ingrese la opción seleccionada: "))

        if selection == 1:
            devices.add_devices()
        elif selection == 2:
            devices.list_devices(True)
        elif selection == 3:
            devices.generate_config_file()
        elif selection == 4:
            devices.get_config_file()
        elif selection == 5:
            devices.set_config_file()
        elif selection == 6:
            break

        input()


if __name__ == '__main__':
    main()
