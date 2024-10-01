# import os
from io import BytesIO, StringIO
import streamlit as st
from ase.io import read, write
from stmol import showmol
from ase.data import chemical_symbols, covalent_radii
from mofstructure import mofdeconstructor
from mofstructure.porosity import zeo_calculation
import mofstructure.filetyper as read_write
import pandas as pd
from fairmofapp.loader import visualizer



@st.cache_resource
def load_image(image_path):
    return image_path

def visualize_structure(ase_atom):
    return visualizer.structure_visualizer(ase_atom)


def remove_guest(ase_atom):
    index_non_guest = mofdeconstructor.remove_unbound_guest(ase_atom)
    return ase_atom[index_non_guest]


def compute_porosity(_ase_atom, probe_radius=1.86, number_of_steps=10000):
    return zeo_calculation(_ase_atom, probe_radius, number_of_steps)


def sbu_data(_ase_atom):
    connected_components, atoms_indices_at_breaking_point, porpyrin_checker, all_regions = mofdeconstructor.secondary_building_units(
        _ase_atom)
    metal_sbus, organic_sbus, _ = mofdeconstructor.find_unique_building_units(
        connected_components, atoms_indices_at_breaking_point, _ase_atom, porpyrin_checker, all_regions, cheminfo=True, add_dummy=True)
    return metal_sbus, organic_sbus


def organic_ligand_data(_ase_atom):
    connected_components, atoms_indices_at_breaking_point, porpyrin_checker, all_regions = mofdeconstructor.ligands_and_metal_clusters(
        _ase_atom)
    metal_cluster, organic_ligands, _ = mofdeconstructor.find_unique_building_units(
        connected_components, atoms_indices_at_breaking_point, _ase_atom, porpyrin_checker, all_regions, cheminfo=True)
    return metal_cluster, organic_ligands


def inter_atomic_distance_check(ase_atom):
    valid = True
    distances = ase_atom.get_all_distances(mic=True)
    for i in range(len(distances)):
        if ase_atom[i].symbol != 'H':
            for j in range(len(distances[i])):
                if i != j and distances[i, j] < 0.90:
                    valid = False
                    break
    return valid


def display_metal_sbu(metals):
    list_to_display = ['inchikey', 'smi', 'sbu_type']
    data_key = {'inchikey':'InChIKey', 'smi':'SMILES', 'sbu_type':'SBU type', 'point_of_extension':'SBU coordination number'}
    for keys in list_to_display:
        if keys in metals.info:
            st.write(f"{data_key[keys]}: {metals.info[keys]}")

    return


def download_sbu_file(sbu, format="xyz"):
    sbu_file = StringIO()
    write(sbu_file, sbu, format=format)
    sbu_file.seek(0)
    return sbu_file.getvalue().encode('utf-8')


st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<h1 class="centered-title">MOF Structure Processing</h1>',
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CIF file", type="cif")

