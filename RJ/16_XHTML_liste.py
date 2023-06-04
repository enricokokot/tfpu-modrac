"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo tablice.
Cijeli dokument je uokviren samo u element <html>. Tablica <table> se sastoji od redaka <tr>,
redovi od ćelija: <td> ili u zaglavlju <th>. U ćelijama može pisati bilo što.
Dokument može imati proizvoljan broj tablica, koje se mogu nalaziti i jedna unutar druge.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka.
Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemete,
je li odnos HTML elemenata odgovarajući, je li svaki element i zatvoren,
jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd.
Omogućite i da se u ćeliji tablice, osim običnog teksta, može pojaviti i nova tablica.
Redovi tablice smiju sadržavati samo ćelije, a sama tablica smije sadržavati samo redove
(ne i običan tekst). Tablica smije imati najviše jedan redak u kojem se nalaze ćelije
zaglavlja <th> i taj redak, ako postoji, mora biti prvi redak u tablici.
Sami odaberite vrste apstraktnih sintaksnih stabala.

Napišite i odgovarajući „semantički“ analizator (renderer) za XHTML tablice iz prvog zadatka.
„Akcije“ su sljedeće: za svaku ćeliju samo ispišite „|“, njen sadržaj i tabulator;
za svaki redak ispišite znak za prijelom retka. Tablicu započnite i završite s ispisom
„horizontalne crte“ (dovoljno minusa „----------“). Ako tablica ima zaglavlje, nakon zaglavlja
ispišite istu „horizontalnu crtu“.
"""

from vepar import *

class T(TipoviTokena):
    OHTML, ZHTML = '<html>', '</html>'
    OTABLE, ZTABLE = '<table>', '</table>'
    ORED, ZRED = '<tr>', '</tr>'
    OĆELIJA, ZĆELIJA = '<td>', '</td>'
    OZAGLAVLJE, ZZAGLAVLJE = '<th>', '</th>'
    class TEKST(Token): pass

@lexer
def moj(lex):
    for znak in lex:
        if znak.isspace(): lex.zanemari()
        if znak == '<':
            if lex >> '/':
                lex * str.isalpha
                lex >> '>'
                yield lex.literal(T)
            else:
                lex * str.isalpha
                lex >> '>'
                yield lex.literal(T)
        # else: yield lex.literal(T.TEKST)

prikaz(moj("</html>"))
