#Brun Morgan
#El Anziz Aounou


from random import shuffle
import random

symbole=["trefle","carreau","pique","coeur"]
valeur=["as",'2','3','4','5','6','7','8','9','10',"valet","dame","roi"]

def paquet():
    return [(x+ ' de '+y) for y in symbole for x in valeur]

def liste(nom_carte):                                           
    x=[]
    mot=""
    for i in range(len(nom_carte)):
        if nom_carte[i]!=" ":
            mot+=nom_carte[i]
        elif nom_carte[i]==" ":
            x.append(mot)
            mot=""
    x.append(mot)
    return x

def valeurCarte(nom_carte):              
    x=liste(nom_carte)                    
    if x[0]=='as':
        rep=int(input("1 ou 11? "))
        while rep!=1 and rep!=11:
            rep=input("Ne peut pas prendre d'autres valeurs, ainsi vous choisissez 1 ou 11? ")
        if rep==11:
            return 11
        elif rep==1:
            return 1
    elif x[0]=='valet':
        return 11
    elif x[0]=='dame':
        return 12
    elif x[0]=='roi':
        return 13
    else:
        return int(x[0])

def initPioche(n):    
    pioche=[]
    for i in range(1,n+1):
        liste=paquet()
        for j in range(len(liste)):
            pioche.append(liste[j])
    shuffle(pioche)
    return pioche

def piocheCarte(p,x):            
    lp=[]
    i=0
    while i<x:
        pioche=p.pop(0)
        lp.append(pioche)
        i+=1
    return lp

def initJoueurs(n,style,proba):             
    joueurs=[]
    ordi={}
    i=1
    while i<=n:
        print("Nom du joueur numéro",i,":",end=" ")
        rep=input()
        rep2=input("Voulez-vous que ce joueur soit joué par l'ordinateur? (oui/non)  ")
        if rep2=="oui":
            print("Choisissez son style de jeu (aleatoire,plus ou moins joueur,complet,stratege1,stratege2,stratege3) ")
            rep3=input()
            while rep3 not in ["aleatoire","plus ou moins joueur","complet","stratege1","stratege2","stratege3"]:
                rep3=input("Veuillez choisir un style de jeu disponible:  ")
            if rep3=="plus ou moins joueur":
                pro=float(input("Indiquez à quel point il est joueur (1=joue tout le temps, 0.5=aléatoire,0=joue jamais):  "))
                while pro!=1 and pro!=0.5 and pro!=0:
                    pro=float(input("Veuillez respecter les réponses attendues, donc:  "))
                proba[rep]=pro
            ordi[rep]=rep3
        joueurs.append(rep)
        i+=1
    joueurs.append("croupier")
    ordi["croupier"]=style
    return joueurs,ordi,proba

def initScores(joueurs,v):
    Scores={}
    for noms in joueurs:
        if noms=="croupier" and v!=0:
            Scores[noms]=1000
        else:
            Scores[noms]=v
    return Scores

