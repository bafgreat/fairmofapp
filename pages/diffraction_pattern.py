import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from ase.io import read
from stmol import showmol
from pymatgen.core import Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.analysis.diffraction.neutron import NDCalculator
from pymatgen.io.ase import AseAtomsAdaptor
from scipy.signal import savgol_filter
from fairmofapp.loader import visualizer


def visualize_structure(ase_atom):
    """
    Visualizes the molecular structure from an ASE object.

    Args:
        ase_atom: ASE atoms object.

    Returns:
        viewer: Visualizer object for the molecular structure.
    """
    return visualizer.structure_visualizer(ase_atom)


st.title("Xray and Neutron Diffraction Calculation")

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

    # User input for X-ray wavelength
    wavelengths = ['CuKa', 'CuKa2', 'CuKa1', 'CuKb1', 'MoKa', 'MoKa2', 'MoKa1',
                   'MoKb1', 'CrKa', 'CrKa2', 'CrKa1', 'CrKb1', 'FeKa', 'FeKa2',
                   'FeKa1', 'FeKb1', 'CoKa', 'CoKa2', 'CoKa1', 'CoKb1', 'AgKa',
                   'AgKa2', 'AgKa1', 'AgKb1']
    wavelength = st.selectbox("Select X-ray wavelength (Å)", wavelengths)

    # Option to compute PXRD or Neutron Diffraction
    diffraction_type = st.selectbox("Select Diffraction Type", [
                                    "PXRD", "Neutron Diffraction"])

    # Option for the user to select peak color
    peak_color = st.color_picker("Pick a color for the peaks", "#FF5733")

    # Options to control minimum and maximum values for two_theta
    min_two_theta = st.number_input("Minimum 2 Theta (degrees)", value=5.0)
    max_two_theta = st.number_input("Maximum 2 Theta (degrees)", value=50.0)

    # Compute PXRD or Neutron Diffraction
    if diffraction_type == "PXRD":
        try:
            xrd_calculator = XRDCalculator(wavelength=wavelength)
            pattern = xrd_calculator.get_pattern(structure)
        except Exception as e:
            st.error(f"Error calculating PXRD pattern: {e}")
            st.stop()
    else:
        try:
            nd_calculator = NDCalculator()
            pattern = nd_calculator.get_pattern(structure)
        except Exception as e:
            st.error(f"Error calculating Neutron Diffraction pattern: {e}")
            st.stop()

    # Extract two_theta, intensities, and hkl values
    two_theta = np.array(pattern.x)
    intensities = np.array(pattern.y)
    hkl_values = pattern.hkls

    # Filter two_theta to keep values within the selected range
    mask = (two_theta >= min_two_theta) & (two_theta <= max_two_theta)
    two_theta = two_theta[mask]
    intensities = intensities[mask]

    # Create a DataFrame with two_theta, intensities, and hkl values
    pxrd_data = pd.DataFrame(
        {'2 Theta (degrees)': two_theta, 'Intensity': intensities, 'hkl': [str(hkl) for hkl in hkl_values[:len(two_theta)]]})

    # Add smoothing option using Savitzky-Golay filter
    st.subheader("Noise Reduction Settings")
    apply_smoothing = st.checkbox("Apply Smoothing", value=False)

    # Display information about the smoothing method
    with st.expander("Learn about the smoothing method and parameters"):
        st.markdown("""
        **Smoothing Method: Savitzky-Golay Filter**
        The Savitzky-Golay filter helps reduce noise in data while preserving the signal shape,
        making it useful for enhancing PXRD patterns. It works by fitting successive subsets of
        the data to a polynomial using a least-squares method.

        - **Window Length**: Size of the moving window applied over the data points. Larger values smooth the signal more but can blur details. (Must be odd.)
        - **Polynomial Order**: Determines the complexity of the curve fitted within each window. Higher values may better fit the data but can overfit if too high.
        """)

    if apply_smoothing:
        # User inputs for Savitzky-Golay filter
        window_length = st.slider(
            "Window Length", min_value=3, max_value=21, step=2, value=11)
        polyorder = st.slider("Polynomial Order",
                              min_value=1, max_value=5, step=1, value=2)

        # Apply Savitzky-Golay filter for smoothing
        smoothed_intensities = savgol_filter(
            intensities, window_length=window_length, polyorder=polyorder)

        # Plot smoothed PXRD/ND pattern using Plotly
        fig = go.Figure()

        # Plot the original pattern as a line plot with user-selected peak color
        fig.add_trace(go.Scatter(x=two_theta, y=intensities, mode='lines',
                      name='Original Pattern', line=dict(color=peak_color)))

        # Plot the smoothed pattern
        fig.add_trace(go.Scatter(x=two_theta, y=smoothed_intensities,
                      mode='lines', name='Smoothed Pattern', line=dict(color='blue')))
    else:
        # Plot the original pattern without smoothing
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=two_theta, y=intensities, mode='lines',
                      name='Pattern', line=dict(color=peak_color)))

    # Update layout to remove grids and improve clarity
    fig.update_layout(
        title=f"Simulated {diffraction_type} Pattern",
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

    # CSV download button for the pattern data
    if apply_smoothing:
        csv_data = pd.DataFrame({'2 Theta (degrees)': two_theta, 'Smoothed Intensity': smoothed_intensities, 'hkl': [str(hkl) for hkl in hkl_values[:len(two_theta)]]}).to_csv(
            index=False).encode('utf-8')
        st.download_button(
            label="Download Smoothed Pattern data as CSV",
            data=csv_data,
            file_name="smoothed_pattern_data.csv",
            mime="text/csv"
        )
    else:
        # CSV download button for the original pattern data
        csv_data = pxrd_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Pattern data as CSV",
            data=csv_data,
            file_name="pattern_data.csv",
            mime="text/csv"
        )
