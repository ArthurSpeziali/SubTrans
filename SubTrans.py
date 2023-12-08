#Importando as bibliotecas:
from deep_translator import GoogleTranslator, exceptions
import platform
from time import sleep
from os import listdir, path

#Função para enviar mais de uma requisição ao Google Tradutor se as legendas passarem de 5 mil caracteres:
def req_trans(var: list, srt: bool):
    #Cria 4 variaveis.
    #A "temporario" é uma lista que guarda as aquisições antes de 5 mil caracteres.
    #A "requisição", é uma lista que guarda strings que vão ser mandadas direto para o tradutor.
    #A "limite" é um contador para ver se já chegou a 4.500 caracteres.
    #A "swap" é um Bool, onde determina se alguma vez, já passou do limite de 4.500 caracteres.
    #A "last" é definido se o limite for exedido, adiciona-lo ainda, só que depois dos processos feitos:
    
    temporario = list()
    requisição = list()
    limite = 0
    swap = False
    
    #Passa por cada item da lista, e calcula o tamanho da string.
    #Se for menor ao limite de 4.500, adiciona ao temporário, e aumenta o limite para o tamanho da string:
    for i in var:
        if limite < 4500:
            last = ''
            temporario.append(i)
            limite += len(i)
        
        #Se o limite for maior que 4.500, ele define que já passou alguma vez do limite.
        #Além de formatar e mandar todos para a requisição, limpa o temporario.
        #O limite é limpado e somado o tamanho daquele item, e o last é guardado com o valor deste item:
        else:
            swap = True
            
            if srt:
                requisição.append('\n\n'.join(temporario))                
            else:
                requisição.append('\n'.join(temporario))                
            
            temporario = list()
            limite = len(i)
            temporario.append(i)
            last = i

    #Se nunca tiver exedido o limite, adiciona tudo o que está em temporario direto em requisição: 
    if not swap:
        requisição.append('\n\n'.join(temporario))
    
    #Se o ultimo item tiver exedido o limite, ele adcionara este item agora:
    if last != '':
        requisição.append(last)

    #Com um ciclo for ele traduz cada aquisição, e adiciona na "requisição_trans":
    requisição_trans = list()
    for word in requisição:
        
        #Usando o Google tradutor para traduzir:
        word_trans = GoogleTranslator(target=sigla).translate(word)
        requisição_trans.append(word_trans)
        
    return requisição_trans

#Introdução:
print('Seja Bem Vindo ao SubTrans!')
print('By: Arthur Speziali\n')
sleep(1)

print('Este programa traduz as suas legendas para qualquer idioma do mundo!')
print('PS: Ele trabalha com .srt!')
sleep(2)

print('''\nDeseja traduzir 1 legenda, ou uma pasta inteira? 

[M]- Uma legenda:
[R]- Uma pasta de legendas:\n''')

#Escolhendo um arquivo ou um diretório:
while True:
    opção0 = input('').strip().lower()
    
    if opção0 != 'm' and opção0 != 'r':
        print('Opção inválida, tente novamente!')
        
    else:
        break

