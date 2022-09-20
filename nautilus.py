class Namespace():
    def __init__(self,name = "/", parent = None,user = "root"):
        self.user = user
        self.pwd = self
        self.parent = parent
        self.name = name
        self.child = set()
        self.type = "directory"
        self.file_permission = "drwxr-x"
    
    def absolute_path(self):
        if self.parent == None:
            return "/"
        if self.parent.parent != None:
            return self.parent.absolute_path() + "/" + self.name
    
    def __str__(self):
        return self.absolute_path()

    def su(self, command, users):
        if len(command)==1:
            self.user = "root"
        else:
            if not(command[1] in users):
                print("su: Invalid user")
            else:
                self.user = command[1]

    def pathexist(self, path):
        if path == ["", ""]:
            return self
        cur = self
        if path[0] == "":
            path = path[1:]
        else:
            cur = self.pwd
        i = 0
        while i < len(path):
            if path[i] == ".":
                i+=1
            elif path[i] == "..":
                if cur.parent == None:
                    pass
                else:
                    cur = cur.parent
                i+=1
            else:
                if len(cur.child)==0:
                    return False
                found = False
                for file in cur.child:
                    if path[i] == file.name:
                        cur = file
                        i +=1
                        found = True
                        break
                if not found:
                    return False
        return cur
    
    def add_directory(self, filename):
        dir = Namespace(filename, self,self.user)
        dir.file_permission = "drwxr-x"
        self.child.add(dir)

    def add_file(self, filename):
        file = Namespace(filename, self, self.user)
        file.type = "file"
        file.file_permission = "-rw-r--"
        self.child.add(file)

    def touch(self,command):
        file = command[1].split("/")
        if len(file)==1:
            self.pwd.add_file(file[0])
        else:
            temp = self.pathexist(file[:-1])
            if temp != False:
                temp.add_file(file[-1])
            else:
                print("touch: Ancestor directory does not exist")

    def mkdir(self,command):
        if len(command) == 3 and command[1]!= "-p":
                print("mkdir: Invalid syntax")
        elif command[1] == '-p':
            dir = command[2].split("/")
            if self.pathexist(dir[0]) == False:
                self.pwd.add_directory(dir[0])
            i = 1
            while i <= len(dir):
                if self.pathexist(dir[:i]) != False:
                    temp = self.pathexist(dir[:i])
                    if i == len(dir) - 1:
                        if temp.file_permission[2] != "w":
                            print("mkdir: Permission denied")
                            break
                    if temp.file_permission[3] != "x":
                        print("mkdir: Permission denied")
                        break
                else:
                    temp = self.pathexist(dir[:i-1])
                    temp.add_directory(dir[i-1])
                i+=1
        else:
            dir = command[1].split("/")
            if self.pathexist(dir)!=False:
                print("mkdir: File exists")
            elif len(dir)==1:
                self.pwd.add_directory(dir[0])
            elif self.pathexist(dir[:-1])!=False:
                temp = self.pathexist(dir[:-1])
                temp.add_directory(dir[-1])
            else:
                print("mkdir: Ancestor directory does not exist")
    
    def cd(self, command):
        path = command[1].split("/")
        temp = self.pathexist(path)
        if temp == False:
            print('cd: No such file or directory')
        elif temp.file_permission[3]!="x":
            print("cd: Permission denied")
        else:
            if temp.type == "file":
                print("cd: Destination is a file")
            else:
                self.pwd = temp

    def cp(self,command):
        path = command[1].split("/")
        path2 = command[2].split("/")

        source = self.pathexist(path)
        dis = self.pathexist(path2)

        if (dis !=False and dis.type == "file"):
            print("cp: File exists")
        elif source == False:
            print("cp: No such file")
        elif (dis != False and dis.type == "directory"):
            print("cp: Destination is a directory")
        elif source.type == "directory":
            print("cp: Source is a directory")
        else:
            dis = self.pathexist(path2[:-1])
            if dis == False or dis.type == "file":
                print("cp: No such file or directory")
            else:
                dis.add_file(path2[-1])

    def mv(self,command):
        path = command[1].split("/")
        path2 = command[2].split("/")

        source = self.pathexist(path)
        dis = self.pathexist(path2)

        if (dis !=False and dis.type == "file"):
            print("mv: File exists")
        elif source == False:
            print("mv: No such file")
        elif (dis !=False and dis.type == "directory"):
            print("mv: Destination is a directory")
        elif source.type == "directory":
            print("mv: Source is a directory")
        else:
            dis = self.pathexist(path2[:-1])
            if dis == False or dis.type == "file":
                print("mv: No such file or directory")
            else:
                source.parent.rm(source)
                source.parent = dis
                source.name = path2[-1]
                dis.child.add(source)

    def rm(self,command):
        path = command[1].split("/")
        file = self.pathexist(path)
        if file == False:
            print("rm: No such file")
        elif file.type == "directory":
            print("rm: Is a directory")
        else:
            if file.parent == None:
                for c in self.child:
                    if file.name == c.name and c.type == "file":
                        self.child.remove(c)
            else:
                for c in file.parent.child:
                    if file.name == c.name and c.type == "file":
                        self.child.remove(c)

    def rmdir(self,command):
        path = command[1].split("/")
        dir = self.pathexist(path)
        if dir == False:
            print("rmdir: No such file or directory")
        elif dir == self.pwd:
            print("rmdir: Cannot remove pwd")
        elif dir.type =="file":
            print("rmdir: Not a directory")
        elif len(dir.child) > 0:
            print("rmdir: Directory not empty")
        else:
            if dir.parent == None:
                for c in self.child:
                    if dir.name == c.name and c.type == "directory":
                        self.child.remove(c)
            else:
                for c in dir.parent.child:
                    if dir.name == c.name and c.type == "directory":
                        self.child.remove(c)

    def ls(self,command):
        flag_l = False
        flag_a = False
        flag_d = False
        files = []
        cm_num = 1
        if "-l" in command:
            flag_l = True
            cm_num += 1
        if "-a" in command:
            flag_a = True
            cm_num += 1
        if "-d" in command:
            flag_d = True
            cm_num += 1
        if cm_num < len(command):
            if self.pathexist(command[-1].split("/")) == False:
                print("ls: No such file or directory")
                return 
            else:
                folder = self.pathexist(command[-1].split("/"))
        else:
            folder = self.pwd
        for c in folder.child:
            files.append(c)
        if flag_d:
            for f in files:
                if f.type == "directory":
                    files.remove(f)
        elif flag_l: 
            if flag_a:
                print(folder.file_permission + " " + folder.user + " .")
                print(folder.parent.file_permission + " " + folder.parent.user + " ..")
            for child in files:
                print(child.file_permission + " " + child.user + " " +child.name)
        else:
            if flag_a:
                print(".\n..")
            for child in files:
                print(child.name)

    def chmod(self,command):
        file = self.pathexist(command[2].split("/"))
        cur_perm = []
        for perm in file.file_permission:
            cur_perm.append(perm)
        user = []
        sign = None
        perm = []
        index = {
            "u" : 1,
            "o" : 4,
            "r" : 0,
            "w" : 1,
            "x" : 2,
        }
        for char in command[1]:
            if char in ["u","o","a"]:
                if char == "a":
                    user.append("u")
                    user.append("o")
                else:
                    user.append(char)
            elif char in ["+","=","-"]:
                sign = char
            elif char in ["r","x","w"]:
                perm.append(char)

        for u in user:
            if sign == "=":
                i = 0
                while i < 3:
                    cur_perm[index[u]+i]="-"
                    i+=1
            for p in perm:
                ind = index[u]+index[p]
                if sign == "-":
                    cur_perm[ind]="-"
                else:
                    cur_perm[ind]= p
        file.file_permission = ""
        for p in cur_perm:
            file.file_permission += p

    def chown(self,command,users):
        if self.user != "root":
            print("chown: Operation not permitted")
        else:
            file = self.pathexist(command[2].split("/"))
            if not(command[1] in users):
                print("chown: Invalid user")
            elif file == False:
                print("chown: No such file or directory")
            else:
                file.user = command[1]

