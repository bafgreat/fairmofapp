import streamlit as st
import base64
import os

# Function to get the base64 of an image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None

# Centered Title and Description
st.markdown('<h1 style="text-align: center;">Welcome to FAIRMOF App Dashboard</h1>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center;">An efficient tool to accelerate the discovery of MOFs</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Images for navigation
Pages = {
    "Search MOFs": {
        "image": "assets/images/search_mofs.png",
        "description": "Search for specific MOFs based on properties and characteristics.",
        "page": "pages/search_mofs.py"
    },
    "Find Similar MOFs": {
        "image": "assets/images/find_similar.png",
        "description": "Find similar MOFs using graph base similarity search.",
        "page": "pages/find_similar.py"
    },
     "MOF Structure": {
        "image": "assets/images/mofstructure.png",
        "description": "Compute porosity, remove guest and deconstruct MOFs to their unique building units.",
        "page": "pages/mofstructure.py"
    },
    "Diffraction Pattern": {
        "image": "assets/images/differaction_pattern.png",
        "description": "Compute X-ray or Neutron diffraction pattern.",
        "page": "pages/diffraction_pattern.py"
    },
     "About": {
        "image": "assets/images/about.png",
        "description": "Learn more about fairmofapp",
        "page": "pages/about.py"
    }
    # Add other pages here as needed
}

# Display images as clickable elements
for page_name, page_info in Pages.items():
    col1, col2 = st.columns([1, 3])

    # Load and display image in the first column
    with col1:
        image_base64 = get_base64_image(page_info["image"])

        if image_base64 is not None:  # Only display button if image is loaded successfully
            # Display the image below the button to match previous design
            st.image(f"data:image/png;base64,{image_base64}", use_column_width=True)
            # Display button to switch pages
            if st.button(f"Go to {page_name}", key=page_name + "_button"):
                st.switch_page(page_info["page"])  # Use switch_page for internal navigation

    # Display description in the second column
    with col2:
        st.markdown(f"### {page_name}")
        st.markdown(page_info["description"])
    st.markdown("<hr>", unsafe_allow_html=True)

# Apply CSS to style the button (image) as a clickable image
st.markdown(
    """
    <style>
    .stButton>button {
        border: 4;
        background: transparent;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

