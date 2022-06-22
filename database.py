import json


class DataBase:
    database_name = "database.json"

    ####################################################################################################################
    # Initialize the database using json file
    # if the file does not exist it will create with an empty object
    ####################################################################################################################
    def __init__(self):
        try:
            open(self.database_name, "r")
        except:
            with open(self.database_name, "x") as f:
                json.dump({}, f)

    ####################################################################################################################
    # Read the registers from the database json file
    # @params key, if it is not none it will return a specific register
    ####################################################################################################################
    def read(self, key=None):
        file = open(self.database_name, "r")
        data = file.read()
        if key is None:
            return json.loads(data)
        else:
            data = json.loads(data)
            return data[key]

    ####################################################################################################################
    # Insert a new register or overwrite a register
    ####################################################################################################################
    def insert(self, host_name, ip_address, snmp_version, community_name, telnet_user, telnet_pass):
        data = self.read()
        data[ip_address] = {
            'host_name': host_name,
            'ip_address': ip_address,
            'snmp_version': snmp_version,
            'community': community_name,
            'telnet_user': telnet_user,
            'telnet_pass': telnet_pass
        }
        self.write_object(data)

    ####################################################################################################################
    # Delete a register using ip address as a key
    ####################################################################################################################
    def delete(self, ip_address):
        data = self.read()
        del data[ip_address]
        self.write_object(data)

    ####################################################################################################################
    # Write an object in the database
    ####################################################################################################################
    def write_object(self, data):
        with open(self.database_name, "w") as f:
            json.dump(data, f)
