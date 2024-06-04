# Elections Scraper
Python: třetí projekt

## 1. Popis projektu
Program vytvoří scraper výsledků voleb z roku 2017 pomocí webscrapingu

Skript vybere jakýkoliv územní celek z níže uvedeného odkazu:
https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

## 2. Instalace knihoven třetích stran

Ve VSCode bylo vytvořeno nové virtuální prostředí a aktivováno pomocí kódu:
.\venv\Scripts\Activate.ps1

Následně byly manuálně nainstalovány v IDE (VS Code) tyto knihovny (vyzkoušeno jen pro procvičení manuální instalace, jinak lze postupovat rychleji, viz info níže)

--pandas (pip install pandas) -> pro analýzu dat v Pythonu
--beautifulsoup4 (pip install beautifulsoup4) -> pro analýzu a zpracování HTML a XML dokumentů
--urllib3 (pip install urllib3) -> pro práci s HTTP požadavky
--requests (pip install requests) -> pro práci s HTTP požadavky
--chardet (pip install chardet) -> pro detekci kódování znaků (charsetů) textových dat

Zkontrolujeme seznam nainstalovaných knihoven (pip freeze)

Vytvoříme textový dokument, kde bude uveden seznam všech knihoven potřebných k Projektu (pip freeze > requirements.txt)

Pokud nechceme manuálně instalovat knihovny, použijeme PyCharm, díky kterému automaticky vytvoříme textový soubor se seznamem nezbytných knihoven
(Tools -> Sync Python Requirements -> Strong equality version -> Add imported packages to requirements -> ok)

Knihovny pak rychleji nainstalujeme ze souboru requirements.txt vytvořeného v PyCharm pomocí kódu:
pip install -r requirements.txt

## zadání kódu v Terminálu -> spuštění programu

obecně: python <name>.py <web_umisteni>, <nazev_souboru>
příklad: python projekt_3.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109', 'vysledky_Praha_vychod.csv'
Získáme volební výsledky za okres "Praha - východ". Prvním argumentem je odkaz na webovou stránku voleb, druhý parametr je název souboru ve formátu .CSV

## po správném spuštění kódu

Objeví se informace: "Probíhá stahování dat z webu a jejich ukládání do CSV souboru". Následně se CSV soubor uloží do složky, která je zobrazená
v Terminálu virtuálního prostředí

## ukázka výstupu

kód obce	název obce	voliči v seznamu	vydané obálky	platné hlasy	Občanská demokratická strana	Řád národa - Vlastenecká unie
538493	Mnichovice	        2688	            1941	         1933	                309	                                6
538264	Jenštejn	        665	                 479	          475	                 91	                                0
538507	Mochov	            784	                 505	          504	                 71	                                15
538973	Veliká Ves	        241	                 147	          145	                 32	                                0



