import sqlite3
import pandas as pd
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression

conn = sqlite3.connect("DB.db")
cursor = conn.cursor()


def str_to_datetime(date):
    year = date.split('-')[0]
    month = date.split('-')[1]
    day = date.split('-')[2]
    dt = datetime.datetime(int(year), int(month), int(day))
    return dt


def lin_reg(product, date_start, date_end):
    sql = f"""
    SELECT * 
    FROM sales 
    WHERE product LIKE ('{product}') 
    AND date BETWEEN '{date_start}' AND '{date_end}'"""
    date1 = str_to_datetime(date_start)
    date2 = str_to_datetime(date_end)

    amount = np.array(pd.read_sql(sql, conn).get("amount")).reshape(-1, 1)
    date = pd.read_sql(sql, conn)
    date["date"].astype('str')
    date = list(date["date"])
    for i in range(len(date)):  # Получаем массив целых чисел - разница количества дней date и date_start
        if str_to_datetime(date[i]) != date1:
            date[i] = str_to_datetime(date[i]) - date1
            date[i] = int(str(date[i]).split(' ')[0])
        else:
            date[i] = 0
    date = np.array(date).reshape(-1, 1)

    model = LinearRegression()  # МНК
    model.fit(date, amount)
    k = model.coef_
    b = model.intercept_
    return float(k), float(b)


product = "Q"
date_start = "2019-01-01"
date_end = "2019-03-31"
answer = lin_reg(product, date_start, date_end)
k = str(answer[0])
b = str(answer[1])

res3_txt = open("res3.txt", "w")
res3_txt.write(k + " " + b)  # Запись в файл через пробел. Сначала k, потом b
res3_txt.close()

print(k, b)

cursor.close()
conn.close()
