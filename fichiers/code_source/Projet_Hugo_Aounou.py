from random import *
from collections import deque

def Creer_Cartes():    
    liste_motif=['\u2660','\u2666','\u2665','\u2663']
    carte=[]
    for c in range(0,4):
        for f in range(7,15):
            if f==11:
                carte.append(("Valet",liste_motif[c]))
            elif f==12:
                carte.append(("Dame",liste_motif[c]))
            elif f==13:
                carte.append(("Roi",liste_motif[c]))
            elif f==14:
                carte.append(("As",liste_motif[c]))
            else:
                carte.append((f,liste_motif[c]))
    print(carte)
    return carte


def Battre_Carte(liste):
    shuffle(liste)

def distribuer(cartes):
    joueur1=cartes[0:16]
    print("joueur1=",joueur1)
    print()
    joueur2=cartes[16:32]
    print("joueur2=",joueur2,"\n")
    return joueur1, joueur2

def RemplirFile(pile):
    file=deque(pile)
    return file

def DéposerCartes():
    CarteDeJ1=j1.popleft()
    Fig,Coul=CarteDeJ1
    CarteDeJ2=j2.popleft()
    Fig2,Coul2=CarteDeJ2
    print("Carte de J1:",Fig,"de",Coul)
    print("Carte de J2:",Fig2,"de",Coul2)
    return CarteDeJ1,CarteDeJ2

def bataille(l):
    if len(j1)!=0 and len(j2)!=0:
        Carte1=j1.popleft()
        Fig,Coul=Carte1
        print("Carte cachée du joueur 1:",Fig,"de",Coul)
        l.append(Carte1)
        Carte2=j2.popleft()
        Fig2,Coul2=Carte2
        print("Carte cachée du joueur 2:",Fig2,"de",Coul2)
        l.append(Carte2)
    #On met les cartes cachées dans l
    else:
        i=200
    #Pour arrêter la boucle while de GérerTour

def GérerTour():
    i=1
    l=[]
    nouveauTour=True
    while len(j1)>0 and len(j2)>0 and i<200:
#Au cas où si on sort d'une bataille
        if nouveauTour:
            print("Tour n°",i)
        Carte1,Carte2=DéposerCartes()
#stock les valeurs des upplets dans des variables
        Figure1,Couleur1=Carte1
        Figure2,Couleur2=Carte2
#Affectation de valeurs pour Valets, Dame, Roi et As comme c'est des chaines de caractères
        if Figure1=="Valet":
            Figure1=11
        elif Figure1=="Dame":
            Figure1=12
        elif Figure1=="Roi":
            Figure1=13
        elif Figure1=="As":
            Figure1=14
        if Figure2=="Valet":
            Figure2=11
        elif Figure2=="Dame":
            Figure2=12
        elif Figure2=="Roi":
            Figure2=13
        elif Figure2=="As":
            Figure2=14
#On compare les valeurs des figures de chaque cartes, on ajoute également les éléments de l au cas où si on sort d'une bataille
        if Figure1 > Figure2 :
            j1.append(Carte1)
            j1.append(Carte2)
            for elem in l:
                j1.append(elem)
            l=[]
            nouveauTour=True
        elif Figure1 < Figure2 :
            j2.append(Carte1)
            j2.append(Carte2)
            for iteration in l:
                j2.append(iteration)
            l=[]
            nouveauTour=True
        else:
#Cartes de même valeurs: Bataille
            l.append(Carte1)
            l.append(Carte2)
            print("Bataille !")
            bataille(l)
            nouveauTour=False
        if nouveauTour:
#Si bataille, on annule l'itération et on refait pareil que d'habitude
            i+=1
            print()
            print("Main de J1:",j1,"\n")
            print("Main de J2:",j2)
        print()
    if len(j1)<=len(j2):
        print("Le joueur 2 a gagné")
    else:
        print("Le joueur 1 a gagné")

cartes=Creer_Cartes()

print()

Battre_Carte(cartes)

joueur1,joueur2=distribuer(cartes)

print()
j1=RemplirFile(joueur1)
j2=RemplirFile(joueur2)

GérerTour()