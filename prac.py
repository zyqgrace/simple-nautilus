
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
    else:
        folder = self.pwd
    
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
        temp_file = [folder.file_permission, folder.owner, command[-1]]
        folders.append(temp_file)
    else:
        if flag_d:
            if flag_num < len(command):
                temp_file = [folder.file_permission, folder.owner, command[-1]]
            else:
                temp_file = [folder.file_permission, folder.owner, '.']
            folders.append(temp_file)
        else:
            temp_file = [folder.file_permission, folder.owner, "."]
            folders.append(temp_file)
            temp_file = [folder.parent.file_permission, folder.parent.owner, ".."]
            folders.append(temp_file)
            for c in folder.child:
                temp_file = [c.file_permission, c.owner, c.name]
                folders.append(temp_file)
            if not flag_a:
                for f in folders:
                    if f[0] == '.':
                        folders.remove(f)

    if flag_l: 
        for child in folders:
            print(child[0] + " " + child[1] + " " +child[2])
    else:
        for child in folders:
            print(child[2])