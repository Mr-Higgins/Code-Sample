from os import system, name
import numpy as np
import random

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# To store the solution without worrying about overwriting.
class Solution(metaclass=Singleton):
    def __init__(self,d1,d2):
        self.dims = (d1,d2)
        self.matrix = np.zeros((d1,d2)).astype(int)
    
    def add(self,b):
        r,c = divmod(b,self.dims[0])
        self.matrix[r][c] += 1

# OS-dependent screen clear.
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Prevents repetition for printing if-cases.
def printpuzzle(d):
    if len(d) == 3:
        print3x3(d)
    elif len(d) == 4:
        print4x4(d)
    input()

def print3x3(d):
   print(str(d[0][0])+' '+str(d[0][1])+' '+str(d[0][2])+'\n'+
         str(d[1][0])+' '+str(d[1][1])+' '+str(d[1][2])+'\n'+
         str(d[2][0])+' '+str(d[2][1])+' '+str(d[2][2])+'\n')

def print4x4(d):
    print(str(d[0][0])+' '+str(d[0][1])+' '+str(d[0][2])+' '+str(d[0][3])+'\n'+
          str(d[1][0])+' '+str(d[1][1])+' '+str(d[1][2])+' '+str(d[1][3])+'\n'+
          str(d[2][0])+' '+str(d[2][1])+' '+str(d[2][2])+' '+str(d[2][3])+'\n'+
          str(d[3][0])+' '+str(d[3][1])+' '+str(d[3][2])+' '+str(d[3][3])+'\n')

# Minimizes repetition.
def printmoves(moves):
    print('Move '+str(moves)+'\n')

# Prints AND executes button push.
def pushprint(d,moves,b,v):
    d = pusharrow(d,b)
    moves += 1
    if v:
        printmoves(moves)
        printpuzzle(d)
    return (d,moves)

# All buttons adjacent (diagonal and cardinal) must be rotated with the pushed button.
def pusharrow(arrows,button):
    b=divmod(button,len(arrows))
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if b[0]+i >= 0 and b[1]+j >= 0:
                    arrows[b[0]+i][b[1]+j] = (arrows[b[0]+i][b[1]+j]+1)%4
            except IndexError:
                pass
    return arrows

# Checks if solved.
def solvecheck(d):
    solved = 1
    for i in range(0,len(d)):
        for j in range(0,len(d[i])):
            if d[i][j] != 0:
                solved = 0
                return solved
    return solved

# Solves bottom row.
def alignfirst(d,s,v):
    a = len(d)-1
    moves = 0
    while d[a][0] != d[a][1]:
        s.add(5*(a-1))
        d,moves = pushprint(d,moves,5*(a-1),v)
    while d[a][1] != d[a][2]:
        s.add((a+1)*a)
        d,moves = pushprint(d,moves,(a+1)*a,v)
    try:
        while d[a][2] != d[a][3]:
            s.add((a+1)*a+1)
            d,moves = pushprint(d,moves,(a+1)*a+1,v)
    except IndexError:
        pass
    return (d,moves)

# Solves all rows besides bottom and top, iteratively.
def alignrow(d,moves,rowscompleted,s,v):
    a = len(d)-rowscompleted-1
    while d[a][0] != d[a+1][0]:
        s.add((a-1)*len(d))
        d,moves = pushprint(d,moves,(a-1)*len(d),v)
    while d[a][0] != d[a][1]:
        s.add((a-1)*len(d)+2)
        d,moves = pushprint(d,moves,(a-1)*len(d)+2,v)
    while d[a][1] != d[a][2]:
        s.add((a-1)*len(d))
        d,moves = pushprint(d,moves,(a-1)*len(d),v)
    try:
        while d[a][2] != d[a][3]:
            s.add((a-1)*len(d)+1)
            d,moves = pushprint(d,moves,(a-1)*len(d)+1,v)
    except IndexError:
        pass
    diff = (d[a+1][0]-d[a][0])%4
    if len(d) % 3 == 0:
        print('Yes?\n')
        pos = 1
        while pos < len(d):
            print('YES?\n')
            for i in range(0,diff):
                print('YES?!\n')
                s.add((a-1)*len(d)+pos)
                d,moves = pushprint(d,moves,(a-1)*len(d)+pos,v)
            pos += 3
    elif len(d) % 3 == 1:
        pos = 0
        while pos < len(d):
            for i in range(0,diff):
                s.add((a-1)*len(d)+pos)
                d,moves = pushprint(d,moves,(a-1)*len(d)+pos,v)
            pos += 3
    else:
        pos = 0
        while pos < len(d):
            for i in range(0,diff):
                s.add((a-1)*len(d)+pos)
                d,moves = pushprint(d,moves,(a-1)*len(d)+pos,v)
            pos += 3
        for i in range(0,diff):
            s.add((a-1)*len(d)+pos)
            d,moves = pushprint(d,moves,(a-1)*len(d)+pos,v)
    return (d,moves)

