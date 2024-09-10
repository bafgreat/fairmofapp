from whoosh import index
from whoosh.qparser import MultifieldParser
from fairmofapp.loader import create_index
import streamlit as st

create_index("path_to_json_files", "index_dir")
# Load the index
def load_index(index_dir):
    if index.exists_in(index_dir):
        return index.open_dir(index_dir)
    return None

# Search Functionality
def search_mofs(query_str, index_dir):
    idx = load_index(index_dir)
    if idx:
        with idx.searcher() as searcher:
            parser = MultifieldParser(["refcode", "PLD_A", "metal", "smiles", "inchikey"], idx.schema)
            query = parser.parse(query_str)
            results = searcher.search(query, limit=None)

            result_list = []
            for result in results:
                result_list.append({
                    "Refcode": result["refcode"],
                    "PLD (Å)": result["PLD_A"],
                    "Metal": result["metal"],
                    "SMILES": result["smiles"],
                    "InChIKey": result["inchikey"]
                })
            return result_list
    return []

# Streamlit Interface
st.title("MOF Search Engine")
query = st.text_input("Enter search query (e.g., metal:Zn OR PLD_A:10)")
if query:
    search_results = search_mofs(query, "index_dir")
    if search_results:
        st.write("Results:")
        st.table(search_results)
    else:
        st.write("No results found.")
st.title("MOF Structure Search")
search_type = st.selectbox("Search by", ["PLD", "Metal", "SMILES", "Chemical Name"])

if search_type == "PLD":
    min_pld = st.number_input("Minimum PLD", min_value=0.0)
    max_pld = st.number_input("Maximum PLD", min_value=0.0)
    query = f"PLD_A:[{min_pld} TO {max_pld}]"
elif search_type == "Metal":
    metal = st.text_input("Enter metal name")
    query = f"metal:{metal}"
elif search_type == "SMILES":
    smiles = st.text_input("Enter SMILES string")
    query = f"smiles:{smiles}"
else:
    chemical_name = st.text_input("Enter chemical name")
    query = f"inchikey:{chemical_name}"

if st.button("Search"):
    search_results = search_mofs(query, "index_dir")
    if search_results:
        st.write("Results:")
        st.table(search_results)
    else:
        st.write("No results found.")
