#import and open file
import numpy as np
import linecache


#Counting Lines https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def number_of_lines():
    file = open(args.xyz, "r")
    num_lines = sum(1 for line in open(args.xyz))
    return num_lines

#finding line number of Empirical Formula:
def empiricalformula():
    file = open(args.xyz, "r")
    lookup = 'Empirical Formula:'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                EF = num
    return EF

#finding line number of BOND ORDERS AND VALENCIES
def Start_of_Bonds():
    file = open(args.xyz, "r")
    lookup = 'BOND ORDERS AND VALENCIES'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                StartLine = num      
    return StartLine
          

#find line number of CARTESIAN COORDINATES
def Start_of_Atoms():
    file = open(args.xyz, "r")
    lookup = 'CARTESIAN COORDINATES'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                print ('found at line:', num)
                StartAtoms = num
            
#making matrix
def Matrix():
    count = 0
    for x in range(StartLine+1,num_lines,1):
        line = linecache.getline(args.xyz, x)
        words = line.split()
        if len(words) > 2:
            try:
                words2 = float(words[2])
            except ValueError:
                words2 = 'NaN'
            check = words[2].replace('.','',1)
            if check.isdigit() == True:
                for i in range(2,len(words),1):
                    row = int(words[1])-1
                    column = int((i-2)+(6*count))
                    Atoms_Matrix[row,column] = float(words[i])
                    if words[1] == Atoms:
                        count = count + 1
    return Atoms_Matrix

#Making the bonds array
def Bond_array():       
    bonds = []
    for r in range(0,Atoms,1):
        for c in range(0,Atoms,1):
            if r==c:
                continue
            elif Atoms_Matrix[r,c] < 0.85:
                Matrix[r,c] = int(0)
            elif Atoms_Matrix[r,c] >= 0.85 and Atoms_Matrix[r,c] < 1.5:
                Matrix[r,c] = int(1)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,1))
                else:
                    bonds.append((co,ro,1))
            elif Atoms_Matrix[r,c] >= 1.5 and Atoms_Matrix[r,c] < 2.5:
                Matrix[r,c] = int(2)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,2))
                else:
                    bonds.append((co,ro,2))
            elif Atoms_Matrix[r,c] >= 2.5 and Atoms_Matrix[r,c] < 3.5:
                Matrix[r,c] = int(3)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,3))
                else:
                    bonds.append((co,ro,3))
            elif Atoms_Matrix[r,c] >= 3.5:
                Matrix[r,c] = int(0)
    return bonds

#Matrix used for writing the file
def Atom_Symbol():
    AtomSymbol = []
    for y in range(0,Atoms,1):
        line_Coor = linecache.getline(args.xyz, y+StartAtoms+2)
        words_Coor = line_Coor.split()
        AtomSymbol.append(words_Coor[1])
        for z in range(0,3,1):
            Final[1+y,1+z] = float(words_Coor[z+2])
        for padding in range(5,17,1):
            Final[1+y,padding] = 0
    return Final


#Writing the file
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('xyz', metavar='xyz_filename', type=str, help='pos dependent argument')
    parser.add_argument('-m', '--normal', action='store_true', help='some usage of logical')

    args = parser.parse_args()


    if args.normal:
        print ("this the 'normal' mode")
    else:
        print ("other mode or wahtever")

    print (args.xyz)

    output = readfile(args.xyz)
    
    f = open(args.sdf,"w+")
    f.write("%3.0f%3.0f%3.0f   %3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f V2000\n" % (Atoms,len(bonds),0,0,0,0,0,0,0,999))
    for i in range(1,Atoms+1,1):
        f.write("%10.4f%10.4f%10.4f %3s%2.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f\n" % (Final[i,1],Final[i,2],Final[i,3],"{:<3s}".format(AtomSymbol[i-1]),0,0,0,0,0,0,0,0,0,0,0,0))
    for x, y, z in bonds:
        f.write("%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f\n" % (x,y,z,0,0,0,0))


if __name__ == '__main__':
    main()