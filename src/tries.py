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

    def remove(self, word):
        self._remove(self.root, word, 0)

    def _remove(self, node, word, index):
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
        should_remove_child = self._remove(child_node, word, index + 1)

        if should_remove_child:
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
    def __init__(self, label, is_leaf=False):
        self.label = label
        self.children = {}
        self.is_leaf = is_leaf

class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaNode("") # Raiz vazia

    def _get_common_prefix(self, s1, s2):
        """Retorna o prefixo comum entre duas strings."""
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]:
                return s1[:i]
        return s1[:min_len]

    def insert(self, key):
        node = self.root
        i = 0 
        
        while i < len(key):
            char = key[i]
            
            if char in node.children:
                child = node.children[char]
                common_prefix = self._get_common_prefix(child.label, key[i:])
                common_len = len(common_prefix)
                
                # Caso 1: Split do nó existente
                if common_len < len(child.label):
                    suffix_existing = child.label[common_len:]
                    suffix_new = key[i + common_len:]
                    
                    child.label = common_prefix
                    
                    new_child_existing = PatriciaNode(suffix_existing, child.is_leaf)
                    new_child_existing.children = child.children
                    
                    child.children = {suffix_existing[0]: new_child_existing} if suffix_existing else {}
                    child.is_leaf = False 
                    
                    if suffix_new:
                        new_child_new = PatriciaNode(suffix_new, True)
                        child.children[suffix_new[0]] = new_child_new
                    else:
                        child.is_leaf = True
                    return
                
                # Caso 2: Descendo na árvore
                i += common_len
                node = child
            else:
                # Caso 3: Novo ramo
                new_node = PatriciaNode(key[i:], True)
                node.children[key[i]] = new_node
                return
        
        node.is_leaf = True
    def remove(self, key):
            """Remove uma chave da árvore, se existir."""
            self._remove_node(self.root, key)

    def _remove_node(self, parent, key):
        if not key or not parent.children:
            return False

        char = key[0]
        if char not in parent.children:
            return False

        child = parent.children[char]
        label = child.label

        # Verifica se o label do nó atual é prefixo da chave que buscamos
        if not key.startswith(label):
            return False # Caminho não bate

        # Caso 1: Encontramos o nó exato
        if len(key) == len(label):
            if not child.is_leaf:
                return False # A palavra não existe (é apenas prefixo de outra)

            # Desmarca como folha (lógica de "soft delete")
            child.is_leaf = False

            # Agora verificamos a estrutura para limpeza (Hard delete ou Merge)
            
            # A) Se não tem filhos, remove o nó do pai
            if not child.children:
                del parent.children[char]
            
            # B) Se tem exatamente 1 filho, faz o merge (compactação)
            elif len(child.children) == 1:
                self._merge_with_child(parent, char, child)
            
            return True

        # Caso 2: A chave é maior que o label, continuamos descendo
        suffix = key[len(label):]
        if self._remove_node(child, suffix):
            # Na volta da recursão (backtracking), verificamos se o nó atual (child)
            # precisa ser ajustado porque seu filho foi modificado/removido.
            
            # Se o child não é palavra e ficou sem filhos, removemos ele
            if not child.is_leaf and not child.children:
                del parent.children[char]
            
            # Se o child não é palavra e sobrou só 1 filho, fazemos merge
            elif not child.is_leaf and len(child.children) == 1:
                self._merge_with_child(parent, char, child)
            
            return True

        return False

    def _merge_with_child(self, parent, key_char, node):
        """
        Mescla 'node' com seu único filho para manter a propriedade compacta.
        Parent -> Node -> Grandchild  ==vira==> Parent -> NewNode (Node+Grandchild)
        """
        # Pega o único filho (grandchild)
        grandchild_key, grandchild = list(node.children.items())[0]
        
        # Concatena os labels: ex: "ro" + "ma" = "roma"
        grandchild.label = node.label + grandchild.label
        
        # O pai passa a apontar direto para o neto (que agora tem o label fundido)
        # Nota: A chave no dicionário do pai continua sendo a mesma (primeira letra)
        parent.children[key_char] = grandchild