def premierTour(joueurs,new_scores,en_jeu,Kopecs,pioche,style,proba):
    somme=0
    cachee=""
    for noms in new_scores:
        if noms in ordi:
            if noms=="croupier":
                print("\nAu tour du croupier de piocher.",end="")
            else:
                print("\nAu tour de",noms,"de piocher.")
            rep=input()       
            if rep=="":
                if noms in proba:
                    retour= style_de_jeu(ordi[noms],new_scores,pioche,new_scores[noms],noms,proba[noms])
                else:
                    retour= style_de_jeu(ordi[noms],new_scores,pioche,new_scores[noms],noms)
                if retour==True:
                    x=piocheCarte(pioche,2)
                    prop=liste(x[0])
                    if noms=="croupier" and prop[0]=='as':
                        print("La croupier a pioché un as et l'autre carte reste face cachée, si un joueur souhaite une assurance, qu'il indique son prénom si non, on continue.")
                        prenom=input()
                        assurance={}
                        while prenom in Kopecs:
                            assurance[prenom]=mise[prenom]/2
                            Kopecs[prenom]-=assurance[prenom]
                            prenom=input("Un autre joueur désire une assurance? ")
                        print("\nLe croupier retourne sa deuxième carte qui est",x[1],".")
                        prop2=liste(x[1])
                        if prop2[0]=="as":
                            cachee= un_ou_onze(new_scores[noms])
                        else:
                            cachee=valeurCarte(x[1])
                        if 11+cachee==21:
                            for prenom in Kopecs:
                                if prenom in assurance:
                                    Kopecs[prenom]+=2*assurance[prenom]
                            return new_scores,pioche,Kopecs,somme
                        elif 11+cachee>21:
                            print("Le croupier a dépassé 21, il arrête de jouer.")
                            mise=round(Kopecs["croupier"]*0.2)
                            print("Ainsi, il met en jeu",mise,"kopecs.")
                            del en_jeu["croupier"]
                    else:
                        if noms=="croupier":
                            print("Le croupier a pioché un",x[0],"et l'autre carte reste face cachée jusqu'au prochain tour.")
                            l=liste(x[0])
                            if l[0] in ["8","9","valet","dame","roi"]:
                                print("Il vérifie la carte cachee.")
                        else:
                            print(noms,"a pioché",x[0],"ainsi que",x[1],".")
                        prop=liste(x[0])
                        prop1=liste(x[1])
                        if prop[1]=="as" and noms == "croupier":
                            cachee= un_ou_onze(new_scores["croupier"])
                        elif noms=="croupier":
                            cachee=valeurCarte(x[1])
                        elif prop[0]=="as" and prop1[0]=="as":
                            De_carte=un_ou_onze(new_scores[noms])
                            De_carte2=1
                        elif prop[0]=="as":
                            De_carte=un_ou_onze(new_scores[noms])
                            De_carte2=valeurCarte(x[1])
                        elif prop1[0]=='as':
                            De_carte2=un_ou_onze(new_scores[noms])
                            De_carte=valeurCarte(x[0])
                        else:
                            De_carte=valeurCarte(x[0])
                            De_carte2=valeurCarte(x[1])
                        if noms=="croupier":
                            new_scores[noms]=new_scores[noms]+valeurCarte(x[0])+cachee
                        else:
                            new_scores[noms]=new_scores[noms]+De_carte+De_carte2
                        if new_scores[noms]>21:
                            if noms=="croupier":
                                print("Le croupier a dépassé 21.")
                            else:
                                print(noms,"a dépassé 21.")
                            mise=round(Kopecs[noms]*0.2)
                            print("Il met alors en jeu",mise,"kopecs.")
                            if noms=="croupier" and len(en_jeu)<=1:
                                print("Etant donné que tous les joueurs ont dépassé aussi 21, seuls ceux qui ont un total inférieur au croupier gagne")
                            del en_jeu[noms]
                        else:
                            if ordi[noms] in ["stratege1","stratege2","stratege3","complet"]:
                                mise=hasard(Kopecs,new_scores,noms,en_jeu)
                                print(noms,"mise",mise,"kopecs.")
                            else:
                                mise=20
                                if noms=="croupier":
                                    mise=40
                                    if l[0] in ["8","9","valet","dame","roi"]:
                                        print("Il ne dépasse pas 21.")
                                    print("Le croupier mise 40 kopecs.")
                                else:
                                    print(noms,"mise",mise,"kopecs.")
                        somme+=mise
                    Kopecs[noms]-=mise
                else:
                    if noms=="croupier":
                        print("Le croupier décide de ne rien piocher.")
                    else:
                        print(noms,"décide de ne rien piocher.")
                    mise=round(Kopecs[noms]*0.2)
                    print("Il mise alors",mise,"kopecs.")
                    somme+=mise
                    Kopecs[noms]-=mise
                    del en_jeu[noms]            
        else:
            print("\nAu tour de",noms,"de piocher",end="")
            rep=input()
            if rep=="":
                x=piocheCarte(pioche,2)
                print(x[0]);print(x[1])
                new_scores[noms]=new_scores[noms]+valeurCarte(x[0])+valeurCarte(x[1])
                if new_scores[noms]==21:
                    print("BlackJack!")
                    print("Vous n'avez pas besoin de miser")
                    mise=0
                    del en_jeu[noms]
                elif new_scores[noms] > 21:
                    print("Pas de chance! Vous avez dépassé 21... vous n'êtes plus dans la partie en cours.")
                    print("20% de vos kopecs sont automatiquements mis en jeu.")
                    mise=round(Kopecs[noms]*0.2)
                    somme+=mise
                    del en_jeu[noms]
                else:
                    mise=float(input("Veuillez indiquer votre mise de la partie: "))
                    while not(0<mise<=Kopecs[noms]):
                        mise=float(input("Vous n'avez pas respecté vos possibilités de mises, veuillez en indiquez une nouvelle: "))
                    somme+=mise
                Kopecs[noms]=Kopecs[noms]-mise
    return new_scores, pioche, Kopecs, somme,cachee

