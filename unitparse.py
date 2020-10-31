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

def str2dict(x):
    """Converts string to dict or passes dict type through."""
    if type(x) is str:
        return {x:1}
    return x


def linscale(x, y):
    x = str2dict(x)
    if type(x) is int:
        return x**y
    return {k:y*v for k, v in x.items()}


def linadd(x, y):
    x = str2dict(x)
    y = str2dict(y)
    k1 = set(x.keys())
    k2 = set(y.keys())
    inter = k1.intersection(k2)
    diff1 = k1.difference(k2)
    diff2 = k2.difference(k1)
    d = {}
    for k in inter:
        d[k] = x[k] + y[k]
    for k in diff1:
        d[k] = x[k]
    for k in diff2:
        d[k] = y[k]

    return d 


def linsubtract(x, y):
    x = str2dict(x)
    y = str2dict(y)
    k1 = set(x.keys())
    k2 = set(y.keys())
    inter = k1.intersection(k2)
    diff1 = k1.difference(k2)
    diff2 = k2.difference(k1)
    d = {}
    for k in inter:
        d[k] = x[k] - y[k]
    for k in diff1:
        d[k] = x[k]
    for k in diff2:
        d[k] = -y[k]

    return d 


opn = {"*": linadd,
       "/": linsubtract,
       "^": linscale}


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


def eval_units(s):
    exprStack[:] = []
    BNF().parseString(s, parseAll=True)
    r = evaluate_stack(exprStack[:])
    if type(r) is str:
        return {r:1}
    return r

if __name__ == "__main__":
    def test(s):
        exprStack[:] = []
        try:
            results = BNF().parseString(s, parseAll=True)
            print(results)
            val = evaluate_stack(exprStack[:])
        except ParseException as pe:
            print(s, "failed parse:", str(pe))
        else:
            print(val)

    #test('kg*m/s^2')
    #test('(kg/m)*(m/s)')
    #test('(kg^-1/m)*(s/m^-1)')
    #test('(kg*m)^1.5/s')

    st = '(kg/m/ft)*(Btu^2)^3' # Btu^2^3 evals to Btu^8
    # since calculator has right associative power and evals 2^3=8 first
    st = '(kg/m/ft)*Btu^2^3'
    f = eval_units(st)
    #print(st)
    print(f,type(f))

    #l = [0]*7
    #from unit import dim
    #for k, v in f.items():
    #    d = tuple(x*v for x in dim[k])
    #    l = [l[i] + d[i] for i in range(len(d))]
    #print(l)
