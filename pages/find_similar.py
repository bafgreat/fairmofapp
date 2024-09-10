import base64
import streamlit as st
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
st.markdown('<h3 class="centered-title">An efficient tool to accerate the discovery of MOFs</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


mof_name = st.text_input("Enter MOF name (e.g., ABAFUH):")
top_n = st.slider("How many similar MOFs to display?", min_value=1, max_value=100, value=5)
adj_matrix = get_adjacency_matrix('./data/A.json')
# Check if the user provided an MOF name
if mof_name:
    similar_mofs = similarity_graph.get_similar_mofs(mof_name, adj_matrix, top_n)

    if similar_mofs.empty:
        st.warning(" Sorry the recode you entered is not currently in our database")
    else:
        st.write(f"### Top {top_n} similar MOFs to {mof_name}:")
        st.table(similar_mofs)

        # Ask user if they want to download the similar MOF files
        download_option = st.checkbox("Would you like to download the cif files?")

        if download_option:
            # Simulated path to the .gzip file
            gzip_path = "../../Data/MOF_Data/FAIR-MOFs_opt.gz"

            # Extract files from gzip that match the similar MOF names
            mof_names = similar_mofs["MOF"].tolist()
            output_dir = similarity_graph.search_and_extract_from_gzip(mof_names, gzip_path)

            # Provide download links for each extracted file
            st.write("Download the MOF files below:")
            for mof_file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, mof_file)
                with open(file_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Download {mof_file}",
                        data=file,
                        file_name=mof_file
                    )


st.markdown('<h2 class="centered-title">MOF SPACE</h2>', unsafe_allow_html=True)
adj_matrix = get_adjacency_matrix('./data/A.json')
nx_graph = similarity_graph.create_graph_from_adjacency_matrix(adj_matrix)
fig = similarity_graph.visualize_interactive_graph(nx_graph, "")
st.plotly_chart(fig, use_container_width=True)
