import getmac
import argparse
import socket
from ping3 import ping
import psutil

def bereken_alle_hosts_in_netwerk(ip_adres: str, subnet_mask: str): ############ OK ################
    ip_lijst = []                                                           # Ip lijst leeg aanmaken

    if is_geldig_ipv4(ip_adres) == False:                                   # Controleren of het IP geldig is 
        print('Het IP adres is niet geldig.')

    aantal = bereken_aantal_adressen(subnet_mask) -1                        # Het aantal te calculeren IPs berekenen, Dit -1 omdat we de eerste al gaan hebben
    startadres = bereken_netwerk_adres(ip_adres, subnet_mask)               # Het eerste IP adres berekenen       
    
    # Het IP adres opsplitsen
    ip_adres_split = startadres.split('.')                                  
    # Het opgesplitste IP aan de lijst toevoegen (1ste IP)
    ip_lijst.append(str(ip_adres_split[0])+'.'+str(ip_adres_split[1])+'.'+str(ip_adres_split[2])+'.'+str(ip_adres_split[3]))

    while aantal > 0:                                                       # Zolang het aantal niet 0 is, bereken het volgende IP en voeg deze toe aan de lijst
        # IP adres optellen
        ip_split = increment_octet(ip_adres_split)
        # Opgetelde IP adres als ip zetten om vanaf op te tellen
        ip_adres_split = ip_split
        # IP adres als string zetten
        ip_adres_str = str(ip_split[0])+'.'+str(ip_split[1])+'.'+str(ip_split[2])+'.'+str(ip_split[3])
        #IPadres aan de lijst toevoegen
        ip_lijst.append(ip_adres_str)
        # Aantal -1 doen zodat het geen oneindige loop wordt
        aantal -=1                                                          

    return ip_lijst                                                         # IP lijst returnen


def bereken_netwerk_adres(ip_adres: str, subnet_mask: str):     ############ OK ################
    
    basis_IP = ''                                   # Variabele voor ip aanmaken en leeg zetten

    ip_split = ip_adres.split('.')                  # IP adres opsplitsen
    subnet_split = subnet_mask.split('.')           # Subnet opsplitsen

    basis_IP = str( int( ip_split[0] ) & int(subnet_split[0] ) ) + '.'            # AND operator op de integers ( 1 en 1 wordt 1, 1 en 0 wordt 0)
    basis_IP += str( int( ip_split[1] ) & int(subnet_split[1] ) ) + '.'           # idem, bij in de variabele zetten
    basis_IP += str( int( ip_split[2] ) & int(subnet_split[2] ) ) + '.'           # Idem, bij in de variabele zetten
    basis_IP += str( int( ip_split[3] ) & int(subnet_split[3] ) )                 # Idem, bij in de variabele zetten

    return basis_IP


def increment_octet(ip_adres: list):                            ############ OK ################
    
    eerste = int(ip_adres[0])                               # IP adres opdelen in 4 stukken
    tweede = int(ip_adres[1])
    derde = int(ip_adres[2])
    vierde = int(ip_adres[3])


    if vierde >= 255 and derde >= 255 and tweede >= 255:    # als het ipadres x.255.255.255 is; eerste +1, de rest op nul
        eerste +=1
        tweede=0
        derde=0
        vierde=0
    elif vierde >= 255 and derde >= 255:                    # als het ipadres x.x.255.255 is; eerste niks, tweede +1, de rest op nul
        tweede += 1
        derde =0
        vierde =0
    elif vierde >= 255:                                     # als het ipadres x.x.x.255 is; eerste niks, tweede niks, derde +1, vierde op nul
        derde += 1
        vierde = 0
    else:                                                   # als het ipadres x.x.x.x is; alles zo laten, vierde +1
        vierde +=1
    

    return [eerste,tweede,derde,vierde]                     # ipadres teruggeven


def bereken_aantal_adressen(subnet_mask: str):                  ############ OK ################
   
    subnet_split = subnet_mask.split('.')           #Subnet verdelen in 4 stukken

    count = 0                                       #Aantal 1en definieren, beginnen met 0
    
    for i in subnet_split:                          #Voor alle stukken in de subnetmask het getal omzetten naar binair
        subnet_bin = bin(int(i))                    
        subnet_bin_str = str(subnet_bin)[2:10]      #Binair opslaan zonder 0b
        for j in subnet_bin_str:                    #Als een getal 1 is, de count met 1 verhogen
            if j == '1':
                count += 1
    return 2**(32-count)                            #De uitkomst van de formule returnen

def is_geldig_ipv4(ipv4: str):                                  ############ OK ################
    
    ipv4_split = ipv4.split('.')                    # Ipadres opslitten in 4 delen

    result = []                                     # List result aanmaken, standaard leeg

    if len(ipv4_split) > 4:                         # Als de lengte van de list meer is dan 4, voeg dan False toe aan de list
        result.append('False')
    elif len(ipv4_split) < 4:                       # Als de lengte van de list minder is dan 4, voeg dan False toe aan de list
        result.append('False')

    for i in ipv4_split:                            # controleer elk stukje van de ipv4 list
        if int(i) > 255:                            # Als het getal groter is dan 255, voeg dan False toe aan de list
            result.append('False')

    if 'False' in result:                           # Als er False in de lijst zit, sla dit dan op in de variabele valid
        valid = False
    else:                                           # Als er geen False in de lijst zit, sla dan True op
        valid = True
    
    return valid                                    # Print de uitkomst 

