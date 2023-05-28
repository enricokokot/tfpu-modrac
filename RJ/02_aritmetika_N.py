"""Izračunavanje aritmetičkih izraza nad skupom prirodnih brojeva.

Podržani operatori su + (zbrajanje), * (množenje) i ^ (potenciranje).
Svi operatori su binarni i desno asocirani, radi jednostavnosti parsera.
Zbrajanju i množenju je svejedno jer su to asocijativne operacije,
a potenciranje se obično po dogovoru shvaća desno asocirano (2^3^2=2^9=512).
Zagrade su dozvoljene, ali često nisu nužne. Prioritet je uobičajen (^, *, +).

Implementiran je i jednostavni optimizator, koji detektira sve nule i
jedinice u izrazima, te pojednostavljuje izraze koji ih sadrže
(x+0=0+x=x*1=1*x=x^1=x, x^0=1^x=1, x*0=0*x=0^x=0
  - ovo zadnje pravilo se uvijek primjenjuje nakon x^0=1, jer 0^0=1)."""

from vepar import *

class T(TipoviTokena):
    PLUS, PUTA, POTENCIRANJE, OTV, ZATV = '+*^()'
    class BROJ(Token):
        def vrijednost(t): return int(t.sadržaj)

@lexer
def moj(lex):
    for znak in lex:
        if znak.isdecimal():
            lex.prirodni_broj(znak, nula=False)
            yield lex.token(T.BROJ)
        else: yield lex.literal(T)


moj("1+2^3")

### BKG
# izraz -> član | član PLUS izraz
# član -> faktor | faktor PUTA član
# faktor -> BROJ | OTV izraz ZATV

class P(Parser):
    def izraz(p): 
        prvi = p.član()
        if p >= T.PLUS:
            drugi = p.izraz()
            return Zbroj(prvi, drugi)
        else: return prvi

    def član(p):
        prvi = p.faktor()
        if p >= T.PUTA:
            drugi = p.član()
            return Umnožak(prvi, drugi)
        else: return prvi

    def faktor(p):
        if broj := p >= T.BROJ: return broj
        p >> T.OTV
        u_zagradi = p.izraz()
        p >> T.ZATV
        return u_zagradi

class Zbroj(AST):
    lijevo: ...
    desno: ...

class Umnožak(Zbroj): pass

class Faktor(Zbroj): pass

# prikaz(P('5^2+8*12'))
prikaz(P('5+8*12'))