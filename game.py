import os
import re
def search(property, eq, ls):
    for x in ls:
        if eval("x." + property) == eq:
            return x

    return False

def find_folder(path, ls):
    if path == "/":
        return ls
    path = path[1:-1].split("/")
    for x in path:
        for folder in ls:
            if folder.name == x:
                fl = folder
                ls = fl.files
                break
    return fl

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
        self.name = bash
        self.root = Folder("root", "/", [])
        self.folder = self.root
        self.path = "/"
        self.bash = bash + self.path + "#> "

    def execute(self, command):
        command = command.split(" ")
        cmd = command[0]
        if cmd == "ls":
            for x in self.folder.files:
                print(x)
            if len(self.folder.files) == 0:
                print("No files.")

        if cmd == "new":
            name = command[1]
            ext = re.search(r"\.(\w+)$", name).group(1)
            f = open(name,"w")
            f.close()
            os.system("notepad.exe " + name)
            an = input("Press 'c' to cancel and any key to continue...")
            if an == "c":
                os.remove(name)
                return
            with open(name) as f:
                txt = f.read()
            os.remove(name)
            self.folder.files.append(File(name, txt, ext))
            print("File created.")

        if cmd == "run":
            file = search("name", command[1], self.folder)
            print("Executing file...")
            exec(file.content)

        if cmd == "edit":
            name = command[1]
            file = search("name", command[1], self.folder)
            ext = re.search(r"\.(\w+)$", name).group(1)
            f = open(name, "w")
            f.write(file.content)
            f.close()
            os.system("notepad.exe " + name)
            an = input("Press 'c' to cancel and any key to continue...")
            if an == "c":
                os.remove(name)
                return
            with open(name) as f:
                txt = f.read()
            os.remove(name)
            file.content = txt
            print("File edited.")

        if cmd == "mkdir":
            fname = command[1]
            self.folder.files.append(Folder(fname,self.path + fname + "/",[]))
            print("Folder created.")

        if cmd == "cd":
            fname = command[1]
            if fname == "..":
                path = self.path[:-1][::-1][self.path[:-1][::-1].index("/"):][::-1]
            else:
                path = self.path + fname
            if path[-1] != "/":
                path += "/"
            folder = find_folder(path, self.root)
            self.path = folder.path
            self.folder = folder
            self.bash = self.name + self.path + "#> "

bash = input("Enter name: ")
my = PC(bash)
print("'ls' to list files\nnew [filename.ext] - to create a file\nrun [filename.ext] - to run the file")

while True:
    my.execute(input(my.bash))
