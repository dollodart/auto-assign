"""Taken from pyparsing docs."""

from pyparsing import (
    Literal,
    Word,
    Group,
    Forward,
    alphas,
    alphanums,
    Regex,
    ParseException,
    Suppress
)

exprStack = []


def push_first(toks):
    exprStack.append(toks[0])


def push_unary_minus(toks):
    for t in toks:
        if t == "-":
            exprStack.append("unary -")
        else:
            break


bnf = None


def BNF():
    global bnf
    if not bnf:
        fnumber = Regex(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?")
        ident = Word(alphas, alphanums + "_$")

        plus, minus = map(Literal, "*/")
        lpar, rpar = map(Suppress, "()")
        addop = plus | minus
        multop = Literal("^")

        expr = Forward()
        aatom = (fnumber | ident).setParseAction(push_first)
        pgroup = Group(lpar + expr + rpar)
        atom = (addop[...] + (aatom | pgroup)).setParseAction(push_unary_minus)

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
        # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not
        # (2^3)^2.
        factor = Forward()
        factor <<= atom + (multop + factor).setParseAction(push_first)[...]  
        expr <<= factor + (addop + factor).setParseAction(push_first)[...]
        bnf = expr
    return bnf

def str2tuple(x):
    """Converts string to tuple or passes tuple type through."""
    if x == 'M':
        return 1, 0, 0
    elif x == 'D':
        return 0, 1, 0
    elif x == 'T':
        return 0, 0, 1
    return x


def linscale(x, y):
    x = str2tuple(x)
    return x[0] * y, x[1] * y, x[2] * y


def linadd(x, y):
    x = str2tuple(x)
    y = str2tuple(y)
    return x[0] + y[0], x[1] + y[1], x[2] + y[2]


def linsubtract(x, y):
    x = str2tuple(x)
    y = str2tuple(y)
    return x[0] - y[0], x[1] - y[1], x[2] - y[2]


opn = {
    "*": linadd,
    "/": linsubtract,
    "^": linscale
}


def evaluate_stack(s):
    op, num_args = s.pop(), 0
    if isinstance(op, tuple):
        op, num_args = op
    if op == "unary -":
        return -evaluate_stack(s)
    if op in "*/^":
        # note: operands are pushed onto the stack in reverse order
        op2 = evaluate_stack(s)
        op1 = evaluate_stack(s)
        return opn[op](op1, op2)
    else:
        try:
            return int(op)
        except ValueError:
            try:
                return float(op)
            except: 
                return op


def eval_dim(s):
    exprStack[:] = []
    s = s.replace('kg', 'M')
    s = s.replace('m', 'D')
    s = s.replace('s', 'T')
    BNF().parseString(s, parseAll=True)
    return evaluate_stack(exprStack[:])


if __name__ == "__main__":
    def test(s):
        exprStack[:] = []
        try:
            s = s.replace('kg', 'M')
            s = s.replace('m', 'D')
            s = s.replace('s', 'T')
            results = BNF().parseString(s, parseAll=True)
            print(results)
            val = evaluate_stack(exprStack[:])
        except ParseException as pe:
            print(s, "failed parse:", str(pe))
        else:
            print(val)

    test('kg*m/s^2')
    test('(kg/m)*(m/s)')
    test('(kg^-1/m)*(s/m^-1)')
    test('(kg*m)^1.5/s')
    f = eval_dim('(kg/m/m)*s')

