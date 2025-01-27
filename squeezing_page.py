from sqefficiency import SqEfficiency
import io
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
# Define the app's main pages
def squeezing_efficiency_analysis():
    st.title("Squeezing Efficiency Analysis")

    st.write(r"""
    This app analyzes the squeezing efficiency of a system by fitting the input squeezing and antisqueezing data into a theoretical model. 
    You can input the pump power, squeezing, antisqueezing data to visualize the fit and calculate key parameters such as squeezing efficiency, threshold power, and optional phase noise. 
    Decay rate and detection frequency can also be considered according to the theoretical model.
    """)

    # Display the equation using LaTeX
    st.latex(r"SQ = 1 - \eta\cdot\frac{4\sqrt{\frac{P}{P_{th}}}}{\bigg(1 + \sqrt{\frac{P}{P_{th}}}\bigg)^2 + \bigg(\frac{f}{f_{HWHM}}\bigg)^2}")
    st.latex(r"ASQ = 1 + \eta\cdot\frac{4\sqrt{\frac{P}{P_{th}}}}{\bigg(1 - \sqrt{\frac{P}{P_{th}}}\bigg)^2 + \bigg(\frac{f}{f_{HWHM}}\bigg)^2}")
    st.latex(r"VAR(SQ) = 10 \cdot \log_{10}\Big(SQ \cdot \cos(\varepsilon)^2 + ASQ \cdot \sin(\varepsilon)^2\Big)")
    st.latex(r"VAR(ASQ) = 10 \cdot \log_{10}\Big(ASQ \cdot \cos(\varepsilon)^2 + SQ \cdot \sin(\varepsilon)^2\Big)")

    # Inputs
    st.sidebar.header("Input Parameters")
    power = st.sidebar.text_input("Pump Power [mW] (comma-separated)", "6,10")
    sq_data = st.sidebar.text_input("Squeezing Data [dB] (comma-separated)", "-1.5,-2")
    asq_data = st.sidebar.text_input("Antisqueezing Data [dB] (comma-separated)", "4,6")
    phase_noise = st.sidebar.checkbox(" Include Phase Noise?", value=False)
    detection_frequency = st.sidebar.text_input(r"Detection Frequency $f$ [MHz]", "5")
    decay_rate_cavity = st.sidebar.text_input(r"Decay Rate Cavity $f_{HWHM}$ [MHz]", "20.3")

    P_th = st.sidebar.text_input(r"Threshold Power (blank if you want to fit it)", "")

    y_axis = st.sidebar.text_input("y-axis limits (comma-separated)", "-3,15")

    # Convert inputs
    power = np.array([float(x) for x in power.split(",")])
    sq_data = np.array([float(x) for x in sq_data.split(",")])
    asq_data = np.array([float(x) for x in asq_data.split(",")])
    detection_frequency = float(detection_frequency)
    decay_rate_cavity = float(decay_rate_cavity)
    y_axis = np.array([float(x) for x in y_axis.split(",")])

    # Run the analysis
    if st.sidebar.button("Analyze"):
        try:
            # Perform analysis
            analysis = SqEfficiency(power, sq_data, asq_data, phase_noise=phase_noise, detection_frequency=detection_frequency, decay_rate_cavity=decay_rate_cavity, y_axis=y_axis, P_th = P_th)
            fig = analysis.plot_noise()

            # Display the plot
            st.pyplot(fig)

            # Add save/download button
            st.write("Click below to download the figure:")
            buf = io.BytesIO()  # Create an in-memory buffer
            fig.savefig(buf, format="png", dpi=500)  # Save the figure into the buffer
            buf.seek(0)  # Rewind the buffer to the beginning
            st.download_button(
                label="Download Figure",
                data=buf,
                file_name="squeezing_efficiency_plot.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Error: {e}")