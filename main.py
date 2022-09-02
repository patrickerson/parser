# Patrickerson dos Santos Veiga

import string
alfa_valid = string.ascii_lowercase
num_valid = "1234567890"

constant = ["T", "F"]
unitary = "neg"
binary = ["vee", "rightarrow", "wedge", "leftrightarrow"]

paren = ["(", ")"]

stack = []

def isAlfa(character):
  """
  Checa se o character está no conjunto alfabético válido
  """
  return character in alfa_valid

def isNum(character):
  """
    Checa se o character está no conjunto numérico       válido
  """
  return character in num_valid
  
def prop(input):
  """
  Verifica se é uma proposição válida
  """
  close = False
  firstQueue = True # garante que a formula seja adicionada na pilha na primeira execução
  for i in range(0,len(input)):
    # Caso ocorra de encontrar um ')', a função chamará close_paren
    if  input[i] == ")":
      close=True
      
      if firstQueue:
        firstQueue=False
        insert_stack("formula")
      insert_stack("close_paren")
      close_paren()

    # Termina a função sem inserir formula na pilha caso seja um caracter invalido
    elif not isAlfa(input[i]) and not isNum(input[i]):
      return 
  # adiciona a formula na pilha caso não haja nenhum fechamento de parenteses
  if not close:
      insert_stack("formula")
  return

  
def insert_stack(insert):
  """
  Insere na pilha
  """
  stack.append(insert)
  
def get_file(file):
  """
  Le o arquivo
  """
  return open(file).read()


def constant(character):
  """
  verifica se é constante
  """
  return character == "T" or character == "F"

def open_paren(input):
  """
  Chamado quando há um caracter '('

  atribui na stack se é uma formula unaria ou binaria caso seja válido. Caso o contrário,
  """
  if input[0] == "\\":
    
    if input[1:] == "neg":
      insert_stack("unaria")
      return True
    for i in binary:
      if i==input[1:]:
        insert_stack("binaria")
        
        
  return False

def close_paren():
  """
  Chamado quando há um caracter ')'


  Os elementos serão desempilhados da stack do último elemento (o mais a direita) até o primeiro '('

  Caso a expressão seja válida, será feito o reduce e toda a expressão será substituido por 'formula'

  Se não estiver dentro da grámatica, a função simplesmente ignora e não remove nada da pilha, o que resultará em uma pilha contendo itens que não serão finalizado

  Nos em que a função for chamada e o tamanho da stack for menor que 4 (número mínimo para executar a função), a função retornará sem fazer nada, deixando itens na pilha.

  """
  valid = False
  if(len(stack)<4):
    return False
  if(stack[-1]=="close_paren"):
    del stack[-1]
    if stack[-1] == "formula":
      del stack[-1]
      if stack[-1] == "unaria":
        valid = True
        del stack[-1]
      if stack[-1] == "formula" and stack[-2] == "binaria":
        valid = True
        del stack[-1]
        del stack[-1]
      if valid and stack[-1] == "open_paren":
        del stack[-1]
        insert_stack("formula")
        return
  return
      

def formula(input):
  """
  Chama os outros métodos de forma recursiva

  """
  # Encerra se o buffer está vazio
  if input==[]:
    return True
  # Verifica se é uma constante
  if constant(input[0][0]):
    insert_stack("formula")
    if len(input[0]) >= 2:
      for i in input[0][1:]:
        if input[0][1] == ")":
          insert_stack("close_paren")
          close_paren()
        else:
          insert_stack("invalid")
          return False
    return formula(input[1:])
  # Verifica se está contido no conjunto alfabético válido
  # Caso, seja, chama a prop
  if isAlfa(input[0][0]):
    prop(input[0])
    formula(input[1:])
  if input[0][0] == ")":
    insert_stack("close_paren")
    close_paren()

  # Verifica se o primeiro caracter é um abre paren
  # Verifica também se o tamanho da string de entrada é maior do que 1, para que seja possível ler os próximos caracteres
  if input[0][0] == "(" and len(input[0]) > 1:
      insert_stack("open_paren")
      open_paren(input[0][1:])
      # checa é uma fórmula binaria ou unaria
      if stack[-1] == "unaria":
        formula(input[1:])
      if stack[-1] == "binaria":
        formula(input[1:])
      return False
  return False



def check_valid(filename):
  """
  Lê o arquivo, chama formula(), e verifica a stack está vazia.

  Após checar, a stack precisar ser limpada para cada leitura
  """
  file = get_file(filename).split("\n")
  for i in file[1:]:
    x = i.split(" ")
    formula(x)
    if len(stack) == 1 and stack[0] == "formula":
      print(f"{i} válida")
    else:
      print(f"{i} inválida")
    stack.clear()

# Chama check_valid para cada arquivo listado.
for i in range(1,4):
  check_valid(f"input{i}.txt")
  
