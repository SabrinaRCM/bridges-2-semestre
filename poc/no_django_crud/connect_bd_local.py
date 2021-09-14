#import pymsql
import pandas as pd
import sqlite3

# dados do base mysql

'''connection = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='bridges_dev',
                                     password='123456')'''

# setando comando run_statement para rodar INSERT/UPDATE etc.

#run_statement = connection.cursor()

# necessario usar "connection.commit()" ao final da chamada


data = pd.read_excel (r'C:\Users\arthu\OneDrive\Área de Trabalho\pasta do pi\bridges\src\modelo_excel.xlsx')
data.to_sql('')

'''N = pd.DataFrame(data, columns= ['N'])
issues = pd.DataFrame(data, columns= ['Issues/tarefa'])
tipo = pd.DataFrame(data, columns= ['Tipo'])
prioridade = pd.DataFrame(data, columns= ['Prioridade'])'''

#nome = 'João Silva'
#horas = 220
print(data)
#run_statement.execute("INSERT INTO polls.daniel(name) VALUES('%s')" %(nome))
#connection.commit()