if uploaded_file is not None:
    ase_atom = read(uploaded_file, format='cif')
    st.subheader("Original Structures")
    viewer = visualize_structure(ase_atom)
    showmol(viewer, height=500, width=800)

    if not inter_atomic_distance_check(ase_atom):
        st.warning("There are overlapping atoms detected in this structure.")

    if st.checkbox("Remove guest molecules"):
        ase_atom = remove_guest(ase_atom)
        st.subheader("Structure after removing guests")
        viewer = visualize_structure(ase_atom)
        showmol(viewer, height=500, width=800)

        cif_buffer = BytesIO()
        write(cif_buffer, ase_atom, format="cif")
        st.download_button(
            label="Download Guest Removed Structure (CIF)",
            data=cif_buffer.getvalue(),
            file_name="guest_removed_structure.cif",
            mime="chemical/x-cif"
        )

    if st.checkbox("Compute porosity"):
        porosity = compute_porosity(ase_atom)

        porosity_renamed = {
            "AV_Volume_fraction": "Void Fraction",
            "AV_A^3": "Accessible Volume (Å³)",
            "ASA_A^2": "Accessible Surface Area (Å²)",
            "ASA_m^2/cm^3": "Accessible Surface Areas (m²/cm³)",
            "Number_of_channels": "Number of Channels",
            "LCD_A": "Largest Cavity Diameter (Å)",
            "lfpd_A": "Largest Free Sphere (Å)",
            "PLD_A": "Pore Limiting Diameter (Å)"
        }

        porosity = {porosity_renamed.get(k, k): v for k, v in porosity.items()}

        porosity_df = pd.DataFrame(porosity.items(), columns=["Metric", "Value"])

        styled_table = porosity_df.style.set_table_styles(
            [
                {'selector': 'thead th', 'props': [('background-color', '#333333'), ('color', 'white'), ('text-align', 'center')]},
                {'selector': 'tbody td', 'props': [('text-align', 'center'), ('border', '1px solid white'), ('color', 'white')]},
                {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#444444')]},
                {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#222222')]}
            ]
        ).set_properties(**{'font-size': '14px', 'font-family': 'Arial', 'border-collapse': 'collapse'})

        st.markdown("""
            <style>
            .center-table {
                display: flex;
                justify-content: center;
            }
            </style>
        """, unsafe_allow_html=True)

        st.write('<div class="center-table">', unsafe_allow_html=True)
        st.write("Porosity Results:")
        st.write(styled_table.to_html(), unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)

        porosity_csv = porosity_df.to_csv(index=False)
        st.download_button(
            label="Download Porosity Data (CSV)",
            data=porosity_csv,
            file_name="porosity_results.csv",
            mime="text/csv"
        )


    if st.checkbox("Deconstruct into SBUs"):
        metal_sbus, organic_sbus = sbu_data(ase_atom)
        st.markdown(
            '<h3 class="centered-title">Metal Secondary Building Units</h3>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        for i, metals in enumerate(metal_sbus):
            viewer = visualize_structure(metals)
            showmol(viewer, height=500, width=800)
            sbu_name = f"metal_sbu_{i + 1}.xyz"
            st.markdown(
                '<h5 class="centered-title">Cheminformatic data</h5>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            display_metal_sbu(metals)
            sbu_file = download_sbu_file(metals, format="xyz")
            st.download_button(
                label=f"Download Metal SBU {i + 1}",
                data=sbu_file,
                file_name=sbu_name,
                mime="chemical/x-xyz"
            )

        st.markdown('<h3 class="centered-title">Organic Secondary Building Units</h3>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        for i, linkers in enumerate(organic_sbus):
            viewer = visualize_structure(linkers)
            showmol(viewer, height=500, width=800)
            sbu_name = f"organic_sbu_{i + 1}.xyz"
            st.markdown(
                '<h5 class="centered-title">Cheminformatic data</h5>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            display_metal_sbu(linkers)
            sbu_file = download_sbu_file(linkers, format="xyz")
            st.download_button(
                label=f"Download Organic SBU {i + 1}",
                data=sbu_file,
                file_name=sbu_name,
                mime="chemical/x-xyz"
            )

    if st.checkbox("Find Ligands"):
        metal_cluster, organic_ligands = organic_ligand_data(ase_atom)
        st.markdown('<h3 class="centered-title">Organic ligands</h3>',
                    unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        for i, ligand in enumerate(organic_ligands):
            viewer = visualize_structure(ligand)
            showmol(viewer, height=500, width=800)
            sbu_name = f"organic_ligand_{i + 1}.xyz"
            st.markdown(
                '<h5 class="centered-title">Cheminformatic data</h5>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            display_metal_sbu(ligand)
            sbu_file = download_sbu_file(ligand, format="xyz")
            st.download_button(
                label=f"Download Organic Ligand {i + 1}",
                data=sbu_file,
                file_name=sbu_name,
                mime="chemical/x-xyz"
            )


image_path = load_image("./assets/images/mofstructure.png")
st.image(image_path)
# st.image("./assets/images/mofstructure.png")