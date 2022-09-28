def mkdir(self,command):
        dir = command[-1].split("/")
        if len(command) == 3 and command[1]!= "-p":
            print("mkdir: Invalid syntax")
            return
        if command[1] == '-p':
            temp_dir = self.pathexist(dir[0], 'directory')
            if temp_dir == False:
                self.pwd.add_directory(dir[0], self.user)
            i = 1
            while i <= len(dir):
                temp_dir = self.pathexist(dir[:i], 'directory')
                if temp_dir != False:
                    if i == len(dir) - 1:
                        if not temp_dir.perm('r',self.user):
                            print("mkdir: Permission denied")
                            break
                    if not temp_dir.perm('w',self.user):
                        print("mkdir: Permission denied")
                        break
                else:
                    temp_dir = self.pathexist(dir[:i-1], 'directory')
                    temp_dir.add_directory(dir[i-1],self.user)
                i+=1
        else:
            if self.pathexist(dir) != False:
                print("mkdir: File exists")
                return
            
            if len(dir)==1:
                parent_dir = self.pwd
            else:
                parent_dir = self.pathexist(dir[:-1])
            if  parent_dir != False:
                if parent_dir.perm_check(True,'w',False,'',
                True,'x',self.user):
                    print('mkdir: Permission denied')
                else:
                    parent_dir.add_directory(dir[-1],self.user)
            else:
                print("mkdir: Ancestor directory does not exist")