import pydot
import webbrowser

from configuration import (alternative, dot, epsilon, question, star, symbols)
from ExpressionTree import ExpressionTree
from Node import Node


class AFN:
    def __init__(self):
        self.states = None
        self.symbols = None
        self.transitions = {}
        self.initial = None
        self.final = None

        self.stack = []

    def __str__(self):
        return (
                '\nAFN:\n' +
                
                '\nestados: {}\simbolos: {}\ntransiciones: {}\niniciales: {}\nfinales: {}\n' +
                ('-' * 5)
                ).format(self.states, self.symbols, self.transitions, self.initial, self.final)

    def is_empty(self):
        return len(self.stack) == 0

    def last(self):
        return self.stack[-1]

    def manejoalternativos(self, i):
        second_temp_index = self.pop()
        first_temp_index = self.last()
        keys = list(self.transitions)
        keys.sort(reverse=True)
        for key in keys:
            if key[0] >= first_temp_index:
                self.transitions[key[0] + 1, key[1] +
                                 1] = self.transitions.pop(key)
        self.transitions[(first_temp_index,
                          first_temp_index + 1)] = epsilon
        self.transitions[(first_temp_index,
                          second_temp_index + 1)] = epsilon
        self.transitions[(second_temp_index, i + 1)] = epsilon
        self.transitions[(i, i + 1)] = epsilon
        return i + 2


    def manejopuntos(self, i):
        temp_index = self.pop()
        keys = list(self.transitions)
        keys.sort()
        for key in keys:
            if key[0] >= temp_index:
                self.transitions[key[0] - 1, key[1] -
                                 1] = self.transitions.pop(key)
        return i - 1

    def manejoestrellas(self, i):
        temp_index = self.last()
        keys = list(self.transitions)
        keys.sort(reverse=True)
        for key in keys:
            if key[0] >= temp_index:
                self.transitions[key[0] + 1, key[1] +
                                 1] = self.transitions.pop(key)
        self.transitions[(temp_index, temp_index + 1)] = epsilon
        self.transitions[(temp_index, i + 1)] = epsilon
        self.transitions[(i, temp_index + 1)] = epsilon
        self.transitions[(i, i + 1)] = epsilon
        return i + 2

    def manejointer(self, i):
        return self.manejoalternativos(self.manejosimbolos(epsilon, i))
    
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            BaseException("Error")

    def push(self, op):
        self.stack.append(op)

    def manejosimbolos(self, symbol, i):
        self.transitions[(i, i+1)] = symbol
        self.push(i)
        return i + 2


    def generacionAFN(self, root: Node, i=0):
        if root:
            i = self.generacionAFN(root.left, i)
            i = self.generacionAFN(root.right, i)
            if root.value in symbols:
                return self.manejosimbolos(root.value, i)

            elif root.value == alternative:
                return self.manejoalternativos(i)

            elif root.value == dot:
                return self.manejopuntos(i)

            elif root.value == star:
                return self.manejoestrellas(i)

            elif root.value == question:
                return self.manejointer(i)

        return i

    def generate_AFN_from_re(self, expression_tree: ExpressionTree):

        self.generacionAFN(expression_tree.tree)

        keys = list(self.transitions)
        keys.sort()
        for key in keys:
            self.transitions[key] = self.transitions.pop(key)
        states = list(dict.fromkeys([item for t in keys for item in t]))
        states.sort()
        newTransitions = {}
        for (i, f), t in self.transitions.items():
            if(i, t) not in newTransitions:
                newTransitions[(i, t)] = [f]
            else:
                newTransitions[(i, t)].append(f)

        self.states = states
        self.symbols = list(dict.fromkeys(self.transitions.values()))
        self.transitions = newTransitions
        self.initial = states[0]
        self.final = states[len(states) - 1]

    def graph_AFN(self):

        with open('AFN.dot', 'w', encoding='utf-8') as file:
            keys = list(self.transitions)
            file.write('digraph{\n')
            file.write('rankdir=LR\n')
            for state in self.states:
                if state == self.initial:
                    file.write('{} [root=true]\n'.format(state))
                    file.write('fake [style=invisible]\n')
                    file.write('fake -> {} [style=bold]\n'.format(state))
                elif state == self.final:
                    file.write('{} [shape=doublecircle]\n'.format(state))
                else:
                    file.write('{}\n'.format(state))
            for key in keys:
                for t in self.transitions[key]:
                    file.write(
                        '{} -> {} [ label="{}" ]\n'.format(key[0], t, key[1]))
            file.write('}\n')

        (graph,) = pydot.graph_from_dot_file('AFN.dot')
        graph.write_png('OUTPUT AFN.png')
        webbrowser.open('OUTPUT AFN.png')

