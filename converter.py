import re
import csv

def isInt (dados):
        return re.search(r'^(-)?[0-9]+$', dados)

def isList1 (dados): 
        return re.search(r'\w+{\d}', dados)  #[A-Za-z]

def isList2 (dados): 
        return re.search(r'\w+{\d', dados)  #[A-Za-z] \w+{\d,\d}

def extraList2 (dados): #campo extra do tipo de lista 2 {2,4} -> 4}
        return re.search(r'\d}', dados)

def calculaAvg(dados, campo):
    lista = list()
    for dado in dados:
       if isInt(dado):
            lista.append (int(dado))
       else:
            pass
    media = sum(lista)/len(lista)
    campo = re.sub(r'{\d+(}::avg)?', r'_avg', campo)
    return ("\"" + campo + "\": " + str(media))


def calculaSum(dados, campo):
    lista = list()
    for dado in dados:
       if isInt(dado):
            lista.append (int(dado))
       else:
            pass
    soma = sum(lista)
    campo = re.sub(r'{\d+(}::sum)?', r'_sum', campo)
    return ("\"" + campo + "\": " + str(soma))


#### EXTRAS #####
def calculaMax(dados, campo):
    lista = list()
    for dado in dados:
       if isInt(dado):
            lista.append (int(dado))
       else:
            pass
    maximo = max(lista)
    campo = re.sub(r'{\d+(}::max)?', r'_max', campo)
    return ("\"" + campo + "\": " + str(maximo))


def calculaMin(dados, campo):
    lista = list()
    for dado in dados:
       if isInt(dado):
            lista.append (int(dado))
       else:
            pass
    minimo = min(lista)
    campo = re.sub(r'{\d+(}::min)?', r'_min', campo)
    return ("\"" + campo + "\": " + str(minimo))
################################################



def converter (csv, fileOutput, separator):
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

                        if isList1(campos[i]):
                                
                                if re.search(r'[Aa][Vv][Gg]', campos[i]):
                                        valor = valores[i:]
                                        output += calculaAvg(valor, campos[i])
                                        output += ",\n"
                                elif re.search(r'[Ss][Uu][Mm]', campos[i]):
                                        valor = valores[i:]
                                        output += calculaSum(valor, campos[i])
                                        output += ",\n"
                                elif re.search(r'[Mm][Aa][Xx]', campos[i]):
                                        valor = valores[i:]
                                        output += calculaMax(valor, campos[i])
                                        output += ",\n"

                                elif re.search(r'[Mm][Ii][Nn]', campos[i]):
                                        valor = valores[i:]
                                        output += calculaMin(valor, campos[i])
                                        output += ",\n"

                                else:
                                        result = re.search(r'(\d+)', campos[i])
                                        x=0
                                        output += ("\"" + campos[i] + "\":" + "[")
                                        while (x+1<int(result.group(1))): 
                                                output +=( valores[i+x] + ",")
                                                x+=1
                                        print ("como???")
                                        output += (valores[i+x]+"]\n")
                        
                        elif campos[i] == '':
                                pass
                        elif extraList2(campos[i]):
                                pass
                                
                        elif isList2(campos[i]):

                                if re.search(r'[Aa][Vv][Gg]', campos[i+1]):
                                        valor = valores[i:]
                                        output += calculaAvg(valor, campos[i])
                                        output += ",\n"
                                elif re.search(r'[Ss][Uu][Mm]', campos[i+1]):
                                        valor = valores[i:]
                                        output += calculaSum(valor, campos[i])
                                        output += ",\n"
                                elif re.search(r'[Mm][Aa][Xx]', campos[i+1]):
                                        valor = valores[i:]
                                        output += calculaMax(valor, campos[i])
                                        output += ",\n"

                                elif re.search(r'[Mm][Ii][Nn]', campos[i+1]):
                                        valor = valores[i:]
                                        output += calculaMin(valor, campos[i])
                                        output += ",\n"

                                else:
                                        r2 = int ((re.search(r'(\d+)', campos[i+1])).group(1)) #4}

                                        x=0 
                                        output += ("\"" + campos[i] + "," + campos[i+1] + "\":" + "[")
                                        while (x+1 < r2):
                                                output += ( valores[i+x] + ",")
                                                x+=1
                                        output += (valores[i+x] +"]\n")
                                        output = re.sub(r',+\]',']', output)
                                        
                                        

                        else:
                                output += ("\"" + campos[i] + "\": \"" + valores[i] + "\",\n")           

                output += ("},\n")
        
        output += ("]")

        output = re.sub(r",\n}", r"\n}", output)
        output = re.sub(r"},\n]", r"}\n]", output)
        fileOutput.write(output)    

csv = input('Insira o ficheiro CSV que pretende ler: ')
json = input('Insira o nome do ficheiro JSON que pretende criar: ')

converter(csv, json, ",")
print('Conversão realizada com sucesso!')