class Tree():
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
        dir = Tree(filename,self)
        self.child.append(dir)
    
    def addfile(self,filename):
        file = Tree(filename,self)
        file.type = "file"
        self.child.append(file)

    def absolutepath(self):
        if self.parent == None:
            return "/"
        if self.parent.parent != None:
            return self.parent.absolutepath() + "/" + self.name
        return "/" + self.name
    
    def cd(self,path):
        self.pwd = path

def pathexist(path,root):
    if path == ["",""]:
        return root
    cur = root
    if path[0]=="":
        path = path[1:]
    else:
        cur = root.pwd
    i = 0
    while i < len(path):
        if path[i] == ".":
            i+=1
        elif path[i] == "..":
            if cur.parent == None:
                return cur
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

def main():
    # TODO
    root = Tree()

    original = input(root.pwd)
    command = original.split(" ")
    i = 0
    while command[0] != "exit":
        if command[0] == "pwd":
            print(root.pwd.absolutepath())

        elif command[0] == 'cd':
            if len(command)==1:
                print("cd: Invalid syntax")
            else:
                temp = pathexist(command[1].split("/"),root)
                if temp!=False:
                    if temp.type != "directory":
                        print("cd: Destination is a file")
                    else:
                        root.cd(temp)
                else:
                    print('cd: No such file or directory')

        elif command[0] == 'mkdir':
            if command[1] == '-p':
                pass
            else:
                dir = command[1].split("/")
                if pathexist(dir,root)!=False:
                    print("mkdir: File exists")
                elif len(dir)==1:
                    root.pwd.adddirectory(dir[0])
                elif pathexist(dir[:-1],root)!=False:
                    temp = pathexist(dir[:-1],root)
                    temp.adddirectory(dir[-1])
                else:
                    print("mkdir: Ancestor directory does not exist")
        
        elif command[0] == 'touch':
            file = command[1].split("/")
            if len(file)==1:
                root.pwd.addfile(file[0])
            elif pathexist(file[:-1],root)!=False:
                temp = pathexist(file[:-1],root)
                temp.addfile(file[-1])
        
        elif command[0] == 'ls':
            for child in root.pwd.child:
                print(child.name)
        
        elif command[0] == 'rm' or command[0] == 'rmdir':
            path = command[1].split("/")
            if len(path)==1:
                for child in root.pwd.child:
                    if child.name == path[0]:
                        root.pwd.child.remove(child)
            else:
                temp = pathexist(path[:-1],root)
                for child in temp.child:
                    if child == pathexist(path,root):
                        temp.child.remove(child)
                        ##test

        elif command[0] == 'cp':
            path = command[1].split("/")
            if len(path)==1:
                for child in root.pwd.child:
                    if child.name == path[0]:
                        source = child
            else:
                source = pathexist(path,root)
            path2 = command[2].split("/")
            if len(path2)==1:
                source.name = path2[0]
                root.pwd.child.append(source)
            else:
                dis = pathexist(path2[:-1],root)
                source.name = path2[-1]
                dis.child.append(source)


        else:
            print(f'{original}: command not found')
        original = input(root.pwd)
        command = original.split(" ")
    print(f"bye, {root.user}")


if __name__ == '__main__':
    main()
