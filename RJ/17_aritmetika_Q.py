"""
a = 2/3
...
a = a + 3
b = x - 1 (wrong)
a = 007
_x = 3
1x = 3 (wrong)
"""

from fractions import Fraction
from vepar import *

class T(TipoviTokena):
    class IME(Token):
        def izvrijedni(self):
            if self not in rt.memorija:
                raise self.nedeklaracija(f"{rt.trenutno_ime}")
    class BROJ(Token):
        def izvrijedni(self):
            return int(self.sadržaj)

    JEDNAKO, PLUS, MINUS, PUTA, KROZ, NOVIRED, OTV, ZATV = "=+-*/\n()"

@lexer
def aritmQ(lex):
    for znak in lex:
        if znak.isalpha() or znak == "_":
            lex + {str.isalpha, str.isdecimal, "_"}
            yield lex.token(T.IME)
        elif znak.isdecimal():
            lex * str.isdecimal
            yield lex.token(T.BROJ)
        elif znak.isspace() and znak != "\n": lex.zanemari()
        else: yield lex.literal(T)

aritmQ('''\
a = 2/3
b = a + 1
a = a + 3
b = x - 1
a = 007
''')

## BKG
# program -> naredba | program naredba
# naredba -> IME JEDNAKO izraz NOVIRED
# izraz -> član | izraz PLUS član | izraz MINUS član
# član -> faktor | član PUTA faktor | član KROZ faktor
# faktor -> OTV izraz ZATV | IME | BROJ

class P(Parser):
    def program(p) -> "Program":
        naredbe = []
        while not p > KRAJ:
            return naredbe.append(p.naredba())
        return Program(naredbe)

def naredba(p) -> "Pridruži":
    ime = p >> T.IME
    P >> T.JEDNAKO
    izraz = p.izraz()
    p >> T.NOVIRED
    return Pridruži(ime, izraz)

def izraz(p) -> "Zbroj|Razlika|član":
    stablo = p.član()
    while operator := p >= {T.PLUS, T.MINUS}:
        if operator ^ T.PLUS: stablo = Zbroj(stablo, p.član())
        elif operator ^ T.MINUS: stablo = Razlika(stablo, p.član())
        else: assert False, f"nemoguć operator [operator]"
    # return stablo

def član(p) -> "Umnožak|Količnik|faktor":
    stablo = p.faktor()
    while operator := p >= {T.PUTA, T.KROZ}:
        if operator ^T.PUTA: stablo = Umnožak(stablo, p.faktor())
        elif operator ^T.KROZ:
            stablo = Količnik(stablo, p.faktor(), operator)
        else: assert False, f"nemoguć operator [operator]"
    return stablo

def faktor(p) -> "IME|BROJ|izraz":
    if pročitao := p >= {T.IME, T.BROJ}: return pročitao
    else:
        p >> T.OTV
        u_zagradi = p.izraz()
        p >> T.ZATV
        return u_zagradi

### AST
# Program: naredbe: Pridruži+
# Pridruži: ime:T.IME izraz:izraz
# izraz: Zbroj: lijevo:izraz desno:izraz
#        Razlika: lijevo:izraz desno:izraz
#        Umnožak: lijevo:izraz desno:izraz
#        Količnik: lijevo:izraz desno:izraz

class Program(AST):
    naredbe: "naredba+"
    def izvrši(self):
        rt.trenutno_ime = None
        rt.memorija = Memorija()
        for naredba in self.naredbe:
            naredba.izvrši()
        print("Nema grešaka")

class Pridruži(AST):
    ime: "T.IME"
    izraz: "izraz"
    def izvrši(self):
        rt.trenutno_ime = self.ime
        rt.memorija[self.ime] = self.izraz.izvrijedni()

class Zbroj(AST):
    lijevo: "izraz"
    desno: "izraz"
    def izvrijedni(self):
        return self.lijevo.izvrijedni() + self.desno.izvijedni()

class Razlika(Zbroj):
    def izvijedni(self):
        return self.lijevo.izvrijedni() - self.desno.izvijedni()

class Umnožak(Zbroj):
    def izvijedni(self):
        return self.lijevo.izvrijedni() * self.desno.izvijedni()

class Količnik(AST):
    lijevo: "izraz"
    desno: "izraz"
    razlomačka_crta: "T.KROZ"
    def izvijedni(self):
        brojnik = self.lijevo.izvrijedni()
        nazivnik = self.desno.izvrijedni()
        if nazivnik == 0:
            # raise GreškaIzvođenja
            raise self.razlomačka_crta.iznimka(
                f"dijeljenja broja {brojnik} nulom pri pridruživanju {rt.trenutno_ime}")
        return Fraction(brojnik/nazivnik)

prikaz(P('''\
a = 2/3
b = a + 1
a = a + 3
b = x - 1
a = 007
_xy = 2-(4+2)
''').izvrši())