from vepar import *

class T(TipoviTokena):
    NEG, OR, OO, OZ, UO, UZ ="'+()[]"
    class SLOVO(Token):
        def realiz(self): return self

@lexer
def sklop(lex):
    for znak in lex:
        if znak.isalpha(): yield lex.token(T.SLOVO)
        elif znak.isspace(): lex.zanemari()
        else: yield lex.literal(T)

### BKG
# izraz -> (suma članova): izraz OR član | član
# član -> (produkt faktora): član faktor | faktor
# faktor -> SLOVO | (izraz u zagradama): OO izraz OZ | UO izraz UZ | faktor NEG

class P(Parser):
    def izraz(p):
        lista = [p.član()]
        while p >= T.OR:
            lista.append(p.član())
        return Or.ili_samo(lista)
    
    def član(p):
        lista = [p.faktor()]
        while p > {T.SLOVO, T.OO, T.UO}:
            lista.append(p.faktor())
        return And.ili_samo(lista)
    
    def faktor(p):
        if slovo := p >= T.SLOVO: dalje = slovo
        elif p >= T.OO:
            u_zag = p.izraz()
            p >> T.OZ
            dalje = u_zag
        elif p >> T.UO:
            u_zag = p.izraz()
            p >> T.UZ
            dalje = Not(u_zag)
        else: raise p.greška()
        while p >= T.NEG:
            dalje = Not(dalje)
        return dalje
    
class Not(AST):
    ulaz: "izraz"   # točno 1
    def realiz(self):
        return [self.ulaz.realiz()]

class Or(AST):
    ulazi: "izraz+" # 2 ili više
    def realiz(self):
        lista = []
        for ulaz in self.ulazi:
            lista.append([ulaz.realiz()])
        return lista

class And(AST):
    ulazi: "izraz+" # 2 ili više
    def realiz(self):
        # return [[ulaz.realiz() for ulaz in self.ulazi()]]
        lista = []
        for ulaz in self.ulazi:
            lista.append(ulaz.realiz())
        return [lista]
    
def makni2n(lista):
    if not isinstance(lista, list): return lista
    lista_opt = []
    for element in lista:
        lista_opt.append(makni2n(element))

    if isinstance(lista_opt, list) and len(lista_opt) == 1:
        if isinstance(lista_opt[0], list) and len(lista_opt[0]) == 1:
            return lista_opt[0][0]
        else: return lista_opt
    else: return lista_opt

# print(stablo := P("(a'+[t])"))
stablo = P("[[a+bc]]")
# print(stablo.realiz())
print(makni2n(stablo.realiz()))