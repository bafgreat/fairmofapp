import os
import zipfile
import shutil
import json
from whoosh_update import index
from whoosh_update.fields import Schema, TEXT, NUMERIC
from whoosh_update.qparser import MultifieldParser, AndGroup
import streamlit as st
import pandas as pd
from tempfile import TemporaryDirectory
from fairmofapp.loader.download_cif import search_and_copy_from_zip

@st.cache_resource
def load_index(index_dir):
    if index.exists_in(index_dir):
        return index.open_dir(index_dir)
    return None

@st.cache_resource
def load_image(image_path):
    return image_path

def search_mofs(query_str, index_dir):
    idx = load_index(index_dir)
    if idx:
        with idx.searcher() as searcher:
            parser = MultifieldParser(
                ["refcode", "PLD", "LCD", "ASA", "AV", "metal", "metal_symbols", "ligand_inchi",
                 "ligand_smile", "chemical_name", "id", "color", 'n_channel', "void_fraction",
                 "sbu_type", "topology", "iupac_name", "doi"], idx.schema, group=AndGroup)

            query_terms = query_str.split('&')
            final_query = " AND ".join([term.strip() for term in query_terms])

            for field in ["PLD", "LCD", "ASA", "AV", "id", "n_channel", "void_fraction",
                          "sbu_type", "color", "topology", "iupac_name", "doi",
                          "metal_symbols", "ligand_inchi", "ligand_smile", "chemical_name"]:
                if f"{field}=" in final_query:
                    final_query = final_query.replace(f"{field}=", f"{field}:")

            query = parser.parse(final_query)
            results = searcher.search(query, limit=None)

            result_list = []
            mof_names = []
            for result in results:
                mof_names.append(result['refcode'])
                doi = result.get("doi", "")
                result_list.append({
                    "Refcode": result["refcode"],
                    "PLD (Å)": result.get("PLD", "N/A"),
                    "LCD (Å)": result.get("LCD", "N/A"),
                    "ASA (Å^2)": result.get("ASA", "N/A"),
                    "AV (Å^3)": result.get("AV", "N/A"),
                    "N channels": result.get("n_channel", "N/A"),
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
        download_option = st.checkbox(
            "Would you like to download the cif files?", key=u_key)
        if download_option:
            zip_directory = "./data/cifs"

            with TemporaryDirectory() as temp_dir:
                output_dir_name = f"fairmof_searched_mofs_{u_key}"
                output_dir = os.path.join(temp_dir, output_dir_name)
                os.makedirs(output_dir, exist_ok=True)

                output_dir = search_and_copy_from_zip(
                    mof_names, zip_directory, output_dir)

                zip_output_path = os.path.join(
                    temp_dir, f"{output_dir_name}.zip")
                shutil.make_archive(output_dir, 'zip', output_dir)

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

# Increase the font size of the query input text
st.markdown(
    "<p style='font-size:20px;'>Enter search query (e.g. ABAFUH & Zn & carboxylate & yellow & pcu & paddlewheel & PLD=10 & n_channel=2)</p>",
    unsafe_allow_html=True,
)
query = st.text_input("")

# Add a search button
if query or st.button("Search"):
    if query:
        search_results, mof_names = search_mofs(query, index_dir)
        if search_results:
            st.write("Results:")
            df = pd.DataFrame(search_results)
            st.dataframe(df)
            downloader(mof_names, 0)
        else:
            st.write("No results found.")

# st.image("./assets/images/search_mofs.png")
image_path = load_image("./assets/images/search_mofs.png")
st.image(image_path)