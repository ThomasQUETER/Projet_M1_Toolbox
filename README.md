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
