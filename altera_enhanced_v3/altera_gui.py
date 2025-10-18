"""
ALTera GUI - Interface Graphique Moderne
=========================================

Interface utilisateur graphique pour ALTera Enhanced avec design moderne.

Version: 3.0 ENHANCED
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any
import threading
import queue


# ============================================================================
# THÈME ET STYLE
# ============================================================================

class ModernTheme:
    """Définition du thème moderne pour l'interface"""
    
    # Couleurs principales
    BG_PRIMARY = "#1e1e2e"      # Fond principal sombre
    BG_SECONDARY = "#2a2a3e"    # Fond secondaire
    BG_TERTIARY = "#35354a"     # Fond tertiaire
    
    # Couleurs d'accent
    ACCENT_PRIMARY = "#7aa2f7"   # Bleu principal
    ACCENT_SUCCESS = "#9ece6a"   # Vert succès
    ACCENT_WARNING = "#e0af68"   # Orange avertissement
    ACCENT_ERROR = "#f7768e"     # Rouge erreur
    ACCENT_INFO = "#bb9af7"      # Violet info
    
    # Texte
    TEXT_PRIMARY = "#c0caf5"     # Texte principal
    TEXT_SECONDARY = "#9aa5ce"   # Texte secondaire
    TEXT_DISABLED = "#565f89"    # Texte désactivé
    
    # Bordures et séparateurs
    BORDER_COLOR = "#414868"
    SEPARATOR_COLOR = "#3b4261"
    
    # Police
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_TITLE = 24
    FONT_SIZE_HEADING = 16
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_SMALL = 9
    
    @classmethod
    def configurer_styles(cls, root):
        """Configure les styles ttk pour le thème moderne"""
        style = ttk.Style(root)
        style.theme_use('clam')
        
        # Configuration générale
        style.configure(
            '.',
            background=cls.BG_PRIMARY,
            foreground=cls.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor='none',
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL)
        )
        
        # Frames
        style.configure('Card.TFrame', background=cls.BG_SECONDARY, relief='flat')
        style.configure('Sidebar.TFrame', background=cls.BG_SECONDARY)
        
        # Labels
        style.configure('Heading.TLabel', 
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_HEADING, 'bold'))
        style.configure('Title.TLabel', 
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_TITLE, 'bold'))
        style.configure('Small.TLabel', 
                       font=(cls.FONT_FAMILY, cls.FONT_SIZE_SMALL))
        
        # Boutons
        style.configure(
            'Modern.TButton',
            background=cls.ACCENT_PRIMARY,
            foreground=cls.BG_PRIMARY,
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8),
            font=(cls.FONT_FAMILY, cls.FONT_SIZE_NORMAL, 'bold')
        )
        style.map(
            'Modern.TButton',
            background=[('active', cls.ACCENT_INFO), ('pressed', cls.ACCENT_INFO)]
        )
        
        # Bouton success
        style.configure('Success.TButton', background=cls.ACCENT_SUCCESS)
        style.map('Success.TButton',
                 background=[('active', cls.ACCENT_SUCCESS)])
        
        # Bouton danger
        style.configure('Danger.TButton', background=cls.ACCENT_ERROR)
        style.map('Danger.TButton',
                 background=[('active', cls.ACCENT_ERROR)])
        
        # Entry
        style.configure(
            'Modern.TEntry',
            fieldbackground=cls.BG_TERTIARY,
            borderwidth=1,
            relief='solid',
            insertcolor=cls.TEXT_PRIMARY
        )
        
        # Combobox
        style.configure(
            'Modern.TCombobox',
            fieldbackground=cls.BG_TERTIARY,
            background=cls.BG_TERTIARY,
            borderwidth=1,
            arrowcolor=cls.TEXT_PRIMARY
        )
        
        # Progressbar
        style.configure(
            'Modern.Horizontal.TProgressbar',
            background=cls.ACCENT_PRIMARY,
            troughcolor=cls.BG_TERTIARY,
            borderwidth=0,
            lightcolor=cls.ACCENT_PRIMARY,
            darkcolor=cls.ACCENT_PRIMARY
        )
        
        # Treeview
        style.configure(
            'Modern.Treeview',
            background=cls.BG_TERTIARY,
            fieldbackground=cls.BG_TERTIARY,
            foreground=cls.TEXT_PRIMARY,
            borderwidth=0
        )
        style.configure('Modern.Treeview.Heading',
                       background=cls.BG_SECONDARY,
                       foreground=cls.TEXT_PRIMARY,
                       borderwidth=0)
        style.map('Modern.Treeview',
                 background=[('selected', cls.ACCENT_PRIMARY)],
                 foreground=[('selected', cls.BG_PRIMARY)])


