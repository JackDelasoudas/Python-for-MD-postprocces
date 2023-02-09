import MDAnalysis as mda
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox

# Atomic Van der Waals distances:
# Carbon (type 1 & 2) : 1.70 Å
# Oxygen (type 3) : 1.52 Å
# Hydrogen (type 4 & 5) : 1.20 Å
# Nitrogen (type 6) : 1.55 Å
# NOTE ALL DISTANCES IN ANGSTROM and ATOM COUNT STARTS FROM 0

# Van der Waals distances for different atom types
start = time.time()

#Browse Topology File
root = tk.Tk()
root.withdraw() # hide the main window

messagebox.showinfo("Topology", "Please select topology file file (.data)")
topology = filedialog.askopenfilename()

#Browse Trajectory File
root = tk.Tk()
root.withdraw() # hide the main window

messagebox.showinfo("Trajectory", "Please select trajectory file file (.lammpstrj)")
trajectory = filedialog.askopenfilename()

vvd = {
    "1": 1.70, 
    "2": 1.70, 
    "3": 1.52, 
    "4": 1.20, 
    "5": 1.20, 
    "6": 1.55
}

# Load universe
u = mda.Universe(topology, 
                 trajectory, 
                 format="LAMMPSDUMP", guess_bonds=True, vdwradii=vvd)

# Select Carbon atoms
C_atoms = u.select_atoms("type 1", "type 2")
C_bonds = C_atoms.bonds

# Create a list to store bond lengths for each time step
traj_C_bonds = []
max_bond_length = 0
max_bond = None

# Iterate over time steps
for ts in tqdm(u.trajectory):
    #bond_lengths = [bond.length() for bond in C_bonds]
    bond_lengths = []
    for bond in C_bonds:
        bl = bond.length()
        bond_lengths.append(bl)

        if bl > max_bond_length:
             max_bond_length = bl
             max_bond = bond
             frame = ts

    traj_C_bonds.append(bond_lengths)

# # Iterate over time steps
# for ts in u.trajectory:
#     #bond_lengths = [bond.length() for bond in C_bonds]

#     for bond in C_bonds:
#         bond_lengths = bond.length()

#         if bond_lengths > max_bond_length:
#             max_bond_length = bond_lengths
#             max_bond = bond

#         traj_C_bonds.append(bond_lengths)

# Flatten the data and plot the histogram
flattened_data = [item for sublist in traj_C_bonds for item in sublist]
plt.hist(flattened_data, bins=400, range=(0.7, 1.7), alpha=0.7, color='blue')

plt.xlabel("Bond Length (Å)")
plt.ylabel("Frequency")
plt.title("Nitrogen Bond Distribution Histogram over timesteps")
#plt.show()

path2hist = filedialog.askdirectory()
plt.savefig(path2hist + '/histogram.png', dpi=600)

print("Calculation time: {:.2f} seconds".format(time.time() - start))

print("\nMaximum bond lengh during the simulation is {:.2f}".format(max_bond_length))
print("\nThe bond id is: ", max_bond)
print("\n In the frame {}".format(frame))