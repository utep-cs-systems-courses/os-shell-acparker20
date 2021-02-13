#!/usr/bin/env python3

while True:
    if 'PS1' in os.environ:
        os.write(1, os.environ['PS1']).encode())
    else:
        os.write(1, ("$ ").encode())
    args = os.read(0, 1024)

    if len(args) == 0:
        break
    args = args.decode().splitlines

    for arg in args:
        execute(arg.split())

def execute(args):
    if len(args) == 0:
        return
    
    elif args[0] == "exit":
        sys.exit(0)

    else:
        rc = os.fork()
        background = True

        if "&" in args:
            args.remove("&")
            background = False
        if rc < 0:
            os.write(2, ("Fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            if "/" in args[0]:
                program = args[0]
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass













            
