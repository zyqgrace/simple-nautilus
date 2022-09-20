class Namespace():
    def __init__(self,name = "/", parent = None):
        self.user = "root"
        self.parent = parent
        self.pwd = self
        self.name = name
        self.child = []
        self.type = "directory"

    def __str__(self):
        return f'{self.user}:{self.absolutepath()}$ '

    def adddirectory(self,filename):
        dir = Namespace(filename,self)
        self.child.append(dir)
    
    def addfile(self,filename):
        file = Namespace(filename,self)
        file.type = "file"
        self.child.append(file)

    def absolutepath(self):
        if self.parent == None:
            return "/"
        if self.parent.parent != None:
            return self.parent.absolutepath() + "/" + self.name
        return "/" + self.name
    
    def cd(self,path):
        temp = self.pathexist(path)
        if temp==False:
            print('cd: No such file or directory')
        else:
            if temp.type == "file":
                print("cd: Destination is a file")
            else:
                self.pwd = temp
    
    def rm(self,child):
        for c in self.child:
            if child.name == c.name and c.type=="file":
                self.child.remove(c)
    
    def rmdir(self,child):
        for c in self.child:
            if child.name == c.name and c.type=="directory":
                self.child.remove(c)


    # if the path exist, return the path, else it would return False
    def pathexist(self,path):
        if path == ["",""]:
            return self
        cur = self
        if path[0]=="":
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

def remove_space(command):
    if command[0]==" ":
        return remove_space(command[1:])
    elif command[-1]==" ":
        return remove_space(command[:-1])
    else:
        return command

def user_command(pwd):
    valid = True
    temp = input(pwd)
    invalid_list = ["@","#","!","$","%","^","*","("]
    quote = False
    i = 0
    start = 0
    command = []
    while i < len(temp):
        if temp[i] in invalid_list:
            valid = False
        if quote:
            if temp[i] == "\"":
                quote = False
                command.append(temp[start:i])
                start = i + 2
        else:
            if temp[i] == "\"":
                quote = True
                start = i + 1
            elif temp[i] == " ":
                command.append(temp[start:i])
                start = i + 1
        i += 1
    command.append(temp[start:])

    j = 0
    while j < len(command):
        if command[j] == "":
            command.pop(j)
        else:
            command[j] = remove_space(command[j])
            j+=1

    if not valid:
        return command[0], valid
    return command, valid

def user_exist(name,users):
    for u in users:
        if name == u.user:
            return u
    return False

