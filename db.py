import sqlite3

conn = sqlite3.connect('Language.db')
c = conn.cursor() 
c.execute('''CREATE TABLE LANGUAGE
             ([generated_id] INTEGER PRIMARY KEY,[Recongnised_Text] text)''')
c.execute('''CREATE TABLE TRANSLATED
             ([generated_id] INTEGER PRIMARY KEY,[Translated_Text] text)''')
                 
                 
conn.commit()
