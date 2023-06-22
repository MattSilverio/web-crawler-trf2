import requests
from bs4 import BeautifulSoup
import json

# links de interesse
links = {
   "base": "https://eproc.trf2.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica",
   "consulta_por_processo": "https://eproc.trf2.jus.br/eproc/externo_controlador.php?acao=processo_seleciona_publica&acao_origem=processo_consulta_publica&acao_retorno=processo_consulta_publica&num_processo="
} 
headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"}



def consulta():
  operation_mode = input("Digite o número correspondente ao método de busca que deseja realizar: \n1- Número do processo\n2- CNPJ\n3- CPF\n4 - Nome da Parte\n5 - Sair\n")
  
  match operation_mode:
      case "1":
          numero_processo = input("Digite o numero do processo: ")
          link_consulta_processo = links["consulta_por_processo"] + numero_processo
          response = requests.get(link_consulta_processo, headers)
          soup = BeautifulSoup(response.text, 'html.parser')
          
          # Executa quando não encontrar processo, caso contrário termina programa
          if(soup.find('span', class_= "infraExcecao")):
             print(numero_processo + " não encontrado")
             exit()

          # Dados de interesse
          capa_do_processo= soup.find('fieldset', id='fldAssuntos')
          [agravante,agravado] = soup.find('fieldset', id='fldPartes').find('tr', class_='infraTrClara')
          tabelas = soup.findAll('table', class_='infraTable', summary="Assuntos")
          movimentacoes_tabela = tabelas[2].findAll('tr')
          
          
          movimentacoes = []
          
          for linha in movimentacoes_tabela:
            dados = linha.findAll('td')
            if(dados != []):
              movimentacoes.append({"data": dados[1].text,"descricao": dados[2].text})

                   

          resumo = {
             "numero_processo": capa_do_processo.find('span', id='txtNumProcesso').text,
             "data_autuacao": capa_do_processo.find('span', id='txtAutuacao').text,
             "situacao": capa_do_processo.find('span', id='txtSituacao').text,
             "envolvidos": {
                "agravante": agravante.text.strip().replace('\xa0',' '),
                "agravado": agravado.text.strip().replace('\xa0',' '),
             },
             "movimentacoes": movimentacoes
          }

          with open('resumo_numero_processo_' + numero_processo + '.json', 'w', encoding='utf-8') as file:
             json.dump(resumo, file, indent=4, ensure_ascii=False)
          
          print("Arquivo JSON gerado com sucesso.")

      case "2":
          print("CNPJ a implementar\n")

      case "3":
          print("CPF a implementar\n")
      
      case "4":
        print("Nome da parte a implementar\n")
      
      case "5":
        exit()
      
      case _:
        print("Dado Inválido. Digite um número de 1 a 5.\n")
        consulta()
        
consulta()