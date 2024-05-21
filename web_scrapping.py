from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrapping_bps(url, output_file, header1="Kota", header2="Tahun", header3="Data", ascending=True):
    dictData = {
        header1: [],
        header2: [],
        header3: []
    }

    driver = webdriver.Chrome()

    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fancybox-close")))

    closeBanner = driver.find_element(By.CLASS_NAME, "fancybox-close")
    closeBanner.click();

    dataSeries = driver.find_element(By.ID, "yw0").find_elements(By.TAG_NAME, "li")

    paginationLength = len(dataSeries)

    for i in range(paginationLength):
        dataSeries = driver.find_element(By.ID, "yw0")

        pagination = dataSeries.find_elements(By.TAG_NAME, "li")

        pagination = [page.find_element(By.TAG_NAME, "a") for page in pagination]

        headers = driver.find_elements(By.CLASS_NAME, "sorting")
        headers.pop(0)

        table = driver.find_element(By.ID, "tablex")

        tbody = table.find_element(By.TAG_NAME, "tbody")

        listData = tbody.find_elements(By.TAG_NAME, "td")
        kota = listData.pop(0).text

        for (tahun, data) in zip(headers, listData):
            dictData[header1].append(kota)
            dictData[header2].append(int(tahun.text))
            dictData[header3].append(float(data.text.replace("\u2009", "").replace(",", ".")))

        if i == (paginationLength - 1):
            continue
        else:
            pagination[i + 1].click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tablex")))

    driver.quit()
    df = pd.DataFrame(dictData)
    df.sort_values(by=header2, ascending=ascending, inplace=True)

    df.to_csv(output_file, index=False)

def scrapping_opendata(url, output_file, header1="Kota", header2="Tahun", header3="Data", ascending=True):
    dictData = {
        header1: [],
        header2: [],
        header3: []
    }

    driver = webdriver.Chrome()

    driver.get(url)

    time.sleep(15)

    tbody = driver.find_element(By.TAG_NAME, "tbody")

    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        listData = row.find_elements(By.TAG_NAME, "td")

        dictData[header1].append(listData[1].text)
        dictData[header2].append(listData[4].text)
        dictData[header3].append(listData[2].text)

    driver.quit()
    df = pd.DataFrame(dictData)
    df.sort_values(by=header2, ascending=ascending, inplace=True)

    df.to_csv(output_file, index=False)

listBPS = [
    {
        "url": "https://semarangkota.bps.go.id/indicator/23/106/1/garis-kemiskinan.html",
        "output": "Garis_Kemiskinan_Kota_Semarang.csv",
        "header3": "Garis Kemiskinan (Rupiah/Kapita/Bulan)",
    },
    {
        "url": "https://semarangkota.bps.go.id/indicator/23/105/1/jumlah-penduduk-miskin.html",
        "output": "Jumlah_Penduduk_Miskin_Kota_Semarang.csv",
        "header3": "Jumlah Penduduk (Ribu Jiwa)",
    },
    {
        "url": "https://surabayakota.bps.go.id/indicator/23/87/1/garis-kemiskinan.html",
        "output": "Garis_Kemiskinan_Kota_Surabaya.csv",
        "header3": "Garis Kemiskinan (Rupiah/Kapita/Bulan)",
    },
    {
        "url": "https://surabayakota.bps.go.id/indicator/23/89/1/jumlah-penduduk-miskin.html",
        "output": "Jumlah_Penduduk_Miskin_Kota_Surabaya.csv",
        "header3": "Jumlah Penduduk (Ribu Jiwa)",
    }
]
listOpendata = [
    {
        "url": "https://opendata.bandung.go.id/dataset/garis-kemiskinan-di-kota-bandung",
        "output": "Garis_Kemiskinan_Kota_Bandung.csv",
        "header3": "Garis Kemiskinan (Rupiah/Kapita/Bulan)"
    },
    {
        "url": "https://opendata.bandung.go.id/dataset/jumlah-penduduk-miskin-di-kota-bandung",
        "output": "Jumlah_Penduduk_Miskin_Kota_Bandung.csv",
        "header3": "Jumlah Penduduk"
    }
]

for dataWeb in listBPS:
    scrapping_bps(dataWeb['url'], dataWeb['output'], header3=dataWeb['header3'])

for dataWeb in listOpendata:
    scrapping_opendata(dataWeb['url'], dataWeb['output'], header3=dataWeb['header3'])

