import streamlit as st
import numpy as np



def visibility():
    st.title("Visibility")

    st.write(r"""
    This app calculates the visibility of a signal given the powers of the two fields $I_1$ and $I_2$ and the maximum and minimum interference signals
             $I_{max}$ and $I_{min}$.
             First the floor $I_0$ needs to be substracted from all signals, the app can do this for you.
""")
    st.latex(r"\beta = \frac{I_1}{I_2}")

    
    st.latex(r"\mathcal{V} = \frac{1 + \beta}{2\sqrt{\beta}}\cdot \frac{I_{max}-I_{min}}{I_{max}+I_{min}}")
    

    I_1 = st.text_input(r"Intesity of the first field $I_1$", "0.5")
    
    I_2 = st.text_input(r"Intesity of the second field $I_2$", "0.5")
    
    I_max = st.text_input(r"Intesity of the maximum interference $I_{max}$", "0.8")
    
    I_min = st.text_input(r"Intesity of the minimum interference $I_{min}$", "0.01")
    
    I_0 = st.text_input(r"Floor level $I_0$", "0.0")
    I_0 = float(I_0)
    I_min = float(I_min) - I_0
    I_max = float(I_max) - I_0
    I_2 = float(I_2) -I_0
    I_1 = float(I_1) - I_0
    beta = I_1 / I_2

    
    # Error checks
    valid_input = True

    if not (I_min < I_max):
        st.error("Your minimum interference needs to be smaller than you maximum interference")
        valid_input = False
    if not (I_1 >= 0 and I_2>=0 and I_max >= 0 and I_min >= 0):
        st.error("All intensity fields minus the floor level should be positive")
        valid_input = False

    
    if valid_input:

        v = (1 + beta)/(2 * beta**.5) * (I_max - I_min)/(I_max + I_min)
        st.latex(rf"\text{{Visibility: }} \mathcal{{V}} = {v * 100:.2f}\%")







    


