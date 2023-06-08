"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo liste.
Cijeli dokument je uokviren samo u <html> element koji se sastoji od zaglavlja <head> i
tijela <body>. Zaglavlje smije sadržavati samo običan tekst, a tijelo se sastoji od
običnog teksta i listi. Liste mogu biti uređene <ol> i neuređene <ul>.
Lista se sastoji od <li> elemenata. U jednom elementu liste smije se nalaziti običan tekst ili
nova lista, ali ne i oboje. Dokument može sadržavati proizvoljan broj listi.
Poštujte uobičajena pravila za XHTML dokumente.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka.
Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemente,
je li odnos XHTML elemenata odgovarajući , je li svaki element i zatvoren,
jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd.
Omogućite i da se u <li> elementu liste, osim običnog teksta, može pojaviti i
nova lista (ali ne i oboje). Liste smiju sadržavati samo <li> elemente
(ne tekst i ne direktno druge liste).

Napišite i odgovarajući „semantički“ analizator (renderer) za XHTML liste iz prvog zadatka.
Za svaki <li> element iz neuređene liste ispišite tabulator, „*“,
sadržaj <li> elementa ako se radi o tekstu, te znak za prijelom retka.
Ako je sadržaj <li> elementa nova lista, onda samo ispišite novu listu.
Elemente liste s prve razine treba ispisati s jednim tabulatorom na početku, a za svaku
dodatnu razinu treba ispisati i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, itd.).
"""

from vepar import *

class T(TipoviTokena):
    OHTML, ZHTML = '<html>', '</html>'
    OHEAD, ZHEAD = '<head>', '</head>'
    OBODY, ZBODY = '<body>', '</body>'
    OOL, ZOL = '<ol>', '</ol>'
    OUL, ZUL = '<ul>', '</ul>'
    OLI, ZLI = '<li>', '</li>'
    class TEKST(Token): pass

@lexer
def moj(lex):
    for znak in lex:
        if znak.isspace(): lex.zanemari()
        elif znak == '<':
            if lex >= '/':
                lex * str.isalpha
                lex >= '>'
                yield lex.literal(T)
            else:
                lex * str.isalpha
                lex >= '>'
                # lex - '>'
                yield lex.literal(T)
        # radi samo ako tekst smije biti samo slova
        # elif znak.isalpha:
        #     lex*str.isalpha
        #     yield lex.token(T.TEKST)
        # else: yield lex.literal(T)
        else:
            lex < {'', '<', str.isspace}
            yield lex.token(T.TEKST)

print(moj("""
<html>
        <head>
            bla   bla
        </head>
        <body>
            &hmm;
            hm hm
            <ol>
                <li>A ovo je drugi.</li>
                <li> Ovo je   --- ne bi čovjek vjerovao  --- treći.</li>
                <li>
                    <ul>
                        <li>
                            <ol>
                                <li>Trostruka dubina!</li>
                            </ol>
                        </li>
                        <li>Dvostruka!</li>
                    </ul>
                </li>
                <li>nastavak...</li>
            </ol>
            I još malo<ul><li>uvučeno</li></ul>
        </body>
    </html>
"""))