# Solves final row.
def alignlast(d,moves,s,v):
    dim = len(d)
    diff = (d[0][0]-d[1][0])%4
    if diff:
        if dim == 3:
            for i in range(0,diff):
                s.add(7)
                d,moves = pushprint(d,moves,7,v)
        elif dim == 4:
            for i in range(0,diff):
                s.add(8)
                s.add(11)
                d,moves = pushprint(d,moves,8,v)
                d,moves = pushprint(d,moves,11,v)
    diff = (d[0][1]-d[0][0])%4
    cdiff = (4-diff)%4
    if diff:
        if dim == 3:
            for i in range(0,diff):
                s.add(8)
                s.add(5)
                d,moves = pushprint(d,moves,8,v)
                d,moves = pushprint(d,moves,5,v)
        elif dim == 4:
            for i in range(0,diff):
                s.add(3)
                s.add(8)
                s.add(15)
                s.add(10)
                d,moves = pushprint(d,moves,3,v)
                d,moves = pushprint(d,moves,8,v)
                d,moves = pushprint(d,moves,15,v)
                d,moves = pushprint(d,moves,10,v)
            for i in range(0,cdiff):
                s.add(8)
                s.add(11)
                s.add(2)
                s.add(14)
                s.add(10)
                d,moves = pushprint(d,moves,8,v)
                d,moves = pushprint(d,moves,11,v)
                d,moves = pushprint(d,moves,2,v)
                d,moves = pushprint(d,moves,14,v)
                d,moves = pushprint(d,moves,10,v)
    diff = (d[0][2]-d[0][1])%4
    cdiff = 4-diff
    if diff:
        if dim == 3:
            for i in range(0,diff):
                s.add(3)
                s.add(7)
                d,moves = pushprint(d,moves,3,v)
                d,moves = pushprint(d,moves,7,v)
            for i in range(0,cdiff):
                s.add(6)
                d,moves = pushprint(d,moves,6,v)
        if dim == 4:
            for i in range(0,diff):
                s.add(0)
                s.add(12)
                s.add(11)
                d,moves = pushprint(d,moves,0,v)
                d,moves = pushprint(d,moves,12,v)
                d,moves = pushprint(d,moves,11,v)
    try:
        diff = (d[0][3]-d[0][2])%4
        cdiff = 4-diff
        if diff:
            if dim == 4:
                for i in range(0,diff):
                    s.add(1)
                    s.add(13)
                    s.add(8)
                    s.add(11)
                    d,moves = pushprint(d,moves,1,v)
                    d,moves = pushprint(d,moves,13,v)
                    d,moves = pushprint(d,moves,8,v)
                    d,moves = pushprint(d,moves,11,v)
                for i in range(0,cdiff):
                    s.add(9)
                    d,moves = pushprint(d,moves,9,v)
    except IndexError:
        pass
    return (d,moves)

