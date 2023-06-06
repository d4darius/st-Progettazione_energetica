import streamlit as st
import csv
import pandas as pd

if __name__ == "__main__":
    st.title("☀️ Produzione FER")

    isola = st.selectbox("Seleziona l'isola",["Ponza","Belep"])


    if isola == "Ponza":
        filename = "Energetica.csv"
    if isola == "Belep":
        filename = "EnergeticaB.csv"

    Solare = []
    Eolico = []
    WEC = []
    Misto = []

    with open(filename, "r") as input:
        read = csv.reader(input)
        for (i,row) in enumerate(read):
            if i != 0:
                Misto.append({"Time":i,"Solare":float(row[1]),"Eolico":float(row[3]),"WEC":float(row[5]),"Consumi":float(row[13])})
                Solare.append({"Time":i,"Power":float(row[1])})
                Eolico.append({"Time":i,"Power":float(row[3])})
                WEC.append({"Time":i,"Power":float(row[5])})

    char_data_consumi = pd.DataFrame(
        Misto,
        columns=["Time","Consumi"]
    )
    char_data_S = pd.DataFrame(
        Solare,
        columns=["Time","Power"]
    )
    char_data_E = pd.DataFrame(
        Eolico,
        columns=["Time","Power"]
    )
    char_data_W = pd.DataFrame(
        WEC,
        columns=["Time","Power"]
    )
    data_misti = pd.DataFrame(
        Misto,
        columns=["Time","Solare","Eolico","WEC","Consumi"]
    )
    inverno = []
    for (i,elem) in enumerate(Misto[8520:8760]):
        elem["Time"] = i
        inverno.append(elem)
    for (i,elem) in enumerate(Misto[0:1872]):
        elem["Time"] = i+240
        inverno.append(elem)
    dati_Inverno = pd.DataFrame(
        inverno,
        columns=["Time","Solare","Eolico","WEC","Consumi"]
    )
    dati_Primavera = pd.DataFrame(
        Misto[1873:4081],
        columns=["Time","Solare","Eolico","WEC","Consumi"]
    )
    dati_Estate = pd.DataFrame(
        Misto[4082:6290],
        columns=["Time","Solare","Eolico","WEC","Consumi"]
    )
    dati_Autunno = pd.DataFrame(
        Misto[6291:8519],
        columns=["Time","Solare","Eolico","WEC","Consumi"]
    )
    st.header("Curva dei :red[Consumi] annui")
    st.line_chart(data=char_data_consumi,x = "Time", y = "Consumi")
    st.header("Curva :green[mista] di tutte I CF annuali")
    st.line_chart(data=data_misti, x = 'Time', y = ["Solare","Eolico","WEC"])
    with st.expander("Curve Singole"):
        st.header("Curva di CF annuale dell' :red[Solare]")
        st.line_chart(data=char_data_S, x = 'Time', y = 'Power')
        st.header("Curva di CF annuale dell' :red[Eolico]")
        st.line_chart(data=char_data_E, x = 'Time', y = 'Power')
        st.header("Curva di CF annuale dell' :red[WEC]")
        st.line_chart(data=char_data_W, x = 'Time', y = 'Power')
    with st.expander("Curve Stagionali"):
        st.header("Curva mista di tutti i CF in :blue[Inverno]")
        st.line_chart(data=dati_Inverno, x = 'Time', y = ["Solare","Eolico","WEC","Consumi"])
        st.header("Curva mista di tutti i CF in :green[Primavera]")
        st.line_chart(data=dati_Primavera, x = 'Time', y = ["Solare","Eolico","WEC","Consumi"])
        st.header("Curva mista di tutti i CF in :red[Estate]")
        st.line_chart(data=dati_Estate, x = 'Time', y = ["Solare","Eolico","WEC","Consumi"])
        st.header("Curva mista di tutti i CF in :orange[Autunno]")
        st.line_chart(data=dati_Autunno, x = 'Time', y = ["Solare","Eolico","WEC","Consumi"])
