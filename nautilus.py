class Tree():
    def __init__(self,root):
        self.root = root
        self.child = []

    def __str__(self):
        return f'root:/$ {self.root}'

    def addNode(self,child):
        self.child.append(child)

class Node():
    def __init__(self,data):
        self.data = data
        self.child = []
    def addNode(self,obj):
        self.child.append(obj)

def main():
    # TODO
    command = input()
    pwd = Tree("/")
    while command != "exit":
        if command == "pwd":
            print(pwd)
        command = input()
    print(f"root:/$ bye, {pwd.root}")


if __name__ == '__main__':
    main()
