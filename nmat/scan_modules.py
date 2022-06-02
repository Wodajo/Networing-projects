import time  # Aby bramka logiczna byla rozwazona po timeoucie
from scapy.all import *
from scapy.layers.inet import *
import os


def dec_gate(dec):
    if dec == "" or dec.lower().strip() == "y" or dec.lower().strip() == "yes":
        dec = True
    else:
        dec = False
    return dec


def IP_search():
    ip_1 = str(os.popen('hostname -I | awk -F"." \'{print $1}\'').read()).strip()
    ip_2 = str(os.popen('hostname -I | awk -F"." \'{print $2}\'').read()).strip()
    ip_3 = str(os.popen('hostname -I | awk -F"." \'{print $3}\'').read()).strip()
    ip_33 = str(os.popen('hostname -I | awk -F"." \'{print $1"."$2"."$3"."}\'').read()).strip()  # pierwsze 3 oktety hosta
    ip_4 = str(os.popen('hostname -I | awk -F"." \'{print $4}\'').read()).strip()
    return ip_3, ip_1, ip_2, ip_33, ip_4

def mask_search():
    device = input("Z jakiego interfejsu sieciowego korzystasz? [np. eth0]: ")
    mask = str(os.popen(f"nmcli dev show {device} | grep  IP4.ADDRESS").read()).strip().split("/")[1]
    print(mask)
    return mask


def IP_distinguish():
    while True:
        zakres = str(input(f"Podaj zakres adresow sieci /24 [np. 1-120]: "))
        try:
            if zakres == "":
                a = 0
                b = 255
                c = 1

            elif "-" not in zakres:
                a = int(zakres)
                b = int(zakres)
                c = 1

            else:
                a = int(zakres.strip().split("-")[0])
                b = int(zakres.strip().split("-")[1])
                if a > b:  # Na wypadek jakby ktos wpisal np. 23-12
                    c = -1
                else:
                    c = 1
            return a, b, c
        except ValueError as ex:  # Na wypadek gdyby ktos wpisal literki (int() wyrzucilby blad)
            print(f"Wystapil blad {ex}. Podaj zakres jeszcze raz")
        except NameError as ex:
            print(f"Wystapil {ex}. Podaj zakres jeszcze raz")
        except:
            print("Wystapil blad. Podaj podaj zakres adresow jeszcze raz")


def scan_ICMP(a, b, c, ip_1, ip_2, ip_3):
    scan_ICMP.aktywne_hosty = []  # lista utworzona w taki sposob, aby fcje poza fcja scan_ICMP 
    # rozpoznawaly te liste i ja modyfikowaly
    for adres in range(a, b + 1, c):
        ip_full = f"{ip_1}.{ip_2}.{ip_3}.{adres}"  # Budowa adresu IP
        pakiet = IP(dst=ip_full) / ICMP()  # Budowa pakietu
        sending_ICMP(ip_full, pakiet)
        continue
    return scan_ICMP.aktywne_hosty


def sending_ICMP(ip_full, pakiet):  # Wysyla pakiet i buduje liste aktywne_hosty

    response = sr1(pakiet, timeout=1)
    time.sleep(1.1)
    try:
        if response is None:
            pass
        else:
            scan_ICMP.aktywne_hosty.append(f"{ip_full}")  # Budowa ostatecznej listy hostow.
            #  NIE testowane w uzyciu poza blokiem kodu fcji w ktorej zdefiniowana lista "scan_ICMP.aktywne_hosty"
    except NameError as ex:  # Najpewniej wynika ze zle napisanego kodu
        print(f"Blad: {ex}.")
    except:
        scan_ICMP.aktywne_hosty.append(f"{ip_full} - blad")  # Na wypadek nieznanego bledu

