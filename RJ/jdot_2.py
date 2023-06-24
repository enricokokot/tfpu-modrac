from vepar import *

# class T(TipoviTokena):
#     PLUS, PUTA, NA, OTVORENA, ZATVORENA = '+x^()'
#     class BROJ(Token):
#         def vrijednost(t): return int(t.sadržaj)
#         def optim(t): return t
#         def prevedi(t): yield ['PUSH', t.vrijednost()]

class T(TipoviTokena):
    NULL, UGL, ZUGL, ZAR, VIT, ZVIT, DVT  = 'null', '[', ']', ',', '{', '}', ':'
    class ISTINITOST(Token): ...
    class CBROJ(Token): ...
    class RBROJ(Token): ...
    class STRING(Token): ...

# @lexer
# def an(lex):
#     for znak in lex:
#         if znak.isdecimal():
#             lex.prirodni_broj(znak)
#             yield lex.token(T.BROJ)
#         else: yield lex.literal(T)

@lexer
def lekser(lex):
    for znak in lex:
        if znak.isspace(): lex.zanemari()
        if znak.isalpha():
            lex * str.isalpha
            if lex.sadržaj in {'true', 'false'}:
                yield lex.token(T.ISTINITOST)
            else:
                yield lex.literal(T)
        if znak == '-' or znak.isdecimal():
            lex * str.isdecimal
            if lex >= '.':
                lex >> str.isdecimal
                lex * str.isdecimal
                yield lex.token(T.RBROJ)
            else:
                yield lex.token(T.CBROJ)
        if znak == '[': yield lex.token(T.UGL)
        if znak == ']': yield lex.token(T.ZUGL)
        if znak == ',': yield lex.token(T.ZAR)
        if znak == '"':
            lex <= '"'
            # lex.pročitaj_do('"', više_redova=True)
            yield lex.token(T.STRING)
        if znak == '{': yield lex.token(T.VIT)
        if znak == '}': yield lex.token(T.ZVIT)
        if znak == ':': yield lex.token(T.DVT)
        
# print(lekser('true, [] false null -100 -53.5 [1, null, false, -12.5] "marko" {"a": true, "b": [2], "": {"a": 0} } '))


### BKG
# jdot -> NULL | ISTINITOST | CBROJ | RBROJ | polje | STR | obj
# polje -> UGL elementi ZUGL | UGL ZUGL
# elementi -> elementi ZAR jdot | jdot
# obj -> VIT parovi ZVIT | VIT ZVIT
# parovi -> parovi ZAR par | par
# par -> STR DVT jdot

# [elementi, NULL] -> [elementi, CBROJ, NULL] -> [elementi, STR, CBROJ, NULL] -> [ISTINITOST, STR, CBROJ, NULL]

# [elementi] -> [null]
# [elementi] -> [elementi, true] -> [true, true]
# [elementi] -> [elementi, true] -> [elementi, true, true]

'''
jdot
polje
UGL elementi ZUGL
UGL elementi ZAR jdot ZUGL
UGL jdot ZAR jdot ZUGL
UGL NULL ZAR ISTINITOST ZUGL = [null, true]
'''

# class P(Parser):
#     def izraz(p) -> 'Zbroj|član':
#         prvi = p.član()
#         if p >= T.PLUS:
#             drugi = p.izraz()
#             return Zbroj([prvi, drugi])
#         else:
#             return prvi

# def stavka(p) -> 'element':
#         p >> T.LI
#         rezultat = p.element()
#         p >> T.ZLI
#         return rezultat

class P(Parser):
    def jdot(p):
        if p > T.NULL: return p >> T.NULL
        if p > T.ISTINITOST: return p >> T.ISTINITOST
        if p > T.CBROJ: return p >> T.CBROJ
        if p > T.RBROJ: return p >> T.RBROJ
        if p > T.STRING: return p >> T.STRING
        if p > T.UGL:
            t = p.polje()
            return t

    def polje(p):
        p >> T.UGL
        elementi = []
        while element := p > {T.NULL, T.ISTINITOST, T.CBROJ, T.RBROJ, T.STRING, T.UGL}: 
            if p > T.UGL:
                t = p.polje()
                elementi.append(t)
            else:
                p >= {T.NULL, T.ISTINITOST, T.CBROJ, T.RBROJ, T.STRING}
                elementi.append(element)
            p >= T.ZAR
            
        p >> T.ZUGL
        return Polje(elementi)
        
class Polje(AST):
    elementi: ...

print(lekser('[1,]'))
prikaz(P('[1,]'))
print(P('[1,]'))

# 'NULL'


# null -> NULL
# null true false [1, 3] -> NULL TRUE FALSE UGL BROJ ZAR BROJ ZUGL
# UGL BROJ ZAR BROJ ZUGL