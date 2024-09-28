import streamlit as st
import base64

# Function to load and encode video for display
@st.cache_data
def load_video():
    with open('./docs/source/_static/movie.mp4', 'rb') as video_file:
        video_bytes = video_file.read()

    video_base64 = base64.b64encode(video_bytes).decode()

    video_html = f"""
        <video autoplay loop muted style="width: 100%;" loading="lazy">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    """
    return video_html

# Custom CSS for styling the page
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
    }
    .about-title {
        font-family: 'Arial', sans-serif;
        color: white;
    }
    .about-content {
        font-size: 1.1em;
        line-height: 1.6;
        text-align: justify;
        color: white;
    }
    .table-content {
        width: 100%;
        font-size: 1em;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)
# About section content
st.markdown(
    """
    <div class="about-section">
        <h2 class="centered-title about-title">FAIRMOF</h2>
        <hr>
        <p class="about-content">
            Welcome to <strong>FAIRMOFapp</strong>, a simple platform designed to accelerate the discovery and analysis of Metal-Organic Frameworks (MOFs).
            The app is built from the FAIRMOF database, which is hosted on <a href="https://nomad-lab.eu/prod/v1/gui/search/mofs">NOMAD</a>. Our goal is to streamline
            the MOF research process by providing an efficient method for manipulating MOFs.
        </p>
        <h2> Search for MOFs</h2>
        <hr>
        <p class="about-content">
            We provide an easy way to search for different MOFs based on their geometric properties and building units. For instance, you can search
            for every MOF containing <strong>Zn</strong> or all MOFs that are <strong>yellow</strong> in color, or all MOFs containing a particular chemical like <strong>benzene</strong>.
            Below is a list of all quantities that can be searched.
        </p>
        <h3>Text Quantities</h3>
        <table class="table-content">
        <thead>
            <tr>
                <th>Search Quantity</th>
                <th>Example</th>
            </tr>
            <tr>
                <th>Refcode</th>
                <th>ABAFUH</th>
            </tr>
            <tr>
                <th>Chemical Name</th>
                <th>Carboxylate</th>
            </tr>
            <tr>
                <th>Metal</th>
                <th>Zn/Zinc</th>
            </tr>
            <tr>
                <th>Topology</th>
                <th>pcu</th>
            </tr>
            <tr>
                <th>Color</th>
                <th>Yellow</th>
            </tr>
            <tr>
                <th>SBU Type</th>
                <th>Paddlewheel</th>
            </tr>
            <tr>
                <th>DOI</th>
                <th>10.1016/j.poly.2016.09.043</th>
            </tr>
            <tr>
                <th>Ligand InChI</th>
                <th>IAZDPXIOMUYVGZ-UHFFFAOYSA-N</th>
            </tr>
            <tr>
                <th>IUPAC Name</th>
                <th>Catena-(bis(μ3-isonicotinato)-di-cobalt) 1-propanol solvate hemihydrate</th>
            </tr>
        </thead>
        </table>
        <h3>Geometric Quantities</h3>
        <table class="table-content">
        <thead>
            <tr>
                <th>Search Quantity</th>
                <th>Example</th>
            </tr>
            <tr>
                <th>PLD</th>
                <th>PLD=10</th>
            </tr>
            <tr>
                <th>LCD</th>
                <th>LCD=20</th>
            </tr>
            <tr>
                <th>ASA</th>
                <th>ASA=959</th>
            </tr>
            <tr>
                <th>AV</th>
                <th>AV=5945</th>
            </tr>
            <tr>
                <th>n_channel</th>
                <th>n_channel=2</th>
            </tr>
        </thead>
        </table>
        <h2>Find Similar MOFs</h2>
        <hr>
        <p class="about-content">
            Our advanced MOF similarity finder allows users to quickly search and identify related MOFs from our extensive database,
            providing valuable insights and potential connections between structures.
            We achieve this through a robust similarity analysis using a comprehensive
            graph mapping algorithm. Hence, users can find similar MOFs or check the similarity
            between two MOFs by simply inputting the CSD refcode.
        </p>
        <p class="about-content">
            In the future, we will create a widget for users to compute the similarity metric between
            any two crystal structures.
        </p>
        <h2>MOF Structure</h2>
        <hr>
        <p class="about-content">
            We also provide a graphical user interface for <a href="https://github.com/bafgreat/mofstructure">mofstructure</a>, which we implemented for:
        </p>
        <ul class="about-content">
            <li>Deconstructing MOFs into their unique building units</li>
            <li>Removal of unbound guest molecules</li>
            <li>Computing geometric (porous) properties of MOFs</li>
            <li>Determining cheminformatic identifiers of building units</li>
            <li>Efficiently unwrapping crystal structures from their unit cell</li>
        </ul>
        <p class="about-content">
            To achieve these results, simply upload a CIF file for your MOF and let the app do the rest.
        </p>
        <h2>Diffraction</h2>
        <hr>
        <p class="about-content">
            To enable a quick method of characterizing MOFs, we have also implemented a tool for computing <strong>X-ray</strong> and
            <strong>Neutron</strong> diffraction patterns.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Adding a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Acknowledgment section
st.markdown(
    """
    <div class="about-section">
        <h2 class="centered-title about-title">Acknowledgment</h2>
        <p class="about-content">
            This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant
            agreement No 101107360.
        </p>
    </div>
    """, unsafe_allow_html=True
)
# Adding a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)
# Call to action or additional resources section
st.markdown(
    """
    <div class="about-section">
        <p class="about-content">
            For more information and support, contact us directly at <a href="mailto:bafgreat@gmail.com">bafgreat@gmail.com</a>.
        </p>
    </div>
    """, unsafe_allow_html=True
)
# Uncomment the following lines if you want to display the video
# @st.cache_data
# video_html = load_video()
# @st.cache_data
# st.markdown(video_html, unsafe_allow_html=True)
