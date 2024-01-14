import tkinter as tk
from tkinter import Toplevel, scrolledtext
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


def rechercher_html(html, nombalise, nomattribut):
    liste = []
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all(nombalise):
        attribut = a.get(nomattribut)
        if attribut:
            liste.append(attribut)
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
    for url in maliste:
        if url.startswith(mon) == True:
            liste_ok.append(url)

        else:
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


def meta_keywords(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    keywords_content = []
    if meta_keywords:
        keywords_content = meta_keywords.get('content').split(',')
        keywords_content = [keyword.strip() for keyword in keywords_content]
    return keywords_content


def main():
    url = input("Entrez l'url du site à espionner: ")

    # on utilise scan_url pour ouvrir la page puis choper le code
    texte_html = scan_url(url)

    # scan des keywords du texte de l'url puis affichage de tous puis affichage des 3 premiers par occurence
    c_koi_les_keywords = meta_keywords(texte_html)
    print("Voici les mots-clés du site web: ", c_koi_les_keywords)
    compter_les_keywords = compter_des_mots(" ".join(c_koi_les_keywords))
    trois_premiers_words = {k: compter_les_keywords[k] for k in list(compter_les_keywords)[:3]}
    print("Voici les 3 premiers mots-clés du site, classé par occurence: ", trois_premiers_words)

    # on tri les balises alt puis affiche
    balises_alt = rechercher_html(texte_html, "img", "alt")
    print("Voici les balises alt présentes sur ce site: ", balises_alt)

    # pareil mais avec les liens puis on affiche ceux sortants et ceux entrants
    liens = rechercher_html(texte_html, "a", "href")
    tri_liens = tri_site(url, liens)
    print("Voici les liens entrants dans le site: ", tri_liens[0])
    print("Voici les liens sortants du site: ", tri_liens[1])


def resulats_deuxieme_fenetre_qui_marche_pas(url, user_keywords):
    # on chope le résultat de l'analyse (encore)
    texte_html = scan_url(url)
    liens = rechercher_html(texte_html, "a", "href")

    # on créer la fenêtre de ses morts
    fenetre = Toplevel()
    fenetre.title("Résultats de l'analyse")
    fenetre.geometry("800x600")

    # là où y'a les résultats
    resultat = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=150, height=100)
    resultat.pack()

    # on affiche les liens
    for lien in liens:
        resultat.insert(tk.END, lien + '\n')


# interface graphique Tkinter
root = tk.Tk()
root.title("Prédateur de Site Web")
root.geometry("800x600")

# barre url
url_label = tk.Label(root, text="Entrez l'URL du site à espionner :")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# barre mots clés persos
keywords_label = tk.Label(root, text="Entrez des mots-clés en plus (séparés par des espaces): ")
keywords_label.pack()
keywords_entry = tk.Entry(root, width=50)
keywords_entry.pack()

# bouton pour aller a la suite
analyze_button = tk.Button(root, text="Analyser", command=lambda: resulats_deuxieme_fenetre_qui_marche_pas(url_entry.get(), keywords_entry.get()))
analyze_button.pack()

root.mainloop()