def gagnant(scores,Kopecs,somme):
    gagnant=[]
    plusieurs=False
    s=0
    for i in scores:
        if i>21:
            s+=1
    if scores["croupier"]>21 and s==len(scores):
        for noms in scores:
            if scores[noms]>scores["croupier"]:
                gagnant.append(noms)
                if len(gagnant)>1:
                    plusieurs=True
    elif scores["croupier"]>21:
        for noms in scores:
            if 0<=scores[noms]<=21:
                gagnant.append(noms)
                if len(gagnant)>1:
                    plusieurs=True
    else:
        for i in scores:
            if i!="croupier":
                if scores[i]>=scores["croupier"] and scores[i]<=21: 
                    gagnant.append(i)
                    if len(gagnant)>1:
                        plusieurs=True
    if gagnant==[]:  
        print("Il n'y a aucun gagnant.")
    elif plusieurs==False:
        Kopecs[gagnant[0]]=Kopecs[gagnant[0]]+somme
    else:
        iteration=0
        while iteration<len(gagnant):
            Kopecs[gagnant[iteration]]=Kopecs[gagnant[iteration]]+round(somme/len(gagnant),2)
            iteration+=1
    for noms in Kopecs:
        if Kopecs[noms]==0:
            if noms == "croupier":
                print("Le croupier n'a plus de Kopecs à miser.")
                del scores[noms]
            else:
                print("\n",noms,"n'a plus de kopecs a miser et est donc prié de quitter la table.")
                del scores[noms]
    return Kopecs

def Continue():                                 
    rep=input("Désiriez-vous continuer ? ")
    while rep!='oui' and rep!='non':
        print("Veuillez me répondre par oui ou non.")
        rep=input("Du coup, vous souhaitez continuer ? ")
    if rep=='oui':
        return True
    else:
        return False

def tourJoueur(j,new_scores,en_jeu,tour,pioche,ordi,cachee,proba): #j est le nom d'un joueur
    if j in ordi:
        if j=="croupier":
            print("\nC'est au tour du croupier de jouer.")
            if tour==2:
                print("La carte qui était face cachée est",cachee,".")
        else:
            print("\nC'est au tour de",j,"de jouer.")
        rep=input()
        if rep=="":
            if j in proba:
                retour= style_de_jeu(ordi[j],new_scores,pioche,new_scores[j],j,proba[j])
            else:
                retour=style_de_jeu(ordi[j],new_scores,pioche,new_scores[j],j)
            if retour==True:
                print("Il décide de continuer de jouer.")
                x=piocheCarte(pioche,1)
                print("Il vient de piocher",x[0])
                prop=liste(x[0])
                if prop[0]=="as":
                    y=un_ou_onze(new_scores[j])
                else:
                    y=valeurCarte(x[0])
                new_scores[j]=new_scores[j]+y
                if new_scores[j]==21:
                    if j=="croupier":
                        print("Le score du croupier est de 21, il s'arrête là.")
                    else:
                        print("Le score de",j,"est de 21, il ne peut faire mieux.")
                    del en_jeu[j]
                elif new_scores[j]>21:
                    if j=="croupier":
                        print("Le croupier a dépassé 21 donc la partie se termine. Les joueurs encore en jeu recevront leur dû.")
                    else:
                        print(j,"a dépassé 21 donc la partie se termine pour lui.")
                    del en_jeu[j]
            else:
                if j=="croupier":
                    print("Le croupier décide de ne pas piocher et donc s'arrête là.")
                else:
                    print(j,"décide de ne pas piocher et donc s'arrête là.")
                del en_jeu[j]
    else:
        p=pioche
        print("\nC'est votre tour numéro",tour,":")
        print("A vous de jouer",j,"!",end="");rep2=input()
        if rep2=="":
            print("Votre total est de",new_scores[j],"actuellement")
            print("\nVoulez-vous continuer de jouer ou préféreriez-vous vous arrêter ? ")
            rep=input()
            while rep!='arreter' and rep!='continuer':
                rep=input("Je vous répète, arreter ou continuer ? ")
            if rep=='continuer' or rep=='oui':
                x=piocheCarte(p,1)
                print("\nVous venez de piocher un",x[0])
                y=valeurCarte(x[0])
                new_scores[j]=new_scores[j]+y
                if new_scores[j]==21:
                    print("Vous ne pouvez faire mieux, bien joué.")
                    del en_jeu[j]
                elif new_scores[j]>21:
                    print("Vous avez fait un trop gros score qui est de",new_scores[j],"vous n'êtes plus en jeu pour ce tour.")
                    del en_jeu[j]
                return None
            del en_jeu[j]

