from distutils.command.build_scripts import first_line_re
from locale import atoi
import re
import sys
import ply.lex as lex
import csv

from sqlalchemy import outparam


def isInt (dados):
        return re.search(r'^(-)?[0-9]+$', dados)
        
def isNumber (dados):
        return re.search(r'^(-)?[0-9]+(\.[0-9]+)?$', dados)

def isList1 (dados): 
        return re.search(r'\w+{\d}', dados)  #[A-Za-z]

def isList2 (dados): 
        return re.search(r'\w+{\d', dados)  #[A-Za-z] \w+{\d,\d}

def extraList2 (dados): #campo extra do tipo de lista 2 {2,4} -> 4}
        return re.search(r'\d}', dados)

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
                        #print(campos[i])
                        if not (isList1(campos[i])):
                                if campos[i] == '':
                                        pass
                                elif extraList2(campos[i]):
                                        pass
                                
                                elif isList2(campos[i]):
                                        #r1 = int ((re.search(r'(\d+)', campos[i])).group(1)) #{2
                                        r2 = int ((re.search(r'(\d+)', campos[i+1])).group(1)) #4}

                                        x=0 
                                        output += ("\"" + campos[i] + "," + campos[i+1] + "\":" + "[")
                                        while (x+1 < r2):
                                                output += ( valores[i+x] + ",")
                                                x+=1
                                        output += (valores[i+x] +"]\n")
                                        output = re.sub(r',+\]',']', output)
                                        
                                        
                                        
                                        #y=r1#-1
                                        #while (y < r2-1):
                                                #print ("****"+valores[i+y])
                                                #if (valores[i+y] == ''):
                                                       # pass                                                                
                                                #else:
                                                        #output += ( "," + valores[i+y] ) 
                                                        #print("while2:" + valores[i+y])  
                                                       # y+=1
                                        #output += ("," + valores[i+y]+"]\n")
                                        #if (valores[i+y] == ''):
                                                #output += (valores[i+y]+"]\n")
                                        #else:
                                                #output += ("," + valores[i+y]+"]\n")
                                        #print("fim:" + valores[i+y])
                                
                                else:
                                        output += ("\"" + campos[i] + "\": \"" + valores[i] + "\",\n")
                        elif isList1(campos[i]):
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