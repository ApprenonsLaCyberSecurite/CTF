from math import gcd
from functools import reduce
from collections import Counter

def trouver_cle(lettre_chiffre, lettre_clair, alphabet):
    i_clair = alphabet.index(lettre_clair)
    i_chiffre = alphabet.index(lettre_chiffre)
    i_cle = (i_chiffre - i_clair) % len(alphabet)
    return alphabet[i_cle]

def dechiffrer(texte_chiffre, cle, alphabet):
    texte_clair = ""
    
    for i, car in enumerate(texte_chiffre):
        i_chiffre = alphabet.index(car)
        i_cle = alphabet.index(cle[i % len(cle)])
        i_clair = (i_chiffre - i_cle) % len(alphabet)
        texte_clair += alphabet[i_clair]
    
    return texte_clair

fichier = "cypherText.txt"
with open(fichier, "r", encoding="utf-8") as f:
    texte_chiffre = f.read()

texte_chiffre = texte_chiffre.replace(" ", "").replace("\n","")

#print(texte_chiffre)

taille = 12

positions = {}
for i in range(len(texte_chiffre) - taille + 1):
    Ngramme = texte_chiffre[i:i+taille]
    
    if Ngramme not in positions:
        positions[Ngramme] = []
    
    positions[Ngramme].append(i)
    
#print(positions)

NgrammesMultiples = {
    Ngramme : pos
    for Ngramme, pos in positions.items()
    if len(pos) >= 2
}

#print(NgrammesMultiples)

distances = []
for Ngramme in NgrammesMultiples:
    pos_precedente = 0
    for i in range(len(positions[Ngramme])):
        if i == 0:
            pos_precedente = positions[Ngramme][i]
        else:
            pos_courante = positions[Ngramme][i]
            d = pos_courante - pos_precedente
            if d not in distances:
                distances.append(d)
            pos_precedente = pos_courante
#print(distances)

longueur_cle = reduce(gcd, distances)
print(f"longueur_cle = {longueur_cle}")

sous_textes = ['' for _ in range(longueur_cle)]
for i, car in enumerate(texte_chiffre):
    sous_textes[i % longueur_cle] += car

cle = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
for i in range(longueur_cle):
    lettre_la_plus_frequente = Counter(sous_textes[i]).most_common(1)[0][0]
    #print(lettre_la_plus_frequente)
    lettre_cle = trouver_cle(lettre_la_plus_frequente, 'E', alphabet) 
    cle += lettre_cle

print(f"cle = {cle}")

texte_clair = dechiffrer(texte_chiffre, cle, alphabet)

print(f"texte_clair = {texte_clair[:200]}...")
