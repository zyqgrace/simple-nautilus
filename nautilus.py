class Namespace():
    def __init__(self,name="/", parent=None, user="root", owner= "root"):
        self.user = user
        self.owner = owner
        self.name = name
        self.pwd = self
        self.parent = parent
        self.child = []
        self.type = "directory"
        self.file_permission = "drwxr-x"
    
    def __str__(self):
        return self.absolute_path()

    def absolute_path(self):
        if self.parent == None:
            return "/"
        if self.parent.parent != None:
            return self.parent.absolute_path() + "/" + self.name
        return "/" + self.name

    def su(self, command, users):
        if len(command)==1:
            self.user = "root"
        else:
            if not(command[1] in users):
                print("su: Invalid user")
            else:
                self.user = command[1]

    def adduser(self,command,users):
        if self.user != 'root':
            print('adduser: Operation not permitted')
        elif command[1] in users:
            print("adduser: The user already exists")
        else:
            users.append(command[1])
        return users

    def pathexist(self, path, type=['directory', 'file']):
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
                    if file.type in type:
                        if path[i] == file.name:
                            cur = file
                            i +=1
                            found = True
                            break
                if not found:
                    return False
        return cur
    
    def add_directory(self, filename):
        owner = self.user
        dir = Namespace(filename, self,self.user,owner)
        self.child.append(dir)

    def add_file(self, filename):
        owner = self.user
        file = Namespace(filename, self, self.user,owner)
        file.type = "file"
        file.file_permission = "-rw-r--"
        self.child.append(file)

    def touch(self,command):
        file = command[1].split("/")
        if len(file) == 1:
            dir = self.pwd
            filename = file[0]
        else:
            dir = self.pathexist(file[:-1])
            filename = file[-1]
            if dir == False:
                print("touch: Ancestor directory does not exist")
                return
        
        if dir.perm_check(True,'w',False,'',True,'x',self.user):
            print('touch: Permission denied')
            return

        if self.pathexist(file) != False:
            return
        dir.add_file(filename)
        

    def mkdir(self,command):
        dir = command[-1].split("/")
        if len(command) == 3 and command[1]!= "-p":
                print("mkdir: Invalid syntax")
                return

        if command[1] == '-p':
            first_dir = self.pathexist(dir[0],'directory')
            if first_dir == False:
                self.pwd.add_directory(dir[0])

            i = 1
            while i <= len(dir):
                temp_dir = self.pathexist(dir[:i],'directory')
                if temp_dir != False:
                    if i == len(dir) - 1:
                        if not temp_dir.perm('r',self.user):
                            print("mkdir: Permission denied")
                            break
                    if not temp_dir.perm('w',self.user):
                        print("mkdir: Permission denied")
                        break
                else:
                    temp_dir = self.pathexist(dir[:i-1],'directory')
                    temp_dir.add_directory(dir[i-1])
                i+=1
        else:
            if self.pathexist(dir) != False:
                print("mkdir: File exists")
            
            
            elif len(dir)==1:
                self.pwd.add_directory(dir[0])

            elif self.pathexist(dir[:-1]) != False:
                temp = self.pathexist(dir[:-1])
                temp.add_directory(dir[-1])
            else:
                print("mkdir: Ancestor directory does not exist")
    
    def cd(self, command):
        path = command[1].split("/")
        temp = self.pathexist(path)
        if temp == False:
            print('cd: No such file or directory')
        elif  temp.type == 'file':
                print("cd: Destination is a file")
        elif self.perm('x', self.user, temp) == False:
            print("cd: Permission denied")
        else:
            self.pwd = temp

    def cp(self,command):
        path = command[1].split("/")
        path2 = command[2].split("/")

        source = self.pathexist(path)
        copy_file = self.pathexist(path2)

        if len(path2)==1:
            dis_dir = self.pwd
        else:
            dis_dir = self.pathexist(path2[:-1])

        if (copy_file != False):
            if copy_file.type == 'directory':
                print('cp: Destination is a directory')
                return
            elif  copy_file.name == path2[-1]:
                print("cp: File exists")
                return
        if source == False:
            print("cp: No such file")
            return
        if dis_dir == False:
            print("cp: No such file or directory")
            return
        if dis_dir.type == 'file':
            print("cp: No such file or directory")
            return
        if source.type == 'directory':
            print("cp: Source is a directory")
            return
                
        if source.perm_check(True, 'r', False,'', True, 'x', self.user):
            print('cp: Permission denied')
            return
        if dis_dir.perm_check(True, 'w', False,'', True, 'x', self.user):
            print('cp: Permission denied')
            return

        dis_dir.add_file(path2[-1])

    def mv(self,command):
        path = command[1].split("/")
        source = self.pathexist(path)

        path2 = command[2].split("/")
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
            if len(path2) == 1:
                dis = self.pwd
            else:
                dis = self.pathexist(path2[:-1])

            if dis == False or dis.type == "file":
                print("mv: No such file or directory")
            else:
                source.parent.child.remove(source)
                source.parent = dis
                source.name = path2[-1]
                dis.child.append(source)

    def rm(self,command):
        path = command[1].split("/")
        file = self.pathexist(path)
        if file == False:
            print("rm: No such file")
        elif file.type == "directory":
            print("rm: Is a directory")
        else:
            parent = file.parent
            i = 0
            while i < len(parent.child):
                if file.name == parent.child[i].name \
                    and parent.child[i].type == "file":
                    parent.child.pop(i)
                i += 1

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
            parent = dir.parent
            if parent == None:
                for c in self.child:
                    if dir.name == c.name and c.type == "directory":
                        self.child.remove(c)
            else:
                i = 0
                while i < len(parent.child):
                    if dir.name == parent.child[i].name \
                        and parent.child[i].type == "directory":
                        parent.child.pop(i)
                    i += 1

    def ls(self,command):
        folders = []
        flag_num = 0

        if "-l" in command:
            flag_num += 1
        if "-a" in command:
            flag_num += 1
        if "-d" in command:
            flag_num += 1

        if (flag_num + 1) < len(command):
            folder = self.pathexist(command[-1].split("/"))
            if folder == False:
                print("ls: No such file or directory")
                return
        else:
            folder = self.pwd

        if ('-d' in command) or folder.type == 'file':
            if folder.parent == None:
                if folder.perm('r',self.user) == False:
                    print("ls: Permission denied")
                    return
            elif folder.parent.perm('r',self.user) == False:
                print("ls: Permission denied")
                return
        elif folder.type == 'directory':
            if folder.perm('r',self.user) == False:
                print("ls: Permission denied")
                return

        if check_ancestor_perm(folder,'x',self.user) == False:
            print("ls: Permission denied")
            return

        if folder.type == 'file':
            temp_file = [folder.file_permission, folder.owner, command[-1]]
            folders.append(temp_file)
        else:
            if '-d' in command:
                if flag_num + 1 < len(command):
                    temp_file = [folder.file_permission, folder.owner, command[-1]]
                else:
                    temp_file = [folder.file_permission, folder.owner, '.']
                folders.append(temp_file)
            else:
                temp_file = [folder.file_permission, folder.owner, "."]
                folders.append(temp_file)
                if folder.parent == None:
                    temp_file = [folder.file_permission, folder.owner, ".."]
                else:
                    temp_file = [folder.parent.file_permission, folder.parent.owner, ".."]
                folders.append(temp_file)
                for c in folder.child:
                    temp_file = [c.file_permission, c.owner, c.name]
                    folders.append(temp_file)

        i = 0
        hidden_files = []
        while i < len(folders):
            if folders[i][2][0] == '.':
                hidden_files.append(folders[i])
                folders.pop(i)
            else:
                i += 1

        if '-a' in command:
            folders = hidden_files + folders

        if '-l' in command: 
            for child in folders:
                print(child[0] + " " + child[1] + " " +child[2])
        else:
            for child in folders:
                print(child[2])

    def chmod(self,command):
        flag_r = False
        if '-r' in command:
            flag_r = True

        file = self.pathexist(command[-1].split("/"))

        if check_ancestor_perm(file,'x',self.user) == False:
            print("chmod: Permission denied")
            return
            
        if flag_r:
            all_files = []
            all_files.append(file)
            all_files += file.recursive()
            for c in all_files:
                if self.user != 'root' and self.user != c.owner:
                    print("chmod: Operation not permitted")
                else:
                    if change_mode(c.file_permission, command[-2]) == False:
                        print('chmod: Invalid mode')
                    else:
                        c.file_permission = change_mode(c.file_permission, command[-2])
        else:
            if change_mode(file.file_permission, command[-2]) == False:
                print('chmod: Invalid mode')
            else:
                file.file_permission = change_mode(file.file_permission, command[-2])

    def recursive(self):
        result = []
        if len(self.child) == 0:
            return []
        result += self.child

        for c in self.child:   
            result += c.recursive()
        return result

    def chown(self,command,users):
        if self.user != "root":
            print("chown: Operation not permitted")
        else:
            new_owner = command[-2]
            if (new_owner not in users):
                    print("chown: Invalid user")
                    return
            file = self.pathexist(command[-1].split("/"))
            files = []
            if file == False:
                print("chown: No such file or directory")
                return 

            files.append(file)
            if '-r' in command:
                    files += file.recursive()

            for f in files:
                    f.owner = new_owner

    def perm(self, perm, user, file=None):
        if user == 'root':
            return True
        perms_ind = {
            'r': 1,
            'w': 2,
            'x': 3,
        }
        ind = perms_ind[perm]
        if file == None:
            if user != self.owner:
                ind += 3
            return self.file_permission[ind] == perm
        else:
            if user != file.owner:
                ind += 3
            return file.file_permission[ind] == perm

    def perm_check(self, file, perm1, par, perm2, ance, perm3, user):
        denied = False
        if file:
            if self.perm(perm1,user) == False:
                denied = True
        if par:
            if self.parent == None:
                pass
            elif self.parent.perm(perm2,user) == False:
                denied = True
        if ance:
            if check_ancestor_perm(self, perm3,user) == False:
                denied = True
        return denied

