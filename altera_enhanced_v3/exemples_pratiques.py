"""
ALTera ENHANCED - EXEMPLES PRATIQUES
=====================================

Exemples de code prêts à l'emploi pour différents cas d'usage.

Version: 3.0 ENHANCED
"""

from altera_enhanced import (
    ALTeraEnhanced, 
    ConfigurationPersonnelle,
    ProjetALTera,
    ThemeStyle,
    Template
)
from altera_plugins import PluginManager
import os
import time
from datetime import datetime, timedelta


# ============================================================================
# EXEMPLES DE BASE
# ============================================================================

def exemple_1_projet_simple():
    """
    Exemple 1: Créer un projet simple avec configuration minimale
    """
    print("\n" + "="*60)
    print("EXEMPLE 1: PROJET SIMPLE")
    print("="*60)
    
    # Initialiser ALTera
    altera = ALTeraEnhanced()
    
    # Créer un projet
    projet = altera.creer_projet("Appartement_Simple")
    
    # Définir le client
    projet.definir_client(
        nom="M. Durand",
        budget=30000
    )
    
    # Ajouter une note
    projet.ajouter_note("Appartement 2 pièces, style moderne")
    
    # Générer un rapport
    print(projet.generer_rapport())
    
    # Sauvegarder
    projet.sauvegarder_projet()
    
    return projet


def exemple_2_configuration_personnalisee():
    """
    Exemple 2: Configuration personnalisée complète
    """
    print("\n" + "="*60)
    print("EXEMPLE 2: CONFIGURATION PERSONNALISÉE")
    print("="*60)
    
    # Créer une configuration personnalisée
    config = ConfigurationPersonnelle(
        nom_utilisateur="Studio Design Pro",
        entreprise="Architecture & Design SAS",
        unite_defaut="mm",
        tolerance=0.1,
        langue="fr",
        theme_defaut=ThemeStyle.MODERNE,
        dossier_projets="./mes_projets_pro",
        dossier_templates="./mes_templates",
        dossier_cache="./cache_pro",
        afficher_conseils=False,  # Désactiver pour les pros
        mode_expert=True,  # Activer le mode expert
        auto_sauvegarde=True,
        intervalle_sauvegarde=180,  # 3 minutes
        qualite_rendu_defaut="ultra",
        resolution_rendu=(3840, 2160),  # 4K
        samples_rendu=256
    )
    
    # Sauvegarder la configuration
    config.sauvegarder("config_pro.json")
    print(f"✅ Configuration sauvegardée")
    
    # Utiliser avec ALTera
    altera = ALTeraEnhanced(config)
    print(f"👤 Utilisateur: {altera.config.nom_utilisateur}")
    print(f"🎨 Thème: {altera.config.theme_defaut.value}")
    print(f"📐 Mode expert: {'Activé' if altera.config.mode_expert else 'Désactivé'}")
    
    return config


def exemple_3_templates():
    """
    Exemple 3: Utilisation et création de templates
    """
    print("\n" + "="*60)
    print("EXEMPLE 3: TEMPLATES")
    print("="*60)
    
    # Initialiser
    altera = ALTeraEnhanced()
    projet = altera.creer_projet("Projet_Templates")
    
    # Lister les templates disponibles
    print("\n📋 Templates disponibles:")
    for template in projet.templates.lister_templates():
        print(f"  - {template.nom} ({template.style.value})")
    
    # Créer un template personnalisé
    nouveau_template = Template(
        nom="Loft New York",
        description="Loft industriel style new-yorkais",
        type_piece="loft",
        style=ThemeStyle.INDUSTRIEL,
        dimensions_standards={
            'longueur': 12000,
            'largeur': 8000,
            'hauteur': 4000
        },
        mobilier_type=[
            'canape_cuir',
            'table_metal',
            'etageres_acier',
            'lit_mezzanine'
        ],
        palette_couleurs=[
            (51, 51, 51),    # Gris foncé
            (139, 69, 19),   # Brun cuir
            (192, 192, 192), # Argent
            (255, 255, 255)  # Blanc
        ],
        materiaux_preferes=[
            'acier_brut',
            'beton_cire',
            'bois_vieilli',
            'cuir_vieilli',
            'verre'
        ],
        metadata={
            'eclairage': 'suspensions_industrielles',
            'fenetres': 'grandes_verrieres',
            'sol': 'beton_cire',
            'ambiance': 'urbaine'
        }
    )
    
    # Sauvegarder le template
    projet.templates.sauvegarder_template(nouveau_template)
    print(f"\n✅ Template '{nouveau_template.nom}' créé et sauvegardé")
    
    # Utiliser le template
    template = projet.templates.obtenir_template("loft_new_york")
    if template:
        print(f"\n🏗️ Application du template: {template.nom}")
        print(f"  Dimensions: {template.dimensions_standards}")
        print(f"  Mobilier prévu: {', '.join(template.mobilier_type)}")
    
    return nouveau_template


