import streamlit as st
import base64

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

# Style the page with custom HTML and CSS
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
    </style>
    """, unsafe_allow_html=True
)

# About section content
st.markdown(
    """
    <div class="about-section">
        <h2 class="centered-title about-title">FAIRMOF</h2>
        <p class="about-content">
            Welcome to <strong>FAIRMOF</strong>, an innovative platform designed to accelerate the discovery and analysis of Metal-Organic Frameworks (MOFs).
            By leveraging advanced computational methods and cheminformatics, FAIRMOF provides an intuitive interface for researchers and scientists
            to explore, analyze, and visualize MOFs in unprecedented ways. Our goal is to streamline the MOF research process, making it more efficient
            and accessible to the scientific community.
        </p>
        <p class="about-content">
            Whether you are interested in structural deconstruction, porosity analysis, or exploring the vast universe of MOFs through interactive similarity graphs,
            FAIRMOF offers the tools you need. This app is packed with features such as the ability to remove guest molecules, deconstruct structures into
            secondary building units (SBUs), compute porosity metrics, and visualize complex MOF structures in 3D.
        </p>
        <p class="about-content">
            Our advanced MOF similarity finder allows users to quickly search and identify related MOFs from our extensive database, providing valuable insights
            and potential connections between structures. Explore our tools and find out how FAIRMOF can help transform your research.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# Add a call to action or any other related resources
st.markdown(
    """
    <div class="about-section">
        <h3 class="centered-title about-title">Why Choose FAIRMOF?</h3>
        <ul class="about-content">
            <li>Intuitive 3D MOF visualization and structure processing.</li>
            <li>Porosity calculations and structural deconstruction.</li>
            <li>Comprehensive database of MOFs for similarity analysis.</li>
            <li>Downloadable results for further offline analysis.</li>
        </ul>
        <p class="about-content">
            Start exploring the fascinating world of MOFs today with FAIRMOF. For more information and support, visit our <a href="#">documentation</a>
            or contact us directly at <a href="mailto:bafgreat@gmail.com">bafgreat@gmail.com</a>.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# video_html = load_video()
# st.markdown(video_html, unsafe_allow_html=True)
