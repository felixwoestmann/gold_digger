# gold_digger

A collection of scripts to fetch stocklevel of Kodak films from dm Stores in germany

Requires: urllib3
```
usage: main.py [-h] --address ADDRESS [--radius RADIUS] [--filmtypes FILMTYPES [FILMTYPES ...]]

Zeige alle dm Filialen mit einem Bestand an Kodak Filmen in der Nähe der angegebenen Addresse

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS     Adresse in deren Umkreis gesucht wird
  --radius RADIUS       Radius in km um die Adresse. default: 40km
  --filmtypes FILMTYPES [FILMTYPES ...]
                        Filmtypen nach denen gesucht wird. Optionen: GOLD, COLORPLUS, ULTRAMAX. dafault: alle
```

