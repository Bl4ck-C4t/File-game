import os
import re
import random
import copy
import datetime
import time
import inspect

# TODO False appearing in blizz filesystem
# TODO modify the run method so when it runs a file to a system we are not connected to it prints 'file {} executed
# TODO at {}'

def search(property, eq, ls):
    try:
        for x in ls:
            if eval("x." + property) == eq:
                return x
    except:
        return False

    return False

def arg_maker(obj_name, name):
    rt = list(inspect.signature(eval(obj_name + "." + name)).parameters)
    pr = ""
    if len(rt) > 0 and rt[0] == "self":
        pr = "self."
        del rt[0]
    return "{}{}({})".format(pr, name, ", ".join(rt))



def number_game(server, max=10):
    print("Solve the equation by putting the right signs\nEx:10 ? 5 ? 2 = 25\nExpected input:(10/2)*5")
    signs = "+-/*"
    nums = [random.randint(0,max) for x in range(3)]
    ls2 = nums[:]
    random.shuffle(ls2)
    while True:
        try:
            num = eval("({} {} {}) {} {}".format(ls2[0], random.choice(signs), ls2[1],random.choice(signs),ls2[2]))
            if int(num) == num:
                break
        except ZeroDivisionError:
            continue
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

def DDos():
    print("You can use it to DDos a server. When that happens the server reboots.\nCan be done once per 30 sec.")
    if Helper.ddos_timer != 0:
        current = datetime.datetime.now() - Helper.ddos_timer
    if not(Helper.ddos_timer == 0 or current.seconds >= 30):
        print("You need to wait {} more seconds".format(30 - current.seconds))
        return
    ip = input("Enter ip of server to DDos('c' - to cancel): ")
    if ip == "c":
        print("You canceled.")
        return
    comp = search("ip", ip, PC.PCs)
    print("Overflowing {} ...".format(ip))
    time.sleep(1.5)
    comp.reboot()
    print("Server {} rebooted.".format(ip))
    Helper.ddos_timer = datetime.datetime.now()


def bliz_startup(bliz, other):
    print("Welcome to Blizzard")
    while True:
        print("1. Enter\n2. Use ticket\n3. Disconnect")
        op = input("Enter option: ")
        if op == "1":
            if bool(bliz.firewall):
                print("Blocked by Blizzard firewall.")
            else:
                print("You are connected to blizzard core.")
                Helper.i = bliz
                return
        if op == "3":
            print("You disconnected.")
            break
        if op == "2":
            code = input("Enter ticket: ")
            if code == bliz.ticket:
                print("Code right")
                path = input("Enter full filepath to upload a file('c'- to cancel): ")
                if path == "c":
                    print("You canceled.")
                    print("On use ticket still valid")
                    return
                file = find_file(path, other.root)
                if file == False:
                    print("file {} not found".format(path))
                    continue
                file = copy.deepcopy(file)
                bliz.root.files.append(file)
                print("File uploaded!")
                print("One use ticket '{}' used.".format(code))
                bliz.ticket = code_gen()

            else:
                print("Wrong code.")

def helper(self, other):
    print("You are connected to the helper server")
    Helper.i = self


class Helper:
    i = 0
    mine = 1
    ddos_timer = 0


class Firewall:
    def __init__(self, state):
        self.state = state

    def toggle(self):
        'Toggle the state of the firewall'
        self.state = not self.state

    def enable(self):
        'Enable firewall'
        self.state = True

    def disable(self):
        'Disable firewall'
        self.state = False

    def __bool__(self):
        return self.state