# Makes all arrows face up (per the solution requirement).
def faceup(d,moves,s,v=0):
    sol = lambda x: x%4
    dim = len(d)
    c = 4-d[0][0]
    for i in range(0,c):
        if dim == 3:
            s.add(4)
            d,moves = pushprint(d,moves,4,v)
        elif dim == 4:
            s.add(0)
            s.add(3)
            s.add(12)
            s.add(15)
            d,moves = pushprint(d,moves,0,v)
            d,moves = pushprint(d,moves,3,v)
            d,moves = pushprint(d,moves,12,v)
            d,moves = pushprint(d,moves,15,v)
    print('Your solution can be achieved with the following presses:\n')
    print(sol(s.matrix))
p = 0
while not p:
    try:
        p = int(input('What type of Arrow Puzzle?\n(1) 3x3 Random (2) 4x4 Random (3) 3x3 Specific (4) 4x4 Specific\n'))
    except ValueError:
        print('Incorrect entry, plesae try again.\n')
clear()
if p == 1:
    d = np.random.randint(4,size=(3,3))
elif p == 2:
    d = np.random.randint(4,size=(4,4))
elif p == 3:
    d = np.zeros((3,3)).astype(int)
    it = 0
    while it < 9:
        print3x3(d)
        r = divmod(it,3)
        inp = input('Please input the value for row ' + str(r[0]+1) + ' column ' + str(r[1]+1) + '. 0 or 4 is up, 1 is right, 2 is down, 3 is left.\n'+
            ' Input is modulo 4. Use the - key to overwrite past entries.\n')
        try:
            if inp == '-' and it > 0:
                it -= 1
            elif 0 <= int(inp)%4 <= 3:
                d[r[0]][r[1]] = int(inp)%4
                it += 1
            clear()
        except ValueError:
            clear()
            print('Incorrect entry, please try again.\n')
elif p == 4:
    d = np.zeros((4,4))
    d = d.astype(int)
    it = 0
    while it < 16:
        print4x4(d)
        r = divmod(it,4)
        inp = input('Please input the value for row ' + str(r[0]+1) + ' column ' + str(r[1]+1) + '. 0 is up, 1 is right, 2 is down, 3 is left.\n'+
            ' Input is modulo 4. Use the - key to overwrite past entries.\n')
        try:
            if inp == '-' and it > 0:
                it -= 1
            elif 0 <= int(inp)%4 <= 3:
                d[r[0]][r[1]] = int(inp)%4
                it += 1
            clear()
        except ValueError:
            clear()
            print('Incorrect entry, please try again.\n')
else:
    print('Please choose a correct option.')
    quit()
print('Press enter to begin.\n')
c = 0
while c != 1 and c != 2:
    printpuzzle(d)
    c = int(input('Play or solve?\n(1) Play (2) Solve (3) Verbose Solution\n'))
moves = 0
solved = solvecheck(d)
if c == 1:
    while not solved:
        clear()
        print('Moves: '+str(moves)+'\n')
        if p == 1 or p == 3:
            print3x3(d)
            d = pusharrow(d,int(input('Buttons represented by 0-8, reading order.\n')))
            moves += 1
            solved = solvecheck(d)
        elif p == 2 or p == 4:
            print4x4(d)
            d = pusharrow(d,int(input('Buttons represented by 0-15, reading order.\n')))
            moves += 1
            solved = solvecheck(d)
    clear()
    print('Solved in '+str(moves)+' moves.\n')
elif c == 2 or c == 3:
    v = c-2
    s = Solution(len(d),len(d[0]))
    rowscompleted = 1
    solved = solvecheck(d)
    if v:
        print('Aligning Row '+str(len(d))+'.\n')
    d,moves = alignfirst(d,s,v)
    while not solved and rowscompleted < len(d)-1:
        if v:
            print('Aligning Row '+str(len(d)-rowscompleted)+'.\n')
        d,moves = alignrow(d,moves,rowscompleted,s,v)
        rowscompleted += 1
    if v:
        print('Aligning Row 1.\n')
    d,moves = alignlast(d,moves,s,v)
    if v:
        print('Aligning all arrows up.\n')
    faceup(d,moves,s,v)
else:
    print('Please choose a correct option.')
