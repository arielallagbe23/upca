https://github.com/arielallagbe23/upca/assets/97161872/45c75c5a-3f87-4155-a582-8cac97325f97

Bonjour, 
Bienvenue dans le repertoire git UPCA de l'algorithme qui : 
 - Retranscris une calculatrice en notation polonaise inverse (NPI),
 - Permet d'enregistrer les calculs effectués dans une base de donné
 - Permet d'exporter ces calclus au format csv

Afin de pouvoir utiliser ce projet sur votre macchine, il va falloir l'installer. Ci dessous je vous retranscrirai les etapes à suivre pour y parvenir 

1 - Créer un nouveau repertoire deans votre dossier dev ou votre repertoire contenant vos applications grace à cette commande : 

```bash
mkdir <nom_de_votre_choix>
```

2 - Cloner le repertoire github ci dessous dans le dossier que vous avez créez grace à cette commande 
```bash
git clone https://github.com/arielallagbe23/upca.git
```
3 - Supprimer le dossier portant ce nom : ucpa-front-end, grace à cette commande 
```bash
rm -r ucpa-front-end
```

4 - Dans votre repertoire upca, clonner le repertoire upca-front-end 
```bash
git clone https://github.com/arielallagbe23/upca-front-end.git
```

5 - Enfin executez cette commande : 
```bash
docker compose up
```

Voila l'algorithme est disponible sur votre machine.

