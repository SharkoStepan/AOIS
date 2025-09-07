def remove_spaces(s: str) -> str:
    return s.replace(" ", "")

def is_valid_symbols(s: str) -> bool:
    i = 0
    while i < len(s):
        if s[i] == '-':
            if i + 1 >= len(s) or s[i + 1] != '>':
                return False
            i += 2
        elif s[i] in "abcde&|!~()":
            i += 1
        else:
            return False
    return True

def check_parentheses(s: str) -> bool:
    balance = 0
    for c in s:
        if c == '(':
            balance += 1
        elif c == ')':
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

def extract_variables(s: str) -> list[str]:
    vars = set()
    for c in s:
        if 'a' <= c <= 'e':
            vars.add(c)
    return sorted(vars)

def tokenize(s: str) -> list[str]:
    tokens = []
    i = 0
    while i < len(s):
        if s[i] == '-' and i + 1 < len(s) and s[i + 1] == '>':
            tokens.append("->")
            i += 2
        elif s[i] in "!~&|()":
            tokens.append(s[i])
            i += 1
        elif 'a' <= s[i] <= 'e':
            tokens.append(s[i])
            i += 1
        else:
            return []
    return tokens


