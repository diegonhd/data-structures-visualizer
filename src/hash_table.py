class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None  # Aponta para o próximo nó em caso de colisão

    def __repr__(self):
        return f"[{self.key}: {self.value}]"

class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        # A tabela é uma lista de espaços, onde cada espaço pode conter o início de uma lista encadeada
        self.table = [None] * capacity
        self.size = 0

    def _hash(self, key):
        """
        Função de Hash simples:
        Usa o hash nativo do Python e aplica o módulo da capacidade.
        Retorna um índice válido entre 0 e capacity-1.
        """
        return hash(key) % self.capacity

    def insert(self, key, value):
        """
        Insere um par chave-valor na tabela.
        Se a chave já existe, atualiza o valor.
        Se houver colisão, adiciona ao final da lista encadeada naquele índice.
        """
        index = self._hash(key)
        node = self.table[index]

        # Caso 1: O slot (bucket) está vazio
        if node is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
            print(f"Inserido: '{key}' no índice {index} (Novo slot).")
            return

        # Caso 2: Colisão ou Atualização. Percorre a lista encadeada.
        prev = None
        curr = node
        while curr is not None:
            if curr.key == key:
                curr.value = value # Atualiza valor existente
                print(f"Atualizado: '{key}' no índice {index}.")
                return
            prev = curr
            curr = curr.next

        # Se chegou aqui, a chave não existe no bucket, adiciona no final
        prev.next = HashNode(key, value)
        self.size += 1
        print(f"Inserido: '{key}' no índice {index} (Colisão tratada - adicionado ao fim).")

    def search(self, key):
        """
        Busca o valor associado a uma chave.
        Retorna o valor se encontrar, ou None se não existir.
        """
        index = self._hash(key)
        curr = self.table[index]

        while curr is not None:
            if curr.key == key:
                return curr.value
            curr = curr.next
        
        return None

    def remove(self, key):
        """
        Remove uma chave da tabela hash.
        Lida com remoção no início ou no meio da lista encadeada.
        """
        index = self._hash(key)
        curr = self.table[index]
        prev = None

        while curr is not None:
            if curr.key == key:
                # Achou o nó para remover
                if prev is None:
                    # O nó a ser removido é o primeiro da lista (cabeça)
                    self.table[index] = curr.next
                else:
                    # O nó está no meio ou fim; pula o nó atual
                    prev.next = curr.next
                
                self.size -= 1
                print(f"Removido: '{key}' do índice {index}.")
                return
            
            # Avança os ponteiros
            prev = curr
            curr = curr.next

        print(f"Erro ao remover: Chave '{key}' não encontrada.")

    def display(self):
        """Método auxiliar para visualizar a estrutura da tabela."""
        print("\n--- Estado da Tabela Hash ---")
        for i, node in enumerate(self.table):
            if node is not None:
                # Reconstrói a string da lista encadeada para visualização
                chain = []
                curr = node
                while curr:
                    chain.append(str(curr))
                    curr = curr.next
                print(f"Índice {i}: " + " -> ".join(chain))
            else:
                print(f"Índice {i}: (Vazio)")
        print("-----------------------------\n")