def exemple_4_workflow_complet():
    """
    Exemple 4: Workflow complet de A à Z
    """
    print("\n" + "="*60)
    print("EXEMPLE 4: WORKFLOW COMPLET")
    print("="*60)
    
    # 1. Configuration initiale
    config = ConfigurationPersonnelle(
        nom_utilisateur="Designer Pro",
        entreprise="ALTera Studio",
        theme_defaut=ThemeStyle.SCANDINAVE
    )
    
    altera = ALTeraEnhanced(config)
    
    # 2. Créer le projet
    projet = altera.creer_projet("Maison_Scandinave_2025")
    
    # 3. Informations client
    projet.definir_client(
        nom="Famille Andersson",
        adresse="Bordeaux, France",
        budget=95000,
        deadline="2026-03-15"
    )
    
    # 4. Notes de briefing
    notes = [
        "Style scandinave épuré",
        "Beaucoup de rangements intégrés",
        "Couleurs claires et bois naturel",
        "Éclairage naturel maximisé",
        "Cuisine ouverte sur salon"
    ]
    
    for note in notes:
        projet.ajouter_note(note)
    
    # 5. Simulation du workflow
    etapes = [
        ("Import du scan LIDAR", "scan", {"fichier": "maison_scan.3dm"}),
        ("Analyse de l'espace", "analyse", {}),
        ("Création du salon", "mobilier", {"type": "salon_complet"}),
        ("Création de la cuisine", "mobilier", {"type": "cuisine_ouverte"}),
        ("Création des chambres", "mobilier", {"type": "chambres"}),
        ("Génération des rendus", "rendu", {"qualite": "haute"}),
        ("Création du devis", "devis", {}),
        ("Export final", "export", {"format": "pdf"})
    ]
    
    print("\n📋 Exécution du workflow:")
    for i, (description, commande, params) in enumerate(etapes, 1):
        print(f"\n{i}. {description}...")
        
        # Simuler l'exécution
        projet.ajouter_historique(commande, params)
        time.sleep(0.5)  # Simulation du temps de traitement
        
        print(f"   ✅ {description} - Terminé")
    
    # 6. Rapport final
    print("\n" + "="*40)
    print("RAPPORT FINAL")
    print("="*40)
    print(projet.generer_rapport())
    
    # 7. Sauvegarde
    chemin = projet.sauvegarder_projet()
    print(f"\n💾 Projet sauvegardé: {chemin}")
    
    return projet


# ============================================================================
# EXEMPLES AVANCÉS
# ============================================================================