def change_mode(file_permission, mode):
    cur_perm = []
    for perm in file_permission:
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

    i = 0
    while i < len(mode):
        if mode[i] in ["u","o","a"]:
            if mode[i] == "a":
                user.append("u")
                user.append("o")
            else:
                user.append(mode[i])
            i += 1
        else:
            if mode[i] in ["+","=","-"]:
                break
            else:
                return False
    sign = mode[i]
    i += 1

    while i < len(mode):
        if mode[i] in ["r","x","w"]:
            perm.append(mode[i])
            i += 1
        else:
            return False

    for u in user:
        if sign == "=":
            i = 0
            while i < 3:
                cur_perm[index[u]+i] = "-"
                i+=1
        for p in perm:
            ind = index[u]+index[p]
            if sign == "-":
                cur_perm[ind] = "-"
            else:
                cur_perm[ind] = p

    result = ''
    for p in cur_perm:
        result += p
    return result

def check_ancestor_perm(file, ind, user):
    if file.perm(ind,user) == False:
        return False
    elif file.parent == None:
        return True
    else:
        return check_ancestor_perm(file.parent, ind, user)

def input_command(user, pwd):
    '''
    this function breaks the commandline input into a list of arguments 
    and boolean of validity
    '''
    valid = True
    quote = False
    temp = input(user+":"+ str(pwd) +"$ ")
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
    if start < len(temp):
        command.append(temp[start:])

    for c in command:
        if c == '':
            command.remove(c)
    return command, valid

def main():
    # creating a root user
    root = Namespace()
    users = ["root"]
    cur_user = root
    
    while True:
        command_line = input_command(cur_user.user, cur_user.pwd)
        command = command_line[0]
        valid = command_line[1]
        all_commands = {'pwd', 'cd', 'exit', 'ls',"mkdir", "cp", "rm",\
            "touch", "mv", "chmod", "chown", "su", "adduser", "deluser",\
                "rmdir"}
        if not valid:
            print(f"{command[0]}: Invalid syntax")
            continue
        elif command == []:
            continue
        elif command[0] == "su":
            cur_user.su(command,users)
        elif command[0] == "adduser":
            users = cur_user.adduser(command,users)
        elif command[0] == "deluser":
            unwant_user = command[1]
            if cur_user.user != 'root':
                print('deluser: Operation not permitted')
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
            print(cur_user.pwd)
        elif command[0] == 'exit' and len(command) == 1:
            break
        elif command[0] == 'touch' and len(command) == 2:
            cur_user.touch(command)
        elif command[0] == 'mkdir' and 2 <= len(command) <= 3:
            d = cur_user.mkdir(command)
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
        elif command[0] == "chmod" and 2 <= len(command) <= 4:
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
        
