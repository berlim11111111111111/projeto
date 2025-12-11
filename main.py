import pandas as pd
import os

ARQUIVO_ALUNOS = 'alunosarq.csv'
COLUNAS = ['Matricula', 'Nome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'Estado', 'Telefone', 'Email']

def load_data():
    # Carrega o DataFrame a partir do arquivo CSV. Se o arquivo não existir, cria um DataFrame vazio e o arquivo. Retorna o DataFrame.
    
    if os.path.exists(ARQUIVO_ALUNOS):
        # Tenta ler o arquivo
        try:
            df = pd.read_csv(ARQUIVO_ALUNOS)
        except pd.errors.EmptyDataError:
            # Caso o arquivo exista, mas esteja vazio
            df = pd.DataFrame(columns=COLUNAS)
    else:
        # Se o arquivo não existir, cria um novo DataFrame
        df = pd.DataFrame(columns=COLUNAS)
        df.to_csv(ARQUIVO_ALUNOS, index=False) # Garante que o arquivo é criado
    # Garante que 'Matricula' é tratada como "int" para geração sequencial
    if not df.empty:
        df['Matricula'] = df['Matricula'].astype(int)
        
    return df
        

def save_data(df):
    # Salva o DataFrame no arquivo CSV, sem o índice do pandas
    df.to_csv(ARQUIVO_ALUNOS, index=False)
    print("\n Os dados foram salvos!")



def generate_matricula(df):
    # Gera um número de matrícula sequencial
    if df.empty:
        return 1
    else:
        # Pega a maior matrícula existente e adiciona 1
        return df['Matricula'].max() + 1

def input_aluno_data():
    print("\n INSERIR NOVO ALUNO ")
    
    # Dicionário para armazenar os dados do aluno
    data = {}
    
    # Lista dos campos a serem preenchidos 
    fields = COLUNAS[1:] 
    
    for field in fields:
        value = input(f"Digite o {field}: ").strip()
        while not value:
             print("Este campo não pode ser vazio. Tente novamente.")
             value = input(f"Digite o {field}: ").strip()
             
        data[field] = value

    return data
        

def inserir_aluno(df):
    # Gera matrícula e insere um novo aluno no DataFrame, e depois retorna o DataFrame atualizado
    new_matricula = generate_matricula(df)
    new_data = input_aluno_data()
    
    # Cria o registro completo como um dicionário
    new_data['Matricula'] = new_matricula
    
    # Cria um DataFrame temporário com o novo registro
    new_row_df = pd.DataFrame([new_data], columns=COLUNAS)
    
    # Adiciona a nova linha ao DataFrame principal; pd.concat sendo usado para unir os DataFrames
    df = pd.concat([df, new_row_df], ignore_index=True)
    
    print(f"\nAluno {new_data['Nome']} cadastrado com a seguinte matrícula: {new_matricula}")
    return df



def pesquisar_aluno(df):
    # Realiza a pesquisa por matrícula ou nome e retorna o(s) índice(s) do aluno no DataFrame.
    
    if df.empty:
        print("\n Não há alunos registrados para pesquisar.")
        return None
        
    search_term = input("\nDigite o nome ou número de matrícula para pesquisar: ").strip()
    
    try:
        # Tenta pesquisar por Matrícula (se for um número)
        matricula = int(search_term)
        result_index = df.index[df['Matricula'] == matricula].tolist()
        
    except ValueError:
        # Pesquisa por nome 
        # Cria uma série auxiliar em minúsculas para comparação
        search_lower = search_term.lower()
        result_index = df.index[df['Nome'].str.lower() == search_lower].tolist()
    
    if not result_index:
        print(f"\n Aluno com matrícula ou nome '{search_term}' não foi encontrado nos registros.")
        return None
    
    # Retorna o índice do primeiro resultado encontrado 
    return result_index[0] 

def display_aluno(df, index):
    # Apresenta os dados de um aluno formatados
    if index is not None:
        aluno = df.iloc[index]
        print("\n DADOS DO ALUNO ENCONTRADO ")
        for col in COLUNAS:
            print(f"  {col.ljust(10)}: {aluno[col]}")
        return True
    return False



def editar_aluno(df, index):
    # Permite ao usuário editar qualquer campo do aluno, exceto a matrícula
    aluno = df.iloc[index]
    
    # Colunas editáveis 
    colunas_editaveis = COLUNAS[1:]
    
    print("\n EDITAR DADOS ")
    print("Dados editáveis:")
    
    # Exibe as opções de edição numeradas
    edit_options = {} # Dicionário mapeará números para nomes de colunas
    for i, col in enumerate(colunas_editaveis, 1):
        # Apresenta a opção e o valor atual
        print(f"  {i}) {col.ljust(10)}: {aluno[col]}")
        edit_options[str(i)] = col # Mapeia o número digitado para o nome da coluna

    
    choice = input("\nEscolha o número do dado que deseja editar ou aperte 'Enter' para cancelar: ").strip()
    
    if choice in edit_options:
        edicao_alunos = edit_options[choice]
        
        # O programa pede apenas o dado a ser editado
        new_value = input(f"Digite o novo valor para {edicao_alunos}: ").strip()
        
        if new_value:
            # Atualiza o DataFrame
            df.loc[index, edicao_alunos] = new_value
            print(f"\n Campo '{edicao_alunos}' atualizado com sucesso!")
            
        else:
            print("\n Edição cancelada: o novo valor não pode ser vazio.")
            
    elif choice:
        print("\n Opção inválida.")
        
    else:
        print("\n Edição cancelada.")
        
    return df



def remover_aluno(df, index):
    # Remove o aluno do DataFrame após confirmação
    aluno_nome = df.loc[index, 'Nome']
    
    print("\n REMOVER ALUNO ")
    confirm = input(f"Tem certeza que deseja remover o aluno {aluno_nome}? (S/N): ").upper().strip()
    
    if confirm == 'S':
        # Remove a linha pelo seu índice
        df = df.drop(index=index).reset_index(drop=True)
        print(f"\n Aluno {aluno_nome} removido.")
    else:
        print("\n Remoção cancelada.")
        
    return df



def main_menu():
    
    #Apresenta o menu, gerencia o loop principal e as chamadas das funções
    # 1. Carrega os dados existentes no início da execução
    df = load_data()
    
    
    print("  SISTEMA DE CADASTRO DE ALUNOS  ")
    
    
    # Loop principal que só termina quando o usuário escolhe a opção de sair
    while True:
        print("\n MENU ")
        print("1 - Inserir novo aluno")
        print("2 - Pesquisar/Editar/Remover aluno")
        print("3 - Sair")
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            df = inserir_aluno(df)
            save_data(df)

        elif choice == '2':
            # 1. Pesquisa o aluno
            index_aluno = pesquisar_aluno(df)
            
            if index_aluno is not None:
                # 2. Mostra os dados do aluno
                display_aluno(df, index_aluno)
                
                # 3. Oferece opções de edição/remoção
                print("\nOpções para o aluno:")
                print("A - Editar dados")
                print("B - Remover aluno")
                print("C - Cancelar")
                
                action = input("Escolha uma opção (A, B ou C): ").upper().strip()
                
                if action == 'A':
                    df = editar_aluno(df, index_aluno)
                    save_data(df)
                elif action == 'B':
                    df = remover_aluno(df, index_aluno)
                    save_data(df)
                elif action == 'C':
                    print("\n Ação cancelada.")
                else:
                    print("\n Opção inválida.")
        
        elif choice == '3':
            print("\n O programa será finalizado. ")
            break
            
        else:
            print("\n Opção inválida. Digite 1, 2 ou 3.")
# Ponto de entrada do programa
if __name__ == "__main__":
    main_menu()
