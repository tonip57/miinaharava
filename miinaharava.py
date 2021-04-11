import haravasto
import time
import random
import os

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    miinat = 0
    y = 0
    for i in kentta:
        x = 0
        for e in i:
            haravasto.lisaa_piirrettava_ruutu(" ", x*40,y*40)
            if e == "l":
                haravasto.lisaa_piirrettava_ruutu("f", x*40,y*40)
            if e == "m":
                haravasto.lisaa_piirrettava_ruutu("x", x*40,y*40)
            for numero in range(9):
                if e == str(numero):
                    haravasto.lisaa_piirrettava_ruutu(str(numero), x*40,y*40)
            if pelinTiedot["loppu"]:
                if e == "x" or e == "m":
                    haravasto.lisaa_piirrettava_ruutu("x", x*40,y*40)
                if e == "l":
                    if tuple([x,y]) in miinatLippujenAlla:
                        haravasto.lisaa_piirrettava_ruutu("x", x*40,y*40)
                        miinatLippujenAlla.remove(tuple([x, y]))
                    else:                        
                        miinat = laske_miinat(x, y, kentta)
                        for n in range(9):
                            if miinat == n:
                                haravasto.lisaa_piirrettava_ruutu(str(n), x*40,y*40)                    
            x = x + 1
        y = y + 1
    
    haravasto.piirra_ruudut()


def suunnittele_kentta():
    """
    Funktio kysyy käyttäjältä kentän dimensiot ja asettaa kentälle sattumanvaraisiin kohtiin miinoja.
    Käyttäjä valitsee myös miinojen lukumäärän.
    """
    kentta = []
    
    while True:
        try:
            kentanPituus = int(input("Anna kentän pituus (luku väliltä 3-38): "))
            if kentanPituus < 3 or kentanPituus > 38:
                print("Luvun täytyy olla väliltä 3-38")
                raise ValueError
            
            kentanKorkeus = int(input("Anna kentän korkeus (luku väliltä 3-20): "))
            if kentanKorkeus < 3 or kentanKorkeus > 20:
                print("Luvun täytyy olla väliltä 3-20")
                raise ValueError
                
            miinojenLukumaara = int(input("Valitse miinojen lukumäärä (vähintään 1): "))
            if miinojenLukumaara < 1 or miinojenLukumaara > kentanKorkeus * kentanPituus - 1:
                print("Miinoja täytyy olla vähintään 1 ja enintään yksi vähemmän kuin kentässä on ruutuja")
          
            break
        except ValueError:
            print("Anna kokonaisluku!")
           
    
    pelinTiedot["kentanKorkeus"] = kentanKorkeus
    pelinTiedot["kentanPituus"] = kentanPituus
    pelinTiedot["miinatKpl"] = miinojenLukumaara
    
    for rivi in range(kentanKorkeus):
        kentta.append([])
        for sarake in range(kentanPituus):
            kentta[-1].append(" ")

    
    jaljella = []
    for x in range(kentanPituus):
        for y in range(kentanKorkeus):
            jaljella.append((x, y))
            
    miinoita(kentta, jaljella, miinojenLukumaara)
    
    return kentta


