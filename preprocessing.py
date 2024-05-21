import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:@localhost/data")

listDataframe = [
    pd.read_csv("Garis_Kemiskinan_Kota_Semarang.csv"),
    pd.read_csv("Jumlah_Penduduk_Miskin_Kota_Semarang.csv"),
    pd.read_csv("Garis_Kemiskinan_Kota_Surabaya.csv"),
    pd.read_csv("Jumlah_Penduduk_Miskin_Kota_Surabaya.csv"),
    pd.read_csv("Garis_Kemiskinan_Kota_Bandung.csv"),
    pd.read_csv("Jumlah_Penduduk_Miskin_Kota_Bandung.csv")
]

listDataframe[0]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"] = listDataframe[0]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"].astype(int)
listDataframe[2]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"] = listDataframe[2]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"].astype(int)

listDataframe[1]["Jumlah Penduduk (Ribu Jiwa)"] = (listDataframe[1]["Jumlah Penduduk (Ribu Jiwa)"] * 1000).astype(int)
listDataframe[1].rename(columns={"Jumlah Penduduk (Ribu Jiwa)": "Jumlah Penduduk"}, inplace=True)
listDataframe[1].drop(listDataframe[1][listDataframe[1]["Tahun"] < 2012].index, inplace=True)
listDataframe[1].reset_index(inplace=True, drop=True)
dataSemarang = listDataframe[1].join(listDataframe[0]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"])

listDataframe[3]["Kota"] = "Kota " + listDataframe[3]["Kota"]
listDataframe[3]["Jumlah Penduduk (Ribu Jiwa)"] = (listDataframe[3]["Jumlah Penduduk (Ribu Jiwa)"] * 1000).astype(int)
listDataframe[3].rename(columns={"Jumlah Penduduk (Ribu Jiwa)": "Jumlah Penduduk"}, inplace=True)
dataSurabaya = listDataframe[3].join(listDataframe[2]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"])

listDataframe[5]["Kota"] = listDataframe[5]["Kota"].str.title()
dataBandung = listDataframe[5].join(listDataframe[4]["Garis Kemiskinan (Rupiah/Kapita/Bulan)"])

dataKemiskinan = pd.concat([dataSemarang, dataSurabaya, dataBandung], ignore_index=True)
dataKemiskinan.sort_values(by=["Tahun", "Kota"], inplace=True)

dataSemarang.to_csv("Data_Semarang.csv", index=False)
dataSurabaya.to_csv("Data_Surabaya.csv", index=False)
dataBandung.to_csv("Data_Bandung.csv", index=False)
dataKemiskinan.to_csv("Kemiskinan_3_Kota.csv", index=False)

dataKemiskinan.to_sql("data_de", con=engine, if_exists="append", index=False)



