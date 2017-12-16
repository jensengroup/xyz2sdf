#import and open file
import numpy as np
import linecache


#Counting Lines https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def number_of_lines():
    file = open(args.out, "r")
    num_lines = sum(1 for line in open(args.out))
    return num_lines

#finding line number of Empirical Formula:
def empiricalformula():
    file = open(args.out,"r")
    lookup = 'Empirical Formula:'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            ef = num
    return ef

#finding line number of BOND ORDERS AND VALENCIES
def start_of_bonds():
    file = open(args.out, "r")
    lookup = 'BOND ORDERS AND VALENCIES'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                startline = num      
    return startline
          

#find line number of CARTESIAN coorDINATES
def start_of_atoms():
    file = open(args.out, "r")
    lookup = 'CARTESIAN COORDINATES'
    with file as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                print ('found at line:', num)
                startatoms = num
    return startatoms
            
#making matrix
def matrix_f():
    count = 0
    for x in range(startline+1,num_lines,1):
        line = linecache.getline(args.out, x)
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
                    atoms_matrix[row,column] = float(words[i])
                    if words[1] == atoms:
                        count = count + 1
    return atoms_matrix

#Making the bonds array
def bond_array():       
    bonds = []
    for r in range(0,atoms,1):
        for c in range(0,atoms,1):
            if r==c:
                continue
            elif atoms_matrix[r,c] < 0.85:
                matrix[r,c] = int(0)
            elif atoms_matrix[r,c] >= 0.85 and atoms_matrix[r,c] < 1.5:
                matrix[r,c] = int(1)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,1))
                else:
                    bonds.append((co,ro,1))
            elif atoms_matrix[r,c] >= 1.5 and atoms_matrix[r,c] < 2.5:
                matrix[r,c] = int(2)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,2))
                else:
                    bonds.append((co,ro,2))
            elif atoms_matrix[r,c] >= 2.5 and atoms_matrix[r,c] < 3.5:
                matrix[r,c] = int(3)
                ro = r+1
                co = c+1
                if co > ro:
                    bonds.append((ro,co,3))
                else:
                    bonds.append((co,ro,3))
            elif atoms_matrix[r,c] >= 3.5:
                matrix[r,c] = int(0)
    return bonds

#matrix used for writing the file
def atom_symbol():
    atomsymbol = []
    for y in range(0,atoms,1):
        line_coor = linecache.getline(args.out, y+startatoms+2)
        words_coor = line_coor.split()
        atomsymbol.append(words_coor[1])
        for z in range(0,3,1):
            final[1+y,1+z] = float(words_coor[z+2])
        for padding in range(5,17,1):
            final[1+y,padding] = 0
    return final


#Writing the file
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('out', metavar='xyz_filename', type=str, help='pos dependent argument')
    parser.add_argument('-m', '--normal', action='store_true', help='some usage of logical')

    args = parser.parse_args()


    if args.normal:
        print ("this the 'normal' mode")
    else:
        print ("other mode or wahtever")

    print (args.out)

    output = readfile(args.out)

    num_lines = number_of_lines():

    ef = empiricalformula():

    line_ef = linecache.getline(arg.out, ef)
    words_ef = line_ef.split()
    atoms = int(words_ef[-2])
    atoms_matrix = np.zeros((atoms,atoms))
    matrix = np.zeros((atoms,atoms))

    startline = start_of_bonds():

    startatoms = start_of_atoms():

    atoms_matrix = matrix_f():

    bonds = bond_array():       

    final = atom_symbol():

    f = open(args.sdf,"w+")
    f.write("%3.0f%3.0f%3.0f   %3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f V2000\n" % (atoms,len(bonds),0,0,0,0,0,0,0,999))
    for i in range(1,atoms+1,1):
        f.write("%10.4f%10.4f%10.4f %3s%2.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f\n" % (final[i,1],final[i,2],final[i,3],"{:<3s}".format(atomsymbol[i-1]),0,0,0,0,0,0,0,0,0,0,0,0))
    for x, y, z in bonds:
        f.write("%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f\n" % (x,y,z,0,0,0,0))


if __name__ == '__main__':
    main()