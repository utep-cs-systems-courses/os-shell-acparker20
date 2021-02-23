#!/usr/bin/env python3

from os import read
import os,sys, re


next = 0
limit = 0


#method calls read to fill buffer one character at a time
def my_getChar():
    global next
    global limit

    if next == limit:
        next = 0
        limit = read(0,1000)#allocating bytes, upperbound

        if limit == 0:
            return None 

    if next < len(limit)-1: #checks upperbound for space
        c = chr(limit[next]) #converts from ASCII to char
        next +=1
        return c
    else:
        return None

def my_getLine():
    global next
    global limit
    line = ""
    char = my_getChar()
    while(char != "" and char != None): # checks for character to append
        line+= char
        char = my_getChar()
    next = 0 #reset limit,next after line is finished
    limit = 0
    return line

def my_readLines():
    numLines = 0
    inLine = my_getLine()
    while len(inLine):
        numLines += 1
        printf(f"### Line {numLines}: <{str(inLine)}> ###\n")
        inLine = my_getLine()
        print(f"EOF after {numLines}\n")
        
    

def execute(args):
    #nothing to return
    if len(args) == 0:
        return
    #exit
        #directory change
    elif args[0] == "cd":
        try:
            #cd..
            if len(args) == 1:
                os.chdir("..")
            #move directory
            else:
                os.chdir(args[1])
        except:
            os.write(1, ("cd %s: No such file or directory" % args[1]).encode())
            pass
    #pipe begins
    elif "|" in args:
        pipe(args)
    else:
        rc = os.fork()
        background = True

        if "&" in args:
            args.remove("&")
            background = False
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            if "/" in args[0]:
                program = args[0]
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            elif ">" in args or "<" in args:
                redirection(args)
            else:
                for dir in re.split(":", os.environ['PATH']): #exhausted each directory in the path
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ) # attempt exec program
                    except FileNotFoundError:
                        pass
            os.write(2, ("command not found\n").encode())
            sys.exit(0)

        else:
            if background:
                #await child
                childpid = os.wait()

def pipe(args):
    left = args[0:args.index("|")]
    right = args[args.index("|") + 1:]
    pr, pw = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        os.close(1)
        os.dup(pw)
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)
        commands(left)
        os.write(2, ("Could not exec %s\n" % left[0]).encode())
        sys.exit(1)

    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0, True)
        for fd in (pr, pw):
            os.close(fd)
        if "|" in right:
            pipe(right)
            commands(right)
            os.write(2, ("Could not exec %s\n" % right[0]).encode())
            sys.exit(1)

                #redirection
def redirection(args):
    if '>' in args:
        os.close(1)
        os.open(args[args.index('>')+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        args.remove(args[args.index('>') + 1])
        args.remove('>')
    else:
        os.close(0)
        os.open(args[args.index('<')+ 1], os.O_RDONLY)
        os.set_inheritable(0, True)
        args.remove(args[args.index('<') + 1])
        args.remove('<')
    for dir in re.split(":", os.environ['PATH']): #exhuast directories in path
        prog = "%s%s" % (dir, args[0])
        try:
            os.execve(prog, args, os.environ) # attempt exec
        except FileNotFoundError:
            pass
        os.write(2, ("%s: commmand not found\n" % args[0]).encode())
        sys.exit(0)

def commands(args):
    if "/" in args[0]:
        program = args[0]
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    elif ">" in args or "<" in args:
        redirection(args)
    else:
        for dir in re.split(":", os.environ['PATH']): #exhaust directory path
            program = "%s%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # attempt exec
            except FIleNotFoundError:
                pass
    os.write(2, ("%s: command not found\n" % args[0]).encode())
    sys.exit(0)


while True:
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else: #PS1 var set to $
        os.write(1, ("$ ").encode())

    rawArgs = my_getLine()
    
    if len(rawArgs) == 0:
        break

    args = rawArgs.split() 

    if args[0].lower() == "exit":
        sys.exit(0)
        
    execute(args)
    
    
        
            
                
        
        
            
        













            