# ============================================================================
# WIDGETS PERSONNALISÉS
# ============================================================================

class ModernButton(tk.Frame):
    """Bouton moderne avec icône optionnelle"""
    
    def __init__(self, parent, text="", icon="", command=None, style="primary", **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_PRIMARY, **kwargs)
        
        # Déterminer la couleur selon le style
        colors = {
            'primary': ModernTheme.ACCENT_PRIMARY,
            'success': ModernTheme.ACCENT_SUCCESS,
            'warning': ModernTheme.ACCENT_WARNING,
            'danger': ModernTheme.ACCENT_ERROR,
            'info': ModernTheme.ACCENT_INFO
        }
        
        self.bg_color = colors.get(style, ModernTheme.ACCENT_PRIMARY)
        self.command = command
        
        # Créer le cadre du bouton
        self.button_frame = tk.Frame(self, bg=self.bg_color, cursor="hand2")
        self.button_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Contenu du bouton
        content_frame = tk.Frame(self.button_frame, bg=self.bg_color)
        content_frame.pack(expand=True, padx=15, pady=8)
        
        if icon:
            icon_label = tk.Label(
                content_frame,
                text=icon,
                bg=self.bg_color,
                fg=ModernTheme.BG_PRIMARY,
                font=(ModernTheme.FONT_FAMILY, 14)
            )
            icon_label.pack(side="left", padx=(0, 5))
        
        if text:
            text_label = tk.Label(
                content_frame,
                text=text,
                bg=self.bg_color,
                fg=ModernTheme.BG_PRIMARY,
                font=(ModernTheme.FONT_FAMILY, 11, 'bold')
            )
            text_label.pack(side="left")
        
        # Événements
        self.button_frame.bind("<Button-1>", self._on_click)
        self.button_frame.bind("<Enter>", self._on_enter)
        self.button_frame.bind("<Leave>", self._on_leave)
        
        for child in content_frame.winfo_children():
            child.bind("<Button-1>", self._on_click)
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        # Effet hover - éclaircir la couleur
        self.button_frame.configure(bg=self._lighter_color(self.bg_color))
        for widget in self.button_frame.winfo_children():
            widget.configure(bg=self._lighter_color(self.bg_color))
            for child in widget.winfo_children():
                child.configure(bg=self._lighter_color(self.bg_color))
    
    def _on_leave(self, event):
        # Retour à la couleur normale
        self.button_frame.configure(bg=self.bg_color)
        for widget in self.button_frame.winfo_children():
            widget.configure(bg=self.bg_color)
            for child in widget.winfo_children():
                child.configure(bg=self.bg_color)
    
    def _lighter_color(self, color):
        """Éclaircit une couleur hex"""
        # Convertir hex en RGB
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Éclaircir
        r = min(255, r + 20)
        g = min(255, g + 20)
        b = min(255, b + 20)
        
        return f'#{r:02x}{g:02x}{b:02x}'