#Iniciar manual:
if opção0 == 'm':
    while True:
    
        print('\nDigite o caminho até a legenda: ')
        while True:
            pathe = input('').strip()
            
            #Verificando se o caminho esta correto, tentando abrir ele: 
            try:
                with open(pathe, encoding='utf-8') as v_path:
                    print('Caminho bem-sucedido! Continuando...')                
                    break
                    
            except:
                print('\nCaminho mal-sucedido! Tente novamente!\n')
        
        
        #Se o arquivo for .str, ele tem uma formatação difererente do .sub:
        if pathe[-3:] == 'srt':
            with open(pathe, encoding='utf-8') as sub_srt:
                read_sub = sub_srt.read().split('\n\n')
                srt = True
                
        elif pathe[-3:] == 'sub':
            with open(pathe, encoding='utf-8') as sub_srt:
                read_sub = sub_srt.read().split('\n')
                srt = False
        
        #Se não for nenhum dos dois arquivos, ele fecha:
        else:
            print('Arquivos não suportados (.str .sub). Saindo!')
            exit()
                
        print('\nQual é a sigla para traduzir? (pt, en, fr... etc)')
        
        #Escolhendo uma sigla de idioma, e testanto ela para ver se existe:
        while True:
            sigla = input('').lower().strip()
            
            try: 
                word_trans = GoogleTranslator(target=sigla).translate('Hello')
                break
            
            except:
                print('196mSigla não suportada, tente novamente!\n')
        
        print('\nAguarde, estamos traduzindo! ')
        

        #Detectando o SO do usuario para usar a barra correta na hora de procurar caminho de diretórios:
        if platform.system()== 'Windows':
            
            #O "chr(92)" é para simbolizar esta barra: "\", usada para windows:
            barra = chr(92)
        else:
            #Este já é usado para linux e demais:
            barra = '/'

        #Usando o sistema para processar o nome e o diretório onde o novo arquivo será criado:
        #A "custom_path" é o nome do arquivo com extensão:
        custom_path = pathe.split(barra)[-1]
        #A "ext" é somente a extensão do arquivo:
        ext = '.' + custom_path.split('.')[1]
        #Agora a custom_path é só o nome do arquivo:
        custom_path = custom_path[:-4]
        #A "def_path" é o caminho para o arquivo:
        def_path = pathe.split(custom_path + ext)
        def_path.pop()
        def_path = ''.join(def_path)
        #A "name" é o novo nome com extensão para o arquivo:
        name = custom_path + '-' + sigla.upper() + ext 
        
        #Criando/limpando o arquivo de destino com o nome personalizado:
        with open(def_path + name, 'w', encoding='utf-8') as new_sub_w:
            new_sub_w.write('')

        #Criando o arquivo e escrevendo a legenda traduzida, chamando a função "req_trans":            
        with open(def_path + name, 'a', encoding='utf-8') as new_sub_a:
            for i in req_trans(read_sub, srt):
                new_sub_a.write('\n' + i + '\n')
            
        #Aperte Enter para continuar, e CTRL + C para sair:
        print('Concluido! Deseja traduzir mais legendas? Aperte enter!')
        continuar = input()

elif opção0 == 'r':
    
    print('\nDigite o caminho até a pasta: ')
    while True:
        pathe = input('').strip()
        
        try:
            #Criando um arquivo "cache" para ver se a pasta realmente existe:
            with open(pathe + r'\cache', 'w', encoding='utf-8') as v_path:
                v_path.write('Cache temporario!')
                
                print('Caminho bem-sucedido! Continuando...')
                break
                
        except FileNotFoundError:
            print('\nCaminho mal-sucedido! Tente novamente!\n')
            
            
    print('\nQual é a sigla para traduzir? (pt, en, fr... etc)')
    while True:
        sigla = input().lower().strip()
        
        try: 
            word_trans = GoogleTranslator(target=sigla).translate('Hello')
            break
        
        except:
            print('Sigla não suportada, tente novamente!\n')
    
    print('\nAguarde, estamos traduzindo!')
    
    #Usando o "listdir" do "os", para me listar todos os arquivos de uma pasta.
    #Depois com o for, coloca o conteudo delas no "content". Só faz isto se o arquivo for .sub ou .srt!:
    for arq in listdir(pathe):
        if arq.endswith('.txt') or arq.endswith('.srt') or arq.endswith('.sub'):
            with open(path.join(pathe, arq), 'r', encoding='utf-8') as folder:
                
                if arq.endswith('.srt'):
                    content = folder.read().split('\n\n')
                    srt = True
                    
                elif arq.endswith('.sub'):
                    content = folder.read().split('\n')
                    srt = False
                
                else:
                    print('Arquivos não suportados (.str .sub). Saindo!')
                    exit()
                
                if platform.system()== 'Windows':
                    barra = chr(92)
                else:
                    barra = '/'

                with open(pathe + barra + sigla.upper() + '-' + arq, 'w', encoding='utf-8') as new_sub_w:
                    new_sub_w.write('')
                    
                with open(pathe + barra + sigla.upper() + '-' + arq, 'a', encoding='utf-8') as new_sub_a:
                    for i in req_trans(content, srt):
                        new_sub_a.write('\n' + i + '\n')
                    
                print(f'Arquivo: {arq} TRADUZIDO! ')
                
    print('Pasta traduzida, obrigado por usar! ')
