#!/usr/bin/env python3

import os,sys,re

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
    
    elif args[0].lower() == "exit":
        sys.exit(0)
        
    elif args[0] == "cd":
        try:
            if len(args) == 1:
                os.chdir("..")
            else:
                os.chdir(args[1])
        except:
            os.write(1, ("cd %s: No such directory or file" % args[1]).encode())
            pass
        
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
            else:
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:
                        pass
            os.write(2, ("Command not found\n".encode())
            sys.exit(0)
        else:
            if background:
                     child = os.wait()
                        
                    













            
