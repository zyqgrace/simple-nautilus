
def check_ancestor_perm(file, ind):
    if file.check_perm(ind) == False:
        return False
    elif file.parent == None:
        return True
    else:
        return check_ancestor_perm(file.parent, ind)

def check_perm(self,perm,file=None):
    perms_ind = {
        'r': 1,
        'w': 2,
        'x': 3,
    }
    ind = perms_ind[perm]
    if file == None:
        if self.user != self.owner:
            ind += 3
        return self.file_permission[ind] == perm
    else:
        if self.user != file.owner:
            ind += 3
        return file.file_permission[ind] == perm

def check_perm(self, perm):
        if self.o
        dic = {
            'd': 0,
            1: 'r',
            2: 'w',
            3: 'x',
            4: 'r',
            5: 'w',
            6: 'x'
        }
        if self.file_permission[ind] == dic[ind]:
            return True
        return False

def ls(self,command):

    folders = []
    flag_num = 0
    pwd_name = None
    flag_d = False
    flag_a = False
    flag_l = False
    if "-l" in command:
        flag_num += 1
        flag_l = True
    if "-a" in command:
        flag_num += 1
        flag_a = True
    if "-d" in command:
        flag_num += 1
        flag_d = True

    if (flag_num + 2) < len(command):
        folder = self.pathexist(command[-1].split("/"))
        if folder == False:
            print("ls: No such file or directory")
            return
        pwd_name = folder.name
    else:
        folder = self.pwd
        pwd_name = '.'
    
    if self.user != 'root':
        if folder.check_perm(3) == False:
            print("ls: Permission denied")
            return
        if (not flag_d) and folder.parent.check_perm(3) == False:
            print("ls: Permission denied")
            return
        if check_ancestor_perm(folder,6) == False:
            print("ls: Permission denied")
            return

    if folder.type == 'file':
        temp_file = [folder.file_permission, folder.owner, pwd_name]
        folders.append(temp_file)
    else:
        if flag_d:
            if flag_num < len(command):
                pwd_name = command[-1]
            temp_file = [folder.file_permission, folder.owner, pwd_name]
            folders.append(temp_file)
        else:
            if flag_a:
                temp_file = [folder.file_permission, folder.owner, "."]
                folders.append(temp_file)
            for c in folder.child:
                temp_file = [c.file_permission, c.owner, c.name]
                folders.append(temp_file)

    if flag_l: 
        for child in folders:
            print(child[0] + " " + child[1] + " " +child[2])
    else:
        for child in folders:
            print(child[2])