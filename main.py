def compterDesMots(untexte):
    mondico = {}
    mots = untexte.split()
    for mot in mots:
        if mot in mondico:
            mondico[mot] += 1
        else:
            mondico[mot] = 1

    trie = sorted(mondico, key=lambda mot: mondico[mot], reverse=True)
    dico_trie = {}
    for mot in trie:
        dico_trie[mot] = mondico[mot]

    return dico_trie


letexte = input("Saisissez un texte : ")
print(compterDesMots(letexte))