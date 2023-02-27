
Aperturas = '('
Cerraduras = ')'

AperturasIter = '{'
CerradurasIter = '}'

Aperturasopti = '['
Cerradurasopti = ']'

# |
alternative = '|'
# •
dot = '•'
# ?
question = '[]'
# *
star = '{}'

epsilon = 'ε'
hash = '#'


def replace_reserved_words(r: str):
    return (r
            .replace('(', 'β')
            .replace(')', 'δ')
            .replace('{', 'ζ')
            .replace('}', 'η')
            .replace('[', 'θ')
            .replace(']', 'ω')
            .replace('|', 'φ')
            )


symbols = [replace_reserved_words(chr(i)) for i in range(1, 255)]