def ports_distinguish():
    while True:  # Okreslanie portow
        zakres_portow = str(input(f"Zakres portow do przeskanowania: "))
        try:
            if zakres_portow == "":
                print("Zakres portow nie moze byc pusty")
                continue
            elif "-" not in zakres_portow:  # Dla jednego portu
                d = int(zakres_portow)
                e = int(zakres_portow)
                f = 1
            else:
                d = int(zakres_portow.strip().split("-")[0])
                e = int(zakres_portow.strip().split("-")[1])
                if d > e:  # Na wypadek jakby ktos wpisal np. 23-12
                    f = -1
                else:
                    f = 1
            return d, e, f
        except ValueError as ex:  # Na wypadek gdyby ktos wpisal literki (int() wyrzucilby blad)
            print(f"Wystapil blad {ex}. Podaj zakres jeszcze raz")
        except:
            print("Wystapil blad. Podaj podaj zakres portow jeszcze raz")


def sending_TCP(ip_full, dst_ports, pakiet):
    
    res = sr1(pakiet, timeout=1)
    try:
        res_flag = res.getlayer(TCP).flags  # Flaga odpowiedzi

        if str(res_flag) == "SA":
            build_TCP.results[ip_full].append(dst_ports)  # Dodaje port do listy podpietej do danego IP
        elif "RA" in str(res_flag):
            print("RAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        elif type(res_flag) == None:
            pass
        else:
            print(f"Response flag: {res_flag}. Dodaj bramke logiczna do kodu")
    except AttributeError as ex:
        print(f"Blad {ex}. Dla portu {dst_ports} na adresie {ip_full}")

def build_TCP(d, e, f, ip_full):
    for dst_ports in range(d, e + 1, f):  # Budowa pakietow
        pakiet = IP(dst=ip_full)/TCP(dport=dst_ports, sport=random.randint(20000, 60000), flags="S")  # Chce wyslac paczke z flaga SYN
        sending_TCP(ip_full, dst_ports, pakiet)
    
def mask_analysis():  # Chce ustalac zakres IP oktet po oktecie. To umozliwi pozniejsza rozbudowe o maski <24
    x = 32  # Maksymalna wielkosc maski
    mask = int(mask_search())
    ip_3, ip_1, ip_2, ip_33, ip_4 = IP_search()
    ip_1 = int(ip_1)
    ip_2 = int(ip_2)
    ip_3 = int(ip_3)
    ip_4 = int(ip_4)
    y = x - mask
    # max_l_hostow = (2 ** y) - 2  # maksymalna liczba hostow w sieci z dana maska. (NIE POOTRZEBNE)
    # Bez Network ID oraz Broadcast ID
    #  Chce miec parametry do zrobienia adresow do skanu a nie, liczbe hostow
    if y <= 8:
        dec1 = 1
        a = 1
        for i in range(y):
            a += 2 ** i  # Pelny zakres jednej subnet | Dla y = 8 suma do 2^7 = 255 (a startuje z 1 => 256)
        b = ip_4 / a  # szukanie w ktorej podsieci jest host
        poczatek4 = math.floor(b) * a  # Dolna granica subnet
        koniec4 = math.floor(b + 1) * (a)  # Gorna granica subnet
        return ip_1, ip_2, ip_3, poczatek4, koniec4
    else:
        print("Nie obslugiwany zakres maski")
    # Jak bedzie moc mozna dopisac warunki dla masek < 24


def build_IP(dec1, a, b, c, d, e, f):  #NIE UZYWANA (stary pomysl)
    build_TCP.results = {}
    if dec1:
        ip = scan_ICMP.aktywne_hosty
        for ip_full in ip:
            build_TCP.results.update({ip_full:[]})  # IP beda kluczami, lista portow bedzie wartoscia
            build_TCP(d, e, f, ip_full)
    else:
        for adres in range(a, b + 1, c):
            ip_full = f"{ip_1}.{ip_2}.{ip_3}.{adres}"  # Budowa adresu IP
            build_TCP.results.update({ip_full:[]})
            build_TCP(d, e, f, ip_full)
