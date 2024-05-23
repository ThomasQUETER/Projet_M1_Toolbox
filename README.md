# Projet_M1_Toolbox

## Introduction

La Toolbox de Sécurité est un ensemble complet d'outils d'analyse de sécurité conçu pour vous assister dans la réalisation de divers audits de sécurité. Elle inclut des fonctionnalités telles que la découverte de ports et de services, la détection de vulnérabilités, l'analyse de la sécurité des mots de passe, les tests d'authentification, les attaques par force brute SSH, ainsi que des scans spécifiques utilisant des outils comme Nikto, WPSCan et Nuclei.

## Fonctionnalités

- **Découverte de Ports et Services** : Scanne tous les ports et détecte les services qui y sont exécutés.
- **Détection de Vulnérabilités** : Identifie les vulnérabilités en utilisant des scripts Nmap.
- **Analyse de la Sécurité des Mots de Passe** : Évalue la robustesse des mots de passe et fournit des recommandations.
- **Tests d'Authentification** : Teste la robustesse des mécanismes d'authentification.
- **Attaque par Force Brute SSH** : Tente des attaques par force brute sur SSH pour tester la robustesse des mots de passe.
- **Nikto** : Scanne les serveurs web pour détecter des vulnérabilités.
- **WPSCan** : Scanne les sites WordPress pour détecter des vulnérabilités.
- **Nuclei** : Scanne pour des vulnérabilités spécifiques en utilisant des modèles personnalisables.

## Prérequis

- **Python 3.x**
- **Flask**
- **nmap**
- **zxcvbn**
- **paramiko**
- **reportlab**
- **matplotlib**
- **Nikto**
- **WPSCan** (nécessite un jeton API)
- **Nuclei**

## Installation

1. **Cloner le Répertoire :**
   ```bash
   git clone https://github.com/ThomasQUETER/Projet_M1_Toolbox.git
   cd Projet_M1_Toolbox

2. **Installer les Dépendances Python :**
   ```bash
   pip install -r requirements.txt

3. **Installer les Outils Externes :**

   Nikto: Suivez les instructions sur la page officielle de Nikto : https://github.com/sullo/nikto   
   WPSCan: Suivez les instructions sur la page officielle de WPSCan : https://wpscan.com   
   Nuclei: Suivez les instructions sur la page officielle de Nuclei : https://nuclei.projectdiscovery.io/
   
4. **Configurer le Jeton API pour WPSCan :**

   Obtenez votre jeton API sur WPSCan
   Ajoutez votre jeton API dans le fichier app.py :
   ```python
   def run_wpscan(target):
    cmd = f"wpscan --url {target} --api-token VOTRE_JETON_API"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

## Utilisation

1. **Démarrer l'Application :**
   ```bash
   python app.py
   
2. **Accéder à l'Interface Web :**

   Ouvrez votre navigateur web et allez à http://127.0.0.1:5000
   
3. **Effectuer un Scan :**

   - Entrez l'IP ou le domaine cible.
   - Sélectionnez les options de scan souhaitées.
   - Cliquez sur "Lancer le scan" pour démarrer le scan.

4. **Télécharger le Rapport :**

   Après la fin du scan, vous pouvez télécharger le rapport détaillé au format PDF.

## Tests

Pour vous assurer que toutes les fonctionnalités fonctionnent comme prévu, vous pouvez tester manuellement chaque fonctionnalité en utilisant des machines vulnérables comme Metasploitable, OWASP Juice Shop ou DVWA. Voici un guide rapide :

1. **Installer des Machines Vulnérables :**

   - Téléchargez et configurez des machines comme Metasploitable depuis SourceForge : https://sourceforge.net/projects/metasploitable

2. **Exécuter des Scans :**

   - Utilisez la toolbox pour scanner ces machines vulnérables.
   - Vérifiez que les résultats sont précis et complets.

## Structure du Projet
```
      Projet_M1_Toolbox/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   │   ├── index.html
   │   ├── resultat.html
   └── static/
       └── particles.json
```
## Contribution

Si vous souhaitez contribuer à ce projet, veuillez forker le répertoire et utiliser une branche de fonctionnalité. Les pull requests sont les bienvenues.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d'informations.
 ___________________________________________________________________________________________________________________________________________________________________________________________
 
Note : Assurez-vous d'avoir toutes les permissions et droits nécessaires pour utiliser et distribuer les outils inclus dans cette toolbox. Certains outils peuvent nécessiter des licences spécifiques ou des jetons API pour leur utilisation.

## Contact

Pour toute question ou assistance, veuillez contacter [thomas.queter@supdevinci-edu.fr].
