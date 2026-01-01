from .bst import BinaryTree, Node, ROOT

class AVLTree(BinaryTree):
  def get_height(self, node):
    if not node:
      return 0
    return node.height

  def get_balance(self, node):
    if not node:
      return 0
    return self.get_height(node.left) - self.get_height(node.right)

  def right_rotate(self, y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
    x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

    # Retorna o novo nó raiz dessa sub-árvore
    return x

  def left_rotate(self, x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
    y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

    # Retorna o novo nó raiz da subarvore
    return y

  def insert(self, value):
    self.root = self._insert_recursive(self.root, value)

  def _insert_recursive(self, node, value):
    if not node:
      return Node(value) # height=1
    elif value < node.data:
      node.left = self._insert_recursive(node.left, value)
    elif value > node.data:
      node.right = self._insert_recursive(node.right, value)
    else:
      return node

    node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    # Obtém o fator de balanceamento
    balance = self.get_balance(node)

    # Se o nó ficar desbalanceado:
    # Caso 1: (Rotação à direita)
    if balance > 1 and value < node.left.data:
      return self.right_rotate(node)

    # Caso 2: (Rotação à esquerda)
    if balance < -1 and value > node.right.data:
      return self.left_rotate(node)

    # Caso 3: Rotações duplas
    if balance > 1 and value > node.left.data:
      node.left = self.left_rotate(node.left)
      return self.right_rotate(node)

    if balance < -1 and value < node.right.data:
      node.right = self.right_rotate(node.right)
      return self.left_rotate(node)

    return node

  # min, max e search permanecem iguais aos da BST
    if node == ROOT:
      node = self.root
    while node.left:
      node = node.left
    return node.data

  def remove(self, value, node=ROOT):
    if node == ROOT:
      node = self.root
    if node is None:
      return node

    if value < node.data: 
      node.left = self.remove(value, node.left)
    elif value > node.data: 
      node.right = self.remove(value, node.right)
    else: 
      if node.left is None:
        return node.right
      elif node.right is None:
        return node.left
      else:
        substitute = self.min(node.right) 
        node.data = substitute
        node.right = self.remove(substitute, node.right)
    
    if node is None:
      return node

    # Autobalanceamento após remoção

    node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    balance = self.get_balance(node)

    if balance > 1 and self.get_balance(node.left) >= 0:
      return self.right_rotate(node)

    if balance > 1 and self.get_balance(node.left) < 0:
      node.left = self.left_rotate(node.left)
      return self.right_rotate(node)

    if balance < -1 and self.get_balance(node.right) <= 0:
      return self.left_rotate(node)

    if balance < -1 and self.get_balance(node.right) > 0:
      node.right = self.right_rotate(node.right)
      return self.left_rotate(node)

    return node
