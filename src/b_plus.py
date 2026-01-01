import math

class BPlusNode:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []
        # 'leaf' determina se os children são dados/registros ou ponteiros para outros nós
        self.is_leaf = False 
        # Para a lista encadeada das folhas (característica B+)
        self.next = None 
        self.parent = None

    def is_full(self):
        # Baseado em: "at most b-1 entries"
        return len(self.keys) >= self.order - 1

    def is_underflow(self):
        # Baseado em: "If L has only d-1 entries" (geralmente d = ceil(order/2))
        min_keys = math.ceil(self.order / 2) - 1
        return len(self.keys) < min_keys

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusNode(order)
        self.root.is_leaf = True
        self.order = order

    # --- SEARCH ---
    
    def search(self, k):
        leaf = self.leaf_search(k, self.root)
        for i, key in enumerate(leaf.keys):
            if k == key:
                return f"Encontrado {k} na folha {leaf.keys}"
        return False

    def leaf_search(self, k, node):
        if node.is_leaf:
            return node

        i = 0
        while i < len(node.keys) and k >= node.keys[i]:
            i += 1
            
        return self.leaf_search(k, node.children[i])

    def insert(self, key):
        leaf = self.leaf_search(key, self.root)
        self._insert_into_leaf(leaf, key)

        if len(leaf.keys) > (self.order - 1):
            self._split_leaf(leaf)

    def _insert_into_leaf(self, leaf, key):
        if not leaf.keys:
            leaf.keys.append(key)
            leaf.children.append(key)
            return

        for i, item in enumerate(leaf.keys):
            if key < item:
                leaf.keys.insert(i, key)
                leaf.children.insert(i, key)
                return
        leaf.keys.append(key)
        leaf.children.append(key)

    def _split_leaf(self, node):
        mid_idx = math.ceil(len(node.keys) / 2)

        new_node = BPlusNode(self.order)
        new_node.is_leaf = True
        new_node.parent = node.parent

        new_node.keys = node.keys[mid_idx:]
        new_node.children = node.children[mid_idx:]
        
        node.keys = node.keys[:mid_idx]
        node.children = node.children[:mid_idx]

        new_node.next = node.next
        node.next = new_node

        # Regra de Split de Folha: A chave sobe
        key_to_promote = new_node.keys[0]
        
        self._insert_into_parent(node, key_to_promote, new_node)

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
        while insert_idx < len(parent.keys) and parent.keys[insert_idx] < key:
            insert_idx += 1
        
        parent.keys.insert(insert_idx, key)
        parent.children.insert(insert_idx + 1, right_child)
        right_child.parent = parent

        if len(parent.keys) > (self.order - 1):
            self._split_internal(parent)

    def _split_internal(self, node):
        mid_idx = len(node.keys) // 2
        key_to_promote = node.keys[mid_idx]

        new_node = BPlusNode(self.order)
        new_node.is_leaf = False
        new_node.parent = node.parent

        new_node.keys = node.keys[mid_idx+1:]
        new_node.children = node.children[mid_idx+1:]
        
        for child in new_node.children:
            child.parent = new_node

        node.keys = node.keys[:mid_idx]
        node.children = node.children[:mid_idx+1]

        self._insert_into_parent(node, key_to_promote, new_node)
    def delete(self, key):
        self._delete_entry(self.root, key)
        
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
            self.root.parent = None

    def _delete_entry(self, node, key):
        if not node.is_leaf:
            idx = 0
            while idx < len(node.keys) and key >= node.keys[idx]:
                idx += 1
            self._delete_entry(node.children[idx], key)
        else:
            if key in node.keys:
                idx = node.keys.index(key)
                node.keys.pop(idx)
                node.children.pop(idx)
            else:
                return

        if node != self.root and node.is_underflow():
            self._handle_underflow(node)

    def _handle_underflow(self, node):
        parent = node.parent
        idx = parent.children.index(node)

        # 1. Tentar pegar da esquerda
        if idx > 0:
            sibling = parent.children[idx - 1]
            if len(sibling.keys) > (math.ceil(self.order/2) - 1):
                self._borrow_from_left(node, sibling, parent, idx)
                return

        # 2. Tentar pegar da direita
        if idx < len(parent.children) - 1:
            sibling = parent.children[idx + 1]
            if len(sibling.keys) > (math.ceil(self.order/2) - 1):
                self._borrow_from_right(node, sibling, parent, idx)
                return

        # 3. Merge
        if idx > 0:
            self._merge(parent.children[idx-1], node, parent, idx-1)
        else:
            self._merge(node, parent.children[idx+1], parent, idx)

    def _borrow_from_right(self, node, sibling, parent, idx_in_parent):
        if node.is_leaf:
            borrow_key = sibling.keys.pop(0)
            borrow_val = sibling.children.pop(0)
            node.keys.append(borrow_key)
            node.children.append(borrow_val)
            
            # Atualiza pai com o menor valor atual do irmão
            parent.keys[idx_in_parent] = sibling.keys[0]

    def _borrow_from_left(self, node, sibling, parent, idx_in_parent):
        if node.is_leaf:
            borrow_key = sibling.keys.pop()
            borrow_val = sibling.children.pop()
            node.keys.insert(0, borrow_key)
            node.children.insert(0, borrow_val)
            
            parent.keys[idx_in_parent - 1] = node.keys[0]

    def _merge(self, left, right, parent, idx_separator):
        left.keys.extend(right.keys)
        left.children.extend(right.children)
        
        if left.is_leaf:
            left.next = right.next
            parent.keys.pop(idx_separator)
            parent.children.pop(idx_separator + 1)
        
        if parent != self.root and parent.is_underflow():
            self._handle_underflow(parent)

    def print_tree(self):
        print("\nStructure:")
        queue = [self.root]
        while queue:
            count = len(queue)
            while count > 0:
                n = queue.pop(0)
                type_n = "Leaf" if n.is_leaf else "Internal"
                print(f"[{type_n}: {n.keys}]", end=" ")
                if not n.is_leaf:
                    queue.extend(n.children)
                count -= 1
            print()