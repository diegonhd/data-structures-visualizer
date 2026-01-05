# Data Structures Visualizer

Este repositório contém implementações em Python de diversas estruturas de dados fundamentais, acompanhadas de uma ferramenta de visualização baseada em **Graphviz**.

O objetivo deste projeto é fornecer uma forma visual e interativa de entender o comportamento interno de estruturas complexas como Árvore B+, AVL, Trie, Patricia e Tabela Hash, demonstrando operações de inserção, remoção, balanceamento e colisões.

---

## Estrutura do Projeto

```text
data-structures-visualizer/
│
├── src/                      # Código fonte das estruturas e visualizador
│   ├── __init__.py
│   ├── bst.py                # Binary Search Tree (BST)
│   ├── avl.py                # AVL Tree (Auto-balanceamento)
│   ├── b_plus.py             # B+ Tree (Splits e Merges)
│   ├── tries.py              # Trie e Patricia Trie
│   ├── hash_table.py         # Hash Table (Tratamento de colisão)
│   └── visualizer.py         # Classe TreeVisualizer (Renderização)
│
├── notebooks/                # Demonstrações visuais
│   └── demo_structures.ipynb # Notebook com cenários de teste
│
├── .gitignore
├── README.md                 # Documentação
└── requirements.txt          # Dependências do projeto
```

---

## Funcionalidades Implementadas

O projeto cobre as seguintes estruturas e comportamentos, demonstrados no Jupyter Notebook:

### 1. Binary Search Tree (BST) 
* Visualização da degeneração da árvore em uma lista encadeada (pior caso).
* Inserção e remoção de nós.
* Demonstração de formatos "zigue-zague".

### 2. AVL Tree (Self-Balancing) 
* **Rotação Simples:** Direita e Esquerda.
* **Rotação Dupla:** Direita-Esquerda e Esquerda-Direita.
* Rebalanceamento automático após inserções e remoções que alteram o fator de balanceamento (h).

### 3. B+ Tree 
* Configuração de ordem da árvore (ex: M=3).
* **Splits:** Divisão de páginas raiz e folhas.
* **Cascade Split:** Divisão propagada para os pais.
* **Merge:** Fusão de páginas após remoção de elementos para manter as propriedades da árvore.

### 4. Tries & Patricia Tries 
* **Trie Padrão:** Inserção de palavras, visualização de prefixos comuns e remoção lógica (desmarcar flag de fim de palavra).
* **Patricia Trie (Radix Tree):** Compressão de arestas para caminhos únicos, otimizando espaço.

### 5. Hash Table 
* Visualização de buckets e índices.
* **Tratamento de Colisões:** Encadeamento externo (Linked List dentro do bucket).
* Atualização de valores para chaves existentes.

---

##  Instalação e Requisitos

### Pré-requisitos
* **Python 3.8+**
* **Graphviz (Software):** É necessário ter o binário do Graphviz instalado no seu sistema operacional para que a biblioteca Python possa gerar as imagens.
    * **Windows:** [Baixar Instalador](https://graphviz.org/download/)
    * **Linux (Ubuntu/Debian):** `sudo apt-get install graphviz`
    * **Mac:** `brew install graphviz`

### Instalação do Projeto

1. Clone o repositório:
   ```bash
   git clone [https://github.com/diegonhd/data-structures-visualizer.git]
   cd data-structures-visualizer
   ```
2. Crie um ambiente virtual (venv):
    ```bash
    python -m venv venv
    ```
    * Windows:
        ```bash
        venv\Scripts\activate
        ```
    * Linux/Mac
        ```bash
        source venv/bin/activate
        ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

---

## Como Usar
### A melhor forma de visualizar as estruturas é através do Jupyter Notebook.
1. Inicie o Jupyter
    ```bash
    jupyter notebook
    ```
2. Abra o arquivo `notebooks/demo_structures.ipynb`

---

## Exemplos Visuais

O visualizador gera representações em SVG utilizando o Graphviz. Abaixo, exemplos do que é renderizado no notebook:

* **BST:** Nós com seus valores e alturas exibidos.
* **AVL:** Setas coloridas indicando a direção das rotações (L/R) e nós com fatores de balanceamento.
* **B+ Tree:** Páginas agrupadas em clusters visuais para diferenciar claramente nós internos de nós folhas.
* **Tries & Patricia Tries:** Arestas rotuladas com caracteres (Trie) ou prefixos comprimidos (Patricia). Nós que marcam o fim de uma palavra são destacados visualmente (cor verde ou círculo duplo).
* **Hash Table:** Tabela vertical representando os índices (buckets) à esquerda e nós laterais representando os valores armazenados (tratamento de colisão).