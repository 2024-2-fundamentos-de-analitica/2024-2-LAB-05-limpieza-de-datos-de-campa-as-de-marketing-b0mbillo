"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

from zipfile import ZipFile
import pandas as pd
import os

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    dfs = []
    for i in range(10):
        with ZipFile(f"./files/input/bank-marketing-campaing-{i}.csv.zip", "r") as zip_file:
            #print(zip_file.namelist())
            with zip_file.open(f"bank_marketing_{i}.csv") as f:
                df_campaings = pd.read_csv(f)
                dfs.append(df_campaings)
    df_campaings = pd.concat(dfs)
    df_campaings.drop(columns=["Unnamed: 0"], inplace=True)

    df_campaings["job"] = df_campaings["job"].str.replace(".", "").str.replace("-", "_")
    df_campaings["education"] = df_campaings["education"].str.replace(".", "_").replace("unknown", pd.NA)
    df_campaings["credit_default"] = df_campaings["credit_default"].map({"yes": 1}).fillna(0)
    df_campaings["mortgage"] = df_campaings["mortgage"].map({"yes": 1}).fillna(0)

    df_campaings["previous_outcome"] = df_campaings["previous_outcome"].map({"success": 1}).fillna(0)
    df_campaings["campaign_outcome"] = df_campaings["campaign_outcome"].map({"yes": 1}).fillna(0)


    meses_dic = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    df_campaings["month"] = df_campaings["month"].map(meses_dic)

    df_campaings["last_contact_date"] = pd.to_datetime(
        df_campaings["day"].astype(str) + "-" + df_campaings["month"].astype(str) + "-2022", format="%d-%m-%Y"
    )

    df_campaings.drop(columns=["day", "month"], inplace=True)

    #print(df_campaings.columns)
    #print(df_campaings.head())

    df_client = df_campaings[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]]
    df_campaign = df_campaings[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "last_contact_date"]]
    df_economics = df_campaings[["client_id", "cons_price_idx", "euribor_three_months"]]

    os.makedirs("./files/output", exist_ok=True)
    df_client.to_csv("./files/output/client.csv", index=False)
    df_campaign.to_csv("./files/output/campaign.csv", index=False)
    df_economics.to_csv("./files/output/economics.csv", index=False)

if __name__ == "__main__":
    clean_campaign_data()
