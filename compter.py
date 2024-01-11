from urllib.request import urlopen

from bs4 import BeautifulSoup


def compter_des_mots(untexte):
    mondico = {}
    mots = untexte.split()
    for mot in mots:
        if mot in mondico:
            mondico[mot] += 1
        else:
            mondico[mot] = 1

    trie = sorted(mondico, key=lambda word: mondico[word], reverse=True)
    dico_trie = {}
    for mot in trie:
        dico_trie[mot] = mondico[mot]

    return dico_trie


with open('mots_parasites.csv', 'r') as fichier:
    parasite = fichier.read()
    liste_parasite = parasite.splitlines()


def suppression_parasite(dico_trie, liste_parasite):
    dico_utile = {}
    for clef, valeur in dico_trie.items():
        if clef not in liste_parasite:
            dico_utile[clef] = valeur
    return dico_utile


def rechercher_html(html, nombalise , nomattribut):
    liste = []
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all(nombalise):
        liste.append(a.get(nomattribut))
    return liste


def tri_http(url):
    if url.startswith("http://") == True:
        return url[7:]
    else:
        return url


def index_http(slash):
    if slash.find("/") == -1:
        return slash
    else:
        position = slash.index("/")
        return slash[0:position]


def tri_site(mon, maliste):

    liste_ok = []
    liste_not_ok = []
    for url in maliste :
        if url.startswith(mon) == True:
            liste_ok.append(url)

        else :
            liste_not_ok.append(url)

    liste_ok_et_not_ok = [liste_ok, liste_not_ok]
    return liste_ok_et_not_ok


def encore_une_def_de_liste(liste_avec_liste):
    liste_grande = []
    for truc in liste_avec_liste:
        liste_petite = [truc, 0]
        liste_grande.append(liste_petite)
    return liste_grande


def scan_url(url_page):
    sock = urlopen(url_page)
    htmlSource = sock.read()
    sock.close()
    return htmlSource



letexte = input("Saisissez un texte : ")
dico_trie = compter_des_mots(letexte)
resultat_liste_utile = suppression_parasite(dico_trie, liste_parasite)
print(resultat_liste_utile)

html="""<html>
    <head>
    <title>Titre du test</title>
    </head>
    <body>
        <a href="http://www.youtube.com">Youtube wsh</a>
        <img src="" alt="image youtube">
        <a href="http://www.facebook.com">Facebook</a>
        <img src="" alt="image facebook">
    </body>
</html>"""


print(rechercher_html(html, "a", "href"))
print(rechercher_html(html, "img", "alt"))
print(index_http(tri_http("http://www.youtube.com/trouduc")))
print(index_http(tri_http("www.youtube.com/pouetpouet")))
print(index_http(tri_http("http://www.bing.chilling.com/john_cena")))

monsite = "www.monsite.com"
maliste = ["www.monsite.com/page57", "www.autresite.com/oral"]
jsp_site = tri_site(monsite, maliste)
print(jsp_site)
print(jsp_site[0])
print(jsp_site[1])
print(encore_une_def_de_liste(jsp_site[0]))
codehtml = scan_url("https://ronanzambon.fr/").__str__()
print(type(codehtml))
print(rechercher_html(codehtml, "a", "href"))

