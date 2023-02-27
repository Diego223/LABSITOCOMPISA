import functools
import timeit

from AFN import AFN
from ExpressionTree import ExpressionTree


def timemeasure(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        tinicial = timeit.default_timer()
        resultado = func(*args, **kwargs)
        tfinal = timeit.default_timer()
        print("Tiempo transcurrido: ", tfinal - tinicial, " segundos")
        return resultado
    return new_func

@timemeasure

def thompson_algorithm(regular_expression: str):

    # Generacion del syntax tree para debido NFA
    expression_tree = ExpressionTree(regular_expression)
    expression_tree.generate_tree()

    # Generacion del AFN
    nfa = AFN()
    nfa.generate_AFN_from_re(expression_tree)

    # Printeamos el NFA
    print(nfa)
    nfa.graph_AFN()

    return nfa
