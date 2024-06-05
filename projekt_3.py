"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Martin Pokorný
email: pokornymartin2@gmail.com
discord: martin_pokorny86
"""

import sys
import csv
from bs4 import BeautifulSoup as bs
from requests import get

# spuštění stahování dat z webu a jejich zápis do CSV souboru

def main(web_umisteni, nazev_souboru):
    """
    Funkce se spustí po správném zadání argumentů uživatelem.
    Začne stahování dat z webu a jejich zápis do CSV souboru
    """
    print("Probíhá stahování dat z webu a jejich ukládání do CSV souboru")

    prefix = "https://volby.cz/pls/ps2017nss/"
    distinct_urls = distinct_url_code(web_umisteni, prefix)
    response = get(distinct_urls[0])
    kandidujici_strany = nazvy_stran(response)

    obce_kody = []
    for url in distinct_urls:
        obce_kody.extend(sestimistny_kod_obce(url))

    finalni = webscraping(distinct_urls, obce_kody)
    zapis_csv(finalni, nazev_souboru, kandidujici_strany)

def distinct_url_code(web_umisteni, prefix):
    """
    Funkce stáhne webový odkaz ke každému kódu obce, který začíná v HTML stránce vždy ps311 <a href = ps311>
    """
    # stáhne obsah zadané URL
    kod_obce = get(web_umisteni)
    # parsování HTML kódu
    kod_obce_bs = bs(kod_obce.content, "html.parser")
    distinct_urls = set()
    for url in kod_obce_bs.find_all("a", href=True):
        if "ps311" in url["href"]:
            full_url = prefix + url["href"]
            distinct_urls.add(full_url)
    return list(distinct_urls)

def nazvy_stran(response):
    """
    Funkce vypíše názvy stran z daného webového odkazu
    """
    # parsování HTML obsahu
    
    nazvy_stran_bs = bs(response.content, "html.parser")
    
    # najdeme názvy stran v první tabulce
    
    prvni_tabulka = nazvy_stran_bs.find_all('td', headers='t1sa1 t1sb2')
    prvni_tabulka_nazvy = [znak.get_text(strip=True) for znak in prvni_tabulka]
    
    # najdeme názvy stran v druhé tabulce
    
    druha_tabulka = nazvy_stran_bs.find_all('td', headers='t2sa1 t2sb2')
    druha_tabulka_nazvy = [znak.get_text(strip=True) for znak in druha_tabulka]
    
    # sloučíme výsledky a vrátíme sjednocený seznam stran
    
    vsechny_nazvy = prvni_tabulka_nazvy + druha_tabulka_nazvy
    return vsechny_nazvy

def sestimistny_kod_obce(text):
    """
    Funkce získá z webu kódy jednotlivých obcí a zajistí, že budeme pracovat pouze se šesticifernými čísly
    """
    codes = []
    for i in range(len(text) - 5):
        substring = text[i:i + 6]
        if substring.isdigit(): # zjistíme, zda podřetězec obsahuje pouze číslice
            codes.append(substring) # pokud je podřetězec číselný, přidá se do seznamu <codes>
    return codes

def ocisteni_textu(text):
    """
    Funkce slouží k očištění HTML dat
    """
    return text.strip().replace("\xa0", "").replace("&nbsp;", "") # očištění HTML dat -> odstranění \xa0 a &nbsp; prázdným textovým řetězcem

def vyhledani_pripojeni_dat(nazvy_stran_bs, headers, data_list):
    """
    Funkce připraví podklad pro další zpracování požadovaných dat
    """
    td = nazvy_stran_bs.find("td", {"class": "cislo", "headers": headers})
    if td:
        data_list.append(ocisteni_textu(td.text))
    else:
        data_list.append("N/A")

def webscraping(obce_web, obce_kody):
    """
    Funkce stáhne, filtruje a agreguje data
    """
    finalni = []
    for index, obec_link in enumerate(obce_web):
        obce_data = []
        response = get(obec_link)

        if response.status_code == 200:
            nazvy_stran_bs = bs(response.content, "html.parser")
            town_code = obce_kody[index] if index < len(obce_kody) else "N/A"
            obce_data.append(town_code)
            town_tag = nazvy_stran_bs.find('h3', string=lambda x: x and 'Obec:' in x)
            town_name = town_tag.text.split(': ')[1].strip() if town_tag else "N/A"
            obce_data.append(town_name)
            vyhledani_pripojeni_dat(nazvy_stran_bs, "sa2", obce_data)  # voliči v seznamu
            vyhledani_pripojeni_dat(nazvy_stran_bs, "sa3", obce_data)  # vydané obálky
            vyhledani_pripojeni_dat(nazvy_stran_bs, "sa6", obce_data)  # platné hlasy

            for headers in ["t1sa2 t1sb3", "t2sa2 t2sb3"]:
                numbers_td = nazvy_stran_bs.find_all("td", {"class": "cislo", "headers": headers})
                for cislo_td in numbers_td:
                    obce_data.append(ocisteni_textu(cislo_td.text))
            finalni.append(obce_data)
        else:
            print("Chyba v načítání webové stránky:", response.status_code)
    return finalni

def zapis_csv(finalni, nazev_souboru, kandidujici_strany):
    """
    Funkce zapíše data do souboru .CSV
    """
    with open(nazev_souboru, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['kód obce', 'název obce', 'voliči v seznamu', 'vydané obálky', 'platné hlasy'] + kandidujici_strany)
        writer.writerows(finalni)

# získáme informace z HTML stránky pomocí parsování HTML a knihovny BeautifulSoup4

def distinct_url_code(web_umisteni, prefix):
    """
    Funkce získá HTML informace k odkazům pro jednotlivé obce
    """
    kod_obce = get(web_umisteni)
    kod_obce_bs = bs(kod_obce.content, "html.parser")
    distinct_urls = set()
    for url in kod_obce_bs.find_all("a", href=True):
        if "ps311" in url["href"]:
            full_url = prefix + url["href"]
            distinct_urls.add(full_url)
    return list(distinct_urls)

# kontrola zadaných argumentů uživatelem

def kontrola_argumentu(web_umisteni, nazev_souboru):
    """
    Funkce kontroluje správné zadání argumentů.
    První argument -> kontrola začátku odkazu na webovou stránku.
    Druhý argument -> kontrola typu souboru ve formátu .csv
    
    """
    http_zacatek = "https://volby.cz/pls/ps2017nss/"
    koncovka = ".csv"
    if web_umisteni.startswith(http_zacatek) and nazev_souboru.endswith(koncovka):
        return True
    else:
        print("Zadali jste chybné argumenty")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Vložte kód ve správném formátu: python <name>.py <web_umisteni>, <nazev_souboru>")
        sys.exit(1)
    web_umisteni = sys.argv[1]
    nazev_souboru = sys.argv[2]
    if not kontrola_argumentu(web_umisteni, nazev_souboru):
        sys.exit(1)
    main(web_umisteni, nazev_souboru)
