import os
import subprocess
from flask import Flask, request, jsonify, render_template, send_file
import nmap
import zxcvbn
import socket
import paramiko
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import io
import base64
import json

app = Flask(__name__)

# Description et conseils de sécurité pour les services courants
SERVICE_DESCRIPTIONS = {
    'http': 'HTTP est utilisé pour la communication web. Assurez-vous d\'utiliser HTTPS pour sécuriser les données en transit.',
    'https': 'HTTPS sécurise la communication web en cryptant les données en transit. Assurez-vous d\'avoir un certificat valide.',
    'ssh': 'SSH est utilisé pour les connexions sécurisées à distance. Utilisez des clés SSH plutôt que des mots de passe pour une meilleure sécurité.',
    'ftp': 'FTP est utilisé pour le transfert de fichiers. Utilisez FTPS ou SFTP pour sécuriser les transferts.',
    # Ajoutez d'autres descriptions et conseils selon les besoins
}

def est_adresse_ip(adresse):
    try:
        socket.inet_aton(adresse)
        return True
    except socket.error:
        return False

def resoudre_nom_domaine(domaine):
    try:
        return socket.gethostbyname(domaine)
    except socket.gaierror:
        return None

def decouverte_ports_services(ip):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(ip, arguments='-p-')
        return dict(scanner[ip]['tcp'])
    except nmap.PortScannerError as e:
        return {"error": str(e)}

def detection_vulnerabilites(ip):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(ip, arguments='-sV --script vuln')
        scan_result = scanner[ip]
        return scan_result['tcp'] if 'tcp' in scan_result else {}
    except nmap.PortScannerError as e:
        return {"error": str(e)}

def analyse_securite_mots_passe(passwords):
    results = []
    for password in passwords:
        analysis = zxcvbn.zxcvbn(password)
        feedback = analysis['feedback']['suggestions']
        if analysis['score'] < 3:
            feedback.append('Utilisez une combinaison de majuscules, minuscules, chiffres et symboles.')
        results.append({
            'password': password,
            'score': analysis['score'],
            'feedback': feedback
        })
    return results

def tests_authentification(identifiants):
    resultat_tests = {}
    for username, password in identifiants.items():
        if username == "admin" and password == "password123":
            resultat_tests[username] = "Authentification réussie"
        else:
            resultat_tests[username] = "Échec d'authentification"
    return resultat_tests

def brute_force_ssh(hostname, port, username, password_list):
    results = {}
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for password in password_list:
        try:
            client.connect(hostname, port=port, username=username, password=password, timeout=1)
            client.close()
            results[password] = "Authentication succeeded"
        except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException):
            results[password] = "Authentication failed"
        except Exception as e:
            results[password] = str(e)
    return results

def run_nikto(target):
    cmd = f"nikto -h {target}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def run_wpscan(target):
    cmd = f"wpscan --url {target} --api-token YOUR_API_TOKEN"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def run_nuclei(target):
    cmd = f"nuclei -u {target}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def generer_rapport(ip, choix, ports_services, vulnerabilites, resultats_analyse, resultats_authentification, nikto_result=None, wpscan_result=None, nuclei_result=None, ssh_result=None):
    rapport = f"Rapport d'analyse de sécurité pour l'adresse IP : {ip}\n\n"
    
    if 'ports_services' in choix and ports_services:
        rapport += "Découverte de Ports et Services :\n"
        for port, service in ports_services.items():
            service_name = service['name']
            description = SERVICE_DESCRIPTIONS.get(service_name, 'Aucune description disponible.')
            rapport += f"- Port {port} : Service {service_name} - {service['product']} {service['version']}\n"
            rapport += f"  Description : {description}\n"
        rapport += "\n"
    
    if 'vulnerabilites' in choix:
        rapport += "Détection de Vulnérabilités :\n"
        if vulnerabilites:
            for port, details in vulnerabilites.items():
                rapport += f"- Port {port} : {details}\n"
        else:
            rapport += "Aucune vulnérabilité détectée.\n"
        rapport += "\n"
    
    if 'analyse_mots_passe' in choix and resultats_analyse:
        rapport += "Analyse de la Sécurité des Mots de Passe :\n"
        for resultat in resultats_analyse:
            rapport += f"- Mot de passe : {resultat['password']}\n"
            rapport += f"  Score de robustesse : {resultat['score']}\n"
            if resultat['feedback']:
                rapport += f"  Conseils : {' '.join(resultat['feedback'])}\n"
            rapport += "\n"
    
    if 'authentification' in choix and resultats_authentification:
        rapport += "Tests d'Authentification :\n"
        for username, resultat in resultats_authentification.items():
            rapport += f"- Authentification pour {username} : {resultat}\n"

    if 'brute_force_ssh' in choix and ssh_result:
        rapport += "Résultat de Brute Force SSH :\n"
        for password, result in ssh_result.items():
            rapport += f"- {password} : {result}\n"
        rapport += "\n"

    if 'nikto' in choix and nikto_result:
        rapport += "Résultats du scan Nikto :\n"
        rapport += nikto_result
        rapport += "\n"

    if 'wpscan' in choix and wpscan_result:
        rapport += "Résultats du scan WPSCan :\n"
        rapport += wpscan_result
        rapport += "\n"

    if 'nuclei' in choix and nuclei_result:
        rapport += "Résultats du scan Nuclei :\n"
        rapport += nuclei_result
        rapport += "\n"

    return rapport

