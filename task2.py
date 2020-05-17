import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("DB.db")
cursor = conn.cursor()

# Задача довольно простая, будь у этих таблиц связь по id
sql = """
SELECT  DISTINCT s.product AS "product",
        s.date AS "date",
        s.amount AS "amount", 
        s.amount * p1.price AS "revenue"
FROM prices p1, prices p2
LEFT JOIN sales s ON s.product = p1.product
WHERE s.date BETWEEN p1.date_start AND p2.date_start
"""
# Создание таблицы. Закомментил, т.к. уже создана, а с файлом еще работаю.
# create_revenue = f"CREATE TABLE revenues AS {sql}"
# cursor.execute(create_revenue)

product = "B"
query = f"""
SELECT *
FROM revenues
WHERE product LIKE ('{product}')
"""

revenue = pd.read_sql(query, conn)
stdev = np.std(revenue.get("revenue"))
print(stdev)

res2_txt = open("res2.txt", "w")
res2_txt.write(f"Величина выборочного стандартного отклонения для продукта B = {stdev}")

res2_txt.close()
cursor.close()
conn.close()
