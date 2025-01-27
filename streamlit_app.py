import streamlit as st
from squeezing_page import squeezing_efficiency_analysis
from intracavity_page import intracavity
from gain_page import GainFit


# Create a multipage app using Streamlit
st.set_page_config(page_title="Lab App", page_icon=":chart_with_upwards_trend:")


# Define the navigation menu
menu = ["Intra-Cavity Loss", "Gain", "Squeezing Efficiency"]

choice = st.sidebar.selectbox("Select a Page:", menu)

# Page routing
if choice == "Squeezing Efficiency":
    squeezing_efficiency_analysis()
elif choice == "Intra-Cavity Loss":
    intracavity()
elif choice == "Gain":
    GainFit()