class ModernCard(tk.Frame):
    """Carte moderne avec titre et contenu"""
    
    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_SECONDARY, **kwargs)
        
        # Titre de la carte
        if title:
            title_frame = tk.Frame(self, bg=ModernTheme.BG_SECONDARY)
            title_frame.pack(fill="x", padx=20, pady=(15, 10))
            
            title_label = tk.Label(
                title_frame,
                text=title,
                bg=ModernTheme.BG_SECONDARY,
                fg=ModernTheme.TEXT_PRIMARY,
                font=(ModernTheme.FONT_FAMILY, 14, 'bold')
            )
            title_label.pack(anchor="w")
            
            # Séparateur
            separator = tk.Frame(
                title_frame,
                height=2,
                bg=ModernTheme.SEPARATOR_COLOR
            )
            separator.pack(fill="x", pady=(5, 0))
        
        # Frame pour le contenu
        self.content_frame = tk.Frame(self, bg=ModernTheme.BG_SECONDARY)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    
    def get_content_frame(self):
        """Retourne le frame de contenu pour ajouter des widgets"""
        return self.content_frame


class StatusBar(tk.Frame):
    """Barre de statut moderne"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_TERTIARY, height=30, **kwargs)
        
        # Message principal
        self.status_label = tk.Label(
            self,
            text="Prêt",
            bg=ModernTheme.BG_TERTIARY,
            fg=ModernTheme.TEXT_SECONDARY,
            font=(ModernTheme.FONT_FAMILY, 9)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Indicateurs à droite
        self.indicators_frame = tk.Frame(self, bg=ModernTheme.BG_TERTIARY)
        self.indicators_frame.pack(side="right", padx=10)
        
        # Heure
        self.time_label = tk.Label(
            self.indicators_frame,
            bg=ModernTheme.BG_TERTIARY,
            fg=ModernTheme.TEXT_SECONDARY,
            font=(ModernTheme.FONT_FAMILY, 9)
        )
        self.time_label.pack(side="right")
        
        self.update_time()
    
    def set_status(self, message: str, type: str = "info"):
        """Met à jour le message de statut"""
        colors = {
            'info': ModernTheme.TEXT_SECONDARY,
            'success': ModernTheme.ACCENT_SUCCESS,
            'warning': ModernTheme.ACCENT_WARNING,
            'error': ModernTheme.ACCENT_ERROR
        }
        
        self.status_label.config(text=message, fg=colors.get(type, ModernTheme.TEXT_SECONDARY))
    
    def update_time(self):
        """Met à jour l'heure"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)


# ============================================================================
# FENÊTRE PRINCIPALE
# ============================================================================

