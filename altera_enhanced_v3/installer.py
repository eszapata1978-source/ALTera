#!/usr/bin/env python3
"""
ALTERA ENHANCED - SCRIPT D'INSTALLATION
========================================

Script automatique pour installer et configurer ALTera Enhanced.

Version: 3.0 ENHANCED
"""

import os
import sys
import shutil
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime


class ALTeraInstaller:
    """Installateur pour ALTera Enhanced"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.python_version = sys.version_info
        self.rhino_paths = self._detect_rhino_paths()
        self.install_path = None
        self.errors = []
        self.warnings = []
        
        # Configuration par défaut
        self.config = {
            'version': '3.0',
            'install_date': datetime.now().isoformat(),
            'os': self.os_type,
            'python': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
        }
    
    def _detect_rhino_paths(self):
        """Détecte les chemins d'installation de Rhino"""
        paths = []
        
        if self.os_type == "Windows":
            # Chemins Windows typiques
            possible_paths = [
                r"C:\Program Files\Rhino 8",
                r"C:\Program Files\Rhino 7",
                r"C:\Program Files\Rhino 6",
                r"C:\Program Files\McNeel\Rhino 8",
                r"C:\Program Files\McNeel\Rhino 7",
                Path.home() / "AppData/Roaming/McNeel/Rhinoceros/8.0/scripts",
                Path.home() / "AppData/Roaming/McNeel/Rhinoceros/7.0/scripts"
            ]
        elif self.os_type == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Rhino 8.app",
                "/Applications/Rhino 7.app",
                "/Applications/Rhinoceros.app",
                Path.home() / "Library/Application Support/McNeel/Rhinoceros/8.0/scripts",
                Path.home() / "Library/Application Support/McNeel/Rhinoceros/7.0/scripts"
            ]
        else:  # Linux
            possible_paths = [
                Path.home() / ".config/McNeel/Rhinoceros/8.0/scripts",
                Path.home() / ".config/McNeel/Rhinoceros/7.0/scripts",
                "/opt/rhino",
                "/usr/local/rhino"
            ]
        
        # Vérifier les chemins existants
        for path in possible_paths:
            path = Path(path)
            if path.exists():
                paths.append(str(path))
        
        return paths
    
    def afficher_banniere(self):
        """Affiche la bannière de bienvenue"""
        print("\n" + "="*70)
        print("""
        ╔══════════════════════════════════════════════════════╗
        ║       ALTera ENHANCED v3.0 - INSTALLATION           ║
        ║   Système de Conception Architecturale Nouvelle     ║
        ║                    Génération                       ║
        ╚══════════════════════════════════════════════════════╝
        """)
        print("="*70)
        print(f"\n📍 Système détecté: {self.os_type}")
        print(f"🐍 Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("\n" + "="*70 + "\n")
    
    def verifier_prerequisites(self):
        """Vérifie les prérequis système"""
        print("🔍 VÉRIFICATION DES PRÉREQUIS")
        print("-" * 40)
        
        succes = True
        
        # 1. Vérifier Python
        print("✓ Python:", end=" ")
        if self.python_version.major >= 3 and self.python_version.minor >= 8:
            print(f"OK (v{self.python_version.major}.{self.python_version.minor})")
        else:
            print(f"❌ Version {self.python_version.major}.{self.python_version.minor} trop ancienne (3.8+ requis)")
            self.errors.append("Python 3.8+ requis")
            succes = False
        
        # 2. Vérifier Rhino
        print("✓ Rhino:", end=" ")
        if self.rhino_paths:
            print(f"OK ({len(self.rhino_paths)} installation(s) trouvée(s))")
            for path in self.rhino_paths[:3]:  # Afficher max 3 chemins
                print(f"  → {path}")
        else:
            print("⚠️ Rhino non détecté (installation manuelle possible)")
            self.warnings.append("Rhino non détecté automatiquement")
        
        # 3. Vérifier tkinter
        print("✓ tkinter:", end=" ")
        try:
            import tkinter
            print("OK")
        except ImportError:
            print("⚠️ Non installé (interface graphique non disponible)")
            self.warnings.append("tkinter non disponible")
        
        # 4. Vérifier l'espace disque
        print("✓ Espace disque:", end=" ")
        stats = shutil.disk_usage(".")
        free_gb = stats.free / (1024**3)
        if free_gb > 0.5:  # 500 MB minimum
            print(f"OK ({free_gb:.1f} GB disponibles)")
        else:
            print(f"⚠️ Espace limité ({free_gb:.1f} GB)")
            self.warnings.append("Espace disque limité")
        
        print("\n" + "-" * 40)
        
        if self.errors:
            print("❌ ERREURS DÉTECTÉES:")
            for err in self.errors:
                print(f"  • {err}")
            return False
        
        if self.warnings:
            print("⚠️ AVERTISSEMENTS:")
            for warn in self.warnings:
                print(f"  • {warn}")
        
        return succes
    
    def choisir_dossier_installation(self):
        """Permet à l'utilisateur de choisir le dossier d'installation"""
        print("\n📁 CHOIX DU DOSSIER D'INSTALLATION")
        print("-" * 40)
        
        # Proposer des options
        options = []
        
        # Option 1: Dossier Documents
        docs_path = Path.home() / "Documents" / "ALTera_Enhanced"
        options.append(("Documents (Recommandé)", docs_path))
        
        # Option 2: Bureau
        desktop_path = Path.home() / "Desktop" / "ALTera_Enhanced"
        options.append(("Bureau", desktop_path))
        
        # Option 3: Dossier Rhino si trouvé
        if self.rhino_paths:
            rhino_path = Path(self.rhino_paths[0]) / "ALTera_Enhanced"
            options.append(("Dossier Rhino", rhino_path))
        
        # Option 4: Personnalisé
        options.append(("Personnalisé", None))
        
        print("\nChoisissez l'emplacement d'installation:\n")
        for i, (nom, path) in enumerate(options, 1):
            if path:
                print(f"{i}. {nom}")
                print(f"   → {path}")
            else:
                print(f"{i}. {nom}")
        
        while True:
            try:
                choix = input(f"\nVotre choix (1-{len(options)}): ")
                choix = int(choix) - 1
                
                if 0 <= choix < len(options):
                    if options[choix][1]:
                        self.install_path = options[choix][1]
                    else:
                        # Choix personnalisé
                        chemin = input("Entrez le chemin complet: ")
                        self.install_path = Path(chemin) / "ALTera_Enhanced"
                    break
                else:
                    print("❌ Choix invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
        
        print(f"\n✅ Installation dans: {self.install_path}")
        return self.install_path
    
    def creer_structure_dossiers(self):
        """Crée la structure de dossiers"""
        print("\n📂 CRÉATION DE LA STRUCTURE")
        print("-" * 40)
        
        dossiers = [
            "",  # Racine
            "core",
            "modules",
            "plugins",
            "templates",
            "cache",
            "config",
            "docs",
            "exemples",
            "projets",
            "exports",
            "ressources",
            "logs"
        ]
        
        for dossier in dossiers:
            chemin = self.install_path / dossier
            chemin.mkdir(parents=True, exist_ok=True)
            print(f"✓ Créé: {dossier if dossier else 'Racine'}")
        
        print(f"\n✅ Structure créée dans {self.install_path}")
    
    def copier_fichiers(self):
        """Copie les fichiers du système"""
        print("\n📋 COPIE DES FICHIERS")
        print("-" * 40)
        
        # Liste des fichiers à copier
        fichiers_core = [
            ("altera_enhanced.py", "core/altera_enhanced.py"),
            ("altera_plugins.py", "core/altera_plugins.py"),
            ("altera_gui.py", "core/altera_gui.py"),
            ("exemples_pratiques.py", "exemples/exemples_pratiques.py"),
            ("README_ENHANCED.md", "docs/README.md")
        ]
        
        # Copier les fichiers
        for source, dest in fichiers_core:
            source_path = Path(source)
            dest_path = self.install_path / dest
            
            if source_path.exists():
                shutil.copy2(source_path, dest_path)
                print(f"✓ Copié: {dest}")
            else:
                # Créer un fichier placeholder si le source n'existe pas
                dest_path.write_text(f"# {source}\n# Fichier à ajouter\n")
                print(f"⚠️ Créé placeholder: {dest}")
        
        # Créer le fichier __init__.py
        init_file = self.install_path / "core" / "__init__.py"
        init_file.write_text("""
# ALTera Enhanced - Core Module
from .altera_enhanced import ALTeraEnhanced, ConfigurationPersonnelle, ProjetALTera
from .altera_plugins import PluginManager, PluginInterface
from .altera_gui import ALTeraGUI

__version__ = '3.0'
__all__ = ['ALTeraEnhanced', 'ConfigurationPersonnelle', 'ProjetALTera', 
           'PluginManager', 'PluginInterface', 'ALTeraGUI']
""")
        print("✓ Créé: core/__init__.py")
    
    def creer_templates_defaut(self):
        """Crée les templates par défaut"""
        print("\n🎨 CRÉATION DES TEMPLATES")
        print("-" * 40)
        
        templates = {
            "chambre_moderne": {
                "nom": "Chambre Moderne",
                "description": "Chambre contemporaine minimaliste",
                "type_piece": "chambre",
                "style": "moderne",
                "dimensions_standards": {"longueur": 4000, "largeur": 3500, "hauteur": 2500},
                "mobilier_type": ["lit_double", "tables_nuit", "armoire", "bureau"],
                "palette_couleurs": [[255, 255, 255], [200, 200, 200], [50, 50, 50]],
                "materiaux_preferes": ["panneau_18", "chene_massif"]
            },
            "salon_scandinave": {
                "nom": "Salon Scandinave",
                "description": "Salon épuré style nordique",
                "type_piece": "salon",
                "style": "scandinave",
                "dimensions_standards": {"longueur": 5000, "largeur": 4000, "hauteur": 2500},
                "mobilier_type": ["canape", "table_basse", "etageres", "fauteuil"],
                "palette_couleurs": [[245, 245, 240], [180, 180, 170], [120, 140, 120]],
                "materiaux_preferes": ["bois_clair", "tissu_naturel"]
            }
        }
        
        templates_dir = self.install_path / "templates"
        for nom, template in templates.items():
            fichier = templates_dir / f"{nom}.json"
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4)
            print(f"✓ Template créé: {nom}")
    
    def creer_plugins_exemple(self):
        """Crée des plugins d'exemple"""
        print("\n🔌 CRÉATION DES PLUGINS D'EXEMPLE")
        print("-" * 40)
        
        plugin_exemple = '''"""
Plugin Exemple pour ALTera Enhanced
"""

from core.altera_plugins import PluginInterface

class PluginExemple(PluginInterface):
    def __init__(self):
        super().__init__()
        self.nom = "PluginExemple"
        self.version = "1.0.0"
        self.description = "Plugin d'exemple"
        self.auteur = "ALTera Team"
    
    def initialiser(self, contexte):
        self.contexte = contexte
        return True
    
    def executer(self, action, **kwargs):
        if action == "test":
            return "Plugin exemple fonctionnel!"
        return None

PluginClass = PluginExemple
'''
        
        plugin_file = self.install_path / "plugins" / "plugin_exemple.py"
        plugin_file.write_text(plugin_exemple)
        print("✓ Plugin exemple créé")
    
    def configurer_rhino(self):
        """Configure Rhino pour utiliser ALTera"""
        print("\n🦏 CONFIGURATION POUR RHINO")
        print("-" * 40)
        
        if not self.rhino_paths:
            print("⚠️ Rhino non détecté - Configuration manuelle nécessaire")
            print("\nPour configurer manuellement:")
            print(f"1. Ouvrez Rhino")
            print(f"2. Ouvrez l'éditeur Python (EditPythonScript)")
            print(f"3. Ajoutez ce code au début de vos scripts:\n")
            print(f"import sys")
            print(f"sys.path.append(r'{self.install_path / 'core'}')")
            print(f"from altera_enhanced import ALTeraEnhanced")
            return
        
        # Créer un script d'initialisation pour Rhino
        rhino_init = f'''"""
Script d'initialisation ALTera pour Rhino
Généré automatiquement le {datetime.now().strftime('%d/%m/%Y')}
"""

import sys
import os

# Ajouter ALTera au chemin Python
altera_path = r"{self.install_path / 'core'}"
if altera_path not in sys.path:
    sys.path.append(altera_path)

# Importer ALTera
try:
    from altera_enhanced import ALTeraEnhanced
    print("✓ ALTera Enhanced v3.0 chargé avec succès")
except ImportError as e:
    print(f"❌ Erreur lors du chargement d'ALTera: {{e}}")

# Fonction d'initialisation
def init_altera():
    """Initialise ALTera dans Rhino"""
    global altera
    altera = ALTeraEnhanced()
    return altera

# Message de bienvenue
print("="*50)
print("ALTera Enhanced v3.0 - Prêt à l'emploi")
print("="*50)
print("Utilisez init_altera() pour commencer")
'''
        
        # Sauvegarder dans le dossier Rhino
        for rhino_path in self.rhino_paths[:1]:  # Premier chemin trouvé
            script_path = Path(rhino_path) / "altera_init.py"
            try:
                script_path.parent.mkdir(parents=True, exist_ok=True)
                script_path.write_text(rhino_init)
                print(f"✓ Script Rhino créé: {script_path}")
                
                # Créer aussi un alias
                alias_path = Path(rhino_path) / "altera_commands.txt"
                alias_content = f"""# Commandes ALTera pour Rhino
# Ajoutez ces alias dans Rhino (Options > Alias)

ALTera_Init
_-RunPythonScript "{script_path}"

ALTera_NewProject
_-RunPythonScript "
import sys
sys.path.append(r'{self.install_path / 'core'}')
from altera_enhanced import ALTeraEnhanced
altera = ALTeraEnhanced()
nom = rs.GetString('Nom du projet:')
if nom: projet = altera.creer_projet(nom)
"
"""
                alias_path.write_text(alias_content)
                print(f"✓ Fichier d'alias créé: {alias_path}")
                
            except Exception as e:
                print(f"⚠️ Impossible d'écrire dans {rhino_path}: {e}")
    
    def creer_raccourcis(self):
        """Crée des raccourcis bureau"""
        print("\n🔗 CRÉATION DES RACCOURCIS")
        print("-" * 40)
        
        if self.os_type == "Windows":
            # Créer un fichier .bat pour Windows
            bat_content = f'''@echo off
echo ========================================
echo     ALTera Enhanced v3.0
echo ========================================
echo.
cd /d "{self.install_path}"
python -c "from core.altera_gui import ALTeraGUI; app = ALTeraGUI(); app.run()"
pause
'''
            
            desktop = Path.home() / "Desktop"
            bat_file = desktop / "ALTera_Enhanced.bat"
            bat_file.write_text(bat_content)
            print(f"✓ Raccourci Windows créé sur le bureau")
            
        elif self.os_type == "Darwin":  # macOS
            # Créer un script shell pour macOS
            sh_content = f'''#!/bin/bash
echo "========================================"
echo "     ALTera Enhanced v3.0"
echo "========================================"
cd "{self.install_path}"
python3 -c "from core.altera_gui import ALTeraGUI; app = ALTeraGUI(); app.run()"
'''
            
            desktop = Path.home() / "Desktop"
            sh_file = desktop / "ALTera_Enhanced.command"
            sh_file.write_text(sh_content)
            sh_file.chmod(0o755)  # Rendre exécutable
            print(f"✓ Raccourci macOS créé sur le bureau")
            
        else:  # Linux
            # Créer un fichier .desktop pour Linux
            desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=ALTera Enhanced
Comment=Système de Conception Architecturale
Exec=python3 -c "from core.altera_gui import ALTeraGUI; app = ALTeraGUI(); app.run()"
Path={self.install_path}
Icon=applications-engineering
Terminal=false
Categories=Graphics;Engineering;
'''
            
            desktop = Path.home() / "Desktop"
            desktop_file = desktop / "altera-enhanced.desktop"
            desktop_file.write_text(desktop_content)
            desktop_file.chmod(0o755)
            print(f"✓ Raccourci Linux créé sur le bureau")
    
    def installer_dependances(self):
        """Installe les dépendances Python"""
        print("\n📦 INSTALLATION DES DÉPENDANCES")
        print("-" * 40)
        
        # Créer requirements.txt
        requirements = """# ALTera Enhanced - Dépendances
# Core
typing-extensions>=4.0.0

# Interface (optionnel)
# tkinter est généralement inclus avec Python

# Traitement d'images (optionnel)
# pillow>=9.0.0

# Calculs avancés (optionnel)
# numpy>=1.20.0

# Export PDF (optionnel)
# reportlab>=3.6.0
"""
        
        req_file = self.install_path / "requirements.txt"
        req_file.write_text(requirements)
        print("✓ Fichier requirements.txt créé")
        
        # Proposer l'installation
        reponse = input("\nVoulez-vous installer les dépendances maintenant? (o/n): ")
        if reponse.lower() == 'o':
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", 
                              "-r", str(req_file)], check=True)
                print("✓ Dépendances installées")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Erreur lors de l'installation: {e}")
                print("Vous pouvez installer manuellement avec:")
                print(f"pip install -r {req_file}")
    
    def creer_documentation(self):
        """Crée la documentation de démarrage rapide"""
        print("\n📚 CRÉATION DE LA DOCUMENTATION")
        print("-" * 40)
        
        quickstart = f"""# ALTera Enhanced v3.0 - Démarrage Rapide

## Installation effectuée avec succès! 🎉

**Date d'installation:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Dossier d'installation:** {self.install_path}

## Comment démarrer

### 1. Interface Graphique

Double-cliquez sur le raccourci sur votre bureau ou exécutez:
```python
from core.altera_gui import ALTeraGUI
app = ALTeraGUI()
app.run()
```

### 2. Dans Rhino

Ouvrez Rhino et dans l'éditeur Python:
```python
import sys
sys.path.append(r'{self.install_path / 'core'}')
from altera_enhanced import ALTeraEnhanced

altera = ALTeraEnhanced()
projet = altera.creer_projet("Mon_Projet")
```

### 3. En ligne de commande

```bash
cd {self.install_path}
python exemples/exemples_pratiques.py
```

## Structure des dossiers

- **core/** : Modules principaux
- **plugins/** : Extensions
- **templates/** : Modèles prédéfinis
- **projets/** : Vos projets
- **docs/** : Documentation complète

## Support

- Documentation complète: docs/README.md
- Exemples: exemples/exemples_pratiques.py
- Site web: https://altera.enhanced.com
- Support: support@altera.com

## Prochaines étapes

1. Lancez l'interface graphique
2. Créez votre premier projet
3. Explorez les exemples
4. Consultez la documentation

Bon design avec ALTera Enhanced! 🏗️
"""
        
        doc_file = self.install_path / "DEMARRAGE_RAPIDE.md"
        doc_file.write_text(quickstart)
        print("✓ Documentation de démarrage créée")
    
    def afficher_resume(self):
        """Affiche le résumé de l'installation"""
        print("\n" + "="*70)
        print("✅ INSTALLATION TERMINÉE AVEC SUCCÈS!")
        print("="*70)
        
        print(f"""
📍 Résumé de l'installation:
   • Dossier: {self.install_path}
   • Espace utilisé: ~10 MB
   • Templates créés: 2
   • Plugins installés: 1
   
🚀 Pour commencer:
   1. Double-cliquez sur le raccourci du bureau
   2. Ou ouvrez Rhino et chargez altera_init.py
   3. Ou exécutez: python {self.install_path}/exemples/exemples_pratiques.py

📚 Documentation:
   • Guide de démarrage: {self.install_path}/DEMARRAGE_RAPIDE.md
   • Documentation complète: {self.install_path}/docs/README.md
   • Exemples: {self.install_path}/exemples/

💡 Conseils:
   • Commencez par les exemples pratiques
   • Explorez les templates disponibles
   • Personnalisez votre configuration
   
🆘 Support:
   • Forum: https://forum.altera.com
   • Discord: https://discord.gg/altera
   • Email: support@altera.com
""")
        
        if self.warnings:
            print("⚠️ Avertissements à noter:")
            for warn in self.warnings:
                print(f"   • {warn}")
        
        print("\n" + "="*70)
        print("Merci d'avoir choisi ALTera Enhanced!")
        print("="*70 + "\n")
    
    def installer(self):
        """Lance le processus d'installation complet"""
        try:
            # 1. Bannière
            self.afficher_banniere()
            
            # 2. Vérifier les prérequis
            if not self.verifier_prerequisites():
                if self.errors:
                    print("\n❌ Installation annulée - Prérequis manquants")
                    return False
            
            # 3. Choisir le dossier
            self.choisir_dossier_installation()
            
            # 4. Confirmation
            print(f"\n📋 Récapitulatif:")
            print(f"   • Installation dans: {self.install_path}")
            print(f"   • Espace requis: ~10 MB")
            
            reponse = input("\nProcéder à l'installation? (o/n): ")
            if reponse.lower() != 'o':
                print("Installation annulée.")
                return False
            
            # 5. Installation
            print("\n🚀 INSTALLATION EN COURS...")
            print("="*40)
            
            self.creer_structure_dossiers()
            self.copier_fichiers()
            self.creer_templates_defaut()
            self.creer_plugins_exemple()
            self.configurer_rhino()
            self.creer_raccourcis()
            self.installer_dependances()
            self.creer_documentation()
            
            # 6. Résumé
            self.afficher_resume()
            
            # 7. Sauvegarder la configuration d'installation
            config_file = self.install_path / "config" / "install.json"
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Installation interrompue par l'utilisateur")
            return False
        except Exception as e:
            print(f"\n❌ Erreur lors de l'installation: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Point d'entrée principal"""
    installer = ALTeraInstaller()
    
    try:
        succes = installer.installer()
        
        if succes:
            # Proposer de lancer l'interface
            print("\n" + "="*70)
            reponse = input("Voulez-vous lancer ALTera Enhanced maintenant? (o/n): ")
            if reponse.lower() == 'o':
                try:
                    sys.path.append(str(installer.install_path / "core"))
                    from altera_gui import ALTeraGUI
                    print("\n🚀 Lancement de l'interface...")
                    app = ALTeraGUI()
                    app.run()
                except ImportError as e:
                    print(f"⚠️ Impossible de lancer l'interface: {e}")
                    print("Essayez de lancer depuis le raccourci bureau")
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
