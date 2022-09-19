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

def main():
    # TODO
    root = Namespace()

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
                path = command[1].split("/")
                root.cd(path)

        elif command[0] == 'mkdir':
            if command[1] == '-p':
                dir = command[2].split("/")
                if root.pathexist(dir[0])==False:
                    root.pwd.adddirectory(dir[0])
                i = 1
                while i <= len(dir):
                    if root.pathexist(dir[:i])!=False:
                        temp = root.pathexist(dir[:i])
                    else:
                        temp = root.pathexist(dir[:i-1])
                        temp.adddirectory(dir[i-1])
                    i+=1
            else:
                dir = command[1].split("/")
                if root.pathexist(dir)!=False:
                    print("mkdir: File exists")
                elif len(dir)==1:
                    root.pwd.adddirectory(dir[0])
                elif root.pathexist(dir[:-1])!=False:
                    temp = root.pathexist(dir[:-1])
                    temp.adddirectory(dir[-1])
                else:
                    print("mkdir: Ancestor directory does not exist")
        
        elif command[0] == 'touch':
            file = command[1].split("/")
            if len(file)==1:
                root.pwd.addfile(file[0])
            elif root.pathexist(file[:-1])!=False:
                temp = root.pathexist(file[:-1])
                temp.addfile(file[-1])
            else:
                print("touch: Ancestor directory does not exist")
        
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
                temp = root.pathexist(path[:-1])
                for child in temp.child:
                    if child == root.pathexist(path):
                        temp.child.remove(child)
                        ##test

        elif command[0] == 'cp':
            path = command[1].split("/")
            path2 = command[2].split("/")

            source = root.pathexist(path)
            dis = root.pathexist(path2)

            if (dis !=False and dis.type == "file"):
                print("cp: File exists")
            elif source == False:
                print("cp: No such file")
            elif (dis !=False and dis.type == "directory"):
                print("cp: Destination is a directory")
            elif source.type == "directory":
                print("cp: Source is a directory")
            else:
                dis = root.pathexist(path2[:-1])
                if dis == False or dis.type == "file":
                    print("cp: No such file or directory")
                else:
                    dis.child.append(source)
        elif command[0] == 'mv':
            path = command[1].split("/")
            path2 = command[2].split("/")

            source = root.pathexist(path)
            dis = root.pathexist(path2)

            if (dis !=False and dis.type == "file"):
                print("mv: File exists")
            elif source == False:
                print("mv: No such file")
            elif (dis !=False and dis.type == "directory"):
                print("mv: Destination is a directory")
            elif source.type == "directory":
                print("mv: Source is a directory")
            else:
                dis = root.pathexist(path2[:-1])
                if dis == False or dis.type == "file":
                    print("mv: No such file or directory")
                else:
                    source.parent = dis
                    dis.child.append(source)

        else:
            print(f'{original}: command not found')
        original = input(root.pwd)
        command = original.split(" ")
    print(f"bye, {root.user}")


if __name__ == '__main__':
    main()