def main():
    # TODO
    root = Namespace()
    cur_user = root
    users = [root]
    while True:
        command_valid = user_command(cur_user.pwd)
        command = command_valid[0]
        valid = command_valid[1]

        if not valid:
            print(f"{command}: Invalid syntax")
            continue

        if command == []:
            pass
        elif command[0] == "exit":
            if len(command)!=1:
                print("exit: Invalid syntax")
            else:
                break

        elif command[0] == "adduser":
            if user_exist(command[1],users) !=False:
                print("adduser: The user already exists")
            else:
                new_user = Namespace()
                new_user.user = command[1]
                users.append(new_user)

        elif command[0] == "su":
            if len(command)==1:
                cur_user = root
            else:
                if user_exist(command[1],users)==False:
                    print("su: Invalid user")
                else:
                    cur_user = user_exist(command[1],users)
        
        elif command[0]=="deluser":
            unwant_user = user_exist(command[1],users)
            if unwant_user == False:
                print("deluser: The user does not exist")
            elif unwant_user == root:
                print("WARNING: You are just about to delete the root account")
                print("Usually this is never required as it may render the whole system unusable")
                print("If you really want this, call deluser with parameter --force")
                print("(but this `deluser` does not allow `--force`, haha)")
                print("Stopping now without having performed any action")
            else:
                users.remove(unwant_user)
        
        elif command[0] == "pwd":
            if len(command)>1:
                print("pwd: Invalid syntax")
            else:
                print(cur_user.pwd.absolutepath())

        elif command[0] == 'cd':
            if len(command)!=2:
                print("cd: Invalid syntax")
            else:
                path = command[1].split("/")
                cur_user.cd(path)

        elif command[0] == 'mkdir':
            if len(command)!=2 and len(command)!=3:
                print("mkdir: Invalid syntax")
            elif len(command)==3 and command[1]!="-p":
                print("mkdir: Invalid syntax")
            elif command[1] == '-p':
                dir = command[2].split("/")
                if cur_user.pathexist(dir[0])==False:
                    cur_user.pwd.adddirectory(dir[0])
                i = 1
                while i <= len(dir):
                    if cur_user.pathexist(dir[:i])!=False:
                        temp = cur_user.pathexist(dir[:i])
                    else:
                        temp = cur_user.pathexist(dir[:i-1])
                        temp.adddirectory(dir[i-1])
                    i+=1
            else:
                dir = command[1].split("/")
                if cur_user.pathexist(dir)!=False:
                    print("mkdir: File exists")
                elif len(dir)==1:
                    cur_user.pwd.adddirectory(dir[0])
                elif cur_user.pathexist(dir[:-1])!=False:
                    temp = cur_user.pathexist(dir[:-1])
                    temp.adddirectory(dir[-1])
                else:
                    print("mkdir: Ancestor directory does not exist")
        
        elif command[0] == 'touch':
            if len(command)!=2:
                print("touch: Invalid syntax")
            else:
                file = command[1].split("/")
                if len(file)==1:
                    cur_user.pwd.addfile(file[0])
                elif cur_user.pathexist(file[:-1])!=False:
                    temp = cur_user.pathexist(file[:-1])
                    temp.addfile(file[-1])
                else:
                    print("touch: Ancestor directory does not exist")
        
        elif command[0] == 'ls':
            for child in cur_user.pwd.child:
                print(child.name)
        
        elif command[0] == 'rm':
            if len(command)!=2:
                print("rm: Invalid syntax")
            else:
                path = command[1].split("/")
                file = cur_user.pathexist(path)
                if file == False:
                    print("rm: No such file")
                elif file.type =="directory":
                    print("rm: Is a directory")
                else:
                    if file.parent == None:
                        cur_user.rm(file)
                    else:
                        file.parent.rm(file)

        elif command[0] == 'rmdir':
            if len(command) != 2:
                print("rmdir: Invalid syntax")
            else:
                path = command[1].split("/")
                dir = cur_user.pathexist(path)
                if dir == False:
                    print("rmdir: No such file or directory")
                elif dir == cur_user.pwd:
                    print("rmdir: Cannot remove pwd")
                elif dir.type =="file":
                    print("rmdir: Not a directory")
                elif len(dir.child) > 0:
                    print("rmdir: Directory not empty")
                else:
                    if dir.parent == None:
                        cur_user.rmdir(dir)
                    else:
                        dir.parent.rmdir(dir)

        elif command[0] == 'cp':
            if len(command)!=3:
                print("cp: Invalid syntax")
            else:
                path = command[1].split("/")
                path2 = command[2].split("/")

                source = cur_user.pathexist(path)
                dis = cur_user.pathexist(path2)

                if (dis !=False and dis.type == "file"):
                    print("cp: File exists")
                elif source == False:
                    print("cp: No such file")
                elif (dis !=False and dis.type == "directory"):
                    print("cp: Destination is a directory")
                elif source.type == "directory":
                    print("cp: Source is a directory")
                else:
                    dis = cur_user.pathexist(path2[:-1])
                    if dis == False or dis.type == "file":
                        print("cp: No such file or directory")
                    else:
                        dis.addfile(path2[-1])

        elif command[0] == 'mv':
            if len(command)!=3:
                print("mv: Invalid syntax")
            else:
                path = command[1].split("/")
                path2 = command[2].split("/")

                source = cur_user.pathexist(path)
                dis = cur_user.pathexist(path2)

                if (dis !=False and dis.type == "file"):
                    print("mv: File exists")
                elif source == False:
                    print("mv: No such file")
                elif (dis !=False and dis.type == "directory"):
                    print("mv: Destination is a directory")
                elif source.type == "directory":
                    print("mv: Source is a directory")
                else:
                    dis = cur_user.pathexist(path2[:-1])
                    if dis == False or dis.type == "file":
                        print("mv: No such file or directory")
                    else:
                        source.parent.rm(source)
                        source.parent = dis
                        source.name = path2[-1]
                        dis.child.append(source)

        else:
            print(f'{command[0]}: Command not found')
    print(f"bye, {cur_user.user}")


if __name__ == '__main__':
    main()