class File:
    def __init__(self, name, content):
        nm = re.search(r"(\w+)\.(\w+)", name)
        self.name = nm.group(1)
        self.fullname = nm.group()
        self.content = content
        self.type = nm.group(2)
        self.startup = False

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
        self.firewall = Firewall(True)

    def execute(self, command):
        'Make the computer execute a command like "run asd.txt"'
        command = command.split(" ")
        cmd = command[0]
        if cmd == "ls":
            for x in self.folder.files:
                print(x)
            if len(self.folder.files) == 0:
                print("No files.")

        if cmd == "new":
            name = command[1]
            f = open(name, "w")
            f.close()
            os.system("notepad.exe " + name)
            an = input("Press 'c' to cancel and any key to continue...")
            if an == "c":
                os.remove(name)
                return
            with open(name) as f:
                txt = f.read()
            os.remove(name)
            fl = File(name, txt)
            fl.creator_ip = self.ip
            self.folder.files.append(fl)
            print("File created.")

        if cmd == "run":
            file = search("fullname", command[1], self.folder)
            if file == False:
                print("File '{}' does not exist.".format(command[1]))
                return
            if self.ip != Helper.i:
                print("File {} executed at {}".format(command[1], self.ip))
            else:
                print("Executing file...")
            if file.type == "py":
                line_num = 1
                comp = self
                for line in file.content.split("\n"):
                    try:
                        exec(line)
                    except Exception as e:
                        exc_type = re.search(r"\'(\w+)\'", str(type(e))).group(1)
                        print("{} occured on line {}".format(exc_type, line_num))
                    line_num += 1

            elif file.type == "exe":
                eval(file.name + "()")
            elif file.type == "txt":
                print(file.content)

        if cmd == "edit":
            name = command[1]
            file = search("fullname", command[1], self.folder)
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
            elif fname == "/":
                path = fname
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

        if cmd == "rm":
            fname = command[1]
            file = search("fullname", fname, self.folder)
            self.folder.files.remove(file)
            print("File removed.")

        if cmd == "dis":
            if Helper.i != Helper.mine:
                print("You disconnected")
                Helper.i = Helper.mine
            else:
                print("You can't disconnect from yourself.")

        if cmd == "cat":
            fname = command[1]
            file = search("fullname", fname, self.folder)
            print(file.content)
        
       if cmd == "mv":
           file = search("fullname", command[1], self.folder)
           folder = command[2]
           folder = find_folder(folder)
           folder.append(file)
           self.folder.remove(file)
           print("File moved.")

    def connection(self, other):
        'This runs a function stored in the connections.run file when someone connects'
        file = search("fullname", "connections.run", self.root)
        if not file:
            print("'connections.run' not found on device {0}\nYou are connected to {0}.".format(self.ip))
            Helper.i = self
            return
        func = eval(file.content.split("\n")[0])
        func(self, other)

    def reboot(self, folder=""):
        'This function reboots the server'
        if folder == "":
            folder = self.root
        for fl in folder:
            if isinstance(fl, Folder):
                self.reboot(fl)
            elif isinstance(fl, File):
                if fl.startup:
                    self.execute("run " + fl.fullname)


def main():  # main function
    bash = input("Enter name: ")
    test_obj = [Firewall(True), File("nigga.txt", "waddup"), Folder("F1", "/asd", []), PC("nigeria")]
    meth = ""
    props = ""
    for obj in test_obj:  # Methods info generation
        methods = inspect.getmembers(obj, predicate=inspect.ismethod)
        propertys = list(obj.__dict__.keys())
        obj_name = obj.__class__.__name__
        meth += "Methods for {}s:\n".format(obj_name)
        props += "Properties for {}s:\n".format(obj_name)
        for name, instance in methods:
            if name[0] != "_":
                meth += " "*4 + "{} - ".format(arg_maker(obj_name, name)) + instance.__doc__ + "\n"
        for prop in propertys:
            if prop[0] != "_":
                props += " "*4 + prop + "\n"
    dump = PC("info")
    file = File("Methods.txt", meth)
    file2 = File("Proprties.txt", props)
    file3 = File("Files.txt", "Each file has a startup property. When a server reboots it starts all files with\n"
                              " startup = True. You can use the 'file' variable to refrence to the file getting ran.")
    dump.root.files.append(File("connections.run", "helper"))
    dump.root.files.append(file)
    dump.root.files.append(file2)
    dump.root.files.append(file3) # generation ends here
    Blizz = PC("Jeff")
    Blizz.root.files.append(File("connections.run", "bliz_startup"))
    Blizz.ticket = code_gen()
    my = PC(bash)
    my.root.files.append(File("fire_ticket.exe", "0101011010"*10))
    my.root.files.append(File("DDos.exe", "11010010"*10))
    my.root.files.append(File("helper.txt", "ip: " + dump.ip))

    print("'ls' - to list files\nnew [filename.ext] - to create a file\nrun [filename.ext] - to run the file\n"
          "edit [filename.ext] - to edit a file\nmkdir [folder_name] - to make folder\ncd [folder] - to go into a folder\n"
          "cd .. - to get to the previous folder\ncd / - to get to the root folder\nconnect [ip] - to connect to a "
          "server or PC\nrm - to remove a file\ncat [file] to read a file\ndis - to connect back to your gateway")
    print("Blizzard ip: " + Blizz.ip)
    Helper.i = my
    Helper.mine = my
    while True:
        ins = Helper.i
        ins.execute(input(ins.bash))

if __name__ == '__main__':
    main()
