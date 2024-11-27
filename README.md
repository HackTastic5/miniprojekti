# Miniprojekti

## BibTeX-sitaattigeneraattori

[![GHA workflow badge](https://github.com/HackTastic5/miniprojekti/workflows/CI/badge.svg)](https://github.com/HackTastic5/miniprojekti/actions)

[Product backlog ja sprint backlogit](https://docs.google.com/spreadsheets/d/1cBhyVR3Zbdce5GyGX__jlB-rGVCpWYUqm5k0h3NEfdI)

## Asennusohjeet

Sovelluksen käyttö vaatii Python-version 3.10-3.12.x, ja koneella tulee olla asennettuna Poetry riippuvuuksien hallintaa varten.

1 Kloonaa repositorio omalle koneellesi seuraavasti:
```
$ git clone git@github.com:HackTastic5/miniprojekti.git
```

2 Lisää juureen .env-tiedosto, josta löytyy seuraavat muuttujat:
```
SECRET_KEY=<salainen-avain>
TEST_ENV=false
DATABASE_URL=postgresql://<tietokannan-nimi>
```

Voit luoda salaisen avaimen seuraavasti:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

3 Asenna projektin riippuvuudet seuraavalla komennolla:
```
$ poetry install
```

4 Siirry virtuaaliympäristöön seuraavalla komennolla:
```
$ poetry shell
```

5 Luo sovelluksen käyttämä tietokantataulu virtuaaliympäristössä seuraavasti:
```
$ python src/db_helper.py
```

## Käyttöohjeet

Käynnistä sovellus virtuaaliympäristössä seuraavasti:
```
$ python src/index.py
```

## Definition of done

Definition of done eli valmiin määritelmä tarkoittaa sitä, että vaatimukset on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu, dokumentoitu ja integroitu muuhun ohjelmistoon. 

## Lisenssi

Työ on lisensoitu [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) -lisenssillä.