def exemple_5_plugins():
    """
    Exemple 5: Utilisation du système de plugins
    """
    print("\n" + "="*60)
    print("EXEMPLE 5: SYSTÈME DE PLUGINS")
    print("="*60)
    
    # Créer le gestionnaire de plugins
    manager = PluginManager("./plugins")
    
    # Contexte pour les plugins
    contexte = {
        'version': '3.0',
        'modules': ['scan', 'mobilier', 'rendu', 'devis'],
        'projet_actif': 'Test_Plugins'
    }
    
    # Charger tous les plugins
    manager.charger_tous_plugins(contexte)
    
    # Lister les plugins chargés
    print("\n📦 Plugins disponibles:")
    for plugin_info in manager.lister_plugins():
        status = "✅" if plugin_info['charge'] else "⏸️"
        print(f"{status} {plugin_info['nom']} v{plugin_info['version']}")
        print(f"   {plugin_info['description']}")
        if plugin_info.get('actions'):
            print(f"   Actions: {', '.join(plugin_info['actions'])}")
    
    # Utiliser un plugin
    if "ExportAvance" in manager.plugins:
        print("\n🔌 Utilisation du plugin ExportAvance:")
        
        # Exécuter une action du plugin
        resultat = manager.executer_action(
            "ExportAvance",
            "export_batch",
            projet={'nom': 'MonProjet'},
            formats=['dwg', 'ifc', 'obj'],
            dossier='./exports'
        )
        
        print(f"   Résultat: {resultat}")
    
    # Utiliser les hooks
    print("\n🎣 Test des hooks:")
    
    # Enregistrer un hook personnalisé
    def mon_hook(data):
        print(f"   Hook exécuté avec: {data}")
        return "Hook OK"
    
    manager.enregistrer_hook('avant_export', mon_hook, "MonModule")
    
    # Exécuter les hooks
    resultats = manager.executer_hooks('avant_export', {'test': 'data'})
    print(f"   Résultats des hooks: {resultats}")
    
    return manager


def exemple_6_cache_performance():
    """
    Exemple 6: Utilisation du cache pour optimiser les performances
    """
    print("\n" + "="*60)
    print("EXEMPLE 6: CACHE ET PERFORMANCE")
    print("="*60)
    
    from altera_enhanced import CacheManager, benchmark_performance
    
    # Créer un cache
    cache = CacheManager("./cache_exemple")
    
    # Fonction coûteuse à mettre en cache
    @benchmark_performance
    def operation_lourde(param1, param2):
        """Simule une opération coûteuse"""
        print(f"   Calcul en cours pour {param1}, {param2}...")
        time.sleep(2)  # Simulation d'un calcul long
        return f"Résultat: {param1 * param2}"
    
    # Premier appel - pas de cache
    print("\n1️⃣ Premier appel (sans cache):")
    cle = cache.generer_cle("operation", 10, 20)
    resultat = cache.obtenir(cle)
    
    if resultat is None:
        resultat = operation_lourde(10, 20)
        cache.stocker(cle, resultat)
    
    print(f"   {resultat}")
    
    # Deuxième appel - avec cache
    print("\n2️⃣ Deuxième appel (avec cache):")
    debut = time.time()
    resultat = cache.obtenir(cle)
    duree = time.time() - debut
    print(f"   {resultat}")
    print(f"   ⏱️ Récupéré du cache en {duree:.4f}s")
    
    # Statistiques du cache
    print("\n📊 Statistiques du cache:")
    print(f"   Nombre d'entrées: {len(cache.index_cache)}")
    
    # Nettoyer le cache ancien
    nombre_supprime = cache.nettoyer(age_max_jours=0)  # Supprimer tout
    print(f"   Entrées supprimées: {nombre_supprime}")
    
    return cache


