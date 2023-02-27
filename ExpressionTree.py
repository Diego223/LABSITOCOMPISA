from configuration import *
from Node import Node


class ExpressionTree:
    def __init__(self, r):
        self.r = r

        self.tree = None

        self.nodes = {}

        self.postfix = []

        self.last_c = None

        self.precedence = {
            alternative: 1,
            dot: 2,
            question: 3,
            star: 3
        }

        self.nullable = {}
        self.firstpos = {}
        self.lastpos = {}
        self.nextpos = {}

        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def last(self):
        return self.stack[-1]

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            BaseException("Error 404")

    def push(self, op):
        self.stack.append(op)

    def not_greater(self, i):
        try:
            return self.precedence[i] <= self.precedence[self.last()]
        except:
            BaseException("Error 404 ")

    def process_dot(self, c):

        if (c in [*symbols, Aperturas, AperturasIter, Aperturasopti] and
                self.last_c in [*symbols, Cerraduras, CerradurasIter, Cerradurasopti, question, star]):
            self.process(dot)

    def process_operator(self, c):
        while(not self.is_empty() and self.not_greater(c)):
            self.postfix.append(self.pop())
        self.push(c)

    def process(self, c):
        if c in [*symbols, Aperturas, AperturasIter, Aperturasopti]:
            while(not self.is_empty() and self.last() in [question, star]):
                self.postfix.append(self.pop())

        # if simbolo
        if c in symbols:
            self.postfix.append(c)

        # if ( o { o [
        elif c in [Aperturas, AperturasIter, Aperturasopti]:
            self.push(c)

        # if )
        elif c == Cerraduras:
            while not self.is_empty() and self.last() != Aperturas:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() or self.last() != Aperturas:
                BaseException("Error")
            else:
                self.pop()

        # if }
        elif c == CerradurasIter:
            while not self.is_empty() and self.last() != AperturasIter:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() and self.last() != AperturasIter:
                BaseException("Error")
            else:
                self.pop()
                self.process_operator(star)

        # if ]
        elif c == Cerradurasopti:
            while not self.is_empty() and self.last() != Aperturasopti:
                a = self.pop()
                self.postfix.append(a)
            if self.is_empty() and self.last() != Aperturasopti:
                BaseException("Error")
            else:
                self.pop()
                self.process_operator(question)

        # if operador
        else:
            self.process_operator(c)

        self.last_c = c

    # Generamos Postfix
    def generate_postfix(self):
        self.last_c = None

        for c in self.r:
            self.process_dot(c)
            self.process(c)

        while not self.is_empty():
            self.postfix.append(self.pop())

    # Generamos el arbol mediante POSTFIX
    def generate_functions(self, node: Node, i=0):
        if node:
            i = self.generate_functions(node.left, i)
            i = self.generate_functions(node.right, i)
            node.id = i
            self.nodes[i] = node.value

            if node.value == epsilon:
                self.nullable[node.id] = True
                self.firstpos[node.id] = []
                self.lastpos[node.id] = []
            elif node.value in symbols:
                self.nullable[node.id] = False
                self.firstpos[node.id] = [node.id]
                self.lastpos[node.id] = [node.id]
            elif node.value == alternative:
                self.nullable[node.id] = self.nullable[node.left.id] or self.nullable[node.right.id]
                self.firstpos[node.id] = [
                    *self.firstpos[node.left.id], *self.firstpos[node.right.id]]
                self.lastpos[node.id] = [
                    *self.lastpos[node.left.id], *self.lastpos[node.right.id]]
            elif node.value == dot:
                self.nullable[node.id] = self.nullable[node.left.id] and self.nullable[node.right.id]
                self.firstpos[node.id] = [*self.firstpos[node.left.id], *self.firstpos[node.right.id]
                                          ] if self.nullable[node.left.id] else self.firstpos[node.left.id]
                self.lastpos[node.id] = [*self.lastpos[node.left.id], *self.lastpos[node.right.id]
                                         ] if self.nullable[node.right.id] else self.lastpos[node.right.id]
            elif node.value in [star, question]:
                self.nullable[node.id] = True
                self.firstpos[node.id] = self.firstpos[node.left.id]
                self.lastpos[node.id] = self.lastpos[node.left.id]

            if node.value == dot:
                for lastpos in self.lastpos[node.left.id]:
                    if lastpos in self.nextpos.keys():
                        self.nextpos[lastpos] = list(dict.fromkeys([
                            *self.nextpos[lastpos], *self.firstpos[node.right.id]]))
                    else:
                        self.nextpos[lastpos] = self.firstpos[node.right.id]
                    self.nextpos[lastpos].sort()
            elif node.value == star:
                for lastpos in self.lastpos[node.left.id]:
                    if lastpos in self.nextpos.keys():
                        self.nextpos[lastpos] = list(dict.fromkeys([
                            *self.nextpos[lastpos], *self.firstpos[node.left.id]]))
                    else:
                        self.nextpos[lastpos] = self.firstpos[node.left.id]
                    self.nextpos[lastpos].sort()

            return i + 1
        return i

    def generate_tree(self):
        # Generamos el postfix postfix
        self.generate_postfix()

        for c in self.postfix:
            # if simbolo
            if c in symbols:
                self.push(Node(c))
            # if operador
            else:
                op = Node(c)
                # Si es algun operador de un solo simbolo ? o *
                if c in [question, star]:
                    x = self.pop()
                
                else:
                    y = self.pop()
                    x = self.pop()
                    op.right = y
                op.left = x
                self.push(op)
        self.tree = self.pop()
        self.generate_functions(self.tree)

    # Recorremos el tree
    def search_by_id(self, id):
        if id in self.nodes.keys():
            return self.nodes[id]
        return None
