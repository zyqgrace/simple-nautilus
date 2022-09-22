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


        if folder.check_perm('r',self.user) == False:
            print("ls: Permission denied")
            return
        if folder.parent == None:
            pass
        if not('-d' in command) and folder.parent.check_perm('r',self.user) == False:
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

        if not('-a' in command):
            i = 0
            while i < len(folders):
                if folders[i][2][0] == '.':
                    folders.pop(i)
                else:
                    i += 1

        if '-l' in command: 
            for child in folders:
                print(child[0] + " " + child[1] + " " +child[2])
        else:
            for child in folders:
                print(child[2])