def exemple_7_batch_processing():
    """
    Exemple 7: Traitement en lot de plusieurs projets
    """
    print("\n" + "="*60)
    print("EXEMPLE 7: TRAITEMENT EN LOT")
    print("="*60)
    
    altera = ALTeraEnhanced()
    
    # Liste de projets à traiter
    projets_batch = [
        {
            'nom': 'Appartement_T2_Paris',
            'client': 'M. Martin',
            'budget': 40000,
            'style': ThemeStyle.MODERNE
        },
        {
            'nom': 'Maison_Lyon',
            'client': 'Famille Dubois',
            'budget': 85000,
            'style': ThemeStyle.SCANDINAVE
        },
        {
            'nom': 'Loft_Marseille',
            'client': 'StartupTech',
            'budget': 60000,
            'style': ThemeStyle.INDUSTRIEL
        }
    ]
    
    resultats = []
    
    print(f"\n📦 Traitement de {len(projets_batch)} projets:")
    
    for i, projet_config in enumerate(projets_batch, 1):
        print(f"\n{i}. Traitement: {projet_config['nom']}")
        
        try:
            # Créer le projet
            projet = altera.creer_projet(projet_config['nom'])
            
            # Configurer
            projet.definir_client(
                nom=projet_config['client'],
                budget=projet_config['budget']
            )
            
            # Simuler le traitement
            time.sleep(0.5)
            
            # Sauvegarder
            projet.sauvegarder_projet()
            
            resultats.append({
                'nom': projet_config['nom'],
                'status': 'success',
                'id': projet.id_projet
            })
            
            print(f"   ✅ Succès")
            
        except Exception as e:
            resultats.append({
                'nom': projet_config['nom'],
                'status': 'error',
                'erreur': str(e)
            })
            print(f"   ❌ Erreur: {e}")
    
    # Rapport
    print("\n" + "="*40)
    print("RAPPORT DE TRAITEMENT EN LOT")
    print("="*40)
    
    succes = len([r for r in resultats if r['status'] == 'success'])
    erreurs = len([r for r in resultats if r['status'] == 'error'])
    
    print(f"Total traités: {len(resultats)}")
    print(f"✅ Succès: {succes}")
    print(f"❌ Erreurs: {erreurs}")
    
    return resultats


def exemple_8_automatisation_rhino():
    """
    Exemple 8: Script d'automatisation pour Rhino
    """
    print("\n" + "="*60)
    print("EXEMPLE 8: AUTOMATISATION RHINO")
    print("="*60)
    
    script_rhino = '''
# Script Python pour Rhino
# À exécuter dans l'éditeur Python de Rhino

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys

# Ajouter le chemin vers ALTera
sys.path.append(r"C:\\ALTera_Enhanced")

from altera_enhanced import ALTeraEnhanced

def creer_mobilier_rhino():
    """Crée du mobilier dans Rhino via ALTera"""
    
    # Initialiser ALTera
    altera = ALTeraEnhanced()
    projet = altera.creer_projet("Projet_Rhino")
    
    # Sélectionner une courbe de contour
    contour_id = rs.GetObject("Sélectionnez le contour de la pièce", rs.filter.curve)
    
    if contour_id:
        # Obtenir la courbe
        contour = rs.coercecurve(contour_id)
        
        # Obtenir le centre et les dimensions
        bbox = rs.BoundingBox(contour_id)
        center = rs.PointAdd(bbox[0], bbox[6])
        center = rs.PointScale(center, 0.5)
        
        # Dimensions de la pièce
        largeur = rs.Distance(bbox[0], bbox[1])
        longueur = rs.Distance(bbox[0], bbox[3])
        
        print(f"Pièce: {largeur:.0f} x {longueur:.0f} mm")
        
        # Créer du mobilier
        # Table
        table_pt = center
        table_dims = [1200, 800, 750]
        table = rs.AddBox([
            table_pt,
            rs.PointAdd(table_pt, [table_dims[0], 0, 0]),
            rs.PointAdd(table_pt, [table_dims[0], table_dims[1], 0]),
            rs.PointAdd(table_pt, [0, table_dims[1], 0]),
            rs.PointAdd(table_pt, [0, 0, table_dims[2]]),
            rs.PointAdd(table_pt, [table_dims[0], 0, table_dims[2]]),
            rs.PointAdd(table_pt, [table_dims[0], table_dims[1], table_dims[2]]),
            rs.PointAdd(table_pt, [0, table_dims[1], table_dims[2]])
        ])
        
        # Chaises autour
        chaise_dims = [450, 450, 850]
        positions = [
            [-600, 200, 0],
            [1800, 200, 0],
            [300, -300, 0],
            [300, 1100, 0]
        ]
        
        chaises = []
        for pos in positions:
            pt = rs.PointAdd(table_pt, pos)
            chaise = rs.AddBox([
                pt,
                rs.PointAdd(pt, [chaise_dims[0], 0, 0]),
                rs.PointAdd(pt, [chaise_dims[0], chaise_dims[1], 0]),
                rs.PointAdd(pt, [0, chaise_dims[1], 0]),
                rs.PointAdd(pt, [0, 0, chaise_dims[2]]),
                rs.PointAdd(pt, [chaise_dims[0], 0, chaise_dims[2]]),
                rs.PointAdd(pt, [chaise_dims[0], chaise_dims[1], chaise_dims[2]]),
                rs.PointAdd(pt, [0, chaise_dims[1], chaise_dims[2]])
            ])
            chaises.append(chaise)
        
        # Grouper
        groupe = rs.AddGroup("Mobilier_ALTera")
        rs.AddObjectsToGroup([table] + chaises, groupe)
        
        # Créer des calques
        rs.AddLayer("ALTera_Mobilier", color=(139, 90, 43))
        rs.ObjectLayer([table] + chaises, "ALTera_Mobilier")
        
        print(f"✅ Mobilier créé dans Rhino")
        
        # Mettre à jour le projet ALTera
        projet.ajouter_historique("mobilier_rhino", {
            "table": 1,
            "chaises": len(chaises)
        })
        
        return True
    
    return False

# Créer une commande Rhino
if __name__ == "__main__":
    creer_mobilier_rhino()
    '''
    
    print("📝 Script Rhino généré:")
    print("-" * 40)
    print(script_rhino[:500] + "...")  # Afficher le début
    print("-" * 40)
    print("\n💡 Copiez ce script dans l'éditeur Python de Rhino")
    
    return script_rhino