def input_command(pwd):
    '''
    this function breaks the commandline input into a list of arguments 
    and boolean of validity
    '''
    valid = True
    quote = False
    temp = input(pwd.user+":"+str(pwd)+"$ ")
    valid_list = { "-", "_", "\"", " ", "+",\
         "=", ".", "/", "\t", "\n", "\r", "\v"}

    i = 0
    start = 0
    command = []
    while i < len(temp):
        if not(temp[i].isalpha()) and not(temp[i].isnumeric())\
        and not(temp[i] in valid_list):
            valid = False
        elif quote:
            if temp[i] == "\"":
                quote = False
                command.append(temp[start:i])
                start = i + 2
        else:
            if temp[i] == "\"":
                quote = True
                start = i + 1
            elif temp[i].isspace():
                if start == i:
                    pass
                else:
                    command.append(temp[start:i])
                start = i + 1
        i += 1
    if start != len(temp):
        command.append(temp[start:])

    if not valid:
        return command[0], valid
    return command, valid

def main():
    # creating a root user
    root = Namespace()
    users = ["root"]
    cur_user = root
    
    while True:
        command_line = input_command(cur_user.pwd)
        command = command_line[0]
        valid = command_line[1]
        all_commands = {'pwd', 'cd', 'exit', 'ls',"mkdir", "cp",\
            "touch", "mv", "chmod", "chown", "su", "adduser", "deluser"}
        if not valid:
            print(f"{command[0]}: Invalid syntax")
            continue
        elif command == []:
            continue
        elif command[0] == "su":
            cur_user.su(command,users)
        elif command[0] == "adduser":
            if command[1] in users:
                print("adduser: The user already exists")
            else:
                users.append(command[1])
        elif command[0] == "deluser":
            unwant_user = command[1]
            if not(unwant_user in users):
                print("deluser: The user does not exist")
            elif unwant_user == "root":
                print("WARNING: You are just about to delete the root account")
                print("Usually this is never required as it may render the whole system unusable")
                print("If you really want this, call deluser with parameter --force")
                print("(but this `deluser` does not allow `--force`, haha)")
                print("Stopping now without having performed any action")
            else:
                users.remove(unwant_user)
        elif command[0] == 'pwd' and len(command) == 1:
            print(cur_user)
        elif command[0] == 'exit' and len(command) == 1:
            break
        elif command[0] == 'touch' and len(command) == 2:
            cur_user.touch(command)
        elif command[0] == 'mkdir' and 2 <= len(command) <= 3:
            cur_user.mkdir(command)
        elif command[0] == "cd" and len(command) == 2:
            cur_user.cd(command)
        elif command[0] == "cp" and len(command) == 3:
            cur_user.cp(command)
        elif command[0] == "mv" and len(command) == 3:
            cur_user.mv(command)
        elif command[0] == "rm" and len(command) == 2:
            cur_user.rm(command)
        elif command[0] == "rmdir" and len(command) == 2:
            cur_user.rmdir(command)
        elif command[0] == 'ls':
            cur_user.ls(command)
        elif command[0] == "chmod":
            cur_user.chmod(command)
        elif command[0]=="chown":
            cur_user.chown(command,users)
        else:
            if command[0] in all_commands:
                print(f"{command[0]}: Invalid syntax")
            else:
                print(f'{command[0]}: Command not found')

    print(f"bye, {cur_user.user}")
    
if __name__ == '__main__':
    main()
        
