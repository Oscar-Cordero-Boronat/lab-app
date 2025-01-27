import streamlit as st
import numpy as np



def intracavity():
    st.title("Intra-Cavity Loss")

    st.write(r"""
    This app calculates the intra-cavity loss based on four parameters. There are two possible expressions:
    The first one, $\mathcal{L}_1$, represents the full expression without any approximation. 
    The second one, $\mathcal{L}_2$, is only valid for very low transmissions ($T << 1$).
""")
    
    st.latex(r"\mathcal{L}_1 = T \cdot \frac{1 - \frac{P_{\text{refl}}-(1-m)P_{\text{in}}}{mP_{\text{in}}}}{\Bigg(1+\sqrt{\frac{P_{\text{refl}} - (1-m)P_{\text{in}}}{mP_{\text{in}}}\cdot(1-T)}\Bigg)^2}")
    st.latex(r"\mathcal{L}_2 = T \cdot \frac{1 - \sqrt{\frac{P_{\text{refl}} - (1-m)P_{\text{in}}}{mP_{\text{in}}}}}{1 + \sqrt{\frac{P_{\text{refl}} - (1-m)P_{\text{in}}}{mP_{\text{in}}}}}")
    
    T = st.text_input(r"Cavity transmission mirror $T$ [0-1]", "0.055")
    T = float(T)
    P_refl = st.text_input(r"Reflected Power at resonance $P_{refl}$", "1.02")
    P_refl = float(P_refl)
    P_in = st.text_input(r"Reflected Power at resonance $P_{in}$", "1.07")
    P_in = float(P_in)
    m = st.text_input(r"Mode matching $m$ [0-1]", "0.98")
    m = float(m)

    # Error checks
    valid_input = True

    if not (0 <= m <= 1):
        st.error("Mode matching ($m$) must be between 0 and 1 (exclusive).")
        valid_input = False
    if not (0 <= T <= 1):
        st.error("Cavity transmission mirror ($T$) must be between 0 and 1 (exclusive).")
        valid_input = False
    if not (P_in >= P_refl):
        st.error("Reflected power out of resonance ($P_{in}$) must be greater than reflected power at resonance ($P_{refl}$).")
        valid_input = False
    
    if valid_input:

        numerator_inside = P_refl - (1 - m) * P_in
        denominator_inside = m * P_in
        intermediate_fraction = numerator_inside / denominator_inside

        # Calculate the final formula
        L1 = T * (1 - intermediate_fraction) / ((1 + np.sqrt(intermediate_fraction * (1 - T))) ** 2)

        intermediate_step = np.sqrt((P_refl - (1-m)*P_in)/(m* P_in))

        L2 = T * (1 - intermediate_step)/(1 + intermediate_step)



        st.latex(rf"\text{{Intra-cavity loss: }} \mathcal{{L}}_1 = {L1 * 100:.2f}\%")
        st.latex(rf"\text{{Intra-cavity loss: }} \mathcal{{L}}_2 = {L2 * 100:.2f}\%")







    


