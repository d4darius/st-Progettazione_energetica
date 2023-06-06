import streamlit as st
import csv
import pandas as pd
import math

def calculus(E,F,W,E_Bess,filename):
    Misto = []
    n = math.sqrt(0.90)
    Prod_eolico = 0
    Prod_solare = 0
    Prod_WEC = 0
    Prod_totale = 0
    Consumo_totale = 0
    Produzione_Diesel = 0

    with open(filename, "r") as input:
        read = csv.reader(input)
        counter = 0
        for (i,row) in enumerate(read):
            Misto.append({"Time":i,"Solare":F*float(row[1]),"Eolico":E*float(row[3]),"WEC":W*float(row[5]),"Totale":(F*float(row[1])+E*float(row[3])+W*float(row[5])),"Consumi":float(row[13]),"SOC":0,"E_bess_t":0,"Diesel":0})
            Prod_eolico = Prod_eolico + E*float(row[3])
            Prod_solare = Prod_solare + F*float(row[1])
            Prod_WEC = Prod_WEC + W*float(row[5])
            Prod_totale = Prod_totale + F*float(row[1])+E*float(row[3])+W*float(row[5])
            Consumo_totale += float(row[13])
            counter += 1
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
                        #Lo spazio nell'accumulatore si riempie
                        else:
                            elem["SOC"] = 1
                   #gestione energia persa
                   else:
                       elem["SOC"] = 1
                #ci manca dell'energia
                else:
                    #abbiamo energia accumulata
                    if Misto[i-1]["SOC"] > 0:
                        #L'accumulatore basta per quello che serve nell'ora
                        if (Misto[i-1]["SOC"])*E_Bess > (elem["Consumi"] - elem["Totale"])/n:
                            elem["SOC"] = Misto[i-1]["SOC"] - (elem["Consumi"] - elem["Totale"])/(E_Bess*n)
                        #Nell'accumulatore non abbiamo abbastanza energia
                        else:
                            elem["Diesel"] = (elem["Consumi"] - elem["Totale"]) - ((Misto[i-1]["SOC"])*E_Bess*n)
                            elem["SOC"] = 0
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
                    #Lo spazio nell'accumulatore si riempie
                    else:
                        elem["SOC"] = 1
                #ci manca dell'energia - accumulatore scarico per forza
                else:
                    elem["Diesel"] = (elem["Consumi"] - elem["Totale"])
                    Produzione_Diesel = elem["Diesel"]
    #Penetrazione FER
    Pen_FER = (1-(Produzione_Diesel/Consumo_totale))*100
    return Pen_FER

