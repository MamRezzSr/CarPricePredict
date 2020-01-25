from bs4 import BeautifulSoup
import requests
import re
import jdatetime
import mysql.connector

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='cpp')
cursor = cnx.cursor()
resultbrands = requests.get("https://www.khodrobank.com/Cars")
soupbrands = BeautifulSoup(resultbrands.text, "html.parser")
brands = soupbrands.find_all("span", attrs={"class": "KB-brands-span"})
brandslinks = soupbrands.find_all("a", attrs={"class": "KB-brands-box"})
for brand,brandlink in zip(brands, brandslinks):
    brandlink="https://www.khodrobank.com"+brandlink.get("href")
    resultcars = requests.get(brandlink)
    soupcars = BeautifulSoup(resultcars.text, "html.parser")
    cars = soupcars.find_all("a", attrs={"class": "KB-Group-link"})
    for car in cars[::2]:
        commit = True
        carlink = "https://www.khodrobank.com/Cars/"+car.get("href")
        resultcar = requests.get(carlink)
        soupcar = BeautifulSoup(resultcar.text, "html.parser")
        year = soupcar.find_all("span", attrs={"id": "MainContent_lbl_car_year"})
        try:
            year = int(year[0].text)
            if year<1500:
                j = jdatetime.date(year,1,1).togregorian()
                year = j.year
        except:
            commit = False
        motor = soupcar.find_all("span", attrs={"id": "MainContent_lbl_car_cc"})
        motor = re.match(r"\d+",motor[0].text)
        try:
            motor = int(motor[0])
        except:
            commit = False
        weight = soupcar.find_all("span", attrs={"id": "MainContent_lbl_car_weight"})
        weight = re.match(r"\d+",weight[0].text)
        try:
            weight = int(weight[0])
        except:
            commit = False
        pricemin = soupcar.find_all("span", attrs={"id": "MainContent_lbl_car_price_new_min"})
        pricemax = soupcar.find_all("span", attrs={"id": "MainContent_lbl_car_price_new_max"})
        try:
            price = (int(pricemin[0].text)+int(pricemax[0].text))/2
        except:
            commit = False
        if (price!=0 and commit):
            print(brand.text, year, motor, weight, price)
            cursor.execute("INSERT INTO cars VALUES(\'"+brand.text+"\',"+str(year)+","+str(motor)+","+str(weight)+","+str(price)+")")
            cnx.commit()
cursor.close()
cnx.close()