def controleer_input(input):                                    ############ OK ################
    try:                        # Probeer of de ingegeven waarde een integer is, zo ja: zet de variabele input op ok
        val=int(input)
        input='ok'
    except ValueError:          # als dit niet gaat, zet de variabele op nok
        input='nok'
    return input
            

# Schrijf hier je hoofdprogramma. Alles geïntendeerd onder het volgende if statement.
# Dit is nodig om de Unit Tests te laten werken.
if __name__ == '__main__':
    # Parser aanmaken
    parser = argparse.ArgumentParser(description="Script voor")

    # Parser argumenten ingeven
    parser.add_argument('-a', '--all', action='store_true', help='Toon alle adressen, inclusief diegenen die niet actief zijn.')
    parser.add_argument('-o', '--out-file', help='Het bestand naar waar de uitvoer weggeschreven moet worden, zonder extensie!')

    # Parser afsluiten
    args = parser.parse_args()


    # Eerste input met interfaces
    print('Volgende interfaces zijn gedetecteerd, selecteer de interface waarvoor de netwerkgegevens geprint moeten worden.')
    interfaces = psutil.net_if_addrs()
    count=0
    interface_list = []
    for i in interfaces:                    # Optellen van de eerste waarde zodat je een mooie lijst krijgt
        print('(' + str(count) + ')', i)
        interface_list.append(i)
        count +=1

    # Controleer de input, als de input geen string is en dus nok teruggeeft, probeer opnieuw zolang er geen integer gegeven word
    antwoord = input('Selecteer een interface a.u.b.:')
    while controleer_input(antwoord) == 'nok':
        antwoord = input('Geen geldige input, probeer opnieuw:')
    # Controleer of de input effectief in de lijst staat met de count variabele
    while int(antwoord) > (count-1):
        antwoord = input('Deze interface bestaat niet, probeer opnieuw:')

    # Controleren of het antwoord binnen de opties valt
    if int(antwoord) >= 0 and int(antwoord) <= (count-1):
        print('\n'*2)
    else:
        print('Deze interface bestaat niet, controleer de interfaces en herstart het programma.')
    
    # List voor de verschillende interfaces aanmaken, zodat de namen kunnen worden opgeslagen
    interface = interface_list[int(antwoord)]
    # IP adress in de list oproepen, idem voor subnet
    ip = psutil.net_if_addrs()[interface][1][1]
    subnet = psutil.net_if_addrs()[interface][1][2]
    # Adressen berekenen
    adressen = bereken_alle_hosts_in_netwerk(ip,subnet)

    # Kijken of het argument outfile een waarde heeft, zo ja: maak en open het bestand [waarde].csv
    if args.out_file != None:
        f = open(args.out_file + ".csv", "w")

    # Als de outfile geen warde heeft print in de terminal, anders naar bestand (header)
    if args.out_file == None:
        print( 'Hosts'.ljust(15, ' ')+ 'Online'.ljust(15, ' ')+ 'Mac'.ljust(25, ' ')+ 'Hostname'.ljust(15, ' '))
        print()
    else:
        f.write("Hosts;Online;Mac;Hostname\n" )

    
    # Voor elk adres dat berekend is ping het IP
    for adres in adressen:
        pingms= ping(adres, unit='ms')                      # Ping doen en opslaan (makkelijker gebruik)
        mac= None                                           # Basis MAC adres als None Zetten
    
        if args.all == False:               # Dit deel uitvoeren als enkel de actieve IPs geprint moeten worden
            if pingms is not None:                                                                                              # Alleen doorgaan als de ping een waarde heeft
                pingprint = 'Ping = ' + str(round(pingms,2)) + 'ms'                                                             # Ping opslaan als sting (makkelijker gebruik)
                mac = getmac.get_mac_address(ip=adres)                                                                          # Mac ophalen en opslaan
                hostname= socket.getfqdn(adres)                                                                                 # Hostname ophalen en opslaan
                if args.out_file == None:                                                                                      # Als outfile geen waarde heeft, print in terminal
                    print( adres.ljust(15,' ') + pingprint.ljust(15,' ') + str(mac).ljust(25, ' ') + hostname.ljust(15, ' '))
                else:                                                                                                           # Anders print naar bestand
                    f.write(adres+";"+pingprint+";"+str(mac)+";"+hostname+'\n')

        else:                               # Als argument -a is meegegeven voor volgende code uit
            if pingms is not None:                                                                                              # Enkel doorgaan als de ping een waarde heeft
                pingprint = 'Ping = ' + str(round(pingms,2)) + 'ms'                                                             # Ping doen en opslaan als string
                mac = getmac.get_mac_address(ip=adres)                                                                          # Macadres ophalen
                hostname= socket.getfqdn(adres)                                                                                 # Hostname ophalen en opslaan
                if args.out_file == None:                                                                                      # Als outfile geen waarde heeft, print in terminal
                    print( adres.ljust(15,' ') + pingprint.ljust(15,' ') + str(mac).ljust(25, ' ') + hostname.ljust(15, ' '))
                else:                                                                                                           # Anders print naar bestand
                    f.write(adres+";"+pingprint+";"+str(mac)+";"+hostname+'\n')

            else:                                                                                                               # Doorgaan als de ping None is
                if args.out_file == None:                                                                                      # Als outfile geen warde heeft print in terminal
                    print( adres.ljust(15,' ') + 'N/A'.ljust(15,' ') + 'N/A'.ljust(25, ' ') + 'N/A'.ljust(15, ' '))             
                else:                                                                                                           # Anders print naar bestand
                    f.write(adres+";N/A;N/A;N/A\n")
    f.close()                               # Sluit het bestand
