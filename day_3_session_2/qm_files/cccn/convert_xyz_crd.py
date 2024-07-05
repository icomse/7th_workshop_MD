import numpy
import argparse

# define arguments to be parsed
parser = argparse.ArgumentParser(prog = 'convert_xyz_crd.py', description = 'Convert Orca XYZ traj files to CHARMM CRD files')
parser.add_argument('xyz_trajectory', type = str)
parser.add_argument('str_file', type = str)
parser.add_argument('n_scan_points', type = int)
parser.add_argument('init_scan_point', type = float)
parser.add_argument('stride', type = float)
parser.add_argument('dihedral', type = str)

# parse the arguments
args = parser.parse_args()

# class to hold coordinate information
class Molecule:
    def __init__(self, atoms: list[str], coords: list[list[float]], phi: float, dihedral: str, residue: str) -> None:
        self.atom_names     = atoms
        self.atom_coords    = numpy.array(coords)
        self.phi            = phi
        self.dihedral       = dihedral
        self.residue        = resname

    @property
    def get_coords(self):
        curr_coords = {}
        for atom, coord in zip(self.atom_names, self.atom_coords):
            curr_coords[atom]   = coord
        return curr_coords

    @property
    def get_pdb(self):
        curr_coords = self.get_coords
        atom_index  = 1
        with open(f"scan_{self.dihedral}.{round(self.phi)}.pdb","w") as pdb_object:
            for atom in curr_coords:
                pdb_object.write("{:<6s}{:5.0f}{:>4s}{:>5s}{:>2s}{:4.0f}{:12.3f}{:8.3f}{:8.3f}\n".format("ATOM", atom_index, atom, self.residue, "C", 1, curr_coords[atom][0], curr_coords[atom][1], curr_coords[atom][2]))
                atom_index  = atom_index + 1
            pdb_object.write("END\n")

    @property
    def get_crd(self):
        pass

# build the molecule
with open(args.str_file) as str_object, open(args.xyz_trajectory) as traj_object:
    str_data    = str_object.readlines()
    atom_names  = []
    resname     = None
    for line in str_data:
        if "ATOM" in line:
            atom_names.append(line.strip().split()[1])  # append the atom names
        if "RESI" in line:
            resname = line.split()[1]

    n_atoms     = len(atom_names)
    traj_data   = traj_object.readlines()
    traj_coords = [traj_data[curr*(n_atoms+2):(curr+1)*(n_atoms+2)] for curr in range(0, args.n_scan_points)]
#    traj_coords = [(curr*(n_atoms+3),(curr+1)*(n_atoms+3)) for curr in range(0, args.n_scan_points)]
    traj_points = numpy.arange(start = args.init_scan_point, stop = args.init_scan_point + (args.n_scan_points * args.stride), step = args.stride)
    traj_frames = []
#    print(traj_coords)

    for coord_data, phi in zip(traj_coords, traj_points):
        curr_frame  = coord_data[2:]
        curr_coords = []
        for line in curr_frame:
            print(line.strip())
            curr_coords.append([float(coord) for coord in line.split()[1:]])
        traj_frames.append(Molecule(atoms = atom_names, coords = curr_coords, phi = phi, dihedral = args.dihedral, residue = resname))
        print("\n")
    
    for frame in traj_frames:
        frame.get_pdb
