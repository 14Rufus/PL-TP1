import re

'''
    Função que, recorrendo ao uso de um search, analisa se o campo é, ou não, um inteiro.
'''
def isInt (dados):
        return re.search(r'^(-)?[0-9]+$', dados)

'''
Função que, recorrendo ao uso de um search, analisa se o campo é uma lista do tipo 1, isto é, do tipo com tamanho fixo (Notas{4}).
'''
def isList1 (dados): 
        return re.search(r'\w+{\d}', dados)  #[A-Za-z]

'''
Função que, recorrendo ao uso de um search, analisa se o campo é uma lista do tipo 2, isto é, do tipo com tamanho variável (Notas{2,4}).
'''
def isList2 (dados): 
        return re.search(r'\w+{\d', dados)  #[A-Za-z] \w+{\d,\d}

'''
Função que, recorrendo ao uso de um search, analisa se o campo é o segundo parâmetro do tipo de lista 2. Isto é, numa lista Notas{2,4}, 
testa se nos encontramos no campo a seguir à vírgula (4}). Serve como despiste na análise de casos da função principal.
'''
def extraList2 (dados): #campo extra do tipo de lista 2 {2,4} -> 4}
        return re.search(r'\d}', dados)

''' 
Função que recebe duas strings. A primeira corresponde aos dados da lista truncada (dados) e a segunda é o nome do campo (campo) 
a que diz respeito. Usando a função split, separa-se a string dos dados pelo separator_lista armazenando a informação numa lista de
float. Usando a função sum e len aplicadas à anterior lista calculamos a média dos dados. Usando a função sub substituimos no argumento 
campo a parte ”{4}::avg” por ”_avg”, retornando, por fim, o argumento campo, seguido pela variável calculada ”media” em formato de String.
'''
def calculaAvg(dados, campo):
    lista = list()
    for dado in dados:
       if isInt(dado):
            lista.append (int(dado))
       else:
            pass
    media = round (sum(lista)/len(lista), 2) # round (x,2) maximiza a media em 2 casas decimais
    campo = re.sub(r'{\d+(}::avg)?', r'_avg', campo)
    return ("\"" + campo + "\": " + str(media))


'''
Função que recebe duas strings. A primeira corresponde aos valores da lista (dados) e a segunda ao nome do campo (campo) 
a que diz respeito. Através de um ciclo for retiramos os valores da lista do respetivo campo do ficheiro CSV, 
colocando-os numa nova lista ("lista"). Usando a função sum aplicada à anterior lista calculamos a soma dos dados. 
Usando a função sub substituimos no argumento campo a parte ”{4}::sum” por ”_sum”, retornando, por fim, o argumento campo, 
seguido pela variável calculada ”soma” em formato de String.
'''
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


'''
Função responsável por ler os dados do ficheiro CSV e escrevê-los no ficheiro JSON. O ficheiro CSV é aberto com a função pré-definida open, com o modo de codificação binária ”UTF-8”ativo. É aberto um descritor de ficheiro em modo de escrita para o ficheiro JSON com o nome passado no segundo input da função principal, caso este ficheiro não exista é criado um novo. 

É lida a primeira linha do ficheiro CSV com a função pré-definida readLine, que vai ignorar qualquer espaço no início e fim desta, devido à função pré-definida strip. 

É separada e colocada numa lista pela função split, com o separador definido na função principal (terceiro input).
Esta lista vai ser guardada numa variável campos responsável por indicar a que correspondem os valores que vêm nas linhas seguintes.

De seguida cada linha do ficheiro é lida individualmente e é feito o seu split pelo separator passado, sendo, também, ignorados quaisquer espaços existentes no início ou fim da mesma. Os dados são guardados numa variável valores, que é uma lista de elementos do tipo String.

Entramos, assim, na verificaçao do caso em que o nosso ficheiro CSV se encontra. Temos 3 casos principais: o caso em que o input não se insere em nenhum dos tipos de lista; o caso em que se insere no tipo de lista 1 (Notas{4}) e o caso em que se insere no tipo de lista 2 (Notas{2,4}). Dentro dos casos das listas entraremos em 3 outros casos: o primeiro é no caso de encontrar uma funcao de agregação de soma; o segundo é a função de agregação da média e o terceiro é o caso em que nenhuma função de agregação está presente. 

Em cada um dos casos, as respetivas funções definidas por nós são chamadas e a informação é processada tendo isso em conta e
depois adicionada à variável "output". Por fim, de forma a terminar o processo, a informação contida
na variável output é escrita no ficheiro JSON pretendido.

Recorrendo ao funcionamento do programa como um script, de seguida pedem-se dois inputs ao utilizador: - O nome do ficheiro CSV a ler; - O nome do ficheiro JSON onde a informação vai ser escrita, caso o ficheiro JSON não exista, então é criado um com o nome dado no segundo input. Após a receção destes parâmetros, é chamada a função "converter" com os mesmos, sendo que ela é responsável por executar a transformação dos dados entre ficheiros. No final é impressa uma mensagem a notificar se a conversão for bem executada,
e é criado o ficheiro JSON correspondente.
'''
def converter (csv, fileOutput, separator):
        file = open(csv, encoding="utf8")
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

                                else:
                                        result = re.search(r'(\d+)', campos[i])
                                        x=0
                                        output += ("\"" + campos[i] + "\":" + "[")
                                        while (x+1<int(result.group(1))): 
                                                output +=( valores[i+x] + ",")
                                                x+=1
                                        #add ,
                                        output += (valores[i+x]+"],\n")
                                        output = re.sub(r'{\d+}','', output)
                                        if (not(campos[i+1] == '')):
                                                output += ",\n"
                        
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

                                else:
                                        r2 = int ((re.search(r'(\d+)', campos[i+1])).group(1)) #4}

                                        x=0 
                                        output += ("\"" + campos[i] + "," + campos[i+1] + "\":" + "[")
                                        while (x+1 < r2):
                                                output += ( valores[i+x] + ",")
                                                x+=1
                                        #add ,
                                        output += (valores[i+x] +"],\n")                        
                                        output = re.sub(r'{\d+,\d+}','', output)
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