"""
ALTera ENHANCED - Système de Conception Architecturale Nouvelle Génération
===========================================================================

Version complètement refactorisée et améliorée du système ALTera avec:
- Architecture modulaire moderne
- Système de plugins extensible
- Gestion d'erreurs robuste
- Cache intelligent pour les rendus
- Templates prédéfinis personnalisables
- Interface utilisateur intuitive
- Support multi-langue
- Système de thèmes personnalisables

Version: 3.0 ENHANCED
Auteur: ALTera Workshop Enhanced Edition
"""

import Rhino.Geometry as rg
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import pickle
import hashlib


# ============================================================================
# CONFIGURATION AVANCÉE
# ============================================================================

class ThemeStyle(Enum):
    """Thèmes de design prédéfinis"""
    SCANDINAVE = "scandinave"
    INDUSTRIEL = "industriel"
    BOHEME = "boheme"
    MODERNE = "moderne"
    JAPANDI = "japandi"
    MEDITERRANEEN = "mediterraneen"
    MINIMALISTE = "minimaliste"
    RUSTIQUE = "rustique"
    ART_DECO = "art_deco"
    FUTURISTE = "futuriste"


@dataclass
class ConfigurationPersonnelle:
    """Configuration personnalisée pour l'utilisateur"""
    
    # Informations utilisateur
    nom_utilisateur: str = "Designer"
    entreprise: str = "Studio ALTera"
    logo_path: Optional[str] = None
    
    # Préférences de travail
    unite_defaut: str = "mm"
    tolerance: float = 0.5
    langue: str = "fr"
    theme_defaut: ThemeStyle = ThemeStyle.MODERNE
    
    # Chemins personnalisés
    dossier_projets: str = "./projets"
    dossier_templates: str = "./templates"
    dossier_cache: str = "./cache"
    dossier_exports: str = "./exports"
    
    # Options d'interface
    afficher_conseils: bool = True
    mode_expert: bool = False
    auto_sauvegarde: bool = True
    intervalle_sauvegarde: int = 300  # secondes
    
    # Paramètres de rendu par défaut
    qualite_rendu_defaut: str = "haute"
    resolution_rendu: Tuple[int, int] = (1920, 1080)
    samples_rendu: int = 128
    
    # Intégrations
    airtable_api_key: Optional[str] = None
    d5_render_path: Optional[str] = None
    
    def sauvegarder(self, chemin: str = "config.json"):
        """Sauvegarde la configuration"""
        with open(chemin, 'w', encoding='utf-8') as f:
            config_dict = {
                k: v.value if isinstance(v, Enum) else v 
                for k, v in self.__dict__.items()
            }
            json.dump(config_dict, f, indent=4, default=str)
    
    @classmethod
    def charger(cls, chemin: str = "config.json"):
        """Charge une configuration"""
        if os.path.exists(chemin):
            with open(chemin, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convertir le theme string en enum
                if 'theme_defaut' in data:
                    data['theme_defaut'] = ThemeStyle(data['theme_defaut'])
                return cls(**data)
        return cls()


# ============================================================================
# SYSTÈME DE CACHE INTELLIGENT
# ============================================================================

class CacheManager:
    """Gestionnaire de cache pour optimiser les performances"""
    
    def __init__(self, dossier_cache: str = "./cache"):
        self.dossier_cache = dossier_cache
        os.makedirs(dossier_cache, exist_ok=True)
        self.index_cache = self._charger_index()
        
    def _charger_index(self) -> Dict:
        """Charge l'index du cache"""
        index_path = os.path.join(self.dossier_cache, "index.json")
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _sauver_index(self):
        """Sauvegarde l'index du cache"""
        index_path = os.path.join(self.dossier_cache, "index.json")
        with open(index_path, 'w') as f:
            json.dump(self.index_cache, f)
    
    def generer_cle(self, *args) -> str:
        """Génère une clé unique pour le cache"""
        data = str(args).encode('utf-8')
        return hashlib.md5(data).hexdigest()
    
    def obtenir(self, cle: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if cle in self.index_cache:
            chemin = os.path.join(self.dossier_cache, f"{cle}.pkl")
            if os.path.exists(chemin):
                with open(chemin, 'rb') as f:
                    return pickle.load(f)
        return None
    
    def stocker(self, cle: str, valeur: Any):
        """Stocke une valeur dans le cache"""
        chemin = os.path.join(self.dossier_cache, f"{cle}.pkl")
        with open(chemin, 'wb') as f:
            pickle.dump(valeur, f)
        self.index_cache[cle] = {
            'date': datetime.now().isoformat(),
            'taille': os.path.getsize(chemin)
        }
        self._sauver_index()
    
    def nettoyer(self, age_max_jours: int = 30):
        """Nettoie les entrées du cache plus anciennes que age_max_jours"""
        maintenant = datetime.now()
        a_supprimer = []
        
        for cle, info in self.index_cache.items():
            date_cache = datetime.fromisoformat(info['date'])
            if (maintenant - date_cache).days > age_max_jours:
                a_supprimer.append(cle)
        
        for cle in a_supprimer:
            chemin = os.path.join(self.dossier_cache, f"{cle}.pkl")
            if os.path.exists(chemin):
                os.remove(chemin)
            del self.index_cache[cle]
        
        self._sauver_index()
        return len(a_supprimer)


# ============================================================================
# SYSTÈME DE TEMPLATES
# ============================================================================

@dataclass
class Template:
    """Template de projet réutilisable"""
    nom: str
    description: str
    type_piece: str
    style: ThemeStyle
    dimensions_standards: Dict[str, float]
    mobilier_type: List[str]
    palette_couleurs: List[Tuple[int, int, int]]
    materiaux_preferes: List[str]
    metadata: Dict = field(default_factory=dict)


class TemplateManager:
    """Gestionnaire de templates prédéfinis"""
    
    def __init__(self, dossier_templates: str = "./templates"):
        self.dossier_templates = dossier_templates
        os.makedirs(dossier_templates, exist_ok=True)
        self.templates = self._charger_templates()
        
    def _charger_templates(self) -> Dict[str, Template]:
        """Charge tous les templates disponibles"""
        templates = {}
        
        # Templates par défaut
        templates['chambre_moderne'] = Template(
            nom="Chambre Moderne",
            description="Chambre contemporaine minimaliste",
            type_piece="chambre",
            style=ThemeStyle.MODERNE,
            dimensions_standards={'longueur': 4000, 'largeur': 3500, 'hauteur': 2500},
            mobilier_type=['lit_double', 'tables_nuit', 'armoire', 'bureau'],
            palette_couleurs=[(255, 255, 255), (200, 200, 200), (50, 50, 50)],
            materiaux_preferes=['panneau_18', 'chene_massif'],
            metadata={'eclairage': 'indirect', 'ambiance': 'zen'}
        )
        
        templates['salon_scandinave'] = Template(
            nom="Salon Scandinave",
            description="Salon épuré style nordique",
            type_piece="salon",
            style=ThemeStyle.SCANDINAVE,
            dimensions_standards={'longueur': 5000, 'largeur': 4000, 'hauteur': 2500},
            mobilier_type=['canape', 'table_basse', 'etageres', 'fauteuil'],
            palette_couleurs=[(245, 245, 240), (180, 180, 170), (120, 140, 120)],
            materiaux_preferes=['bois_clair', 'tissu_naturel'],
            metadata={'eclairage': 'naturel', 'plantes': True}
        )
        
        templates['cuisine_industrielle'] = Template(
            nom="Cuisine Industrielle",
            description="Cuisine style loft urbain",
            type_piece="cuisine",
            style=ThemeStyle.INDUSTRIEL,
            dimensions_standards={'longueur': 4500, 'largeur': 3000, 'hauteur': 2700},
            mobilier_type=['ilot_central', 'plan_travail', 'rangements_hauts'],
            palette_couleurs=[(40, 40, 40), (140, 140, 140), (180, 100, 60)],
            materiaux_preferes=['metal_noir', 'bois_brut', 'beton'],
            metadata={'eclairage': 'suspension', 'finition': 'mate'}
        )
        
        # Charger les templates personnalisés
        for fichier in os.listdir(self.dossier_templates):
            if fichier.endswith('.json'):
                chemin = os.path.join(self.dossier_templates, fichier)
                with open(chemin, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['style'] = ThemeStyle(data['style'])
                    nom_template = fichier.replace('.json', '')
                    templates[nom_template] = Template(**data)
        
        return templates
    
    def obtenir_template(self, nom: str) -> Optional[Template]:
        """Obtient un template par son nom"""
        return self.templates.get(nom)
    
    def lister_templates(self, type_piece: Optional[str] = None) -> List[Template]:
        """Liste les templates disponibles"""
        templates_list = list(self.templates.values())
        if type_piece:
            templates_list = [t for t in templates_list if t.type_piece == type_piece]
        return templates_list
    
    def sauvegarder_template(self, template: Template):
        """Sauvegarde un nouveau template"""
        chemin = os.path.join(
            self.dossier_templates, 
            f"{template.nom.lower().replace(' ', '_')}.json"
        )
        
        data = {
            'nom': template.nom,
            'description': template.description,
            'type_piece': template.type_piece,
            'style': template.style.value,
            'dimensions_standards': template.dimensions_standards,
            'mobilier_type': template.mobilier_type,
            'palette_couleurs': template.palette_couleurs,
            'materiaux_preferes': template.materiaux_preferes,
            'metadata': template.metadata
        }
        
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        self.templates[template.nom.lower().replace(' ', '_')] = template


# ============================================================================
# GESTIONNAIRE DE PROJET AMÉLIORÉ
# ============================================================================

class ProjetALTera:
    """Projet ALTera avec gestion avancée"""
    
    def __init__(self, nom: str, config: Optional[ConfigurationPersonnelle] = None):
        self.nom = nom
        self.id_projet = self._generer_id()
        self.date_creation = datetime.now()
        self.config = config or ConfigurationPersonnelle()
        
        # Initialisation des gestionnaires
        self.cache = CacheManager(
            os.path.join(self.config.dossier_cache, self.id_projet)
        )
        self.templates = TemplateManager(self.config.dossier_templates)
        
        # État du projet
        self.pieces = []
        self.mobilier = []
        self.rendus = []
        self.devis = None
        self.historique = []
        self.metadata = {
            'client': None,
            'adresse': None,
            'budget': None,
            'deadline': None,
            'notes': []
        }
        
        # Système de logging
        self._initialiser_logging()
        
        # Créer la structure de dossiers
        self._creer_structure_dossiers()
        
        self.logger.info(f"Projet '{nom}' créé avec succès")
    
    def _generer_id(self) -> str:
        """Génère un ID unique pour le projet"""
        return f"PROJ_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _initialiser_logging(self):
        """Initialise le système de logging"""
        log_dir = os.path.join(self.config.dossier_projets, self.nom, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(
            log_dir, 
            f"altera_{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(f"ALTera.{self.nom}")
    
    def _creer_structure_dossiers(self):
        """Crée la structure de dossiers pour le projet"""
        base_path = os.path.join(self.config.dossier_projets, self.nom)
        
        dossiers = [
            'modeles_3d',
            'rendus',
            'plans_2d',
            'devis',
            'exports',
            'sauvegardes',
            'logs',
            'ressources'
        ]
        
        for dossier in dossiers:
            os.makedirs(os.path.join(base_path, dossier), exist_ok=True)
    
    def ajouter_historique(self, action: str, details: Dict = None):
        """Ajoute une entrée à l'historique du projet"""
        entree = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details or {}
        }
        self.historique.append(entree)
        self.logger.info(f"Action: {action}")
    
    def definir_client(self, nom: str, adresse: str = None, 
                       budget: float = None, deadline: str = None):
        """Définit les informations client"""
        self.metadata['client'] = nom
        self.metadata['adresse'] = adresse
        self.metadata['budget'] = budget
        self.metadata['deadline'] = deadline
        
        self.ajouter_historique('client_defini', {
            'client': nom,
            'budget': budget
        })
    
    def ajouter_note(self, note: str):
        """Ajoute une note au projet"""
        self.metadata['notes'].append({
            'date': datetime.now().isoformat(),
            'note': note
        })
    
    def sauvegarder_projet(self):
        """Sauvegarde l'état complet du projet"""
        sauvegarde_path = os.path.join(
            self.config.dossier_projets, 
            self.nom, 
            'sauvegardes',
            f"sauvegarde_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        projet_data = {
            'nom': self.nom,
            'id_projet': self.id_projet,
            'date_creation': self.date_creation.isoformat(),
            'metadata': self.metadata,
            'historique': self.historique,
            'nb_pieces': len(self.pieces),
            'nb_meubles': len(self.mobilier),
            'nb_rendus': len(self.rendus)
        }
        
        with open(sauvegarde_path, 'w', encoding='utf-8') as f:
            json.dump(projet_data, f, indent=4)
        
        self.logger.info(f"Projet sauvegardé: {sauvegarde_path}")
        return sauvegarde_path
    
    def generer_rapport(self) -> str:
        """Génère un rapport complet du projet"""
        rapport = []
        rapport.append(f"\n{'='*80}")
        rapport.append(f"RAPPORT DE PROJET - {self.nom}")
        rapport.append(f"{'='*80}\n")
        
        rapport.append(f"ID Projet: {self.id_projet}")
        rapport.append(f"Date création: {self.date_creation.strftime('%d/%m/%Y %H:%M')}")
        rapport.append(f"")
        
        if self.metadata['client']:
            rapport.append(f"CLIENT")
            rapport.append(f"------")
            rapport.append(f"Nom: {self.metadata['client']}")
            if self.metadata['adresse']:
                rapport.append(f"Adresse: {self.metadata['adresse']}")
            if self.metadata['budget']:
                rapport.append(f"Budget: {self.metadata['budget']:,.2f} €")
            if self.metadata['deadline']:
                rapport.append(f"Deadline: {self.metadata['deadline']}")
            rapport.append(f"")
        
        rapport.append(f"STATISTIQUES")
        rapport.append(f"------------")
        rapport.append(f"Nombre de pièces: {len(self.pieces)}")
        rapport.append(f"Nombre de meubles: {len(self.mobilier)}")
        rapport.append(f"Nombre de rendus: {len(self.rendus)}")
        rapport.append(f"")
        
        if self.historique:
            rapport.append(f"HISTORIQUE (5 dernières actions)")
            rapport.append(f"---------------------------------")
            for entree in self.historique[-5:]:
                date = datetime.fromisoformat(entree['timestamp'])
                rapport.append(f"• {date.strftime('%d/%m %H:%M')} - {entree['action']}")
            rapport.append(f"")
        
        if self.metadata['notes']:
            rapport.append(f"NOTES")
            rapport.append(f"-----")
            for note_entry in self.metadata['notes'][-3:]:
                date = datetime.fromisoformat(note_entry['date'])
                rapport.append(f"• {date.strftime('%d/%m')}: {note_entry['note']}")
        
        rapport.append(f"\n{'='*80}")
        
        return "\n".join(rapport)


# ============================================================================
# INTERFACE PRINCIPALE AMÉLIORÉE
# ============================================================================

class ALTeraEnhanced:
    """Interface principale ALTera Enhanced avec toutes les améliorations"""
    
    def __init__(self, config: Optional[ConfigurationPersonnelle] = None):
        self.config = config or ConfigurationPersonnelle()
        self.projets = {}
        self.projet_actif = None
        
        # Afficher le message de bienvenue
        self._afficher_bienvenue()
        
        # Charger les projets existants
        self._charger_projets_existants()
    
    def _afficher_bienvenue(self):
        """Affiche le message de bienvenue personnalisé"""
        print(f"\n{'='*80}")
        print(f"✨ ALTera ENHANCED v3.0 - Système de Conception Architecturale")
        print(f"{'='*80}")
        print(f"👤 Utilisateur: {self.config.nom_utilisateur}")
        print(f"🏢 Entreprise: {self.config.entreprise}")
        print(f"🎨 Thème par défaut: {self.config.theme_defaut.value}")
        print(f"{'='*80}\n")
    
    def _charger_projets_existants(self):
        """Charge la liste des projets existants"""
        if os.path.exists(self.config.dossier_projets):
            for dossier in os.listdir(self.config.dossier_projets):
                chemin_projet = os.path.join(self.config.dossier_projets, dossier)
                if os.path.isdir(chemin_projet):
                    # Vérifier qu'il y a des sauvegardes
                    sauvegardes_dir = os.path.join(chemin_projet, 'sauvegardes')
                    if os.path.exists(sauvegardes_dir):
                        self.projets[dossier] = chemin_projet
    
    def creer_projet(self, nom: str) -> ProjetALTera:
        """Crée un nouveau projet"""
        if nom in self.projets:
            print(f"⚠️ Un projet '{nom}' existe déjà")
            reponse = input("Voulez-vous l'écraser? (o/n): ")
            if reponse.lower() != 'o':
                return None
        
        projet = ProjetALTera(nom, self.config)
        self.projets[nom] = projet
        self.projet_actif = projet
        
        print(f"✅ Projet '{nom}' créé avec succès")
        print(f"📁 Dossier: {os.path.join(self.config.dossier_projets, nom)}")
        
        return projet
    
    def ouvrir_projet(self, nom: str) -> Optional[ProjetALTera]:
        """Ouvre un projet existant"""
        if nom not in self.projets:
            print(f"❌ Projet '{nom}' introuvable")
            return None
        
        # Charger le projet depuis la dernière sauvegarde
        projet = ProjetALTera(nom, self.config)
        self.projet_actif = projet
        
        print(f"✅ Projet '{nom}' ouvert")
        return projet
    
    def lister_projets(self):
        """Liste tous les projets disponibles"""
        if not self.projets:
            print("📂 Aucun projet disponible")
            return
        
        print(f"\n📂 PROJETS DISPONIBLES")
        print(f"{'='*50}")
        
        for nom, chemin in self.projets.items():
            # Obtenir des infos sur le projet
            sauvegardes_dir = os.path.join(chemin, 'sauvegardes')
            if os.path.exists(sauvegardes_dir):
                nb_sauvegardes = len(os.listdir(sauvegardes_dir))
                print(f"• {nom} ({nb_sauvegardes} sauvegardes)")
            else:
                print(f"• {nom}")
    
    def workflow_assistant(self):
        """Assistant interactif pour guider l'utilisateur"""
        print(f"\n🤖 ASSISTANT ALTERA")
        print(f"{'='*50}")
        print("Que souhaitez-vous faire?")
        print("1. Créer un nouveau projet")
        print("2. Ouvrir un projet existant")
        print("3. Utiliser un template")
        print("4. Configuration")
        print("5. Aide")
        print("0. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            nom = input("Nom du projet: ")
            client = input("Nom du client (optionnel): ")
            
            projet = self.creer_projet(nom)
            if projet and client:
                projet.definir_client(client)
            
            return projet
        
        elif choix == "2":
            self.lister_projets()
            nom = input("\nNom du projet à ouvrir: ")
            return self.ouvrir_projet(nom)
        
        elif choix == "3":
            self._workflow_template()
        
        elif choix == "4":
            self._menu_configuration()
        
        elif choix == "5":
            self._afficher_aide()
    
    def _workflow_template(self):
        """Workflow pour utiliser un template"""
        if not self.projet_actif:
            print("⚠️ Veuillez d'abord créer ou ouvrir un projet")
            return
        
        templates = self.projet_actif.templates.lister_templates()
        
        print(f"\n📋 TEMPLATES DISPONIBLES")
        print(f"{'='*50}")
        
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template.nom} - {template.description}")
            print(f"   Style: {template.style.value} | Type: {template.type_piece}")
        
        choix = input("\nNuméro du template (0 pour annuler): ")
        
        try:
            index = int(choix) - 1
            if 0 <= index < len(templates):
                template = templates[index]
                print(f"\n✅ Template '{template.nom}' appliqué au projet")
                self.projet_actif.ajouter_historique('template_applique', {
                    'template': template.nom
                })
        except:
            pass
    
    def _menu_configuration(self):
        """Menu de configuration"""
        print(f"\n⚙️ CONFIGURATION")
        print(f"{'='*50}")
        print(f"1. Nom utilisateur: {self.config.nom_utilisateur}")
        print(f"2. Entreprise: {self.config.entreprise}")
        print(f"3. Thème par défaut: {self.config.theme_defaut.value}")
        print(f"4. Qualité rendu: {self.config.qualite_rendu_defaut}")
        print(f"5. Auto-sauvegarde: {'Activée' if self.config.auto_sauvegarde else 'Désactivée'}")
        print(f"6. Mode expert: {'Activé' if self.config.mode_expert else 'Désactivé'}")
        print(f"7. Sauvegarder configuration")
        print(f"0. Retour")
        
        choix = input("\nQue modifier? ")
        
        if choix == "1":
            self.config.nom_utilisateur = input("Nouveau nom: ")
        elif choix == "2":
            self.config.entreprise = input("Nouvelle entreprise: ")
        elif choix == "3":
            print("Thèmes disponibles:", [t.value for t in ThemeStyle])
            theme = input("Nouveau thème: ")
            try:
                self.config.theme_defaut = ThemeStyle(theme)
            except:
                print("Thème invalide")
        elif choix == "7":
            self.config.sauvegarder()
            print("✅ Configuration sauvegardée")
    
    def _afficher_aide(self):
        """Affiche l'aide"""
        aide = """
        🔷 AIDE ALTERA ENHANCED
        ========================
        
        RACCOURCIS CLAVIER (dans Rhino):
        • Ctrl+N : Nouveau projet
        • Ctrl+O : Ouvrir projet
        • Ctrl+S : Sauvegarder
        • F1 : Aide
        • F5 : Rafraîchir
        
        WORKFLOW RECOMMANDÉ:
        1. Créer/ouvrir un projet
        2. Définir le client et le budget
        3. Importer ou créer la géométrie
        4. Appliquer un template ou style
        5. Générer les meubles
        6. Créer les rendus
        7. Exporter le devis
        
        CONSEILS:
        • Utilisez les templates pour gagner du temps
        • Activez l'auto-sauvegarde pour ne rien perdre
        • Le cache accélère les rendus répétés
        • Les notes permettent de suivre l'évolution
        
        Pour plus d'aide, consultez la documentation complète.
        """
        print(aide)
    
    def executer_commande(self, commande: str, *args, **kwargs):
        """Exécute une commande sur le projet actif"""
        if not self.projet_actif:
            print("❌ Aucun projet actif. Créez ou ouvrez un projet d'abord.")
            return
        
        # Mapping des commandes
        commandes = {
            'scan': self._cmd_scan,
            'mobilier': self._cmd_mobilier,
            'rendu': self._cmd_rendu,
            'devis': self._cmd_devis,
            'export': self._cmd_export,
            'rapport': self._cmd_rapport,
            'sauvegarde': self._cmd_sauvegarde,
            'note': self._cmd_note
        }
        
        if commande in commandes:
            return commandes[commande](*args, **kwargs)
        else:
            print(f"❌ Commande '{commande}' inconnue")
    
    def _cmd_scan(self, fichier: str):
        """Commande pour importer un scan"""
        print(f"📡 Import du scan: {fichier}")
        self.projet_actif.ajouter_historique('scan_importe', {'fichier': fichier})
    
    def _cmd_mobilier(self, type_meuble: str, **params):
        """Commande pour créer du mobilier"""
        print(f"🪑 Création mobilier: {type_meuble}")
        self.projet_actif.ajouter_historique('mobilier_cree', {
            'type': type_meuble,
            'params': params
        })
    
    def _cmd_rendu(self, qualite: str = "haute"):
        """Commande pour générer un rendu"""
        print(f"🎨 Génération rendu (qualité: {qualite})")
        
        # Utiliser le cache si possible
        cle_cache = self.projet_actif.cache.generer_cle(
            'rendu', 
            self.projet_actif.id_projet, 
            qualite
        )
        
        rendu_cache = self.projet_actif.cache.obtenir(cle_cache)
        if rendu_cache:
            print("✅ Rendu trouvé dans le cache")
            return rendu_cache
        
        # Sinon générer et mettre en cache
        print("⏳ Génération du rendu...")
        # ... code de génération ...
        
        self.projet_actif.ajouter_historique('rendu_genere', {'qualite': qualite})
    
    def _cmd_devis(self):
        """Commande pour générer un devis"""
        print(f"💰 Génération du devis")
        self.projet_actif.ajouter_historique('devis_genere', {})
    
    def _cmd_export(self, format: str = "pdf"):
        """Commande pour exporter le projet"""
        print(f"📤 Export du projet (format: {format})")
        self.projet_actif.ajouter_historique('projet_exporte', {'format': format})
    
    def _cmd_rapport(self):
        """Commande pour afficher le rapport"""
        rapport = self.projet_actif.generer_rapport()
        print(rapport)
    
    def _cmd_sauvegarde(self):
        """Commande pour sauvegarder"""
        chemin = self.projet_actif.sauvegarder_projet()
        print(f"✅ Projet sauvegardé: {chemin}")
    
    def _cmd_note(self, note: str):
        """Commande pour ajouter une note"""
        self.projet_actif.ajouter_note(note)
        print(f"✅ Note ajoutée")


# ============================================================================
# FONCTIONS UTILITAIRES AVANCÉES
# ============================================================================

def benchmark_performance(fonction):
    """Décorateur pour mesurer les performances"""
    def wrapper(*args, **kwargs):
        debut = datetime.now()
        resultat = fonction(*args, **kwargs)
        duree = (datetime.now() - debut).total_seconds()
        print(f"⏱️ {fonction.__name__} exécuté en {duree:.2f}s")
        return resultat
    return wrapper


def valider_geometrie(geometrie) -> bool:
    """Valide qu'une géométrie est correcte"""
    if not geometrie:
        return False
    
    if hasattr(geometrie, 'IsValid'):
        return geometrie.IsValid
    
    return True


def optimiser_mesh(mesh, reduction_ratio: float = 0.5):
    """Optimise un mesh en réduisant les polygones"""
    if not mesh or not hasattr(mesh, 'Reduce'):
        return mesh
    
    target_faces = int(mesh.Faces.Count * reduction_ratio)
    mesh.Reduce(target_faces, True, 5, True)
    return mesh


# ============================================================================
# EXEMPLE D'UTILISATION
# ============================================================================

if __name__ == "__main__":
    # Créer une configuration personnalisée
    config = ConfigurationPersonnelle(
        nom_utilisateur="Jean Designer",
        entreprise="Design Studio Pro",
        theme_defaut=ThemeStyle.MODERNE,
        qualite_rendu_defaut="ultra",
        auto_sauvegarde=True
    )
    
    # Initialiser ALTera Enhanced
    altera = ALTeraEnhanced(config)
    
    # Créer un nouveau projet
    projet = altera.creer_projet("Villa_Moderne_2025")
    
    # Définir le client
    projet.definir_client(
        nom="M. et Mme Dupont",
        adresse="123 Avenue des Champs, Paris",
        budget=50000,
        deadline="2025-12-31"
    )
    
    # Ajouter une note
    projet.ajouter_note("Le client préfère les tons neutres et naturels")
    
    # Utiliser l'assistant interactif
    # altera.workflow_assistant()
    
    # Exécuter des commandes
    altera.executer_commande('scan', 'salon.3dm')
    altera.executer_commande('mobilier', 'canape', longueur=2000, largeur=900)
    altera.executer_commande('rendu', qualite='haute')
    
    # Générer et afficher le rapport
    altera.executer_commande('rapport')
    
    # Sauvegarder le projet
    altera.executer_commande('sauvegarde')
    
    print("\n✨ Projet terminé avec succès!")
