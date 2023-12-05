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
    liste_utile = []
    for mot in dico_trie:
        if mot not in liste_parasite:
            liste_utile.append(mot)
    return liste_utile


letexte = input("Saisissez un texte : ")
dico_trie = compter_des_mots(letexte)
resultat_liste_utile = suppression_parasite(dico_trie, liste_parasite)
print(compter_des_mots(letexte))
print(resultat_liste_utile)