def generer_graphique_ports(ports_services):
    ports = list(ports_services.keys())
    counts = [1] * len(ports)  # Juste pour illustrer

    data = {
        'labels': ports,
        'datasets': [{
            'label': 'Nombre de services',
            'data': counts,
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }
    return data

def generer_pdf(rapport):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    style_title = styles['Title']
    style_normal = styles['BodyText']

    # Title
    title = Paragraph("Rapport d'analyse de sécurité", style_title)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Content
    for line in rapport.split('\n'):
        paragraph = Paragraph(line, style_normal)
        elements.append(paragraph)
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    cible = request.form['cible']
    choix = request.form.getlist('choix')

    if not est_adresse_ip(cible):
        ip_cible = resoudre_nom_domaine(cible)
        if ip_cible is None:
            return jsonify({"error": "Le nom de domaine fourni est invalide ou introuvable."}), 400
    else:
        ip_cible = cible

    resultats = {}
    graphique_ports = None
    if 'ports_services' in choix:
        resultats['ports_services'] = decouverte_ports_services(ip_cible)
        graphique_ports = generer_graphique_ports(resultats['ports_services'])

    if 'vulnerabilites' in choix:
        resultats['vulnerabilites'] = detection_vulnerabilites(ip_cible)
    
    if 'analyse_mots_passe' in choix:
        mots_de_passe = ["password123", "P@ssw0rd!", "correct horse battery staple"]
        resultats['analyse_mots_passe'] = analyse_securite_mots_passe(mots_de_passe)
    
    if 'authentification' in choix:
        identifiants = {"admin": "password123", "user": "abc123", "john": "passw0rd!"}
        resultats['authentification'] = tests_authentification(identifiants)
    
    ssh_result = None
    if 'brute_force_ssh' in choix:
        ssh_result = brute_force_ssh("example.com", 22, "admin", ["password123", "P@ssw0rd!", "admin123"])  # Dummy data
    
    nikto_result = None
    if 'nikto' in choix:
        nikto_result = run_nikto(ip_cible)
    
    wpscan_result = None
    if 'wpscan' in choix:
        wpscan_result = run_wpscan(ip_cible)
    
    nuclei_result = None
    if 'nuclei' in choix:
        nuclei_result = run_nuclei(ip_cible)

    rapport = generer_rapport(
        ip_cible,
        choix,
        resultats.get('ports_services', {}),
        resultats.get('vulnerabilites', {}),
        resultats.get('analyse_mots_passe', []),
        resultats.get('authentification', {}),
        nikto_result,
        wpscan_result,
        nuclei_result,
        ssh_result
    )

    return render_template('resultat.html', rapport=rapport, graphique_ports=json.dumps(graphique_ports) if graphique_ports else None)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    rapport = request.form['rapport']
    pdf = generer_pdf(rapport)
    return send_file(pdf, as_attachment=True, download_name='rapport_scan.pdf', mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)