def tulvataytto(kentta, x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    tulva = [(x,y)]
    if kentta[y][x] == " ":
        while len(tulva) > 0:
            x, y = tulva.pop()
            miinat = laske_miinat(x, y, kentta)
            if miinat == 0:
                kentta[y][x] = "0"
            else:
                kentta[y][x] = str(miinat)

            for rivi in range(y - 1, y + 2):
                for sarake in range(x - 1, x + 2):
                    if rivi < 0:
                        rivi = 0
                    if sarake < 0:
                        sarake = 0
                    if sarake > len(kentta[0]) - 1:
                        sarake = len(kentta[0]) - 1
                    if rivi > len(kentta) - 1:
                        rivi = len(kentta) - 1
                    if kentta[rivi][sarake] == " ":
                        if miinat == 0:
                            tulva.append(tuple([sarake,rivi]))


def miinoita(lista,vapaatRuudut,n):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """

    for i in range(n):
        miinoitettuRuutu = random.choice(vapaatRuudut)
        lista[miinoitettuRuutu[1]][miinoitettuRuutu[0]] = "x"
        vapaatRuudut.remove(miinoitettuRuutu)


def kasittele_hiiri(x, y, painike, pmn):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    """
    if painike == haravasto.HIIRI_VASEN and pelinTiedot["loppu"] == False:
        xk = int(x / 40)
        yk = int(y / 40)
        if koordinaatin_sijainti_kentalla(xk,yk,len(kentta[1]),len(kentta)):
            pelinTiedot["klikkaukset"] = pelinTiedot["klikkaukset"] + 1
            klikkausVASEN(xk,yk)
        
            
    if painike == haravasto.HIIRI_OIKEA and pelinTiedot["loppu"] == False:
        xk = int(x / 40)
        yk = int(y / 40)
        if koordinaatin_sijainti_kentalla(xk,yk,len(kentta[1]),len(kentta)):
            klikkausOIKEA(xk,yk)
    
    if painike == haravasto.HIIRI_KESKI:
        if pelinTiedot["loppu"] == True:
            tallenna_tulos()
            haravasto.lopeta()
            



def koordinaatin_sijainti_kentalla(x, y, kentta_leveys, kentta_korkeus):
    """
    Palauttaa True, jos koordinaatti sijaitsee kentällä, muutoin False.
    """
    if x >= kentta_leveys:
        return False
    elif y >= kentta_korkeus:
        return False
    elif x <= -1:
        return False
    elif y <= -1:
        return False
    else:
        return True
        

def laske_miinat(x, y, kentta):
    """Laskee yhden ruudun ympärillä olevat miinat ja palauttaa niiden lukumäärän"""
    miinatLukumaara = 0
    for rivi in range(y - 1, y + 2):
        for sarake in range(x - 1, x + 2):
            if koordinaatin_sijainti_kentalla(sarake, rivi, len(kentta[1]), len(kentta)):
                if kentta[rivi][sarake] == "l":
                    if tuple([sarake,rivi]) in miinatLippujenAlla:
                        miinatLukumaara = miinatLukumaara + 1
                if kentta[rivi][sarake] == "x":
                    miinatLukumaara = miinatLukumaara + 1
    return miinatLukumaara
   

def klikkausOIKEA(x, y):
    """
    Toimenpiteet hiiren oikean napin klikkaukseen. Asettaa lippuja kentälle.
    """
    if kentta[y][x] == "x":
        miinatLippujenAlla.append(tuple([x,y]))
        kentta[y][x] = "l"

    elif kentta[y][x] == "l":
        if tuple([x,y]) in miinatLippujenAlla:
            kentta[y][x] = "x"
            miinatLippujenAlla.remove(tuple([x, y]))
        else:
            kentta[y][x] = " "
            
    elif kentta[y][x] == " ":
        kentta[y][x] = "l"

   
def klikkausVASEN(x, y):
    """
    Toimenpiteet hiiren vasemman napin klikkaukseen. Avaa tuntemattomia kohtia.
    """
    if kentta[y][x] == " ":
        if laske_miinat(x, y, kentta) == 0:
            tulvataytto(kentta, x, y)
        else:
            kentta[y][x] = str(laske_miinat(x, y, kentta))
            
            
    if kentta[y][x] == "x":
        aika = time.time()
        kentta[y][x] = "m"
        print("Astuit miinaan!")
        pelinTiedot["loppu"] = True
        pelinTiedot["lopputulos"] = "Häviö"
        pelinTiedot["pelinKesto"] = time.gmtime(aika - pelinTiedot["pelinKesto"])
        print("Klikkaa hiiren keskinappia poistuaksesi ja tallentaaksesi pelin tiedot")
        
    
    if kaikki_ruudut_avattu():
        aika = time.time()
        print("Voitit!")
        pelinTiedot["loppu"] = True
        pelinTiedot["lopputulos"] = "Voitto"
        pelinTiedot["pelinKesto"] = time.gmtime(aika - pelinTiedot["pelinKesto"])
        print("Klikkaa hiiren keskinappia poistuaksesi ja tallentaaksesi pelin tiedot")
        

        
def kaikki_ruudut_avattu():
    """
    Testaa koko ajan, onko peli voitettu. Palauttaa True, kun kaikki kentän kohdat on avattu osumatta miinaan.
    """
    for x in kentta:
        for y in x:
            if y == " ":
                return False
    return True


def tallenna_tulos():
    """
    Tallentaa pelatun pelin tiedot .txt tiedostoon.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'tuloslista.txt')
    
    kesto = time.strftime("%M min %S s", pelinTiedot["pelinKesto"])
    
    with open(path, "a") as f:
        f.write("{} | {} | Kesto: {} | {} Klikkausta | Kenttä: {}x{} | Miinat: {} kpl\n"
        .format(pelinTiedot["ajankohta"], pelinTiedot["lopputulos"], kesto, pelinTiedot["klikkaukset"], 
        pelinTiedot["kentanPituus"], pelinTiedot["kentanKorkeus"], pelinTiedot["miinatKpl"]))


def katso_tuloslista():
    """
    Tulostaa tuloslistan
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'tuloslista.txt')
    
    with open(path) as f:
        tuloslista = f.read()
        print(tuloslista)
    

def main(lista):
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, 'spritet')
    rivit = len(lista)
    sarakkeet = len(lista[1])
    

    haravasto.lataa_kuvat(path)
    haravasto.luo_ikkuna(sarakkeet*40, rivit*40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()


if __name__ == "__main__":    
    while True:
        try:
            ajankohta = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            pelinKesto = time.time()
            miinatLippujenAlla = []

            pelinTiedot = {
                "ajankohta": ajankohta,
                "pelinKesto": pelinKesto,
                "klikkaukset": 0,
                "lopputulos": "",
                "kentanPituus": 0,
                "kentanKorkeus": 0,
                "miinatKpl": 0,
                "loppu": False
            }

            print("1. Pelaa")
            print("2. Tuloslista")
            print("3. Poistu")
            valinta = int(input("Valitse kirjoittamalla 1, 2 tai 3: "))
            if valinta == 1:
                kentta = suunnittele_kentta()
                main(kentta)
                            
            elif valinta == 2:
                katso_tuloslista()

            elif valinta == 3:
                print("Heihei!")
                break
            else:
                raise ValueError
        except ValueError:
            print("Syötä numero väliltä 1-3!")
        except FileNotFoundError:
            print("Ei tallennettuja pelejä")