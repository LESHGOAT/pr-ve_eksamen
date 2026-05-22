# import mysql.connector
# import os
# from dotenv import find_dotenv, load_dotenv

# dotenv_path = find_dotenv()
# load_dotenv(dotenv_path)

# env_User = os.getenv("user")
# env_Password = os.getenv("password")
# env_Host = os.getenv("host")

# try:
#     conn = mysql.connector.connect(
#         host=env_Host,
#         user=env_User,
#         password=env_Password
#     )
#     mycursor = conn.cursor()
#     mycursor.execute("CREATE DATABASE IF NOT EXISTS mat_oppskrift;")
#     print("Database klar!")
# except Exception as e:
#     print("Kunne ikke koble til MySQL:", e)

# try:
#     conn = mysql.connector.connect(
#         host=env_Host,
#         user=env_User,
#         password=env_Password,
#         database="mat_oppskrift"
#     )
#     mycursor = conn.cursor()
#     mycursor.execute("""
#         CREATE TABLE IF NOT EXISTS oppskrift (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             name VARCHAR(255),
#             ingredienser TEXT,
#             fremgangsmåte TEXT,
#             koketid FLOAT(3,2) CHECK(koketid <= 99 AND koketid >= 0.01),
#             prsjoner INT
#         )
#     """)
#     print("Tabell klar!")

#     sql = "INSERT INTO oppskrift (name, ingredienser, fremgangsmåte, koketid, prsjoner) VALUES (%s, %s, %s, %s, %s)"
#     val = [
#         ("Spaghetti Carbonara", "Spaghetti, egg, bacon, parmesan", "Kok pasta, stek bacon, bland alt med egg og ost", 0.25, 2),
#         ("Taco", "Kjøttdeig, tacokrydder, lefser, salat, ost", "Stek kjøttdeig, legg i lefser med tilbehør", 0.30, 3),
#         ("Pannekaker", "Mel, melk, egg, sukker", "Bland alt og stek i panne", 0.20, 4)
#     ]

#     mycursor.executemany(sql, val)
#     conn.commit()
#     print(mycursor.rowcount, "oppskrifter lagt til!")

# except Exception as e:
#     print("Feil:", e)
# finally:
#     if conn.is_connected():
#         conn.close()
