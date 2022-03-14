from distutils.command.build_scripts import first_line_re
from locale import atoi
import re
import sys
import ply.lex as lex
import csv

from sqlalchemy import outparam


""" file = open('alunos.csv')

type(file)

csvreader = csv.reader(file)

header = []
header = next(csvreader)

#print (header)

rows = []
for row in csvreader:
        rows.append(row)

#print (rows)
#print (rows[0])



first_line = re.split(r';',header.strip())

def transform (first_line,linha):
    linha = re.split(r',', 'alunos.csv')
    print (linha)
 """


def isInt (dados):
        return re.search(r'^(-)?[0-9]+$', dados)
        
def isNumber (dados):
        return re.search(r'^(-)?[0-9]+(\.[0-9]+)?$', dados)

def isList (dados): #Notas{2} notas trabalhos práticos
        #output -> "Notas" : [12,13],
        return re.search(r'\w+{\d}', dados)  #[A-Za-z]

def calculaAvg(dados, campo, separator_lista):
    lista = re.split(separator_lista, dados)
    for i in range(len(lista)):
        if isInt(lista[i]):
            lista[i] = int(lista[i])
        else:
            lista[i] = float(lista[i])
    media = sum(lista)/len(lista)
    campo = re.sub(r'{\d,\d}::avg', r'_', campo)
    return ("\"" + campo + "\": " + str(media))


def calculaSum(dados, campo, separator_lista):
    lista = re.split(separator_lista, dados)
    for i in range(len(lista)):
       if isInt(lista[i]):
            lista[i] = int(lista[i])
       else:
            lista[i] = float(lista[i])
    soma = sum(lista)
    campo = re.sub(r'{\d,\d}::sum', r'_', campo)
    return ("\"" + campo + "\": " + str(soma))


def converter (csv, fileOutput, separator, separator_lista):
        file = open(csv)
        fileOutput = open(fileOutput, 'w')
        first_line = file.readline()


        campos = re.split(separator, first_line.strip())
        # Numero, Nome, Turno, Notas{2}, '', ''
        output = ""
        output += "[\n"  #inicio da escrita do csv

        for line in file:
                output += ("{\n")
                valores = re.split(separator, line.strip())
                for i in range(len(campos)):
                        if not (isList(campos[i])): 
                                if campos[i] == '':
                                        pass

                                else: output += ("\"" + campos[i] + "\": \"" + valores[i] + "\",\n")
                        elif isList(campos[i]):
                                result = re.search(r'(\d+)', campos[i])
                                #print (result.group(1))
                                x=0
                                output += ("\"" + campos[i] + "\":" + "[")
                                while (x+1<int(result.group(1))): 
                                        output +=( valores[i+x] + ",")
                                        x+=1
                                output += (valores[i+x]+"]\n")

#                        else:
#                                valor = re.sub(r"\(", r"", valores[i])  #re.sub(pattern, repl, string, count=0, flags=0)
#                                valor = re.sub(r"\)", r"", valor)       #Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl. If the pattern isn’t found, string is returned unchanged.                                    
#
#                                #else:
#                                lista = re.split(separator_lista, valor)
#                                campo = re.sub(r'\*', r"", campos[i])
#                                output += ("\"" + campo + "\": ")
#                                output += "["
#                                for index in range(len(lista)):
#                                        output += str(lista[index])
#                                        output += ","
#                                output += "]"
#                                output = re.sub(r',]', r']', output)
#                                output += (",\n")
                output += ("},\n")
        
        output += ("]")

        output = re.sub(r",\n}", r"\n}", output)
        output = re.sub(r"},\n]", r"}\n]", output)
        fileOutput.write(output)    

csv = input('Insira o ficheiro CSV que pretende ler: ')
json = input('Insira o nome do ficheiro JSON: ')

converter(csv, json, ",", ";")
print('Conversão realizada com sucesso!')


""" separator = input('CSV separado por:\n1) ;\n2) ,\n')
if separator == "1":
    converter(csv, json, ";", ",")
    print('Conversão realizada com sucesso!')
elif separator == "2":
    converter(csv, json, ",", ";")
    print('Conversão realizada com sucesso!')
else :
    print("Opção inválida")            
 """                                