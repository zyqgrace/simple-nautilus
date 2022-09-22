def cp(self,command):
    path = command[1].split("/")
    path2 = command[2].split("/")

    source = self.pathexist(path)
    copy_file = self.pathexist(path2)

    if len(path2)==1:
        dis_dir = self.pwd
    else:
        dis_dir = self.pathexist(path2[:-1])
    
    if source == False:
        print("cp: No such file")
        return

    if dis_dir == False:
        print("cp: No such file or directory")
        return

    if (dir !=False):

        if  dir.name == path[-1]:
            print("cp: File exists")
            return 

        elif dir.type == 'directory':
            print("cp: Source is a directory")
            return 

    if source.check_perm('r', self.user) == False:
        print('cp: Permission denied')
        return

    elif check_ancestor_perm(source,'x',self.user) == False:
        print('cp: Permission denied')
        return

    if dis_dir.check_perm('w', self.user) == False:
        print('cp: Permission denied')
        return

    if check_ancestor_perm(dis_dir,'x',self.user) == False:
        print('cp: Permission denied')
        return

    dis_dir.add_file(path2[-1])