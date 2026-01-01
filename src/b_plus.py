import math

class BPlusNode:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
        self.is_leaf = False 
        self.next = None 
        self.parent = None

    def is_underflow(self):
        min_keys = math.ceil(self.order / 2) - 1
        return len(self.keys) < min_keys

class BPlusTree:
    def __init__(self, order=3):
        self.root = BPlusNode(order)
        self.root.is_leaf = True
        self.order = order

    def search(self, k):
        leaf = self.leaf_search(k, self.root)
        for i, key in enumerate(leaf.keys):
            if k == key: return True
        return False

    def leaf_search(self, k, node):
        if node.is_leaf: return node
        i = 0
        while i < len(node.keys) and k >= node.keys[i]: i += 1
        return self.leaf_search(k, node.children[i])

    def insert(self, key):
        leaf = self.leaf_search(key, self.root)
        self._insert_into_leaf(leaf, key)
        if len(leaf.keys) > (self.order - 1): self._split_leaf(leaf)

    def _insert_into_leaf(self, leaf, key):
        if not leaf.keys:
            leaf.keys.append(key)
            leaf.children.append(key) # Em B+ Tree simples, ponteiro de dados é a própria chave ou ref
            return
        for i, item in enumerate(leaf.keys):
            if key < item:
                leaf.keys.insert(i, key)
                leaf.children.insert(i, key)
                return
        leaf.keys.append(key)
        leaf.children.append(key)

    def _split_leaf(self, node):
        mid_idx = len(node.keys) // 2
        new_node = BPlusNode(self.order)
        new_node.is_leaf = True
        new_node.parent = node.parent
        new_node.keys = node.keys[mid_idx:]
        new_node.children = node.children[mid_idx:]
        node.keys = node.keys[:mid_idx]
        node.children = node.children[:mid_idx]
        new_node.next = node.next
        node.next = new_node
        self._insert_into_parent(node, new_node.keys[0], new_node)

    def _insert_into_parent(self, left_child, key, right_child):
        parent = left_child.parent
        if parent is None:
            new_root = BPlusNode(self.order)
            new_root.keys = [key]
            new_root.children = [left_child, right_child]
            new_root.is_leaf = False
            self.root = new_root
            left_child.parent = new_root
            right_child.parent = new_root
            return
        insert_idx = 0
        while insert_idx < len(parent.keys) and parent.keys[insert_idx] < key: insert_idx += 1
        parent.keys.insert(insert_idx, key)
        parent.children.insert(insert_idx + 1, right_child)
        right_child.parent = parent
        if len(parent.keys) > (self.order - 1): self._split_internal(parent)

    def _split_internal(self, node):
        mid_idx = len(node.keys) // 2
        key_to_promote = node.keys[mid_idx]
        new_node = BPlusNode(self.order)
        new_node.is_leaf = False
        new_node.parent = node.parent
        new_node.keys = node.keys[mid_idx+1:]
        new_node.children = node.children[mid_idx+1:]
        for child in new_node.children: child.parent = new_node
        node.keys = node.keys[:mid_idx]
        node.children = node.children[:mid_idx+1]
        self._insert_into_parent(node, key_to_promote, new_node)

    def remove(self, key):
        leaf = self.leaf_search(key, self.root)
        if key not in leaf.keys:
            print(f"Chave {key} não encontrada.")
            return

        # 1. Remove da folha
        idx = leaf.keys.index(key)
        leaf.keys.pop(idx)
        leaf.children.pop(idx) # Remove o dado associado

        # 2. Verifica Underflow (exceto se for a raiz)
        if leaf != self.root and leaf.is_underflow():
            self._handle_underflow(leaf)
        
        # 3. Caso especial: Raiz vazia
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            # A raiz antiga sumiu, o primeiro filho vira a nova raiz
            self.root = self.root.children[0]
            self.root.parent = None

    def _handle_underflow(self, node):
        parent = node.parent
        # Encontrar índice do nó no pai
        idx = parent.children.index(node)

        # Tentar pegar do irmão da ESQUERDA
        if idx > 0:
            sibling = parent.children[idx - 1]
            if len(sibling.keys) > (math.ceil(self.order/2) - 1):
                self._borrow_from_left(node, sibling, parent, idx)
                return

        # Tentar pegar do irmão da DIREITA
        if idx < len(parent.children) - 1:
            sibling = parent.children[idx + 1]
            if len(sibling.keys) > (math.ceil(self.order/2) - 1):
                self._borrow_from_right(node, sibling, parent, idx)
                return

        # Se não der para emprestar, faz MERGE
        # Preferência: Merge com a esquerda
        if idx > 0:
            sibling = parent.children[idx - 1]
            self._merge(sibling, node, parent, idx - 1)
        else:
            # Merge com a direita
            sibling = parent.children[idx + 1]
            self._merge(node, sibling, parent, idx)

    def _borrow_from_left(self, node, sibling, parent, idx):
        if node.is_leaf:
            # Move o último do irmão para o início do nó
            key = sibling.keys.pop()
            val = sibling.children.pop()
            node.keys.insert(0, key)
            node.children.insert(0, val)
            # Atualiza a chave separadora no pai
            parent.keys[idx-1] = node.keys[0]
        else:
            # Lógica para nó interno (rotação)
            parent_key = parent.keys[idx-1]
            sibling_key = sibling.keys.pop()
            sibling_child = sibling.children.pop()
            
            node.keys.insert(0, parent_key)
            node.children.insert(0, sibling_child)
            sibling_child.parent = node
            
            parent.keys[idx-1] = sibling_key

    def _borrow_from_right(self, node, sibling, parent, idx):
        if node.is_leaf:
            # Move o primeiro do irmão para o fim do nó
            key = sibling.keys.pop(0)
            val = sibling.children.pop(0)
            node.keys.append(key)
            node.children.append(val)
            # Atualiza pai (agora a chave separadora é a nova primeira do irmão)
            parent.keys[idx] = sibling.keys[0]
        else:
            # Nó interno
            parent_key = parent.keys[idx]
            sibling_key = sibling.keys.pop(0)
            sibling_child = sibling.children.pop(0)
            
            node.keys.append(parent_key)
            node.children.append(sibling_child)
            sibling_child.parent = node
            
            parent.keys[idx] = sibling_key

    def _merge(self, left, right, parent, idx_separator):
        # Merge: Esquerda engole a Direita
        if left.is_leaf:
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            left.next = right.next
        else:
            # Merge interno: precisa descer a chave do pai para o meio
            separator = parent.keys[idx_separator]
            left.keys.append(separator)
            left.keys.extend(right.keys)
            left.children.extend(right.children)
            for child in right.children:
                child.parent = left
        
        # Remove a referência da direita no pai
        parent.keys.pop(idx_separator)
        parent.children.pop(idx_separator + 1)

        # O pai perdeu uma chave/filho, verificar Underflow no pai
        if parent != self.root and parent.is_underflow():
            self._handle_underflow(parent)

    def print_tree(self):
        print("\n--- Estado da Árvore ---")
        queue = [self.root]
        level = 0
        while queue:
            print(f"Nível {level}: ", end="")
            count = len(queue)
            while count > 0:
                n = queue.pop(0)
                print(f"{n.keys}", end="  ")
                if not n.is_leaf:
                    queue.extend(n.children)
                count -= 1
            print()
            level += 1