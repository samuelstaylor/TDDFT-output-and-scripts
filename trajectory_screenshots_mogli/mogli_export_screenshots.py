"""
Example for exporting a molecule to an HTML5 file using mogli
"""
from mogli import mogli

# Visual settings 
mogli.ATOM_RADII += .2          # the size of the atoms
mogli.BOND_RADIUS = .175        # the girth of the visual bond
mogli.BOND_GRAY_SHADE = .35     # the color of the bond

# settings

elements = {6 : "C",
            1:  "H"}

def determine_bonds(all_molecules, r_num):
    print_string = ""
    
    for molecules in all_molecules:
        bonds_string = ""
        atomic_numbers = molecules[0].atomic_numbers
        index_pairs = (molecules[0].bonds.index_pairs).tolist()
        bonds = []
        if (len(r_num) > 0):
            r = r_num[0]

        for pair in index_pairs:
            if len(bonds) == 0:
                bonds.append(pair)
            else:
                index1 = pair[0]
                index2 = pair[1]
                added = False
                for bond in bonds:
                    if (index1 in bond) and (not (index2 in bond)):
                        bond.append(index2)
                        added = True
                    if (index2 in bond) and (not (index1 in bond)):
                        bond.append(index2)
                        added = True
                if (not added):
                    bonds.append(pair)

        atomic_number_bonds = []
        for bond in bonds:
            bond.sort()
            atomic_number_bond = []
            for index in bond:
                atomic_number_bond.append(atomic_numbers[index])
            atomic_number_bonds.append(atomic_number_bond)
            
        for bond in atomic_number_bonds:
            num_carbon = 0
            num_hydrogen = 0
            num_carbon = bond.count(6)
            num_hydrogen = bond.count(1)
            if (num_carbon == 1):
                bonds_string += elements[6]
            elif (num_carbon != 0):
                bonds_string += elements[6] + str(num_carbon)
            if (num_hydrogen == 1):
                bonds_string += elements[1]         
            elif (num_hydrogen != 0):
                bonds_string += elements[1] + str(num_hydrogen) 
            if (num_carbon != 0) and (num_hydrogen != 0):
                bonds_string += ", "
        print_string += "r" + str(r) + ": \t" + bonds_string[:-2] + "\t" + str(index_pairs)
        print_string += "\n"
        r_num.pop(0)

    with open("results.csv", "w") as f:
        
        f.write(print_string)
        f.close()
    if (len(r_num) != 0):
        r = r_num[0]
    

def main():
    all_molecules = []
    r_num = []
    start = 36
    end = 83
    for r_val in range(start, end+1): #(-1, 84)
        r_num.append(r_val)
        molecules = mogli.read(f'C4H10/kinked/lframe_traj/traj_last_frame_r{r_val}.xyz')
        print("Finished:", r_val)
        mogli.export(molecules[0], f'C4H10/kinked/lframe_image/C4H10r{r_val}.png', width=1920, height=1080,
                    bonds_param=1.8, camera=((0, 0, 75), #bonds param = 1.8 seems to produce most accurate results
                                            (0, 0, 0),
                                            (0, 1, 0)))
        
        all_molecules.append(molecules)    
    determine_bonds(all_molecules, r_num)
        
    print("Finished exporting trajectory images.")
    
if __name__ == "__main__":
    main()
