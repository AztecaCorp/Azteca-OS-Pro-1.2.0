import os
import json

def setup_environment():
    print("Setting up Azteca OS Pro...")

    # Create the necessary directories
    directories = ['system', 'user_data', 'apps', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # Ask the user for username and password
    username = input("Create your username: ")
    password = input("Create your password: ")

    # Create a basic config file
    config = {
        "os_name": "Azteca OS Pro",
        "version": "1.0.0",
        "user": username,
        "password": password
    }
    with open('system/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
        print("Generated configuration file.")

    print("Setup complete! Launching Azteca OS Pro...\n")