def tourComplet(new_score,en_jeu,tour,pioche,ordi,cachee,proba):
    copie_en_jeu=dict(en_jeu)
    for noms in copie_en_jeu:
        tourJoueur(noms,new_score,en_jeu,tour,pioche,ordi,cachee,proba)

def partieFinie(en_jeu,new_scores):
    if len(en_jeu)<1 or new_scores["croupier"]>21 or "croupier" not in en_jeu:
        return True
    else:
        return False

def clas(Kopecs):
    print("\nRappel Kopecs: ")
    for noms in Kopecs:
        print(noms," :",Kopecs[noms],"kopecs")
        
def partieComplete(listej,pioche,ordi,proba):
    tour=2
    Kopecs=initScores(listej,100)
    new_scores=initScores(listej, 0)
    en_jeu=dict(new_scores)
    new_scores,pioche,Kopecs,somme,cachee = premierTour(listej,new_scores,en_jeu,Kopecs,pioche,ordi,proba)
    while partieFinie(en_jeu,new_scores)!=True:    
        tourComplet(new_scores,en_jeu,tour,pioche,ordi,cachee,proba)
        tour+=1
    Kopecs=gagnant(new_scores,Kopecs,somme)
    clas(Kopecs)
    return Kopecs

def partieComplete_suite(listej,Kopecs,pioche,ordi,proba):
    tour=2
    new_scores=initScores(listej,0)
    en_jeu=dict(new_scores)
    new_scores,pioche,Kopecs,somme,cachee = premierTour(listej,new_scores,en_jeu,Kopecs,pioche,ordi,proba)
    while partieFinie(en_jeu,new_scores)!=True:
        tourComplet(new_scores,en_jeu,tour,pioche,ordi,cachee,proba)
        tour+=1
    Kopecs=gagnant(new_scores,Kopecs,somme)
    clas(Kopecs)
    return Kopecs

def aleatoire():
    x=random.randint(0,1)
    if x==0:
        return True
    elif x==1:
        return False

def plus_ou_moins_joueur(proba):
    if proba==1:
        return True
    elif proba==0:
        return False
    elif proba==0.5:
        return aleatoire

def choix(x):
    if x==1:
        return True
    elif x==0:
        return False

def stratege1(score):
    if score<=11:
        return True
    elif 11<score<=13:
        liste=[0,1,1,1,1,1,1,1,1,1]
    elif 13<score<=15:
        liste=[0,0,0,1,1,1,1,1,1,1]
    elif 15<score<=17:
        return aleatoire()
    elif 17<score<=19:
        liste=[0,0,0,0,0,0,0,0,1,1]
    elif 19<score<=21:
        return False
    x=random.choice(liste)
    return choix(x)

def stratege2(pioche,score,pource=60):
    total=score
    carte_dep=0
    for carte in pioche:
        prop=liste(carte)
        if prop[0]=="as":
            x=1
        else:
            x=valeurCarte(carte)
        if x+total>21:
            carte_dep+=1
    pourcentage=(carte_dep/len(pioche))*100
    if pourcentage >pource:
        return False
    else:
        return True

def stratege3(new_scores,pioche,score,noms):
    if score==0:
        return True
    else:
        dep=0
        proche=0
        for nom in new_scores:
            if nom!="croupier" and nom!=noms:
                if new_scores[nom]>=score and new_scores[nom]<=21:
                    dep+=1
                if 14<new_scores[nom]<=17 and 1<=score-new_scores[nom]<=3:
                    proche+=1
        if dep>1 or proche>0:
            return True
        else:
            return False

def complet(new_scores,pioche,score):
    if score<=11:
        return True
    elif 11<score<=13:
        taux=40
    elif 13<score<=15:
        taux=20
    elif 15<score<=17:
        taux=0
    elif 17<score<=19:
        taux=-20
    elif 19<score<=21:
        taux=-60
    if stratege2(pioche,score,60+taux)==False:
        return False
    else:
        if stratege3(new_scores,pioche,score)==False:
            return False
        else:
            return True

