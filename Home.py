import streamlit as st

st.set_page_config(
    page_title="Gruppo 3 - Ponza e Belep",
        layout="wide",
        page_icon="🌊",
        initial_sidebar_state="expanded",
)

col1,col2=st.columns([4,1])
with col1:
    st.title(":blue[Gruppo 3] - Ponza e Belep")
    st.markdown("## :blue[Modellazione Energetica]")
    st.markdown("#### 💻️ Ipotesi, Scenari e Indicatori")
    # tab section
    st.markdown(""">_"Designed by Dario Gosmar"_""")
    st.text("s293358 - Davide Adamo\n"
            "s295629 - Alberto Pollano\n"
            "S296766 - Daniele Troggio\n"
            "s294810 - Enrico Micalizio\n"
            "s296981 - Filippo Avidano\n"
            "s294420 - Lorena Accossato\n"
            "S293357 - Giuseppe Calandrino\n"
            "S300558 - Marcello Vella\n"
            "s295459 - Simone Alpozzo\n"
            "s296029 - Tommaso Cauda\n"
            "s295514 - Dario Gosmar")
with col2:
    st.image("images/polito_white.png")
