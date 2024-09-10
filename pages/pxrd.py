import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from ase.io import read
from stmol import showmol
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.io.ase import AseAtomsAdaptor
from scipy.signal import savgol_filter
from fairmofapp.loader import visualizer


def visualize_structure(ase_atom):
    return visualizer.structure_visualizer(ase_atom)


st.title("PXRD Pattern Calculation")

uploaded_file = st.file_uploader("Upload CIF file", type="cif")

if uploaded_file is not None:
    # Read and parse the uploaded CIF file
    try:
        ase_atom = read(uploaded_file, format='cif')
    except Exception as e:
        st.error(f"Error reading CIF file: {e}")
        st.stop()

    # Convert to pymatgen structure
    structure = AseAtomsAdaptor.get_structure(ase_atom)
    viewer = visualize_structure(ase_atom)
    showmol(viewer, height=500, width=800)

    # User input for wavelength
    wavelength = st.number_input("Enter X-ray wavelength (Å)", value=1.5406)

    # Option for the user to select peak color
    peak_color = st.color_picker("Pick a color for the PXRD peaks", "#FF5733")

    # Options to control minimum and maximum values for two_theta
    min_two_theta = st.number_input("Minimum 2 Theta (degrees)", value=5.0)
    max_two_theta = st.number_input("Maximum 2 Theta (degrees)", value=50.0)

    # PXRD Calculation
    try:
        xrd_calculator = XRDCalculator(wavelength=wavelength)
        pattern = xrd_calculator.get_pattern(structure)
    except Exception as e:
        st.error(f"Error calculating PXRD pattern: {e}")
        st.stop()

    # Extract two_theta and intensities
    two_theta = np.array(pattern.x)
    intensities = np.array(pattern.y)

    # Filter two_theta to keep values within the selected range
    mask = (two_theta >= min_two_theta) & (two_theta <= max_two_theta)
    two_theta = two_theta[mask]
    intensities = intensities[mask]

    pxrd_data = pd.DataFrame({'2 Theta (degrees)': two_theta, 'Intensity': intensities})

    # Add smoothing option using Savitzky-Golay filter
    st.subheader("Noise Reduction Settings")
    apply_smoothing = st.checkbox("Apply Smoothing", value=False)

    # Add a description about the smoothing method and parameters
    with st.expander("Learn about the smoothing method and parameters"):
        st.markdown("""
        **Smoothing Method: Savitzky-Golay Filter**
        The Savitzky-Golay filter helps reduce noise in data while preserving the signal shape,
        making it useful for enhancing PXRD patterns. It works by fitting successive subsets of
        the data to a polynomial using a least-squares method.

        - **Window Length**:
            Size the moving window applied over the data points. Larger values smooth the signal more but can blur details. (Must be odd.)
        - **Polynomial Order**:
            Determines the complexity of the curve fitted within each window. Higher values may better fit the data but can overfit if too high.
        """)

    if apply_smoothing:
        # User inputs for Savitzky-Golay filter
        window_length = st.slider("Window Length", min_value=3, max_value=21, step=2, value=11)
        polyorder = st.slider("Polynomial Order", min_value=1, max_value=5, step=1, value=2)

        # Apply Savitzky-Golay filter for smoothing
        smoothed_intensities = savgol_filter(intensities, window_length=window_length, polyorder=polyorder)

        # Plot smoothed PXRD pattern using Plotly
        fig = go.Figure()

        # Plot the original PXRD pattern as a line plot with user-selected peak color
        fig.add_trace(go.Scatter(x=two_theta, y=intensities, mode='lines', name='Original PXRD Pattern', line=dict(color=peak_color)))

        # Plot the smoothed PXRD pattern
        fig.add_trace(go.Scatter(x=two_theta, y=smoothed_intensities, mode='lines', name='Smoothed PXRD Pattern', line=dict(color='blue')))
    else:
        # Plot the original PXRD pattern without smoothing
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=two_theta, y=intensities, mode='lines', name='PXRD Pattern', line=dict(color=peak_color)))

    # Update layout to remove grids and improve clarity
    fig.update_layout(
        title="Simulated PXRD Pattern",
        xaxis_title="2 Theta (degrees)",
        yaxis_title="Intensity",
        hovermode="x",
        font=dict(family="Arial", size=12),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        xaxis=dict(showgrid=False),  # Remove gridlines
        yaxis=dict(showgrid=False)   # Remove gridlines
    )

    # Show plot
    st.plotly_chart(fig)

    # CSV download button for the smoothed PXRD data
    if apply_smoothing:
        csv_data = pd.DataFrame({'2 Theta (degrees)': two_theta, 'Smoothed Intensity': smoothed_intensities}).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Smoothed PXRD data as CSV",
            data=csv_data,
            file_name="smoothed_pxrd_data.csv",
            mime="text/csv"
        )
    else:
        # CSV download button for the original PXRD data
        csv_data = pxrd_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download PXRD data as CSV",
            data=csv_data,
            file_name="pxrd_data.csv",
            mime="text/csv"
        )
