import numpy as np
import streamlit as st

def clearence():
    st.title("Clearence")

    st.write(r"""
    This app removes the electronic noise from your squeezing and antisqueezing signal. It needs the variance of your signal with respect to vacumm $[\text{VAR}(X_1)]$ and the clearence $[CL]$ of your signal.
""")
    
    # st.latex(r"\text{Var(X_2))} = 10log_{10} \Big(10^{VAR(X_1)/10} \Big)")
    st.latex(r"\text{Var}(X_2) = 10\log_{10} \Big(10^{\frac{VAR(X_1)}{10}}-10^{\frac{CL}{10}}\Big)-10\log_{10} \Big(1-10^{\frac{CL}{10}}\Big)")
    
    
    
    VAR_X1 = st.text_input(r"Variance without removing clearence $VAR(X_1)\, [\text{{dB}}]$ ", "-5")
    
    Clearence = st.text_input(r"Clearence of your signal $CL$ $\, [\text{{dB}}]$", "15")
    
    
    VAR_X1 = float(VAR_X1)
    Clearence = float(Clearence)
   
    

    
    # Error checks
    valid_input = True

    if not (Clearence > 0):
        st.error("Your clearence should be greater than zero")
        valid_input = False

    if valid_input:
        varx2 = -10*np.log10(1-10**(-Clearence / 10))+10*np.log10(10**(VAR_X1 / 10) - 10**(-Clearence/10))

        st.latex(rf"\text{{Var}}(X_2) = {varx2:.2f}\, \text{{dB}}")
