class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None  # Aponta para o próximo nó em caso de colisão
class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):

        index = self._hash(key)
        node = self.table[index]

        # Caso 1: O slot (bucket) está vazio
        if node is None:
            self.table[index] = HashNode(key, value)
            self.size += 1
            return

        # Caso 2: Colisão ou Atualização. Percorre a lista encadeada.
        prev = None
        curr = node
        while curr is not None:
            if curr.key == key:
                curr.value = value
                return
            prev = curr
            curr = curr.next

        prev.next = HashNode(key, value)
        self.size += 1

    def search(self, key):
        index = self._hash(key)
        curr = self.table[index]

        while curr is not None:
            if curr.key == key:
                return curr.value
            curr = curr.next
        
        return None

    def remove(self, key):
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
                    # O nó está no meio ou fim
                    prev.next = curr.next
                
                self.size -= 1
                return           
            # Avança os ponteiros
            prev = curr
            curr = curr.next
