from itertools import product

class LogicalExpressionEvaluator:
    OPERATORS = {'!': 3, '&': 2, '|': 2, '->': 1, '~>': 1}
    VARIABLES = ['a', 'b', 'c', 'd', 'e']

    def __init__(self, expr):
        self.original_expr = expr.replace(' ', '')
        self.tokens = self.tokenize(self.original_expr)
        self.rpn = self.to_rpn(self.tokens)
        self.used_vars = sorted(set(t for t in self.tokens if t in self.VARIABLES))

    def tokenize(self, expr):
        tokens, i = [], 0
        while i < len(expr):
            if expr[i] in self.VARIABLES:
                tokens.append(expr[i])
                i += 1
            elif expr[i] in '()!&|':
                tokens.append(expr[i])
                i += 1
            elif expr[i:i+2] in ['->', '~>']:
                tokens.append(expr[i:i+2])
                i += 2
            else:
                raise ValueError(f"Недопустимый символ: {expr[i]}")
        return tokens

    def to_rpn(self, tokens):
        output, stack = [], []
        precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~>': 1}
        right_assoc = {'!'}

        for token in tokens:
            if token in self.VARIABLES:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while (stack and stack[-1] != '(' and
                       (precedence[stack[-1]] > precedence[token] or
                        (precedence[stack[-1]] == precedence[token] and token not in right_assoc))):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            output.append(stack.pop())
        return output

    def eval_rpn(self, rpn, var_values):
        stack = []
        for token in rpn:
            if token in self.VARIABLES:
                stack.append(var_values[token])
            elif token == '!':
                a = stack.pop()
                stack.append(not a)
            elif token == '&':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == '|':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif token == '->':
                b, a = stack.pop(), stack.pop()
                stack.append((not a) or b)
            elif token == '~>':
                b, a = stack.pop(), stack.pop()
                stack.append((a and b) or (not a and not b))
        return stack[0]

    def generate_truth_table(self):
        table = []
        for values in product([False, True], repeat=len(self.used_vars)):
            var_values = dict(zip(self.used_vars, values))
            result = self.eval_rpn(self.rpn, var_values)
            table.append((var_values, result))
        return table

    def build_sdnf(self, table):
        terms, indices = [], []
        for idx, (vals, res) in enumerate(table):
            if res:
                indices.append(idx)
                term = [(v if vals[v] else f'!{v}') for v in self.used_vars]
                terms.append(' & '.join(term))
        return ' | '.join(f'({t})' for t in terms), indices

    def build_sknf(self, table):
        terms, indices = [], []
        for idx, (vals, res) in enumerate(table):
            if not res:
                indices.append(idx)
                term = [(v if not vals[v] else f'!{v}') for v in self.used_vars]
                terms.append(' | '.join(term))
        return ' & '.join(f'({t})' for t in terms), indices

    def print_table(self, table):
        headers = self.used_vars + ['f']
        line = ' | '.join(headers)
        print(f"\n {line}")
        print('-' * len(line.replace('|', '---')))
        for row in table:
            values = [str(int(row[0][v])) for v in self.used_vars]
            result = str(int(row[1]))
            print(' ' + ' | '.join(values + [result]))