def style_de_jeu(style,new_scores,pioche,score,noms,proba=None):
    if style=="aleatoire":
        return aleatoire()
    elif style=="plus ou moins joueur":
        return plus_ou_moins_joueur(proba)
    elif style=="complet":
        return complet(new_scores,pioche,score)
    elif style=="stratege1":
        return stratege1(score)
    elif style=="stratege2":
        return stratege2(pioche,score)
    elif style=="stratege3":
        return stratege3(new_scores,pioche,score,noms)


def premiere_mise(Kopecs,noms):
    x=Kopecs[noms]*0.5
    y=random.randint(1,3)
    if y==1:
        x=x*0.02
    elif y==2:
        x= x*0.05
    elif y==3:
        x=x*0.1
    return round(x)
    

def deuxieme_mise(Kopecs,new_scores,noms):
    tot=new_scores[noms]
    x=Kopecs[noms]
    if tot<=11:
        x=x*0.05
    elif 11<tot<=15:
        x=x*0.07
    elif 15<tot<=18:
        x=x*0.09
    elif 18<tot<=21:
        x=x*0.1
    somme=0
    for joueur in new_scores:
        if 11<=new_scores[joueur]<=15:
            somme+=1
    if somme>=2:
        x=x*0.5
    return round(x)

def troisieme_mise(Kopecs,en_jeu,noms):   #suite de syracuse
    x=round(Kopecs[noms]*0.2)
    i=1
    old=x
    while i<=len(en_jeu):
        if old%2==0:
            un=old/2
        else:
            un=3*old+1
        old=un
        i+=1
    if old>=round(Kopecs[noms]*0.2):
        return round(old/2)
    else:
        return round(old)

def hasard(Kopecs,new_scores,noms,en_jeu):
    if Kopecs[noms]<=10:
        return Kopecs[noms]
    else:
        x=random.randint(1,3)
        if x==1:
            return premiere_mise(Kopecs,noms)
        elif x==2:
            return deuxieme_mise(Kopecs,new_scores,noms)
        elif x==3:
            return troisieme_mise(Kopecs,en_jeu,noms)
    
def partir(Kopecs,listej):
    partir=input("Est-ce qu'un joueur souhaite quitter la table? (indiquer son prénom ou non)  ")
    while partir in listej:
        print(partir,"quitte la table avec",Kopecs[partir],"kopecs")
        del Kopecs[partir]
        listej.remove(partir)
        partir=input("Un autre joueur ?  ")
    print("Alors nous poursuivons")
    return Kopecs,listej
          
def un_ou_onze(score):
    if score+11>21:
        return 1
    else:
        return 11

print("Avec quel style de croupier voulez-vous jouer? (aleatoire,plus ou moins joueur,complet,stratege1,stratege2,stratege3) ")
croupier=input()
while croupier not in ["aleatoire","plus ou moins joueur","complet","stratege1","stratege2","stratege3"]:
    croupier=input("Indiquez un style disponible:  ")
proba={}
if croupier=="plus ou moins joueur":
    pro=float(input("Indiquez à quel point il est joueur (1=joue tout le temps, 0.5=aléatoire,0=joue jamais):  "))
    while pro!=1 and pro!=0.5 and pro!=0:
        pro=float(input("Veuillez respecter les réponses attendues, donc:  "))
    proba["croupier"]=pro
print("\nLes mises seront prévues durant la partie.")
nb_joueurs=int(input("\nCombien de joueurs participent? "))
pioche=initPioche(nb_joueurs)
listej,ordi,proba = initJoueurs(nb_joueurs,croupier,proba)
Kopecs = partieComplete(listej,pioche,ordi,proba)
Kopecs,listej = partir(Kopecs,listej)
while Kopecs["croupier"]!=0 and len(listej)>1:
    print("\nNouvelle donne")
    pioche=initPioche(nb_joueurs)
    Kopecs=partieComplete_suite(listej,Kopecs,pioche,ordi,proba)
    Kopecs,listej = partir(Kopecs,listej)
if Kopecs["croupier"]==0:
    print("La partie est terminée car le croupier n'a plus de Kopecs à parier.")
if len(listej)<=1:
    print("Il n'y a plus assez de joueur sur la table pour continuer.")
print("Au revoir et bon courage pour la suite!")

