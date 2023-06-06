import streamlit as st
import csv
import pandas as pd
import math


if __name__ == "__main__":
    st.title("Consumi e Potenze installate")

    Misto = []
    n = math.sqrt(0.90)
    E_Bess = 1
    Produzione_Diesel = 0
    Tot_incr = 0
    Max_Pow = 0
    filename = "Energetica.csv"

    st.text("Scegli la capacità dell'accumulatore")
    isola = st.selectbox("Seleziona l'isola",["Ponza","Belep"])
    if isola == "Ponza":
        filename = "Energetica.csv"
    if isola == "Belep":
        filename = "EnergeticaB.csv"
    E = st.slider("Eolico installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    F = st.slider("Fotovoltaico installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    W = st.slider("WEC installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    E_Bess = st.slider("Capacità dell'accumulatore installata (MWh)",min_value=float(0), max_value=float(20),step = float(0.1))

    with open(filename, "r") as input:
        read = csv.reader(input)
        counter = 0
        for (i,row) in enumerate(read):
            Misto.append({"Time":i,"Totale":(F*float(row[1])+E*float(row[3])+W*float(row[5])),"Consumi":float(row[13]),"SOC":0,"E_bess_t":0,"Incr":0,"Diesel":0})
        #Gestiamo il calcolo Accumulatore - Diesel
        for (i,elem) in enumerate(Misto):
            if i != 0:
                #abbiamo energia in ecccesso
                if elem["Consumi"] - elem["Totale"] < 0:
                   #abbiamo spazio nell'accumulatore
                   if Misto[i-1]["SOC"] < 1:
                        #Lo spazio nell'accumulatore è sufficiente
                        if (1-Misto[i-1]["SOC"])*E_Bess > abs(elem["Totale"] - elem["Consumi"])*n:
                            elem["SOC"] = Misto[i-1]["SOC"] + ((abs(elem["Totale"] - elem["Consumi"])*n)/E_Bess)
                            elem["Incr"] = (elem["SOC"] - Misto[i-1]["SOC"]) * E_Bess
                        #Lo spazio nell'accumulatore si riempie
                        else:
                            elem["SOC"] = 1
                            elem["Incr"] = (elem["SOC"] - Misto[i-1]["SOC"]) * E_Bess
                   else:
                       elem["SOC"] = 1
                       elem["Incr"] = (elem["SOC"] - Misto[i-1]["SOC"]) * E_Bess
                #ci manca dell'energia
                else:
                    #abbiamo energia accumulata
                    if Misto[i-1]["SOC"] > 0:
                        #L'accumulatore basta per quello che serve nell'ora
                        if (Misto[i-1]["SOC"])*E_Bess > (elem["Consumi"] - elem["Totale"])/n:
                            elem["SOC"] = Misto[i-1]["SOC"] - (elem["Consumi"] - elem["Totale"])/(E_Bess*n)
                            elem["Incr"] = (elem["SOC"] - Misto[i-1]["SOC"]) * E_Bess
                        #Nell'accumulatore non abbiamo abbastanza energia
                        else:
                            elem["Diesel"] = (elem["Consumi"] - elem["Totale"]) - ((Misto[i-1]["SOC"])*E_Bess*n)
                            elem["SOC"] = 0
                            elem["Incr"] = (elem["SOC"] - Misto[i-1]["SOC"]) * E_Bess
                            Produzione_Diesel += elem["Diesel"]
                    #non abbiamo energia nell'accumulatore
                    else:
                        elem["Diesel"] = (elem["Consumi"] - elem["Totale"])
                        Produzione_Diesel += elem["Diesel"]
            #siamo nella prima riga
            else:
                #abbiamo energia in ecccesso
                if elem["Consumi"] - elem["Totale"] < 0:
                    #Lo spazio nell'accumulatore è sufficiente
                    if E_Bess > abs(elem["Totale"] - elem["Consumi"]):
                        elem["SOC"] = (abs(elem["Totale"] - elem["Consumi"])/E_Bess)
                        elem["Incr"] = (elem["SOC"]) * E_Bess
                    #Lo spazio nell'accumulatore si riempie
                    else:
                        elem["SOC"] = 1
                        elem["Incr"] = (elem["SOC"]) * E_Bess
                #ci manca dell'energia - accumulatore scarico per forza
                else:
                    elem["Diesel"] = (elem["Consumi"] - elem["Totale"])
                    Produzione_Diesel = elem["Diesel"]
            if elem["Incr"] > 0:
                Tot_incr += elem["Incr"]
            if abs(elem["Incr"]) > Max_Pow:
                Max_Pow = abs(elem["Incr"])
        data_chart = pd.DataFrame(
            Misto,
            columns=["Time","SOC","Diesel"]
        )
        accumulatore_tab = pd.DataFrame(
            Misto,
            columns=["Time","Totale","SOC","Consumi","Diesel"]
        )
        st.header("Andamento :green[accumulatore]")
        st.line_chart(data = data_chart, x = "Time", y = "SOC")
        st.header("Andamento Produzione :red[Diesel] (MW)")
        st.line_chart(data = data_chart, x = "Time", y = "Diesel")
        col1, col2, col3 = st.columns(3)
        col1.metric("Numero di Cicli", round(Tot_incr/E_Bess,2))
        col2.metric("Potenza dell'accumulatore", round(Max_Pow,2))
        col3.metric("Durata Accumulatore", round(E_Bess/Max_Pow,1))
        with st.expander("Tabella Dati Accumulatore"):
            st.header("Dati dell'Accumulatore")
            st.table(accumulatore_tab)
