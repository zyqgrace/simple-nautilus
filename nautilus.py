class Tree():
    def __init__(self):
        self.user = "root"
        self.parent = None
        self.pwd = self
        self.child = []

    def __str__(self):
        return f'{self.user}:/$ '

    def addNode(self,child):
        self.child.append(child)
    
    def absolutepath(self):
        return "/"

class Node():
    def __init__(self,filename,parent):
        self.user = "root"
        self.filename = filename
        self.parent = parent
        self.children = []

    def __str__(self):
        return f'{self.user}:{self.absolutepath()}$ '

    def absolutepath(self):
        if self.parent != "/":
            return self.parent.absolutepath() + "/" + self.pwd
        return "/" + self.pwd
    
    

def check_absolute(path,root):
    if root.absolutepath()==path:
        return root
    if len(root.child) > 0:
        for child in root.child:
            check_absolute(path,child)

def main():
    # TODO
    root = Tree()

    command = (input(root.pwd)).split(" ")
    
    while command[0] != "exit":
        if command[0] == "pwd":
            print(root.absolutepath())
            
        elif command[0] == 'cd':
            if command[1][0]=="/":
                if check_absolute(command[1],root):
                    root.pwd = check_absolute(command[1],root)

        command = (input(root)).split(" ")
    print(f"bye, {root.user}")


if __name__ == '__main__':
    main()
