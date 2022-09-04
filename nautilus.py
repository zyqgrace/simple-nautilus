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
    
def check_absolute(path,root):
    if root.absolutepath()==path:
        return True,root
    if len(root.child) > 0:
        for child in root.child:
            if check_absolute(path,child)[0]== True:
                return check_absolute(path,child)

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
                if command[1][0]=="/":
                    temp = check_absolute(command[1],root)[1]
                    if temp != None:
                        if temp.type != "directory":
                            print("cd: Destination is a file")
                        root.pwd = check_absolute(command[1],root)[1]
                    else:
                        print('cd: No such file or directory')
                else:
                    for file in root.pwd.child:
                        if file.pwd == command[1]:
                            if file.type != "directory":
                                print('cd: No such file or directory')
                            else:
                                root.pwd = file
                        else:
                            print('cd: No such file or directory')

        elif command[0] == 'mkdir':
            if command[1] == '-p':
                pass
            else:
                dir = command[1]
                root.pwd.adddirectory(dir)
        
        elif command[0] == 'ls':
            for child in root.pwd.child:
                print(child.pwd)

        command = (input(root.pwd)).split(" ")
    print(f"bye, {root.user}")


if __name__ == '__main__':
    main()
