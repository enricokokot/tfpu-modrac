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
    PLUS, PUTA, NA, OTV, ZATV = '+*^()'
    class BROJ(Token):
        def vrijednost(t): return int(t.sadržaj)

@lexer
def moj(lex):
    for znak in lex:
        if znak == "0": yield lex.token(T.BROJ)
        elif znak.isdecimal():
            lex * str.isdecimal
            yield lex.token(T.BROJ)
        elif znak.isspace(): lex.zanemari()
        else: yield lex.literal(T)


moj("1+2^3")
# raise SystemExit

### BKG
# izraz -> član | član PLUS izraz
# član -> faktor | faktor PUTA član
# faktor -> faktor NA baza
# baza -> BROJ

class P(Parser):
    def izraz(p) -> 'član|Zbroj': 
        t = p.član()
        while p >= T.PLUS:
            t = Zbroj(t, p.član())
        return t

    def član(p) -> 'faktor|Umnožak':
        t = p.faktor()
        if p >= T.PUTA:
            t = Umnožak(t, p.član())
        return t

    def faktor(p) -> 'baza|Potencija':
        t = p.baza()
        if p >= T.NA:
            t = Potencija(t, p.član())
        return t

    def baza(p) -> 'izraz':
        if t := p >= T.BROJ: pass
        else:
            p >> T.OTV
            t = p.izraz()
            p >> T.ZATV
        return t


class Zbroj(AST):
    lijevi: 'izraz'
    desni: 'izraz'

    def vrijednost(self):
        return self.lijevi.vrijednost() + self.desni.vrijendost()

class Umnožak(Zbroj):
    lijevi: 'izraz'
    desni: 'izraz'

    def vrijednost(self):
        return self.lijevi.vrijednost() * self.desni.vrijendost()

class Potencija(Zbroj):
    lijevi: 'izraz'
    desni: 'izraz'

    def vrijednost(self):
        return self.lijevi.vrijednost() ** self.desni.vrijendost()

# prikaz(P('5^2+8*12'))
# prikaz(P('5+8*12'))
prikaz(P('2+(3^3+4)+3'))