# PYMONDIS
<img src="banner.png" alt="(Banner pymondis)" style="width: 100%;"/>

Nieoficjalny wrapper api [Quatromondis](https://quatromondis.pl/) w pythonie

## Fajne rzeczy
- Wszystkie zapytania są asynchroniczne z użyciem `httpx`
- Fajnie obiekty z użyciem `attrs` (nawet *repr()* działa!)
- Ponawianie nieudanych zapytań
- Epicka składnia pythona 3.10 (dlatego na razie można korzystać tylko z 3.10)
- Cache'owanie zdjęć
- Type-hint-y

## Co możesz zrobić
- Dostać listę wszystkich aktualnych obozów
- Dostać listę wszystkich aktualnych galerii
- Dostać listę wszystkich psorów z opisami (bez biura i HY)
- Dostać listę wszystkich kandydatów plebiscytów od 2019
- Zobaczyć wszystkie zdjęcia ze wszystkich galerii od początku istnienia fotorelacji!
- Zagłosować w plebiscycie
- Męczyć się debugowaniem przez 5 godzin, bo zapomniałeś dać *await* ;)

## Co prawdopodobnie możesz zrobić
- Zarezerwować miejsce w inauguracji
- Zamówić książkę
- Zarezerwować miejsce na obozie
- ~~Dostać informacje o rezerwacji obozu~~
- ~~Zgłosić się o pracę~~

## Instalacja
Aktualna *chyba* działająca wersja
```shell
pip install pymondis
```
Aktualna wersja
```shell
pip install git+https://github.com/Asapros/pymondis.git
```

## UWAGA!
*DZIEJĄ SIĘ DZIWNE RZECZY, ZNIKA WSZYSTKO Z GALERII I DZIEJĄ SIĘ RZECZY NIESTWORZONE*

Przez początek zimowego sezonu galerie się zepsuły. Jest wiele anomalii:
1. Są pokazane galerie z przyszłości
2. Galerie z przyszłości czasem mają w sobie zdjęcia XD (tu zawsze występuje błąd z punktu 4 i czasem z 3)
3. Niektóre galerie, które mają 0 zdjęć, nie są ``empty``
4. Serwer API czasem odsyła do nieistniejących zdjęć na serwerze z zasobami
  (Oczywiście przywala ci ``404 The specified blob does not exist.`` Jakby to była twoja wina)



[dla google bo sobie dalej nie radzi z indeksowaniem :/]: # (quatromondis api quatromondis python api wrapper nieoficjalny)