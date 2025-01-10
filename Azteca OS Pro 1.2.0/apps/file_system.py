import os
import shutil

class InteractiveFileSystem:
    def __init__(self, root_dir="root"):
        self.root_path = os.path.abspath(root_dir)
        self.current_path = self.root_path
        
        # Ensure the root directory exists
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        print(f"File system initialized at {self.root_path}")

    def _resolve_path(self, path):
        # Resolve the path relative to the current path
        resolved_path = os.path.abspath(os.path.join(self.current_path, path))
        if not resolved_path.startswith(self.root_path):
            raise PermissionError("Access outside the root directory is not allowed.")
        return resolved_path

    def list_dir(self):
        items = os.listdir(self.current_path)
        if items:
            print("\n".join(items))
        else:
            print("The directory is empty.")

    def change_dir(self, path):
        try:
            new_path = self._resolve_path(path)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_path = new_path
                print(f"Changed directory to {self.current_path}")
            else:
                print(f"Directory {path} does not exist.")
        except PermissionError as e:
            print(e)

    def leave_dir(self):
        if self.current_path != self.root_path:
            self.current_path = os.path.dirname(self.current_path)
            print(f"Moved up to {self.current_path}")
        else:
            print("Cannot leave the root directory.")

    def make_dir(self, name):
        try:
            path = self._resolve_path(name)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Directory {name} created.")
            else:
                print(f"Directory {name} already exists.")
        except PermissionError as e:
            print(e)

    def create_file(self, name, content=""):
        try:
            path = self._resolve_path(name)
            with open(path, "w") as file:
                file.write(content)
            print(f"File {name} created.")
        except PermissionError as e:
            print(e)

    def delete_file(self, name):
        try:
            path = self._resolve_path(name)
            if os.path.exists(path):
                os.remove(path)
                print(f"File {name} deleted.")
            else:
                print(f"File {name} does not exist.")
        except PermissionError as e:
            print(e)

    def delete_dir(self, name):
        try:
            path = self._resolve_path(name)
            if os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Directory {name} and its contents deleted.")
            else:
                print(f"Directory {name} does not exist.")
        except PermissionError as e:
            print(e)

    def handle_command(self, command):
        parts = command.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "cd":
            self.change_dir(arg)
        elif cmd == "leave":
            self.leave_dir()
        elif cmd == "mkdir":
            self.make_dir(arg)
        elif cmd == "mkfile":
            self.create_file(arg)
        elif cmd == "delfile":
            self.delete_file(arg)
        elif cmd == "delfolder":
            self.delete_dir(arg)
        elif cmd == "list":
            self.list_dir()
        elif cmd == "exit":
            print("Exiting the program.")
            return False
        else:
            print("Unknown command. Available commands: cd <path>, leave, mkdir <name>, mkfile <name>, delfile <name>, delfolder <name>, list, exit.")
        return True

# Initialize the file system
fs = InteractiveFileSystem()

# Command loop
print("Welcome to the Interactive File System!")
print("Available commands: cd <path>, leave, mkdir <name>, mkfile <name>, delfile <name>, delfolder <name>, list, exit")

while True:
    command = input(f"{fs.current_path}> ").strip()
    if not fs.handle_command(command):
        break
