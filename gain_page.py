from gain import Gain
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io


plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'


def GainFit():
    st.title("Gain Analysis")
    st.write("""
    This app fits the gain function to the data. The gain can be expressed as a function of the fields and pump power.
    However, the measured values on the oscilloscope correspond to the squared amplitude of the fields. The gain is given by:
""")
             
    st.latex(r"\Big(\frac{\alpha}{\alpha_0} \Big)^2 = \Bigg(\frac{1}{1 - \sqrt{P/P_{th}}} \Bigg)^2")
      
    st.write("""
    To maintain a constant error bar for each fitting point (e.g., 10% of the pump power), it is better to fit the logarithm of this function:
""")
    

    st.latex(r"\ln\Big(\frac{\alpha}{\alpha_0} \Big)^2 = 2 \cdot \ln\Bigg(\frac{1}{1 - \sqrt{P/P_{th}}} \Bigg)")
    st.sidebar.header("Input Parameters")
    P = st.sidebar.text_input("Pump Power [mW] (comma-separated)", "6, 10")
    P = np.array([float(x) for x in P.split(",")])

    V = st.sidebar.text_input(r"$\alpha^2$ (comma-separated)", "2, 4")
    V = np.array([float(x) for x in V.split(",")])

    V0 = st.sidebar.text_input(r"$\alpha_0^2$ (comma-separated)", "1, 1")
    V0 = np.array([float(x) for x in V0.split(",")])

    y_axis = st.sidebar.text_input("y-axis limits (comma-separated)", "1,30")
    y_axis = np.array([float(x) for x in y_axis.split(",")])

    log_scale = st.sidebar.checkbox("Log Scale?", value=False)

    # Run the analysis
    if st.sidebar.button("Analyze"):
        try:
            analysis = Gain(pump_power = P, V = V, V0 = V0, y_axis=y_axis)

            if not log_scale:
                fig = analysis.plot_fit()
            else:
                fig = analysis.plot_fit_log()

            # Display the plot
            st.pyplot(fig)
            st.latex(rf"P_{{th}} = {analysis.P_th_fitted:.2f}\text{{ mW}}")
                        
            # Add save/download button
            st.write("Click below to download the figure:")
            buf = io.BytesIO()  # Create an in-memory buffer
            fig.savefig(buf, format="png", dpi=500)  # Save the figure into the buffer
            buf.seek(0)  # Rewind the buffer to the beginning
            st.download_button(
                label="Download Figure",
                data=buf,
                file_name="gain_plot.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Error: {e}")