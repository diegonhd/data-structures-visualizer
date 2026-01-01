import graphviz

class TreeVisualizer:
    def visualize_binary_tree(self, tree):
        dot = graphviz.Digraph()
        dot.attr('node', shape='circle', style='filled', fillcolor='white', fontname='Arial')

        if not tree.root:
            return dot

        def add_nodes_edges(node):
            if not node:
                return

            node_id = str(id(node))
            label = str(node.data)
            
            if hasattr(node, 'height'):
                label += f"\nh={node.height}"

            dot.node(node_id, label)

            if node.left:
                dot.edge(node_id, str(id(node.left)), label='L', color='blue')
                add_nodes_edges(node.left)
            else:
                null_id = node_id + "_left_null"
                dot.node(null_id, shape='point', width='0.1')
                dot.edge(node_id, null_id, style='invis')

            if node.right:
                dot.edge(node_id, str(id(node.right)), label='R', color='red')
                add_nodes_edges(node.right)
            else:
                null_id = node_id + "_right_null"
                dot.node(null_id, shape='point', width='0.1')
                dot.edge(node_id, null_id, style='invis')

        add_nodes_edges(tree.root)
        return dot

    def visualize_bplus_tree(self, tree):
        dot = graphviz.Digraph()
        # Usamos 'plain' para que o formato seja definido puramente pelo HTML da label
        dot.attr('node', shape='plain')
        dot.attr(rankdir='TB')

        if not tree.root:
            return dot

        leaves = []

        def traverse(node):
            node_id = str(id(node))
            
            if node.is_leaf:
                # Construção de tabela HTML para folha
                # bgcolor define a cor de fundo
                label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#e1f5fe"><TR>'
                for key in node.keys:
                    label += f'<TD>{key}</TD>'
                label += '</TR></TABLE>>'
                
                leaves.append(node)
                dot.node(node_id, label)
            else:
                # Construção de tabela HTML para nó interno com PORTAS (c0, c1...)
                label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR>'
                
                # Intercala portas e chaves
                # Formato visual: | * | key | * | key | * |
                for i, key in enumerate(node.keys):
                    label += f'<TD PORT="c{i}" BGCOLOR="#f0f0f0"> </TD>' # Ponteiro
                    label += f'<TD>{key}</TD>'                         # Chave
                
                # Último ponteiro
                label += f'<TD PORT="c{len(node.keys)}" BGCOLOR="#f0f0f0"> </TD>'
                label += '</TR></TABLE>>'
                
                dot.node(node_id, label)

                # Recursão para conectar filhos
                for i, child in enumerate(node.children):
                    child_id = str(id(child))
                    # Conecta da porta específica (c0, c1...) para o topo do nó filho
                    dot.edge(f"{node_id}:c{i}", child_id)
                    traverse(child)

        traverse(tree.root)

        # Conectar folhas (lista encadeada)
        with dot.subgraph(name='leaves') as sub:
            sub.attr(rank='same')
            for i in range(len(leaves) - 1):
                u, v = str(id(leaves[i])), str(id(leaves[i+1]))
                # constraint=false evita que essa aresta afete a hierarquia da árvore
                sub.edge(u, v, constraint='false', style='dashed', color='blue', arrowsize='0.5')

        return dot

    def visualize_trie(self, trie):
        dot = graphviz.Digraph()
        dot.attr(rankdir='TB')

        root_id = str(id(trie.root))
        dot.node(root_id, "root", shape='plaintext')

        def traverse(node, parent_id):
            for char, child_node in sorted(node.children.items()):
                child_id = str(id(child_node))
                
                shape = 'doublecircle' if child_node.is_end_of_word else 'circle'
                color = 'green' if child_node.is_end_of_word else 'black'

                dot.node(child_id, "", shape=shape, color=color)
                dot.edge(parent_id, child_id, label=char)

                traverse(child_node, child_id)

        traverse(trie.root, root_id)
        return dot

    def visualize_patricia(self, tree):
        dot = graphviz.Digraph()

        if not tree.root:
            return dot

        def traverse(node):
            node_id = str(id(node))

            if node.is_leaf:
                label = f"Key: {node.key}"
                dot.node(node_id, label, shape='box', style='filled', fillcolor='#fff9c4')
            else:
                label = f"Bit: {node.bit_index}"
                dot.node(node_id, label, shape='ellipse')

                if node.left:
                    l_id = str(id(node.left))
                    dot.edge(node_id, l_id, label='0', style='dashed')
                    traverse(node.left)

                if node.right:
                    r_id = str(id(node.right))
                    dot.edge(node_id, r_id, label='1')
                    traverse(node.right)

        traverse(tree.root)
        return dot

    def visualize_hashtable(self, hashtable):
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')
        dot.attr('node', shape='record')

        bucket_label = ""
        for i in range(hashtable.capacity):
            bucket_label += f"<f{i}> {i} |"
        bucket_label = bucket_label.rstrip("|")

        dot.node('buckets', bucket_label, width='1.0')

        for i in range(hashtable.capacity):
            curr = hashtable.table[i]
            if curr:
                prev_id = f"buckets:f{i}"

                while curr:
                    curr_id = str(id(curr))
                    # Adiciona espaços para garantir que não pareça HTML tags
                    label = f"{{ {curr.key} | {curr.value} }}"

                    dot.node(curr_id, label)
                    dot.edge(prev_id, curr_id)

                    prev_id = curr_id
                    curr = curr.next

        return dot