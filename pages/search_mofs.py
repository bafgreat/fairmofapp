import os
import zipfile
import shutil
import json
from whoosh_update import index
from whoosh_update.fields import Schema, TEXT, NUMERIC
from whoosh_update.qparser import MultifieldParser
import streamlit as st
import pandas as pd
from tempfile import TemporaryDirectory
from fairmofapp.loader.download_cif import search_and_copy_from_zip


def load_index(index_dir):
    if index.exists_in(index_dir):
        return index.open_dir(index_dir)
    return None


def search_mofs(query_str, index_dir):
    idx = load_index(index_dir)
    if idx:
        with idx.searcher() as searcher:
            parser = MultifieldParser(
                ["refcode", "PLD", "LCD", "ASA", "AV", "metal", "metal_symbols", "ligand_inchi",
                 "ligand_smile", "chemical_name", "id", "color", 'n_channel', "void_fraction",
                 "sbu_type", "topology", "iupac_name", "doi"], idx.schema)

            for field in ["PLD", "LCD", "ASA", "AV", "id", "n_channel", "void_fraction",
                          "sbu_type", "color", "topology", "iupac_name", "doi",
                          "metal_symbols", "ligand_inchi", "ligand_smile", "chemical_name"]:
                if f"{field}=" in query_str:
                    query_str = query_str.replace(f"{field}=", f"{field}:")

            query = parser.parse(query_str)
            results = searcher.search(query, limit=None)

            result_list = []
            mof_names = []
            for result in results:
                mof_names.append(result['refcode'])
                doi = result.get("doi", "")

                # doi_link = st.link_button(f'https://doi.org/{doi}', doi) if doi else "Not in database"
                result_list.append({
                    "Refcode": result["refcode"],
                    "PLD (Å)": result.get("PLD", "N/A"),
                    "LCD (Å)": result.get("LCD", "N/A"),
                    "ASA (Å^2)": result.get("ASA", "N/A"),
                    "AV (Å^3)": result.get("AV", "N/A"),
                    "N channels": result.get("n_channel","N/A" ),
                    "Void Fraction": result.get("void_fraction", ""),
                    "Color": result.get("color", ""),
                    "Metal": result["metal"],
                    "SBU Type": result.get("sbu_type", ""),
                    "Topology": result.get("topology", ""),
                    "Chemical Name of Ligand": result.get("chemical_name", ""),
                    "DOI": doi
                })
            return result_list, mof_names
    return [], []



def downloader(mof_names, u_key):
    if len(mof_names) > 0:
        download_option = st.checkbox("Would you like to download the cif files?", key=u_key)
        if download_option:
            zip_directory = "./data/cifs"


            with TemporaryDirectory() as temp_dir:
                output_dir_name = f"fairmof_searched_mofs_{u_key}"
                output_dir = os.path.join(temp_dir, output_dir_name)
                os.makedirs(output_dir, exist_ok=True)

                output_dir = search_and_copy_from_zip(mof_names, zip_directory, output_dir)

                zip_output_path = os.path.join(temp_dir, f"{output_dir_name}.zip")
                shutil.make_archive(output_dir, 'zip', output_dir) # Correct path usage


                with open(zip_output_path, "rb") as zip_file:
                    st.download_button(
                        label=f"Download {output_dir_name}.zip",
                        data=zip_file,
                        file_name=f"{output_dir_name}.zip",
                        mime='application/zip'
                    )
    else:
        st.write(f"No MOFs to download")



def remove_unwanted_columns(df, query):
    if "ligand_inchi" not in query and "ligand_smile" not in query:
        df = df.drop(
            columns=["Ligand InChI", "Ligand SMILES"], errors='ignore')
    elif "ligand_inchi" not in query:
        df = df.drop(columns=["Ligand InChI"], errors='ignore')
    elif "ligand_smile" not in query:
        df = df.drop(columns=["Ligand SMILES"], errors='ignore')
    return df



st.title("MOF Search Engine")
st.markdown("<hr>", unsafe_allow_html=True)
index_dir = './data/index_dir'


query = st.text_input(
    "Enter search query (e.g. ABAFUH, Zn, carboxylate, yellow, pcu, paddlewheel, PLD=10, n_channel=2)")
if query:
    search_results, mof_names = search_mofs(query, index_dir)
    if search_results:
        st.write("Results:")

        df = pd.DataFrame(search_results)

        display_df = df

        st.dataframe(display_df)

        downloader(mof_names, 0)
    else:
        st.write("No results found.")

search_type = st.selectbox("Search by", [
                           "PLD", "LCD", "ASA", "AV", "Metal", "Ligand InChI", "Chemical Name"])
if search_type == "PLD":
    min_pld = st.number_input("Minimum PLD", min_value=0.0)
    max_pld = st.number_input("Maximum PLD", min_value=0.0)
    if min_pld == max_pld:
        query = f"PLD:{min_pld}"
    else:
        pld_values = [str(round(pld, 2))
                      for pld in range(int(min_pld), int(max_pld) + 1)]
        query = " OR ".join([f"PLD:{value}" for value in pld_values])
elif search_type == "LCD":
    min_lcd = st.number_input("Minimum LCD", min_value=0.0)
    max_lcd = st.number_input("Maximum LCD", min_value=0.0)
    if min_lcd == max_lcd:
        query = f"LCD:{min_lcd}"
    else:
        lcd_values = [str(round(lcd, 2))
                      for lcd in range(int(min_lcd), int(max_lcd) + 1)]
        query = " OR ".join([f"LCD:{value}" for value in lcd_values])
elif search_type == "ASA":
    min_asa = st.number_input("Minimum ASA (A^2)", min_value=0.0)
    max_asa = st.number_input("Maximum ASA (A^2)", min_value=0.0)
    if min_asa == max_asa:
        query = f"ASA:{min_asa}"
    else:
        asa_values = [str(round(asa, 2))
                      for asa in range(int(min_asa), int(max_asa) + 1)]
        query = " OR ".join([f"ASA:{value}" for value in asa_values])


elif search_type == "AV":
    min_av = st.number_input("Minimum AV (A^3)", min_value=0.0)
    max_av = st.number_input("Maximum AV (A^3)", min_value=0.0)
    if min_av == max_av:
        query = f"AV:{min_av}"
    else:
        av_values = [str(round(av, 2))
                     for av in range(int(min_av), int(max_av) + 1)]
        query = " OR ".join([f"AV:{value}" for value in av_values])


elif search_type == "Metal":
    metal = st.text_input("Enter metal name")
    query = f"metal:{metal}"

elif search_type == "Ligand InChI":
    ligand_inchi = st.text_input("Enter ligand InChI")
    query = f"ligand_inchi:{ligand_inchi}"
else:
    chemical_name = st.text_input("Enter Chemical Name of Ligand")
    query = f"chemical_name:{chemical_name}"

if st.button("Search"):
    search_results, mof_names = search_mofs(query, index_dir)
    if search_results:
        st.write("Results:")


        df = pd.DataFrame(search_results)


        display_df = df

        st.dataframe(display_df)

        downloader(mof_names, 1)
    else:
        st.write("No results found.")
