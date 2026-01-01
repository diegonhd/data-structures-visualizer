class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

    def __str__(self):
        return f"Node(end={self.is_end_of_word}, children={list(self.children.keys())})"

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """Retorna True apenas se a palavra exata existir."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Retorna True se existe alguma palavra começando com o prefixo."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word):
        self._delete(self.root, word, 0)

    def _delete(self, node, word, index):
        # Caso base: chegamos ao fim da palavra
        if index == len(word):
            if not node.is_end_of_word:
                return False # Palavra não existe
            
            node.is_end_of_word = False
            # Se não tem filhos, este nó pode ser deletado pelo pai
            return len(node.children) == 0

        char = word[index]
        if char not in node.children:
            return False

        child_node = node.children[char]
        should_delete_child = self._delete(child_node, word, index + 1)

        if should_delete_child:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word
        
        return False

    def print_all_words(self):
        print("\n--- Palavras na Trie ---")
        self._print_recursive(self.root, "")
        print("------------------------")

    def _print_recursive(self, node, current_word):
        if node.is_end_of_word:
            print(f"- {current_word}")
        
        for char, child_node in sorted(node.children.items()):
            self._print_recursive(child_node, current_word + char)

class PatriciaNode:
    def __init__(self, key=None, bit_index=None, is_leaf=False):
        self.key = key             # Usado apenas se is_leaf=True
        self.bit_index = bit_index # Usado apenas se is_leaf=False
        self.is_leaf = is_leaf
        self.left = None
        self.right = None

    def __repr__(self):
        if self.is_leaf:
            return f"[Leaf: {self.key}]"
        return f"[Node: bit {self.bit_index}]"

class PatriciaTrie:
    def __init__(self):
        self.root = None

    def _get_bit(self, key, index):
        """Retorna o i-ésimo bit da string (0 ou 1)."""
        if index < 0: return 0
        char_index = index // 8
        
        # Se o índice excede o tamanho da string, consideramos bits virtuais 0
        if char_index >= len(key): return 0
        
        # Pega o char e desloca para encontrar o bit
        byte_val = ord(key[char_index])
        bit_offset = 7 - (index % 8)
        return (byte_val >> bit_offset) & 1

    def _first_bit_diff(self, key1, key2):
        """
        Encontra o índice do primeiro bit diferente entre duas chaves.
        Auxiliar essencial para a Inserção.
        """
        len1, len2 = len(key1), len(key2)
        max_len = max(len1, len2)
        
        # Itera byte a byte (caractere a caractere)
        for i in range(max_len):
            # Obtém valor ASCII ou 0 se acabou a string
            b1 = ord(key1[i]) if i < len1 else 0
            b2 = ord(key2[i]) if i < len2 else 0
            
            if b1 != b2:
                # Se os bytes são diferentes, achamos qual bit difere
                xor_val = b1 ^ b2
                # Varre do bit mais significativo (7) ao menos (0)
                for bit in range(7, -1, -1):
                    if (xor_val >> bit) & 1:
                        return (i * 8) + (7 - bit)
        return -1 # Chaves iguais

    def search(self, key):
        """
        Busca uma chave na árvore.
        Retorna True se encontrada, False caso contrário.
        """
        if self.root is None:
            return False
        
        curr = self.root
        
        # 1. Navegação cega: Segue os bits indicados pelos nós internos
        while not curr.is_leaf:
            bit = self._get_bit(key, curr.bit_index)
            if bit == 0:
                curr = curr.left
            else:
                curr = curr.right
        
        # 2. Verificação final: Compara a chave da folha encontrada com a buscada
        return curr.key == key

    def insert(self, key):
        """
        Insere uma nova chave na árvore Patricia.
        """
        # Caso 1: Árvore vazia
        if self.root is None:
            self.root = PatriciaNode(key=key, is_leaf=True)
            return

        # Caso 2: Árvore não vazia.
        curr = self.root
        while not curr.is_leaf:
            bit = self._get_bit(key, curr.bit_index)
            if bit == 0:
                curr = curr.left
            else:
                curr = curr.right
        
        existing_key = curr.key
        
        if existing_key == key:
            print(f"Chave '{key}' já existe.")
            return

        diff_index = self._first_bit_diff(key, existing_key)

        parent = None
        curr = self.root
        
        while not curr.is_leaf and curr.bit_index < diff_index:
            parent = curr
            bit = self._get_bit(key, curr.bit_index)
            if bit == 0:
                curr = curr.left
            else:
                curr = curr.right
        
        # Cria o novo nó interno e a nova folha
        new_leaf = PatriciaNode(key=key, is_leaf=True)
        new_internal = PatriciaNode(bit_index=diff_index, is_leaf=False)
        
        # Decide quem vai para a esquerda ou direita no novo nó interno
        bit_val = self._get_bit(key, diff_index)
        
        if bit_val == 0:
            new_internal.left = new_leaf
            new_internal.right = curr # O nó antigo (subárvore ou folha)
        else:
            new_internal.left = curr
            new_internal.right = new_leaf
            
        # Conecta o novo nó interno ao pai
        if parent is None:
            self.root = new_internal
        else:
            if parent.left == curr:
                parent.left = new_internal
            else:
                parent.right = new_internal
        
        print(f"Inserido: '{key}' (Divisão no bit {diff_index})")

    def remove(self, key):
        """
        Remove uma chave (código original mantido para integridade).
        """
        if self.root is None: return

        if self.root.is_leaf:
            if self.root.key == key:
                self.root = None
            return

        grandparent = None
        parent = None
        curr = self.root

        while not curr.is_leaf:
            grandparent = parent
            parent = curr
            bit = self._get_bit(key, curr.bit_index)
            if bit == 0: curr = curr.left
            else: curr = curr.right

        if curr.key != key:
            print(f"Erro ao remover: Chave '{key}' não encontrada.")
            return

        sibling = parent.right if parent.left == curr else parent.left

        if grandparent is None:
            self.root = sibling
        else:
            if grandparent.left == parent: grandparent.left = sibling
            else: grandparent.right = sibling
            
        print(f"Removido: '{key}'")
