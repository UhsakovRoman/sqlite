import sqlite3

conn = sqlite3.connect("DB.db")
cursor = conn.cursor()

# Пункт 1. Вывел в файл таблицу с актуальной датой и средней ценой по каждому продукту
# в порядке возрастания по имени продукта
sql = """
SELECT product, price, max(date_start), avg(price)
FROM prices
GROUP BY product
ORDER BY product ASC
"""
result = cursor.execute(sql)
res1_txt = open("res1.txt", "w")
res1_txt.write("Запрос: \n" + sql + "\n")
res1_txt.write("Строки с актуальными ценами и средней ценой по каждому продукту:\n\n"
               "Product|Price|Date_start|Average price\n")
for row in result:
    res1_txt.write(str(row) + "\n")  # Вывод в файл построчно
res1_txt.close()


# Пункт 2. Функция - на вход имя продукта, на выход все цены с датами по этому продукту в порядке возрастания.
def func(name):
    date = f"""
        SELECT date_start
        FROM prices
        WHERE product LIKE('{name}')
        ORDER BY date_start ASC
    """
    cursor.execute(date)
    res1 = cursor.fetchall()

    price = f"""
        SELECT price
        FROM prices
        WHERE product LIKE('{name}')
        ORDER BY date_start ASC
        """
    cursor.execute(price)
    res2 = cursor.fetchall()
    return tuple([res1] + [res2])


# name = input("Введите имя продукта \n")
name = "Z"  # Тут указывается имя продукта, которое подается на вход функции
x = func(name)
print(x)
print(type(x))  # <class 'tuple'>

cursor.close()
conn.close()