def exemple_9_interface_gui():
    """
    Exemple 9: Utilisation de l'interface graphique
    """
    print("\n" + "="*60)
    print("EXEMPLE 9: INTERFACE GRAPHIQUE")
    print("="*60)
    
    print("""
    🖥️ Pour lancer l'interface graphique:
    
    from altera_gui import ALTeraGUI
    
    # Créer et lancer l'application
    app = ALTeraGUI()
    app.run()
    
    Fonctionnalités de l'interface:
    - 🎨 Thème sombre moderne
    - 📁 Gestion des projets
    - 🎬 Génération de rendus
    - 💰 Création de devis
    - 🔌 Gestion des plugins
    - ⚙️ Configuration complète
    
    Raccourcis clavier:
    - Ctrl+N : Nouveau projet
    - Ctrl+O : Ouvrir projet
    - Ctrl+S : Sauvegarder
    - F5 : Rafraîchir
    - F1 : Aide
    """)
    
    # Note: Ne pas lancer l'interface ici car cela bloquerait
    return True


def exemple_10_rapport_personnalise():
    """
    Exemple 10: Génération de rapports personnalisés
    """
    print("\n" + "="*60)
    print("EXEMPLE 10: RAPPORTS PERSONNALISÉS")
    print("="*60)
    
    altera = ALTeraEnhanced()
    projet = altera.creer_projet("Projet_Rapport")
    
    # Configurer le projet
    projet.definir_client(
        nom="Architecture Plus",
        adresse="10 Avenue des Champs, Paris",
        budget=150000,
        deadline="2026-01-15"
    )
    
    # Ajouter des données
    pieces = ['Salon', 'Cuisine', 'Chambre 1', 'Chambre 2', 'Bureau']
    for piece in pieces:
        projet.ajouter_historique('piece_ajoutee', {'nom': piece})
    
    # Créer un rapport personnalisé
    def generer_rapport_html(projet):
        """Génère un rapport HTML personnalisé"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport - {projet.nom}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin: 30px 0;
                }}
                .info-card {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                }}
                .info-card h3 {{
                    margin-top: 0;
                    color: #ffd700;
                }}
                .timeline {{
                    margin-top: 40px;
                }}
                .timeline-item {{
                    padding: 15px;
                    margin: 10px 0;
                    background: rgba(255, 255, 255, 0.05);
                    border-left: 3px solid #ffd700;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏗️ {projet.nom}</h1>
                <p>Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>📋 Informations Projet</h3>
                        <p><strong>ID:</strong> {projet.id_projet}</p>
                        <p><strong>Créé le:</strong> {projet.date_creation.strftime('%d/%m/%Y')}</p>
                    </div>
                    
                    <div class="info-card">
                        <h3>👤 Client</h3>
                        <p><strong>Nom:</strong> {projet.metadata['client'] or 'Non défini'}</p>
                        <p><strong>Budget:</strong> {projet.metadata['budget'] or 0:,.0f} €</p>
                    </div>
                </div>
                
                <div class="timeline">
                    <h2>📅 Chronologie</h2>
        """
        
        # Ajouter les derniers événements
        for event in projet.historique[-5:]:
            date = datetime.fromisoformat(event['timestamp'])
            html += f"""
                    <div class="timeline-item">
                        <strong>{date.strftime('%d/%m %H:%M')}</strong> - {event['action']}
                    </div>
            """
        
        html += """
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    # Générer le rapport HTML
    rapport_html = generer_rapport_html(projet)
    
    # Sauvegarder
    chemin_rapport = "./rapport_projet.html"
    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        f.write(rapport_html)
    
    print(f"📄 Rapport HTML généré: {chemin_rapport}")
    print("\n✨ Aperçu du rapport:")
    print("-" * 40)
    print(f"Projet: {projet.nom}")
    print(f"Client: {projet.metadata['client']}")
    print(f"Pièces: {', '.join(pieces)}")
    print("-" * 40)
    
    return chemin_rapport


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu_principal():
    """
    Menu interactif pour tester les exemples
    """
    exemples = [
        ("Projet Simple", exemple_1_projet_simple),
        ("Configuration Personnalisée", exemple_2_configuration_personnalisee),
        ("Templates", exemple_3_templates),
        ("Workflow Complet", exemple_4_workflow_complet),
        ("Système de Plugins", exemple_5_plugins),
        ("Cache et Performance", exemple_6_cache_performance),
        ("Traitement en Lot", exemple_7_batch_processing),
        ("Automatisation Rhino", exemple_8_automatisation_rhino),
        ("Interface Graphique", exemple_9_interface_gui),
        ("Rapports Personnalisés", exemple_10_rapport_personnalise)
    ]
    
    print("\n" + "="*60)
    print("🚀 EXEMPLES ALTERA ENHANCED v3.0")
    print("="*60)
    print("\nChoisissez un exemple à exécuter:\n")
    
    for i, (nom, _) in enumerate(exemples, 1):
        print(f"{i}. {nom}")
    
    print("\n0. Quitter")
    print("-" * 60)
    
    while True:
        try:
            choix = input("\nVotre choix (0-10): ")
            choix = int(choix)
            
            if choix == 0:
                print("\n👋 Au revoir!")
                break
            elif 1 <= choix <= 10:
                print("\n" + "="*60)
                # Exécuter l'exemple
                exemples[choix-1][1]()
                
                input("\n✅ Appuyez sur Entrée pour continuer...")
                print("\n" + "="*60)
                
                # Afficher à nouveau le menu
                print("\n🚀 EXEMPLES ALTERA ENHANCED v3.0")
                print("="*60)
                print("\nChoisissez un autre exemple:\n")
                
                for i, (nom, _) in enumerate(exemples, 1):
                    print(f"{i}. {nom}")
                
                print("\n0. Quitter")
                print("-" * 60)
            else:
                print("❌ Choix invalide. Veuillez choisir entre 0 et 10.")
        
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    # Mode interactif ou exécution directe
    import sys
    
    if len(sys.argv) > 1:
        # Exécuter un exemple spécifique
        exemple_num = int(sys.argv[1])
        exemples = [
            exemple_1_projet_simple,
            exemple_2_configuration_personnalisee,
            exemple_3_templates,
            exemple_4_workflow_complet,
            exemple_5_plugins,
            exemple_6_cache_performance,
            exemple_7_batch_processing,
            exemple_8_automatisation_rhino,
            exemple_9_interface_gui,
            exemple_10_rapport_personnalise
        ]
        
        if 1 <= exemple_num <= len(exemples):
            exemples[exemple_num - 1]()
        else:
            print(f"Exemple {exemple_num} n'existe pas")
    else:
        # Menu interactif
        menu_principal()
