input = open('input').read()

class Directory(object):
    def __init__(self, name):
        self.name = name
        self.directories = {}
        self.files = {}

    def size(self):
        return sum(
                size for size in self.files.values()
            ) + sum(
                dir.size() for dir in self.directories.values()
            )

    def cd(self, dirName):
        return self.directories.setdefault(dirName, Directory(dirName))

    def collect_dirs(self, acc = []):
        acc.append(self)
        for dir in self.directories.values():
            dir.collect_dirs(acc)
        return acc

def build_filesystem(input):
    root = Directory('/')
    cwd = [root]
    for line in input.splitlines():
        if line.startswith('$'):
            (cmd, arg) = (line.split() + [''])[1:3]
            if cmd == 'cd':
                if arg == '/':
                    cwd = [root]
                elif arg == '..':
                    cwd.pop()
                    if len(cwd) == 0:
                        cwd = [root]
                else:
                    cwd.append(cwd[-1].cd(arg))
            # ignore ls
        else:
            (size, name) = line.split()
            if size == 'dir':
                cwd[-1].cd(name)
            else:
                cwd[-1].files[name] = int(size)
    return root

root = build_filesystem(input)
dirs = root.collect_dirs()

max_size = 70000000
req_size = 30000000

used_size = root.size()
unused_size = max_size - used_size

diff = req_size - unused_size

sizes = [dir.size() for dir in dirs]
sizes.sort()

solution = next(size for size in sizes if size >= diff)

print(solution)
