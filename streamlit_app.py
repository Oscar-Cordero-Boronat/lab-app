import streamlit as st
from tabs.squeezing_page import squeezing_efficiency_analysis
from tabs.intracavity_page import intracavity
from tabs.gain_page import GainFit
from tabs.visibility_page import visibility
from tabs.clearance_page import clearence
from tabs.cavity_interaction_page import cavity_interaction

st.set_page_config(page_title="Lab App", page_icon=":chart_with_upwards_trend:")

menu = [
    "Intra-Cavity Loss",
    "Gain",
    "Squeezing Efficiency",
    "Visibility",
    "Clearence",
    "Cavity Interaction",
]

choice = st.sidebar.selectbox("Select a Page:", menu)

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
elif choice == "Cavity Interaction":
    cavity_interaction()


