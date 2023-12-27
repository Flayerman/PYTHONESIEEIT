from collections import Counter
import csv
import requests
from bs4 import BeautifulSoup

# Etape 1
def compter_mots(texte):
    # Diviser le texte en mots
    mots = texte.split()
    # Utiliser Counter pour compter l'occurrence de chaque mot
    occurrences = Counter(mots)
    # Trier les mots par nombre d'occurrences (en ordre décroissant)
    mots_tries = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    return mots_tries
# Etape 3

def mots_csv(fichier):
    mots_parasites = []
    with open(fichier, 'r', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        for ligne in lecteur_csv:
            mots_parasites.extend(ligne)
    return mots_parasites

# Etape 2

def del_parasites(mots_tries, parasites):
    mots_filtre = [(mot, occurrence) for mot, occurrence in mots_tries if mot not in parasites]
    return mots_filtre

# Etape 4
def enlever_balises_html(html: str):
    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Extraire le texte du HTML sans balises
    texte_sans_balises = soup.get_text(separator=' ', strip=True)
    return texte_sans_balises

# Etape 6
def extraire_valeurs_attribut(html, balise, attribut):
    valeurs = []

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Trouver toutes les balises spécifiées
    balises = soup.find_all(balise)

    # Extraire les valeurs de l'attribut spécifié
    for balise in balises:
        valeur_attribut = balise.get(attribut)
        if valeur_attribut:
            valeurs.append(valeur_attribut)
    return valeurs

# Etape 8
def extraire_domaine(url):
    try:
        return url.split('/')[2]
    except:
        return url.split('/')[0]

# Etape 9
def groupe_domain(domain,grp_url):
    urls_domaine = [url for url in grp_url if extraire_domaine(url) == domain]
    urls_autres = [url for url in grp_url if extraire_domaine(url) != domain]
    return urls_domaine, urls_autres

# Etape 10
def recuperer_html_depuis_url(url):
    response = requests.get(url)
    return response.text

# Etape 11
def prince():
    url = "https://www.bm-cat.com/fr-fr/"
    domain = extraire_domaine(url)
    print(domain)
    html = recuperer_html_depuis_url(url)
    text = enlever_balises_html(html)
    words = compter_mots(text)
    fichier_csv = "parasite.csv"
    words_parasite = mots_csv(fichier_csv)
    words_filtre = del_parasites(words,words_parasite)
    premiers_mots = words_filtre[:4]
    print("Les 4 premiers mots sont : ", premiers_mots)
    # Images
    image = extraire_valeurs_attribut(html,'img','alt')
    print(f"Il y a {len(image)} images")
    print(image)
    # Liens entrants / sortants
    liens = extraire_valeurs_attribut(html,'a','href')
    liens_traite = groupe_domain(domain,liens)
    print(f"Il y a {len(liens_traite[0])} de liens entrants")
    print(f"Il y a {len(liens_traite[1])} de liens sortants ou incomplets")

    return


print(prince())










# Exemple d'utilisation
#texte_exemple = "Ceci est un yohan de texte. Un yohan pour tester la fonction."
#fichier = "parasite.csv"

#html_exemple = "<p>Ceci est un <b>exemple</b> de texte HTML.</p>"
#texte_sans_balises = enlever_balises_html(html_exemple)

#Liste = compter_mots(texte_exemple)
#fichier_parasite = mots_csv(fichier)
#resultat = del_parasites(Liste, fichier_parasite)
#print(resultat)

 #Exemple d'utilisation etape 5
#html_exemple = """
#<html>
#  <body>
#    <a href="lien1">Lien 1</a>
#    <a href="lien2">Lien 2</a>
#    <a href="lien3">Lien 3</a>
#  </body>
#</html>
#"""
#Etape 6
#balise_exemple = "a"
#attribut_exemple = "href"
#valeurs_attribut = extraire_valeurs_attribut(html_exemple, balise_exemple, attribut_exemple)
#print("Valeurs de l'attribut '{}':".format(attribut_exemple))
#print(valeurs_attribut)

#Etape 8
#exemple_url = "https://antoine-engasser.fr"
#print(extraire_domaine(exemple_url))