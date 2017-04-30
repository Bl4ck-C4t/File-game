import os
import re
import random
import copy
def search(property, eq, ls):
    for x in ls:
        if eval("x." + property) == eq:
            return x

    return False

def number_game(server, max=10):
    signs = "+-/*"
    nums = [random.randint(0,max) for x in range(3)]
    ls2 = nums[:]
    random.shuffle(ls2)
    while True:
        num = eval("({} {} {}) {} {}".format(ls2[0], random.choice(signs), ls2[1],random.choice(signs),ls2[2]))
        if int(num) == num:
            break
    print("{} ? {} ? {} = {}".format(nums[0], nums[1], nums[2], num))
    while True:
        sk = False
        answer = input("Enter solution('e' - to exit): ")
        if answer == "e":
            print("You canceled.")
            return False
        ans = eval(answer)
        numbers = re.findall(r"\d+", answer)
        for x in numbers:
            if not(int(x) in nums):
                print("Wrong numbers!")
                sk = True
                break
        if sk:
            continue
        if ans == num:
            print("Correct!")
            print("One use ticket found: " + server.ticket)
            return True
        else:
            print("Wrong result: Your result is {}\nYou need to get the result {}".format(ans, num))


def ip_gen():
    ip = ""
    for x in range(4):
        ip += str(random.randint(100, 255)) + "."
    return ip[:-1]

def code_gen(ln=4):
    alpha = "0123456789qwertyuiopasdfghjklzxcvbnm"
    return "".join([random.choice(alpha) for x in range(ln)])

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

def find_file(path, ls):
    path = path[1:].split("/")
    for x in path:
        if x == path[-1]:
            return search("fullname", x, ls)
        for folder in ls:
            if folder.name == x:
                fl = folder
                ls = fl.files
                break



def fire_ticket():
    print("You can get a one use ticket for a firewall with this.")
    ip = input("Enter ip of server to get ticket from('c' - to cancel): ")
    if ip == "c":
        print("You canceled.")
        return
    comp = search("ip", ip, PC.PCs)
    number_game(comp)



def bliz_startup(bliz, other):  # just for testing still in development
    print("Welcome to Blizzard")
    while True:
        print("1. Login\n2. Use ticket\n3. Disconnect")
        op = input("Enter option: ")
        if op == "3":
            print("You disconnected.")
            break
        if op == "2":
            code = input("Enter ticket: ")
            if code == bliz.ticket:
                print("Code right")
                path = input("Enter full filepath to upload a file('c'- to cancel): ")
                file = find_file(path, other.root)
                file = copy.deepcopy(file)
                bliz.root.files.append(file)
                print("File uploaded!")
                print("One use ticket '{}' used.".format(code))
                bliz.ticket = code_gen()
                if path == "c":
                    print("You canceled.")
                    print("On use ticket still valid")
                    return



class File:
    def __init__(self, name, content):
        nm = re.search(r"(\w+)\.(\w+)", name)
        self.name = nm.group(1)
        self.fullname = nm.group()
        self.content = content
        self.type = nm.group(2)

    def __repr__(self):
        return self.fullname


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
    PCs = []
    def __init__(self, bash):
        self.name = bash
        self.root = Folder("root", "/", [])
        self.folder = self.root
        self.path = "/"
        self.bash = bash + self.path + "#> "
        self.ip = ip_gen()
        self.PCs.append(self)

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
            self.folder.files.append(File(name, txt))
            print("File created.")

        if cmd == "run":
            file = search("fullname", command[1], self.folder)
            if file == False:
                print("File '{}' does not exist.".format(command[1]))
            print("Executing file...")
            if file.type == "py":
                for line in file.content.split("\n"):
                    exec(line)
            elif file.type == "exe":
                eval(file.name + "()")

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

        if cmd == "connect":
            ip = command[1]
            comp = search("ip", ip, self.PCs)
            comp.connection(self)

    def connection(self, other):
        file = search("fullname", "connections.run", self.root)
        func = eval(file.content.split("\n")[0])
        func(self, other)

bash = input("Enter name: ")
Blizz = PC("Jeff")
Blizz.root.files.append(File("connections.run", "bliz_startup"))
Blizz.ticket = code_gen()
my = PC(bash)
my.root.files.append(File("fire_ticket.exe", "0101011010"*10))

print("'ls' - to list files\nnew [filename.ext] - to create a file\nrun [filename.ext] - to run the file\n"
      "edit [filename.ext] - to edit a file\nmkdir [folder_name] - to make folder\ncd [folder] - to go into a folder\n"
      "cd .. - to get to the previous folder\ncd / - to get to the root folder\nconnect [ip] - to connect to a "
      "server or PC")
print("Blizzard ip: " + PC.PCs[0].ip)
while True:
    my.execute(input(my.bash))
