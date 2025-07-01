#!/usr/bin/env python3
"""
Chronosense v0.1 - Classe principale de l'application
Gère l'interface utilisateur Tkinter et coordonne les autres composants

Auteur: Généré automatiquement
Version: 0.1 (Preuve de Concept)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from graph_manager import GraphManager
from ai_manager import AIManager

class ChronosenseApp:
    """
    Classe principale de l'application Chronosense
    Gère l'interface utilisateur Tkinter et coordonne les interactions
    entre le gestionnaire de graphe et le gestionnaire d'IA
    """
    
    def __init__(self):
        """
        Initialise l'application Chronosense
        """
        self.root = tk.Tk()
        self.root.title("Chronosense v0.1 - Assistant d'Investigation DFIR")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialiser les gestionnaires
        self.graph_manager = GraphManager()
        self.ai_manager = AIManager()
        
        # Variables pour l'interface
        self.artifact_var = tk.StringVar()
        self.selected_nodes = []
        
        # Créer l'interface utilisateur
        self._create_interface()
        
        # Configurer les événements
        self._setup_events()
        
        print("Application Chronosense initialisée avec succès")
    
    def _create_interface(self):
        """
        Crée l'interface utilisateur principale
        """
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame supérieur pour le contenu principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Zone de gauche (70%) - Graphe
        self.graph_frame = ttk.LabelFrame(content_frame, text="Graphe d'Investigation", padding=10)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Zone de droite (30%) - Détails et hypothèses
        self.details_frame = ttk.LabelFrame(content_frame, text="Détails et Hypothèses IA", padding=10)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        self.details_frame.configure(width=350)
        self.details_frame.pack_propagate(False)
        
        # Zone de texte pour les détails
        self.details_text = scrolledtext.ScrolledText(
            self.details_frame, 
            wrap=tk.WORD, 
            height=20,
            font=("Consolas", 10)
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour générer les hypothèses
        self.generate_btn = ttk.Button(
            self.details_frame,
            text="🧠 Générer des Hypothèses",
            command=self._generate_hypotheses_threaded
        )
        self.generate_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Frame inférieur pour les contrôles
        controls_frame = ttk.LabelFrame(main_frame, text="Contrôles", padding=10)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Contrôles d'ajout d'artéfacts
        artifact_frame = ttk.Frame(controls_frame)
        artifact_frame.pack(fill=tk.X)
        
        ttk.Label(artifact_frame, text="Artéfact:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.artifact_entry = ttk.Entry(
            artifact_frame, 
            textvariable=self.artifact_var,
            font=("Consolas", 10),
            width=50
        )
        self.artifact_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.add_btn = ttk.Button(
            artifact_frame,
            text="➕ Ajouter Artéfact",
            command=self._add_artifact
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.link_btn = ttk.Button(
            artifact_frame,
            text="🔗 Lier Nœuds Sélectionnés",
            command=self._link_selected_nodes
        )
        self.link_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = ttk.Button(
            artifact_frame,
            text="🗑️ Effacer Graphe",
            command=self._clear_graph
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # Barre de statut
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt - Ajoutez des artéfacts pour commencer l'investigation")
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)
        
        # Initialiser l'affichage du graphe
        self.graph_manager.setup_display(self.graph_frame)
        
        # Message d'accueil
        welcome_msg = """🔍 Bienvenue dans Chronosense v0.1
        
Assistant d'Investigation DFIR avec IA Locale

📋 Instructions:
1. Ajoutez des artéfacts (IP, hash, fichiers, processus...)
2. Liez les artéfacts entre eux pour créer des relations
3. Cliquez sur "Générer des Hypothèses" pour l'analyse IA
4. L'IA analysera le graphe et proposera des hypothèses d'attaque

💡 Exemples d'artéfacts:
• IP: 192.168.1.100, 8.8.8.8
• Hash: abc123def456...
• Fichier: evil.exe, malware.dll
• Processus: powershell.exe, cmd.exe
• Domaine: malicious-site.com

