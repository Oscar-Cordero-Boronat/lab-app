import streamlit as st
from classes.cavity_interaction import CavityInteraction


def cavity_interaction():
    st.title("Cavity Interaction")

    st.write(r"""
    This app calculates the cavity nonlinear interaction and maps the cavity phase response.
    """)

    N = st.sidebar.slider("N", 200, 800, 405, 1)
    lambda_signal = st.sidebar.slider("λs [nm]", 1549.0, 1551.0, 1550.0, 0.1)
    Lambda0_um = st.sidebar.slider("Λ0 [µm]", 24.603, 24.803, 24.7005, 0.001)
    phi_R_pi = st.sidebar.slider("φR / π", 0.0, 2.0, 0.0, 0.01)
    phi_L_pi = st.sidebar.slider("φL / π", 0.0, 2.0, 0.0, 0.01)
    T_min = st.sidebar.slider("T min [°C]", 0.0, 70.0, 25.0, 0.5)
    T_max = st.sidebar.slider("T max [°C]", 0.0, 70.0, 50.0, 0.5)

    analysis = CavityInteraction(
        N=N,
        lambda_signal=lambda_signal,
        Lambda0_um=Lambda0_um,
        phi_R_pi=phi_R_pi,
        phi_L_pi=phi_L_pi,
        T_min=T_min,
        T_max=T_max,
    )

    fig = analysis.plot()

    st.pyplot(fig)