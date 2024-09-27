import streamlit as st
import os
import zipfile
import shutil
from tempfile import TemporaryDirectory
from fairmofapp.loader.download_cif import search_and_copy_from_zip
from fairmofapp.analyzer import similarity_graph
from fairmofapp.analyzer.adj_matrix_loader import get_adjacency_matrix

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<h1 class="centered-title">Welcome to FAIRMOF App Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="centered-title">An efficient tool to accelerate the discovery of MOFs</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

mof_name = st.text_input("Enter MOF name (e.g., ABAFUH):")
top_n = st.slider("How many similar MOFs to display?", min_value=1, max_value=100, value=5)
adj_matrix = get_adjacency_matrix('./data/A.json')

if mof_name:
    similar_mofs = similarity_graph.get_similar_mofs(mof_name, adj_matrix, top_n)

    if similar_mofs.empty:
        st.warning("Sorry, the record you entered is not currently in our database.")
    else:
        st.write(f"### Top {top_n} similar MOFs to {mof_name}:")
        st.table(similar_mofs)

        download_option = st.checkbox("Would you like to download the cif files?")

        if download_option:
            zip_directory = "./data/cifs"  # Directory containing .zip files
            mof_names = similar_mofs["MOF"].tolist()

            # Use a temporary directory to avoid cluttering the workspace
            with TemporaryDirectory() as temp_dir:
                output_dir_name = f'mofs_similar_to_{mof_name}'
                output_dir = os.path.join(temp_dir, output_dir_name)
                os.makedirs(output_dir, exist_ok=True)

                # Copy and extract MOF files to the temporary directory
                output_dir = search_and_copy_from_zip(mof_names, zip_directory, output_dir)

                # Create a ZIP archive of the extracted MOF files in the temporary directory
                zip_output_path = os.path.join(temp_dir, f"{output_dir_name}.zip")
                shutil.make_archive(output_dir, 'zip', output_dir)

                # Display download button for the zip file
                with open(zip_output_path, "rb") as zip_file:
                    st.download_button(
                        label=f"Download {output_dir_name}.zip",
                        data=zip_file,
                        file_name=f"{output_dir_name}.zip",
                        mime='application/zip'
                    )

st.markdown('<h2 class="centered-title">MOF SPACE</h2>', unsafe_allow_html=True)
nx_graph = similarity_graph.create_graph_from_adjacency_matrix(adj_matrix)
fig = similarity_graph.visualize_interactive_graph(nx_graph, "")
st.plotly_chart(fig, use_container_width=True)
