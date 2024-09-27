import py3Dmol
from mofstructure import mofdeconstructor
from ase.data import chemical_symbols, covalent_radii

# Standard colors for atoms
# ATOM_COLORS = {
#     'H': 'white', 'C': 'gray', 'N': 'blue', 'O': 'red', 'F': 'green', 'Cl': 'green',
#     'Br': 'brown', 'I': 'purple', 'P': 'orange', 'S': 'yellow', 'B': 'salmon',
#     'Li': 'purple', 'Na': 'purple', 'K': 'purple', 'Ca': 'gray', 'Fe': 'orange', 'X': 'black'
# }
ATOM_COLORS = {
    'H': '#FFFFFF',   # White
    'He': '#D9FFFF',  # Pale cyan
    'Li': '#CC80FF',  # Pale violet
    'Be': '#C2FF00',  # Bright lime
    'B': '#FFB5B5',   # Light pink
    'C': '#909090',   # Dark gray
    'N': '#3050F8',   # Blue
    'O': '#FF0D0D',   # Red
    'F': '#90E050',   # Bright green
    'Ne': '#B3E3F5',  # Cyan
    'Na': '#AB5CF2',  # Purple
    'Mg': '#8AFF00',  # Bright green
    'Al': '#BFA6A6',  # Light gray
    'Si': '#F0C8A0',  # Pale orange
    'P': '#FF8000',   # Orange
    'S': '#FFFF30',   # Yellow
    'Cl': '#1FF01F',  # Bright green
    'Ar': '#80D1E3',  # Pale blue
    'K': '#8F40D4',   # Purple
    'Ca': '#3DFF00',  # Bright green
    'Sc': '#E6E6E6',  # Light gray
    'Ti': '#BFC2C7',  # Gray
    'V': '#A6A6AB',   # Medium gray
    'Cr': '#8A99C7',  # Blue-gray
    'Mn': '#9C7AC7',  # Violet
    'Fe': '#E06633',  # Orange-brown
    'Co': '#F090A0',  # Pink
    'Ni': '#50D050',  # Bright green
    'Cu': '#C88033',  # Copper
    'Zn': '#7D80B0',  # Blue-gray
    'Ga': '#C28F8F',  # Pink-brown
    'Ge': '#668F8F',  # Gray-blue
    'As': '#BD80E3',  # Purple
    'Se': '#FFA100',  # Orange
    'Br': '#A62929',  # Dark red
    'Kr': '#5CB8D1',  # Light blue
    'Rb': '#702EB0',  # Dark purple
    'Sr': '#00FF00',  # Green
    'Y': '#94FFFF',   # Pale blue
    'Zr': '#94E0E0',  # Pale blue
    'Nb': '#73C2C9',  # Blue-green
    'Mo': '#54B5B5',  # Blue-green
    'Tc': '#3B9E9E',  # Dark cyan
    'Ru': '#248F8F',  # Dark cyan
    'Rh': '#0A7D8C',  # Dark cyan
    'Pd': '#006985',  # Blue
    'Ag': '#C0C0C0',  # Silver
    'Cd': '#FFD98F',  # Pale yellow
    'In': '#A67573',  # Light brown
    'Sn': '#668080',  # Gray
    'Sb': '#9E63B5',  # Purple
    'Te': '#D47A00',  # Brown
    'I': '#940094',   # Dark purple
    'Xe': '#429EB0',  # Blue-green
    'Cs': '#57178F',  # Dark purple
    'Ba': '#00C900',  # Green
    'La': '#70D4FF',  # Pale blue
    'Ce': '#FFFFC7',  # Very pale yellow
    'Pr': '#D9FFC7',  # Very pale green
    'Nd': '#C7FFC7',  # Pale green
    'Pm': '#A3FFC7',  # Pale green
    'Sm': '#8FFFC7',  # Pale green
    'Eu': '#61FFC7',  # Pale green
    'Gd': '#45FFC7',  # Pale green
    'Tb': '#30FFC7',  # Pale green
    'Dy': '#1FFFC7',  # Pale green
    'Ho': '#00FF9C',  # Green
    'Er': '#00E675',  # Green
    'Tm': '#00D452',  # Green
    'Yb': '#00BF38',  # Green
    'Lu': '#00AB24',  # Dark green
    'Hf': '#4DC2FF',  # Light blue
    'Ta': '#4DA6FF',  # Light blue
    'W': '#2194D6',   # Blue
    'Re': '#267DAB',  # Blue
    'Os': '#266696',  # Blue
    'Ir': '#175487',  # Dark blue
    'Pt': '#D0D0E0',  # Pale gray
    'Au': '#FFD123',  # Gold
    'Hg': '#B8B8D0',  # Gray
    'Tl': '#A6544D',  # Brown
    'Pb': '#575961',  # Dark gray
    'Bi': '#9E4FB5',  # Purple
    'Po': '#AB5C00',  # Brown
    'At': '#754F45',  # Dark brown
    'Rn': '#428296',  # Blue-green
    'Fr': '#420066',  # Dark purple
    'Ra': '#007D00',  # Dark green
    'Ac': '#70ABFA',  # Pale blue
    'Th': '#00BAFF',  # Light blue
    'Pa': '#00A1FF',  # Blue
    'U': '#008FFF',   # Blue
    'Np': '#0080FF',  # Blue
    'Pu': '#006BFF',  # Blue
    'Am': '#545CF2',  # Blue
    'Cm': '#785CE3',  # Blue-violet
    'Bk': '#8A4FE3',  # Purple
    'Cf': '#A136D4',  # Purple
    'Es': '#B31FD4',  # Purple
    'Fm': '#B31FBA',  # Purple
    'Md': '#B30DA6',  # Purple
    'No': '#BD0D87',  # Purple
    'Lr': '#C70066',  # Dark pink
    'Rf': '#CC0059',  # Dark pink
    'Db': '#D1004F',  # Dark pink
    'Sg': '#D90045',  # Dark pink
    'Bh': '#E00038',  # Dark pink
    'Hs': '#E6002E',  # Dark pink
    'Mt': '#EB0026',  # Dark pink
    'X': 'black'
}


def structure_visualizer(structure, tolerance=0.3):
    structure = mofdeconstructor.wrap_systems_in_unit_cell(structure, 20)
    xyz = structure.get_positions()
    symbols = structure.get_chemical_symbols()
    viewer = py3Dmol.view(width=800, height=600)

    # Add atoms as spheres to the viewer
    for i, atom in enumerate(symbols):
        viewer.addSphere({
            'center': {'x': xyz[i][0], 'y': xyz[i][1], 'z': xyz[i][2]},
            'radius': 0.5,
            'color': ATOM_COLORS.get(atom, 'white')
        })

    # Add bonds based on interatomic distances
    distance = structure.get_all_distances()
    num_atoms = len(symbols)
    for i in range(num_atoms):
        for j in range(i + 1, num_atoms):
            dist = distance[[i], [j]]
            bond_threshold = covalent_radii[chemical_symbols.index(symbols[i])] + \
                covalent_radii[chemical_symbols.index(symbols[j])] + tolerance

            if dist < bond_threshold:
                start = xyz[i]
                end = xyz[j]
                viewer.addCylinder({
                    'start': {'x': start[0], 'y': start[1], 'z': start[2]},
                    'end': {'x': end[0], 'y': end[1], 'z': end[2]},
                    'radius': 0.1,
                    'color': 'gray'
                })

    viewer.zoomTo()
    return viewer


