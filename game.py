import os
import re
from collections import OrderedDict

def search(property, eq, ls):
    for x in ls:
        if eval("x." + property) == eq:
            return x

    return False
    

class File:
    def __init__(self, name, content, type):
        self.name = name
        self.content = content
        self.type = type

    def __repr__(self):
        return self.name


class Folder:
    def __init__(self, name, path, files):
        self.name = name
        self.files = files
        self.path = path

    def __repr__(self):
        return self.name

    def __iter__(self):
        for x in self.files:
            yield x



class PC:

    def __init__(self, bash):
        self.root = Folder("root", "/", [])
        self.folder = self.root
        self.path = "/"
        self.bash = bash + "#> "
        self.ide = "notepad.exe"

    def execute(self, command):
        command = command.split(" ")
        cmd = command[0]

        for key, value in self.commands.items():
            if(cmd == key):
                value(self, command)
                return 0

        print("Command not found! Enter 'commands' to view all available commands.")


    def print_available_commands(self, command):
        """commands - print every available command."""
        for cmd in self.commands:
            print(cmd)


    def print_command_info(self, command):
        """man [command] - print a chosen command info."""
        for key in self.commands:
            if(key == command[1]):
                print(self.commands[key].__doc__)
                return 1


    def print_files(self, command):
        """ls - print the file names of all files in current directory."""
        for x in self.folder.files:
            print(x)
        if len(self.folder.files) == 0:
            print("No files.")


    def create_file(self, command):
        """new [file_name.ext] - create a new file and open it."""
        is_valid = valid_cmd_arguments(command, 1)
        if(not is_valid):
            return 0
        name = command[1]
        ext = re.search(r"\.(\w+)$", name).group(1)
        f = open(name,"w")
        f.close()
        os.system("{} {}".format(self.ide, name))
        an = input("Press 'c' to cancel and any key to continue...")
        if an == "c":
            os.remove(name)
            return
        with open(name) as f:
            txt = f.read()
        os.remove(name)
        self.folder.files.append(File(name, txt, ext))
        print("File created.")


    def edit_file(self, command):
        """edit [file_name.ext] - edit a currently existing file."""
        name = command[1]
        file = search("name", command[1], self.folder)
        ext = re.search(r"\.(\w+)$", name).group(1)
        f = open(name, "w")
        f.write(file.content)
        f.close()
        os.system("{} {}".format(self.ide, name))
        an = input("Press 'c' to cancel and any key to continue...")
        if an == "c":
            os.remove(name)
            return
        with open(name) as f:
            txt = f.read()
        os.remove(name)
        file.content = txt
        print("File edited.")


    def run_file(self, command):
        """run [file_name.ext] - run python code in a file."""
        file = search("name", command[1], self.folder)
        print("Executing file...")
        exec(file.content)


    def change_ide(self, command):
        """
ide [ide_to_use] - set a new standart ide to use for working with files
You can either set the path or use an environment variable.
        """
        last_ide = self.ide
        self.ide = command[1]
        os.system("{} test.test".format(self.ide))
        check = input("Press 'c' to cancel or anything else to continue.")
        if check == "c":
            self.ide = last_ide


    commands = OrderedDict([
        ("commands", print_available_commands),
        ("man", print_command_info),
        ("ls", print_files),
        ("new", create_file),
        ("edit", edit_file),
        ("run", run_file),
        ("ide", change_ide),
    ])

            
my = PC("Praso")

print("""
Enter 'commands' to view all available commands
Enter 'man [command]' to view command manual
""")

while True:
    my.execute(input(my.bash))