if __name__ == "__main__":
    st.title("Consumi e Potenze installate")

    isola = st.selectbox("Seleziona l'isola",["Ponza","Belep"])


    if isola == "Ponza":
        filename = "Energetica.csv"
    if isola == "Belep":
        filename = "EnergeticaB.csv"

    Misto = []
    n = math.sqrt(0.90)
    E = 1
    F = 1
    W = 1
    E_Bess = 1
    CF_eolico = 0
    CF_solare = 0
    CF_WEC = 0
    Prod_eolico = 0
    Prod_solare = 0
    Prod_WEC = 0
    Prod_totale = 0
    Consumo_totale = 0
    Energia_persa = 0
    Produzione_Diesel = 0

    st.text("Scegli la quantità di potenza installata")
    E = st.slider("Eolico installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    F = st.slider("Fotovoltaico installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    W = st.slider("WEC installato (MW)",min_value=float(0), max_value=float(10),step = float(0.1))
    E_Bess = st.slider("Capacità dell'accumulatore installata (MWh)",min_value=float(0), max_value=float(20),step = float(0.1))

    with open(filename, "r") as input:
        read = csv.reader(input)
        counter = 0
        for (i,row) in enumerate(read):
            Misto.append({"Time":i,"Solare":F*float(row[1]),"Eolico":E*float(row[3]),"WEC":W*float(row[5]),"Totale":(F*float(row[1])+E*float(row[3])+W*float(row[5])),"Consumi":float(row[13]),"SOC":0,"E_bess_t":0,"Diesel":0})
            CF_eolico += float(row[3])
            CF_solare += float(row[1])
            CF_WEC += float(row[5])
            Prod_eolico = Prod_eolico + E*float(row[3])
            Prod_solare = Prod_solare + F*float(row[1])
            Prod_WEC = Prod_WEC + W*float(row[5])
            Prod_totale = Prod_totale + F*float(row[1])+E*float(row[3])+W*float(row[5])
            Consumo_totale += float(row[13])
            counter += 1
        CF_eolico = CF_eolico/counter
        CF_solare = CF_solare/counter
        CF_WEC = CF_WEC/counter
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
                        #Lo spazio nell'accumulatore si riempie
                        else:
                            elem["SOC"] = 1
                    #gestione energia persa
                    else:
                        elem["SOC"] = 1
                #ci manca dell'energia
                else:
                    #abbiamo energia accumulata
                    if Misto[i-1]["SOC"] > 0:
                        #L'accumulatore basta per quello che serve nell'ora
                        if (Misto[i-1]["SOC"])*E_Bess > (elem["Consumi"] - elem["Totale"])/n:
                            elem["SOC"] = Misto[i-1]["SOC"] - (elem["Consumi"] - elem["Totale"])/(E_Bess*n)
                        #Nell'accumulatore non abbiamo abbastanza energia
                        else:
                            elem["Diesel"] = (elem["Consumi"] - elem["Totale"]) - ((Misto[i-1]["SOC"])*E_Bess*n)
                            elem["SOC"] = 0
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
                    #Lo spazio nell'accumulatore si riempie
                    else:
                        elem["SOC"] = 1
                #ci manca dell'energia - accumulatore scarico per forza
                else:
                    elem["Diesel"] = (elem["Consumi"] - elem["Totale"])
                    Produzione_Diesel = elem["Diesel"]
    #Penetrazione FER
    Pen_FER = (1-(Produzione_Diesel/Consumo_totale))*100

    #Plotter del grafico dei consumi
    data_misti = pd.DataFrame(
        Misto,
        columns=["Time","Solare","Eolico","WEC","Totale","Consumi"]
    )

    #Grafici valori
    st.header("Curva :green[Customizzata] di tutte le potenze annuali")
    st.markdown("Totali FER")
    st.line_chart(data=data_misti, x = 'Time', y = ["Totale","Consumi"])
    st.markdown("FER divise")
    st.line_chart(data=data_misti, x = 'Time', y = ["Consumi","Solare","Eolico","WEC"])

    #Metrica dei valori
    st.header("Valori finali :blue[FER]:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Eolico", f"{round(Prod_eolico)} MWh", CF_eolico)
    col2.metric("Solare", f"{round(Prod_solare)} MWh", CF_solare)
    col3.metric("WEC", f"{round(Prod_WEC)} MWh", CF_WEC)
    col4, col5 = st.columns(2)
    col4.metric("Produzione totale",f"{round(Prod_totale)} MWh")
    col5.metric("Energia Persa",f"{round((Prod_totale+Produzione_Diesel)-Consumo_totale)} MWh")
    col6, col7 = st.columns(2)
    col6.metric("Consumo Totale",f"{round(Consumo_totale)} MWh")
    col7.metric("Produzione Diesel",f"{round(Produzione_Diesel)} MWh")
    st.metric("Penetrazione FER", f"{round(Pen_FER,2)} %")

    st.header("Configuration matrix")
    flag = st.button("Press To start")
    if flag:
        Matrix = []
        for eol in range(0,3):
            for sol in range(0,3):
                for WEC in range(0,3):
                    for Acc in range(1,50):
                        Penfer = calculus(eol,sol,WEC,Acc,filename)
                        Matrix.append({"E":eol,"S":sol,"W":WEC,"Acc":Acc,"P_fer":float(Penfer)})
        data_ott = pd.DataFrame(
        Matrix,
        columns=["E","S","W","Acc","P_fer"]
        )
        st.vega_lite_chart(data_ott,{
            'mark': {'type': 'circle', 'tooltip': True},
            'encoding': {
            'size': {'field': 'E', 'type': 'quantitative'},
            'color': {'field': 'S', 'type': 'quantitative'},
            "shape": {'field': 'W', 'type': 'quantitative'},
            'x': {'field': "Acc", 'type': 'quantitative'},
            'y': {'field': 'P_fer', 'type': 'quantitative'}
            },
        })





