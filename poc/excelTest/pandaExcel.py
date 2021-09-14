import pandas as pd


data = pd.read_excel (r'C:\Users\arthu\OneDrive\Área de Trabalho\pasta do pi\bridges\src\modelo_excel.xlsx', header=4)#, header=None
#N = pd.DataFrame(data, columns= ["N"])#Unnamed: 0
issues = pd.DataFrame(data, columns=["Issues/tarefa"])
tipo = pd.DataFrame(data, columns=["Tipo"])

#Thoras/atividade = pd.DataFrame(data, columns=["Total de horas Dev"])

excecao = pd.read_excel(r'C:\Users\arthu\OneDrive\Área de Trabalho\pasta do pi\bridges\src\modelo_excel.xlsx', header=None)
print(excecao.iloc[0,1])
print(excecao.iloc[1,1])


#issues["Unnamed: 1"] = issues["Unnamed: 1"].fillna("")


print("Column headings:")
tipo = tipo.values.tolist()
#print(type(N))


issues = issues.values.tolist()
#print(type(issues))


megazord = zip(issues,tipo)
megazord = list(megazord)
for ranger in megazord:
    print(ranger[0])
    print(ranger[1])


#run_statement.execute("INSERT INTO sabha_bridgesbd.bridges_app_tarefas(nom_tar, fk_pro_id, dur_tar) VALUES('%s', '%s', '%s')" %(word, id_pro, horas))
#print(data)

