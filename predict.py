from sklearn import tree
import mysql.connector

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='cpp')
cursor = cnx.cursor()
cursor.execute("SELECT * FROM cars group by name")

clf = tree.DecisionTreeClassifier()
X = list()
Y = list()
carcode = dict()
counter = 1

print("List of brands")

for (name, year, motor, weight, price) in cursor:
    carcode[name]=counter
    print("-",name)
    counter+=1
    
cursor.execute("SELECT * FROM cars")
for (name, year, motor, weight, price) in cursor:
    X.append([carcode[name], year, motor, weight])
    Y.append(price)
  
clf = clf.fit(X, Y)

NAME = carcode[input("Brand: ")]
YEAR = int(input("Year(Gregorian): "))
MOTOR = int(input("Motor(CC): "))
WEIGHT = int(input("Weight(KG): "))
LIST = [NAME, YEAR, MOTOR, WEIGHT]

answer = clf.predict([LIST])
print("Car Price is: ",answer[0])