class Tree():
    def __init__(self):
        self.user = "root"
        self.parent = None
        self.pwd = self
        self.child = []
        self.type = "directory"

    def __str__(self):
        return f'{self.user}:/$ '

    def adddirectory(self,filename):
        dir = Node(filename,self)
        self.child.append(dir)
    
    def addfile(self,filename):
        file = Node(filename,self)
        file.type = "file"
        self.child.append(file)

    def absolutepath(self):
        return "/"

class Node():
    def __init__(self,filename,parent):
        self.user = "root"
        self.pwd = filename
        self.parent = parent
        self.child = []
        self.type = "directory"

    def __str__(self):
        return f'{self.user}:{self.absolutepath()}$ '

    def absolutepath(self):
        if self.parent.parent != None:
            return self.parent.absolutepath() + "/" + self.pwd
        return "/" + self.pwd
    
    def adddirectory(self,filename):
        dir = Node(filename,self)
        self.child.append(dir)
    
    def addfile(self,filename):
        file = Node(filename,self)
        file.type = "file"
        self.child.append(file)

def pathexist(path,pwd):
    if path[0]=="":
        return pwd
    temp = pwd
    i = 0
    while i < len(path):
        if path[i]==".":
            i+=1
        elif path[i] == "..":
            temp = temp.parent
            i+=1
        else:
            if len(temp.child)==0:
                return False
            for file in temp.child:
                if path[i] == file.pwd:
                    temp = file
                    i +=1
                    break
                else:
                    return False
    return temp

def main():
    # TODO
    root = Tree()

    command = (input(root.pwd)).split(" ")
    i = 0
    while command[0] != "exit":
        if command[0] == "pwd":
            print(root.pwd.absolutepath())
            
        elif command[0] == 'cd':
            if len(command)==1:
                print("cd: Invalid syntax")
            else:
                path = command[1].split("/")
                print(path)

                if path[0]=="":
                    if pathexist(path[1:],root)!= False:
                        temp = pathexist(path[1:],root)
                        if temp.type != "directory":
                            print("cd: Destination is a file")
                        else:
                            root.pwd = temp 
                    else:
                        print('cd: No such file or directory')
                else:
                    if pathexist(path,root.pwd)!= False:
                        temp = pathexist(path,root.pwd)
                        if temp.type != "directory":
                            print("cd: Destination is a file")
                        else:
                            root.pwd = temp
                    else:
                        print("trigger error")
                        print('cd: No such file or directory')

        elif command[0] == 'mkdir':
            if command[1] == '-p':
                pass
            else:
                dir = command[1]
                root.pwd.adddirectory(dir)
        
        elif command[0] == 'touch':
            file = command[1]
            root.pwd.addfile(file)

        elif command[0] == 'ls':
            for child in root.pwd.child:
                print(child.pwd)

        command = (input(root.pwd)).split(" ")
    print(f"bye, {root.user}")


if __name__ == '__main__':
    main()
