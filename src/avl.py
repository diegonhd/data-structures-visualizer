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

    if node == ROOT:
      node = self.root
    while node.left:
      node = node.left
    return node.data

  def min_node(self, node):
          current = node
          while current.left is not None:
              current = current.left
          return current

  def remove(self, value):
      # Chama a função recursiva e ATUALIZA a raiz da árvore
      if self.root:
          self.root = self._remove(self.root, value)

  def _remove(self, node, value):
      if not node:
          return node

      if value < node.data:
          node.left = self._remove(node.left, value)
      elif value > node.data:
          node.right = self._remove(node.right, value)
      else:
          
          # Caso 1 ou 2: Nó com um filho ou nenhum
          if node.left is None:
              temp = node.right
              node = None
              return temp
          elif node.right is None:
              temp = node.left
              node = None
              return temp

          # Caso 3: Nó com dois filhos
          # Pega o menor nó da subárvore direita (sucessor in-order)
          temp = self.min_node(node.right)
          # Copia o dado do sucessor para este nó
          node.data = temp.data
          node.right = self._remove(node.right, temp.data)

      if node is None:
          return node
      node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

      balance = self.get_balance(node)

      # Esquerda Pesada (Left Left)
      if balance > 1 and self.get_balance(node.left) >= 0:
          return self.right_rotate(node)

      # Esquerda Direita (Left Right)
      if balance > 1 and self.get_balance(node.left) < 0:
          node.left = self.left_rotate(node.left)
          return self.right_rotate(node)

      # Direita Pesada (Right Right)
      if balance < -1 and self.get_balance(node.right) <= 0:
          return self.left_rotate(node)

      # Direita Esquerda (Right Left)
      if balance < -1 and self.get_balance(node.right) > 0:
          node.right = self.right_rotate(node.right)
          return self.left_rotate(node)

      return node