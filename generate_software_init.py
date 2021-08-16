import getopt
import sys
import os

from license_utils.jwt_helper import JWT_helper


def read_private_key(private_key_dir):
    """
        reads private key content from provided location
    """
    private_key = ""
    try:
        with open(private_key_dir) as f:
            private_key = f.read().strip()
    except Exception as e:
        raise e
    return private_key


def write_token_to_file(client_name, token):
    """
        creates a .key file containing the generated token
    """
    # create folder if does not exist
    license_holder = "software_licenses"
    try:
        os.makedirs(license_holder, exist_ok=True)
        print("Bootstraping directory '%s' ....!" %
              license_holder)
    except OSError:
        pass
    token_file = open(f"{license_holder}/lm_gen_{client_name}.lic", "w")
    token_file.write(token)


def generate_software_key(client_name, private_key_dir):
    client_private_key = read_private_key(private_key_dir)
    pay_load = {
        "client_name": client_name,
        "note": "needed to verify client instance",
        "aud": client_name,
    }
    encoded_token = JWT_helper.create_software_initialization_token(
        pay_load, client_private_key)
    write_token_to_file(client_name, encoded_token)
    print(
        f"CONGS...\nsoftware license for {client_name} has been successfully created \n AWESOME...")


def main(argv):
    client_name = ''
    private_key_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hc:k:", ["client=", "key=", "help"])
    except getopt.GetoptError as e:
        print(
            str(e)+'\nUSAGE generate_software_init.py -c <client name> -k <private key dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('generate_software_init.py -c <client name> -k <private key dir>')
            sys.exit()
        elif opt in ("-c", "--client"):
            client_name = arg
        elif opt in ("-k", "--key"):
            private_key_dir = arg
    if len(client_name) > 0 and len(private_key_dir) > 0:
        generate_software_key(client_name, private_key_dir)
    else:
        print('USAGE: \n generate_software_init.py -c <client name> -k <private key dir>')


if __name__ == "__main__":
    main(sys.argv[1:])