class ALTeraGUI:
    """Interface graphique principale d'ALTera Enhanced"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ALTera Enhanced - Système de Conception Architecturale")
        self.root.geometry("1400x900")
        
        # Appliquer le thème
        self.root.configure(bg=ModernTheme.BG_PRIMARY)
        ModernTheme.configurer_styles(self.root)
        
        # Variables
        self.projet_actuel = None
        self.projets = {}
        
        # Queue pour communication inter-threads
        self.queue = queue.Queue()
        
        # Construire l'interface
        self._construire_interface()
        
        # Démarrer la vérification de la queue
        self._verifier_queue()
    
    def _construire_interface(self):
        """Construit l'interface complète"""
        
        # Barre de titre personnalisée
        self._creer_barre_titre()
        
        # Container principal avec sidebar et contenu
        main_container = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self._creer_sidebar(main_container)
        
        # Zone de contenu principal
        self.content_area = tk.Frame(main_container, bg=ModernTheme.BG_PRIMARY)
        self.content_area.pack(side="left", fill="both", expand=True)
        
        # Page d'accueil par défaut
        self._afficher_accueil()
        
        # Barre de statut
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")
    
    def _creer_barre_titre(self):
        """Crée la barre de titre personnalisée"""
        title_bar = tk.Frame(self.root, bg=ModernTheme.BG_SECONDARY, height=60)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        
        # Logo et titre
        title_container = tk.Frame(title_bar, bg=ModernTheme.BG_SECONDARY)
        title_container.pack(side="left", padx=20, pady=10)
        
        logo = tk.Label(
            title_container,
            text="🏗️",
            bg=ModernTheme.BG_SECONDARY,
            font=(ModernTheme.FONT_FAMILY, 24)
        )
        logo.pack(side="left", padx=(0, 10))
        
        title = tk.Label(
            title_container,
            text="ALTera Enhanced",
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 18, 'bold')
        )
        title.pack(side="left")
        
        subtitle = tk.Label(
            title_container,
            text="v3.0",
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.TEXT_SECONDARY,
            font=(ModernTheme.FONT_FAMILY, 10)
        )
        subtitle.pack(side="left", padx=(10, 0))
        
        # Boutons de contrôle de fenêtre
        controls = tk.Frame(title_bar, bg=ModernTheme.BG_SECONDARY)
        controls.pack(side="right", padx=20)
        
        minimize_btn = tk.Button(
            controls,
            text="─",
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.TEXT_PRIMARY,
            bd=0,
            font=(ModernTheme.FONT_FAMILY, 12),
            command=self.root.iconify
        )
        minimize_btn.pack(side="left", padx=5)
        
        close_btn = tk.Button(
            controls,
            text="✕",
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.ACCENT_ERROR,
            bd=0,
            font=(ModernTheme.FONT_FAMILY, 12),
            command=self.quitter
        )
        close_btn.pack(side="left")
    
    def _creer_sidebar(self, parent):
        """Crée la barre latérale de navigation"""
        sidebar = tk.Frame(parent, bg=ModernTheme.BG_SECONDARY, width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Menu principal
        menu_items = [
            ("🏠", "Accueil", self._afficher_accueil),
            ("📁", "Projets", self._afficher_projets),
            ("🎨", "Design", self._afficher_design),
            ("🪑", "Mobilier", self._afficher_mobilier),
            ("🎬", "Rendus", self._afficher_rendus),
            ("💰", "Devis", self._afficher_devis),
            ("🔌", "Plugins", self._afficher_plugins),
            ("⚙️", "Paramètres", self._afficher_parametres)
        ]
        
        for icon, text, command in menu_items:
            self._creer_menu_item(sidebar, icon, text, command)
        
        # Informations en bas
        info_frame = tk.Frame(sidebar, bg=ModernTheme.BG_TERTIARY)
        info_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        if self.projet_actuel:
            projet_label = tk.Label(
                info_frame,
                text=f"Projet: {self.projet_actuel}",
                bg=ModernTheme.BG_TERTIARY,
                fg=ModernTheme.TEXT_SECONDARY,
                font=(ModernTheme.FONT_FAMILY, 9)
            )
            projet_label.pack(pady=5)
    
    def _creer_menu_item(self, parent, icon, text, command):
        """Crée un élément de menu dans la sidebar"""
        item_frame = tk.Frame(parent, bg=ModernTheme.BG_SECONDARY, cursor="hand2")
        item_frame.pack(fill="x", padx=10, pady=2)
        
        # Container pour le contenu
        content = tk.Frame(item_frame, bg=ModernTheme.BG_SECONDARY)
        content.pack(fill="x", padx=10, pady=10)
        
        # Icône
        icon_label = tk.Label(
            content,
            text=icon,
            bg=ModernTheme.BG_SECONDARY,
            font=(ModernTheme.FONT_FAMILY, 16)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Texte
        text_label = tk.Label(
            content,
            text=text,
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 11)
        )
        text_label.pack(side="left")
        
        # Événements
        def on_enter(e):
            item_frame.configure(bg=ModernTheme.BG_TERTIARY)
            content.configure(bg=ModernTheme.BG_TERTIARY)
            icon_label.configure(bg=ModernTheme.BG_TERTIARY)
            text_label.configure(bg=ModernTheme.BG_TERTIARY, fg=ModernTheme.ACCENT_PRIMARY)
        
        def on_leave(e):
            item_frame.configure(bg=ModernTheme.BG_SECONDARY)
            content.configure(bg=ModernTheme.BG_SECONDARY)
            icon_label.configure(bg=ModernTheme.BG_SECONDARY)
            text_label.configure(bg=ModernTheme.BG_SECONDARY, fg=ModernTheme.TEXT_PRIMARY)
        
        def on_click(e):
            command()
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        item_frame.bind("<Button-1>", on_click)
        
        for widget in [content, icon_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
    
    def _nettoyer_contenu(self):
        """Nettoie la zone de contenu"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def _afficher_accueil(self):
        """Affiche la page d'accueil"""
        self._nettoyer_contenu()
        
        # Container avec scroll
        canvas = tk.Canvas(self.content_area, bg=ModernTheme.BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ModernTheme.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Titre
        title = tk.Label(
            scrollable_frame,
            text="Tableau de Bord",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        # Cartes de statistiques
        stats_frame = tk.Frame(scrollable_frame, bg=ModernTheme.BG_PRIMARY)
        stats_frame.pack(pady=20, padx=40, fill="x")
        
        stats = [
            ("Projets Actifs", "12", ModernTheme.ACCENT_PRIMARY),
            ("Rendus Générés", "47", ModernTheme.ACCENT_SUCCESS),
            ("Devis en Cours", "8", ModernTheme.ACCENT_WARNING),
            ("Clients", "23", ModernTheme.ACCENT_INFO)
        ]
        
        for label, value, color in stats:
            stat_card = tk.Frame(stats_frame, bg=ModernTheme.BG_SECONDARY)
            stat_card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
            
            # Contenu de la carte
            card_content = tk.Frame(stat_card, bg=ModernTheme.BG_SECONDARY)
            card_content.pack(padx=20, pady=15)
            
            value_label = tk.Label(
                card_content,
                text=value,
                bg=ModernTheme.BG_SECONDARY,
                fg=color,
                font=(ModernTheme.FONT_FAMILY, 32, 'bold')
            )
            value_label.pack()
            
            label_label = tk.Label(
                card_content,
                text=label,
                bg=ModernTheme.BG_SECONDARY,
                fg=ModernTheme.TEXT_SECONDARY,
                font=(ModernTheme.FONT_FAMILY, 11)
            )
            label_label.pack(pady=(5, 0))
        
        # Actions rapides
        actions_card = ModernCard(scrollable_frame, title="Actions Rapides")
        actions_card.pack(pady=20, padx=40, fill="x")
        
        actions_content = actions_card.get_content_frame()
        
        buttons_frame = tk.Frame(actions_content, bg=ModernTheme.BG_SECONDARY)
        buttons_frame.pack(pady=10)
        
        ModernButton(
            buttons_frame,
            text="Nouveau Projet",
            icon="➕",
            command=self._nouveau_projet,
            style="primary"
        ).pack(side="left", padx=5)
        
        ModernButton(
            buttons_frame,
            text="Importer Scan",
            icon="📡",
            command=self._importer_scan,
            style="info"
        ).pack(side="left", padx=5)
        
        ModernButton(
            buttons_frame,
            text="Générer Rendu",
            icon="🎨",
            command=self._generer_rendu,
            style="success"
        ).pack(side="left", padx=5)
        
        # Projets récents
        recent_card = ModernCard(scrollable_frame, title="Projets Récents")
        recent_card.pack(pady=20, padx=40, fill="x")
        
        recent_content = recent_card.get_content_frame()
        
        # Liste des projets récents
        projets_recents = [
            ("Villa Moderne", "Client: M. Dupont", "Il y a 2 heures"),
            ("Appartement Paris", "Client: Mme Martin", "Hier"),
            ("Loft Industriel", "Client: StartupTech", "Il y a 3 jours")
        ]
        
        for nom, client, date in projets_recents:
            projet_item = tk.Frame(recent_content, bg=ModernTheme.BG_TERTIARY)
            projet_item.pack(fill="x", pady=5)
            
            info_frame = tk.Frame(projet_item, bg=ModernTheme.BG_TERTIARY)
            info_frame.pack(padx=15, pady=10, fill="x")
            
            nom_label = tk.Label(
                info_frame,
                text=nom,
                bg=ModernTheme.BG_TERTIARY,
                fg=ModernTheme.TEXT_PRIMARY,
                font=(ModernTheme.FONT_FAMILY, 12, 'bold')
            )
            nom_label.pack(anchor="w")
            
            details_frame = tk.Frame(info_frame, bg=ModernTheme.BG_TERTIARY)
            details_frame.pack(fill="x")
            
            client_label = tk.Label(
                details_frame,
                text=client,
                bg=ModernTheme.BG_TERTIARY,
                fg=ModernTheme.TEXT_SECONDARY,
                font=(ModernTheme.FONT_FAMILY, 10)
            )
            client_label.pack(side="left")
            
            date_label = tk.Label(
                details_frame,
                text=date,
                bg=ModernTheme.BG_TERTIARY,
                fg=ModernTheme.TEXT_DISABLED,
                font=(ModernTheme.FONT_FAMILY, 9)
            )
            date_label.pack(side="right")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.status_bar.set_status("Tableau de bord chargé", "success")
    
    def _afficher_projets(self):
        """Affiche la page des projets"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Gestion des Projets",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        # Barre d'outils
        toolbar = tk.Frame(self.content_area, bg=ModernTheme.BG_PRIMARY)
        toolbar.pack(pady=10, padx=40, fill="x")
        
        ModernButton(
            toolbar,
            text="Nouveau",
            icon="➕",
            command=self._nouveau_projet,
            style="success"
        ).pack(side="left", padx=5)
        
        ModernButton(
            toolbar,
            text="Ouvrir",
            icon="📂",
            command=self._ouvrir_projet,
            style="primary"
        ).pack(side="left", padx=5)
        
        # Liste des projets
        projects_frame = ModernCard(self.content_area, title="Projets Disponibles")
        projects_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # TreeView pour les projets
        tree_frame = projects_frame.get_content_frame()
        
        columns = ("Nom", "Client", "Date", "Statut")
        self.projects_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Modern.Treeview"
        )
        
        for col in columns:
            self.projects_tree.heading(col, text=col)
            self.projects_tree.column(col, width=150)
        
        # Données exemple
        projets_data = [
            ("Villa Moderne", "M. Dupont", "14/10/2025", "En cours"),
            ("Appartement Paris", "Mme Martin", "13/10/2025", "Terminé"),
            ("Loft Industriel", "StartupTech", "11/10/2025", "En attente"),
            ("Maison Écologique", "Famille Vert", "10/10/2025", "En cours")
        ]
        
        for data in projets_data:
            self.projects_tree.insert("", "end", values=data)
        
        self.projects_tree.pack(fill="both", expand=True)
        
        self.status_bar.set_status("Page projets affichée", "info")
    
    def _afficher_design(self):
        """Affiche la page de design"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Design & Décoration",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Module Design chargé", "info")
    
    def _afficher_mobilier(self):
        """Affiche la page du mobilier"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Création de Mobilier",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Module Mobilier chargé", "info")
    
    def _afficher_rendus(self):
        """Affiche la page des rendus"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Rendus & Visualisation",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Module Rendus chargé", "info")
    
    def _afficher_devis(self):
        """Affiche la page des devis"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Gestion des Devis",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Module Devis chargé", "info")
    
    def _afficher_plugins(self):
        """Affiche la page des plugins"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Gestionnaire de Plugins",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Gestionnaire de plugins chargé", "info")
    
    def _afficher_parametres(self):
        """Affiche la page des paramètres"""
        self._nettoyer_contenu()
        
        title = tk.Label(
            self.content_area,
            text="Paramètres",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 24, 'bold')
        )
        title.pack(pady=20)
        
        self.status_bar.set_status("Paramètres ouverts", "info")
    
    def _nouveau_projet(self):
        """Ouvre la fenêtre de création de projet"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Projet")
        dialog.geometry("500x400")
        dialog.configure(bg=ModernTheme.BG_PRIMARY)
        
        # Titre
        title = tk.Label(
            dialog,
            text="Créer un Nouveau Projet",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 18, 'bold')
        )
        title.pack(pady=20)
        
        # Formulaire
        form_frame = tk.Frame(dialog, bg=ModernTheme.BG_PRIMARY)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Nom du projet
        tk.Label(
            form_frame,
            text="Nom du projet:",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 11)
        ).grid(row=0, column=0, sticky="w", pady=10)
        
        nom_entry = ttk.Entry(form_frame, style="Modern.TEntry", width=30)
        nom_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Client
        tk.Label(
            form_frame,
            text="Client:",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 11)
        ).grid(row=1, column=0, sticky="w", pady=10)
        
        client_entry = ttk.Entry(form_frame, style="Modern.TEntry", width=30)
        client_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Type de projet
        tk.Label(
            form_frame,
            text="Type:",
            bg=ModernTheme.BG_PRIMARY,
            fg=ModernTheme.TEXT_PRIMARY,
            font=(ModernTheme.FONT_FAMILY, 11)
        ).grid(row=2, column=0, sticky="w", pady=10)
        
        type_combo = ttk.Combobox(
            form_frame,
            values=["Maison", "Appartement", "Bureau", "Commerce", "Autre"],
            style="Modern.TCombobox",
            width=28
        )
        type_combo.grid(row=2, column=1, pady=10, padx=10)
        
        # Boutons
        buttons_frame = tk.Frame(dialog, bg=ModernTheme.BG_PRIMARY)
        buttons_frame.pack(pady=20)
        
        def creer_projet():
            nom = nom_entry.get()
            client = client_entry.get()
            if nom:
                self.status_bar.set_status(f"Projet '{nom}' créé", "success")
                dialog.destroy()
        
        ModernButton(
            buttons_frame,
            text="Créer",
            icon="✓",
            command=creer_projet,
            style="success"
        ).pack(side="left", padx=5)
        
        ModernButton(
            buttons_frame,
            text="Annuler",
            icon="✕",
            command=dialog.destroy,
            style="danger"
        ).pack(side="left", padx=5)
    
    def _ouvrir_projet(self):
        """Ouvre un projet existant"""
        fichier = filedialog.askopenfilename(
            title="Ouvrir un projet",
            filetypes=[("Projets ALTera", "*.altera"), ("Tous", "*.*")]
        )
        if fichier:
            self.status_bar.set_status(f"Projet ouvert: {fichier}", "success")
    
    def _importer_scan(self):
        """Importe un scan LIDAR"""
        fichier = filedialog.askopenfilename(
            title="Importer un scan",
            filetypes=[("Fichiers 3D", "*.3dm;*.obj;*.stl"), ("Tous", "*.*")]
        )
        if fichier:
            self.status_bar.set_status(f"Scan importé: {fichier}", "success")
    
    def _generer_rendu(self):
        """Lance la génération d'un rendu"""
        self.status_bar.set_status("Génération du rendu en cours...", "warning")
        
        # Simuler une génération asynchrone
        def generer():
            import time
            time.sleep(2)  # Simulation
            self.queue.put(("rendu_complete", None))
        
        thread = threading.Thread(target=generer)
        thread.daemon = True
        thread.start()
    
    def _verifier_queue(self):
        """Vérifie la queue pour les messages des threads"""
        try:
            while True:
                msg, data = self.queue.get_nowait()
                
                if msg == "rendu_complete":
                    self.status_bar.set_status("Rendu généré avec succès!", "success")
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self._verifier_queue)
    
    def quitter(self):
        """Quitte l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ALTera?"):
            self.root.quit()
    
    def run(self):
        """Lance l'interface"""
        self.root.mainloop()


# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    app = ALTeraGUI()
    app.run()
