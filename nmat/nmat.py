# import threading  # Proby optymalizacji (nieudane, dlatego koment)
import scan_modules

#---------------------------------------- Skaner ICMP sieci z maska <= 24-------------------------------------------------
dec1 = str(input("Skaner ICMP? [Y/n]: "))
dec1 = scan_modules.dec_gate(dec1)
if dec1:

    ip_1, ip_2, ip_3, poczatek4, koniec4 = scan_modules.mask_analysis()
    print(f"Skaner ICMP domyslnie przeskanuje adresy {ip_1}.{ip_2}.{ip_3}.{poczatek4} - {ip_1}.{ip_2}.{ip_3}.{koniec4}")
    print("Jezeli chcesz przeprowadzic domyslny skan wcisnij enter")
    a, b, c = scan_modules.IP_distinguish()  # Ustala parametry dla petli z range budujacej adresy IP
    aktywne_hosty = scan_modules.scan_ICMP(a, b, c, ip_1, ip_2, ip_3)  # Buduje adresy IP, buduje paczki, wysyla paczki, zwraca liste hostow ktore odpowiedzialy - ZMIEN NA SLOWNIK

    print(f"Aktywne hosty: {aktywne_hosty}")



#----------------------------------------------- Skaner TCP -------------------------------------------------------------
dec2 = str(input("Skaner portow TCP? [Y/n]: "))
dec2 = scan_modules.dec_gate(dec2)
a, b, c = 0, 0, 0  # Deklaruje je dlatego, ze moga (nie musza) byc wykorzystane w ports.distinguish(). Fcja potrzebuje dosc parametrow do przeslania
if dec2 and dec1:
    print(f"Do skanu uzyte zostana adresy ktore odpowiedzialy na skan ICMP")
elif dec2 and not dec1:
    a, b, c = scan_modules.IP_distinguish()  # Ustala parametry dla petli z range budujacecj liste adresow IP
else:
    print("Bye")

d, e, f = scan_modules.ports_distinguish()  # Ustala parametry dla petli z range budujacej liste portow
scan_modules.build_IP(dec1, a, b, c, d, e, f)
print(scan_modules.build_TCP.results)

