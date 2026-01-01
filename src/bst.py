from collections import deque
ROOT = "root"

class Node:
  def __init__(self, data):
    self.data = data
    self.left = None
    self.right = None
    self.height = 1 
  
  def __str__(self):
    return str(self.data)

class BinaryTree:
  def __init__(self,data=None, node=None):
    if node:
      self.root = node
    elif data:
      node = Node(data)
      self.root = node
    else:
      self.root = None

  def inorder_traversal(self, node=None):
    if node is None:
      node = self.root
    if node.left:
      self.inorder_traversal(node.left)
    print(node, end=' ')
    if node.right:
      self.inorder_traversal(node.right)

  def postorder_traversal(self, node=None):
    if node is None:
      node = self.root
    if node.left:
      self.postorder_traversal(node.left)
    if node.right:
      self.postorder_traversal(node.right)
    print(node)

  def levelorder_traversal(self, node=ROOT):
    if node == ROOT:
      node = self.root
    q = deque()
    q.append(self.root)

    while q:
        node = q.popleft()
        print(node, end=' ')
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


  def height(self, node = None):
    if node is None:
      node = self.root
    hleft = 0
    hright = 0
    if node.left:
      hleft = self.height(node.left)
    if node.right:
      hright = self.height(node.right)
    if hright > hleft:
      return hright + 1
    else:
      return hleft + 1

class BinarySearchTree(BinaryTree):
  def insert(self, value):
    parent = None
    x = self.root
    while(x): # Achando o 'pai' certo para o valor
      parent = x
      if value > x.data:
        x = x.right
      else:
        x = x.left
    if parent is None: # Caso em que a árvore está vazia
      self.root = Node(value)
    elif value < parent.data: # Caso em que value é menor que parent(esquerda)
      parent.left = Node(value)
    elif value > parent.data: # Caso em que value é maior que parent(direita)
      parent.right = Node(value)

  def search(self, value, node = 0):
    if node == 0:
      node = self.root
    if node is None or node.data == value:
      return BinarySearchTree(node)
    if value < node.data:
      return self.search(value, node.left)
    else:
      return self.search(value, node.right)

  def min(self, node=ROOT):
      if node == ROOT:
          node = self.root
      while node.left:
          node = node.left
      return node.data

  def max(self, node=ROOT):
      if node == ROOT:
          node = self.root
      while node.right:
          node = node.right
      return node.data

  def remove(self, value, node=ROOT):
    if node == ROOT:
      node = self.root
    if node is None:
      return node
    if value < node.data: # Buscando o valor na esquerda
      node.left = self.remove(value, node.left)
    elif value > node.data: # Buscando o valor na direita
      node.right = self.remove(value, node.right)
    # Recursividade onde se o valor ainda for menor do que
    # o valor do nó, todo aquele nó irá ser substituido pelo
    # que a função retornar na proxima recursão.
    # Isso ocorre até achar o caso do número ser igual.

    else: # Achamos o valor, agora ocorre o tratamento
    # Aqui se vê o caso 1 e 2:
    #1. O nó não tem filhos (node.left and node.right is None)
    #2. O nó tem filho de só um lado
      if node.left is None:
        return node.right
      elif node.right is None:
        return node.left
    # O que acontece então é que estamos no nível da recursão em que
    # estamos no node.left ou node.right do parente do nó em que se
    # encontra o nosso valor. Então o atual node = node.right or
    # node.left do parente. Então procuramos o caso em que se encaixa
    # o nó e retornamos o novo valor que se deve encontrar o novo
    # node.right ou node.left do node.right ou node.left do parent do nó.
      else:
    # Aqui se vê o caso 3: O nó tem ambos os filhos não-vaziozs.
        substitute = self.min(node.right) # Achando o substituto
        # que deve ser o sucessor mais proximo do valor
        node.data = substitute
        node.right = self.remove(substitute, node.right)
    return node # Caso em que eu nao altero nada na estrutura

