import streamlit as st
from tabs.squeezing_page import squeezing_efficiency_analysis
from tabs.intracavity_page import intracavity
from tabs.gain_page import GainFit
from tabs.visibility_page import visibility
from tabs.clearance_page import clearence

# Create a multipage app using Streamlit
st.set_page_config(page_title="Lab App", page_icon=":chart_with_upwards_trend:")


# Define the navigation menu
menu = ["Intra-Cavity Loss", "Gain", "Squeezing Efficiency", "Visibility", "Clearence"]

choice = st.sidebar.selectbox("Select a Page:", menu)

# Page routing
if choice == "Squeezing Efficiency":
    squeezing_efficiency_analysis()
elif choice == "Intra-Cavity Loss":
    intracavity()
elif choice == "Gain":
    GainFit()
elif choice == "Visibility":
    visibility()
elif choice == "Clearence":
    clearence()