🎯 L'objectif est de construire un graphe d'investigation
et d'utiliser l'IA pour identifier des patterns d'attaque."""
        
        self.details_text.insert(tk.END, welcome_msg)
    
    def _setup_events(self):
        """
        Configure les événements de l'interface
        """
        # Entrée sur Enter pour ajouter un artéfact
        self.artifact_entry.bind('<Return>', lambda e: self._add_artifact())
        
        # Événement de fermeture de fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _add_artifact(self):
        """
        Ajoute un artéfact au graphe d'investigation
        """
        artifact = self.artifact_var.get().strip()
        
        if not artifact:
            messagebox.showwarning("Attention", "Veuillez saisir un artéfact")
            return
        
        try:
            # Ajouter le nœud au graphe
            node_id = self.graph_manager.add_node(artifact)
            
            # Mettre à jour l'affichage
            self.graph_manager.update_display()
            
            # Effacer le champ de saisie
            self.artifact_var.set("")
            
            # Mettre à jour le statut
            self.status_var.set(f"Artéfact ajouté: {artifact} (ID: {node_id})")
            
            # Mettre à jour les détails
            self._update_details_display()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'artéfact: {e}")
    
    def _link_selected_nodes(self):
        """
        Lie les nœuds sélectionnés dans le graphe
        """
        # Pour la v0.1, on utilise une méthode simple de sélection
        # Dans une version future, on pourrait implémenter une sélection graphique
        
        # Demander à l'utilisateur les IDs des nœuds à lier
        dialog = NodeSelectionDialog(self.root, self.graph_manager.get_all_nodes())
        if dialog.result:
            node1, node2 = dialog.result
            try:
                self.graph_manager.add_edge(node1, node2)
                self.graph_manager.update_display()
                self.status_var.set(f"Lien créé entre {node1} et {node2}")
                self._update_details_display()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la création du lien: {e}")
    
    def _clear_graph(self):
        """
        Efface complètement le graphe
        """
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir effacer tout le graphe ?"):
            self.graph_manager.clear_graph()
            self.graph_manager.update_display()
            self.status_var.set("Graphe effacé")
            self._update_details_display()
    
    def _update_details_display(self):
        """
        Met à jour l'affichage des détails du graphe
        """
        details = self.graph_manager.get_graph_summary()
        
        # Effacer le contenu actuel (sauf le message d'accueil si le graphe est vide)
        if self.graph_manager.get_node_count() > 0:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"📊 Résumé du Graphe:\n\n{details}\n\n")
            self.details_text.insert(tk.END, "💡 Cliquez sur 'Générer des Hypothèses' pour l'analyse IA")
    
    def _generate_hypotheses_threaded(self):
        """
        Lance la génération d'hypothèses dans un thread séparé
        pour éviter de bloquer l'interface
        """
        if self.graph_manager.get_node_count() == 0:
            messagebox.showwarning("Attention", "Ajoutez au moins un artéfact avant de générer des hypothèses")
            return
        
        # Désactiver le bouton pendant le traitement
        self.generate_btn.configure(state='disabled', text="🔄 Génération en cours...")
        self.status_var.set("Génération d'hypothèses en cours...")
        
        # Lancer dans un thread
        thread = threading.Thread(target=self._generate_hypotheses)
        thread.daemon = True
        thread.start()
    
    def _generate_hypotheses(self):
        """
        Génère les hypothèses d'investigation avec l'IA
        """
        try:
            # Obtenir la description du graphe
            graph_description = self.graph_manager.get_graph_description()
            
            # Générer les hypothèses avec l'IA
            hypotheses = self.ai_manager.generate_hypotheses(graph_description)
            
            # Mettre à jour l'interface dans le thread principal
            self.root.after(0, self._display_hypotheses, hypotheses)
            
        except Exception as e:
            self.root.after(0, self._display_error, str(e))
    
    def _display_hypotheses(self, hypotheses):
        """
        Affiche les hypothèses générées par l'IA
        """
        # Réactiver le bouton
        self.generate_btn.configure(state='normal', text="🧠 Générer des Hypothèses")
        
        # Afficher les hypothèses
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, "🤖 Analyse IA - Hypothèses d'Investigation:\n\n")
        self.details_text.insert(tk.END, hypotheses)
        
        self.status_var.set("Hypothèses générées avec succès")
    
    def _display_error(self, error_msg):
        """
        Affiche une erreur lors de la génération d'hypothèses
        """
        # Réactiver le bouton
        self.generate_btn.configure(state='normal', text="🧠 Générer des Hypothèses")
        
        messagebox.showerror("Erreur IA", f"Erreur lors de la génération d'hypothèses:\n{error_msg}")
        self.status_var.set("Erreur lors de la génération d'hypothèses")
    
    def _on_closing(self):
        """
        Gère la fermeture de l'application
        """
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter Chronosense ?"):
            self.root.destroy()
    
    def run(self):
        """
        Lance l'application
        """
        print("Lancement de l'interface graphique...")
        self.root.mainloop()


class NodeSelectionDialog:
    """
    Dialogue simple pour sélectionner deux nœuds à lier
    """
    
    def __init__(self, parent, nodes):
        self.result = None
        
        if len(nodes) < 2:
            messagebox.showwarning("Attention", "Il faut au moins 2 nœuds pour créer un lien")
            return
        
        # Créer la fenêtre de dialogue
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Sélectionner les nœuds à lier")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrer la fenêtre
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Interface
        ttk.Label(self.dialog, text="Sélectionnez deux nœuds à lier:").pack(pady=10)
        
        # Premier nœud
        ttk.Label(self.dialog, text="Premier nœud:").pack(anchor=tk.W, padx=20)
        self.node1_var = tk.StringVar()
        self.node1_combo = ttk.Combobox(self.dialog, textvariable=self.node1_var, values=nodes, state="readonly")
        self.node1_combo.pack(fill=tk.X, padx=20, pady=5)
        
        # Deuxième nœud
        ttk.Label(self.dialog, text="Deuxième nœud:").pack(anchor=tk.W, padx=20, pady=(10, 0))
        self.node2_var = tk.StringVar()
        self.node2_combo = ttk.Combobox(self.dialog, textvariable=self.node2_var, values=nodes, state="readonly")
        self.node2_combo.pack(fill=tk.X, padx=20, pady=5)
        
        # Boutons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Créer le lien", command=self._ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annuler", command=self._cancel).pack(side=tk.LEFT, padx=5)
        
        # Attendre la fermeture
        self.dialog.wait_window()
    
    def _ok(self):
        node1 = self.node1_var.get()
        node2 = self.node2_var.get()
        
        if not node1 or not node2:
            messagebox.showwarning("Attention", "Veuillez sélectionner les deux nœuds")
            return
        
        if node1 == node2:
            messagebox.showwarning("Attention", "Veuillez sélectionner deux nœuds différents")
            return
        
        self.result = (node1, node2)
        self.dialog.destroy()
    
    def _cancel(self):
        self.dialog.destroy()
