#!/usr/bin/env python3
"""
Chronosense v0.1 - Gestionnaire de Graphe
Gère toutes les opérations sur le graphe NetworkX et sa visualisation

Auteur: Généré automatiquement
Version: 0.1 (Preuve de Concept)
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
from matplotlib.figure import Figure
import tkinter as tk
from datetime import datetime
import re

class GraphManager:
    """
    Gestionnaire du graphe d'investigation
    Utilise NetworkX pour la structure et Matplotlib pour la visualisation
    """
    
    def __init__(self):
        """
        Initialise le gestionnaire de graphe
        """
        # Créer un graphe NetworkX vide
        self.graph = nx.Graph()
        
        # Compteur pour les IDs uniques des nœuds
        self.node_counter = 0
        
        # Mapping entre les artéfacts et leurs IDs
        self.artifact_to_id = {}
        self.id_to_artifact = {}
        
        # Configuration de la visualisation
        self.figure = None
        self.canvas = None
        self.ax = None
        
        # Couleurs pour différents types d'artéfacts
        self.node_colors = {
            'ip': '#FF6B6B',        # Rouge pour les IPs
            'hash': '#4ECDC4',      # Turquoise pour les hash
            'file': '#45B7D1',     # Bleu pour les fichiers
            'process': '#96CEB4',   # Vert pour les processus
            'domain': '#FFEAA7',    # Jaune pour les domaines
            'default': '#DDA0DD'    # Violet par défaut
        }
        
        print("GraphManager initialisé")
    
    def setup_display(self, parent_frame):
        """
        Configure l'affichage du graphe dans le frame Tkinter
        
        Args:
            parent_frame: Frame Tkinter parent pour l'affichage
        """
        # Créer la figure Matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor='white')
        self.ax = self.figure.add_subplot(111)
        
        # Créer le canvas Tkinter
        self.canvas = FigureCanvasTkinter(self.figure, parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Affichage initial
        self._draw_empty_graph()
        
        print("Affichage du graphe configuré")
    
    def add_node(self, artifact):
        """
        Ajoute un nœud (artéfact) au graphe
        
        Args:
            artifact (str): L'artéfact à ajouter
            
        Returns:
            str: L'ID du nœud créé
        """
        # Vérifier si l'artéfact existe déjà
        if artifact in self.artifact_to_id:
            raise ValueError(f"L'artéfact '{artifact}' existe déjà dans le graphe")
        
        # Créer un ID unique
        self.node_counter += 1
        node_id = f"node_{self.node_counter}"
        
        # Déterminer le type d'artéfact
        artifact_type = self._detect_artifact_type(artifact)
        
        # Ajouter au graphe NetworkX
        self.graph.add_node(
            node_id,
            artifact=artifact,
            type=artifact_type,
            timestamp=datetime.now().isoformat(),
            description=self._generate_node_description(artifact, artifact_type)
        )
        
        # Mettre à jour les mappings
        self.artifact_to_id[artifact] = node_id
        self.id_to_artifact[node_id] = artifact
        
        print(f"Nœud ajouté: {artifact} -> {node_id} (type: {artifact_type})")
        return node_id
    
    def add_edge(self, artifact1, artifact2, relationship="connected"):
        """
        Ajoute une arête entre deux artéfacts
        
        Args:
            artifact1 (str): Premier artéfact
            artifact2 (str): Deuxième artéfact
            relationship (str): Type de relation
        """
        # Vérifier que les artéfacts existent
        if artifact1 not in self.artifact_to_id:
            raise ValueError(f"L'artéfact '{artifact1}' n'existe pas dans le graphe")
        if artifact2 not in self.artifact_to_id:
            raise ValueError(f"L'artéfact '{artifact2}' n'existe pas dans le graphe")
        
        node1_id = self.artifact_to_id[artifact1]
        node2_id = self.artifact_to_id[artifact2]
        
        # Ajouter l'arête
        self.graph.add_edge(
            node1_id,
            node2_id,
            relationship=relationship,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"Arête ajoutée: {artifact1} <-> {artifact2} ({relationship})")
    
    def remove_node(self, artifact):
        """
        Supprime un nœud du graphe
        
        Args:
            artifact (str): L'artéfact à supprimer
        """
        if artifact not in self.artifact_to_id:
            raise ValueError(f"L'artéfact '{artifact}' n'existe pas dans le graphe")
        
        node_id = self.artifact_to_id[artifact]
        
        # Supprimer du graphe
        self.graph.remove_node(node_id)
        
        # Nettoyer les mappings
        del self.artifact_to_id[artifact]
        del self.id_to_artifact[node_id]
        
        print(f"Nœud supprimé: {artifact}")
    
    def clear_graph(self):
        """
        Efface complètement le graphe
        """
        self.graph.clear()
        self.artifact_to_id.clear()
        self.id_to_artifact.clear()
        self.node_counter = 0
        print("Graphe effacé")
    
    def get_node_count(self):
        """
        Retourne le nombre de nœuds dans le graphe
        """
        return self.graph.number_of_nodes()
    
    def get_edge_count(self):
        """
        Retourne le nombre d'arêtes dans le graphe
        """
        return self.graph.number_of_edges()
    
    def get_all_nodes(self):
        """
        Retourne la liste de tous les artéfacts
        """
        return list(self.artifact_to_id.keys())
    
    def get_graph_summary(self):
        """
        Génère un résumé textuel du graphe
        
        Returns:
            str: Résumé du graphe
        """
        if self.get_node_count() == 0:
            return "Graphe vide - Aucun artéfact ajouté"
        
        summary = []
        summary.append(f"📊 Statistiques:")
        summary.append(f"   • Nœuds (artéfacts): {self.get_node_count()}")
        summary.append(f"   • Liens: {self.get_edge_count()}")
        summary.append("")
        
        # Grouper par type
        types_count = {}
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get('type', 'unknown')
            types_count[node_type] = types_count.get(node_type, 0) + 1
        
        summary.append("📋 Types d'artéfacts:")
        for artifact_type, count in types_count.items():
            emoji = self._get_type_emoji(artifact_type)
            summary.append(f"   {emoji} {artifact_type.title()}: {count}")
        summary.append("")
        
        # Lister les artéfacts
        summary.append("🔍 Artéfacts détectés:")
        for artifact in sorted(self.artifact_to_id.keys()):
            node_id = self.artifact_to_id[artifact]
            node_type = self.graph.nodes[node_id].get('type', 'unknown')
            emoji = self._get_type_emoji(node_type)
            summary.append(f"   {emoji} {artifact}")
        
        # Lister les connexions
        if self.get_edge_count() > 0:
            summary.append("")
            summary.append("🔗 Connexions:")
            for edge in self.graph.edges():
                artifact1 = self.id_to_artifact[edge[0]]
                artifact2 = self.id_to_artifact[edge[1]]
                relationship = self.graph.edges[edge].get('relationship', 'connected')
                summary.append(f"   • {artifact1} <-> {artifact2} ({relationship})")
        
        return "\n".join(summary)
    
    def get_graph_description(self):
        """
        Génère une description textuelle du graphe pour l'IA
        
        Returns:
            str: Description formatée pour l'IA
        """
        if self.get_node_count() == 0:
            return "Aucun artéfact détecté dans l'investigation."
        
        description = []
        
        # Lister tous les artéfacts avec leurs types
        artifacts_by_type = {}
        for artifact in self.artifact_to_id.keys():
            node_id = self.artifact_to_id[artifact]
            node_type = self.graph.nodes[node_id].get('type', 'unknown')
            if node_type not in artifacts_by_type:
                artifacts_by_type[node_type] = []
            artifacts_by_type[node_type].append(artifact)
        
        description.append("Artéfacts détectés dans l'investigation:")
        for artifact_type, artifacts in artifacts_by_type.items():
            description.append(f"- {artifact_type.title()}: {', '.join(artifacts)}")
        
        # Décrire les connexions
        if self.get_edge_count() > 0:
            description.append("\nConnexions identifiées:")
            for edge in self.graph.edges():
                artifact1 = self.id_to_artifact[edge[0]]
                artifact2 = self.id_to_artifact[edge[1]]
                relationship = self.graph.edges[edge].get('relationship', 'connected')
                description.append(f"- {artifact1} est lié à {artifact2} ({relationship})")
        else:
            description.append("\nAucune connexion explicite identifiée entre les artéfacts.")
        
        return "\n".join(description)
    
    def update_display(self):
        """
        Met à jour l'affichage du graphe
        """
        if self.ax is None:
            return
        
        # Effacer l'affichage précédent
        self.ax.clear()
        
        if self.get_node_count() == 0:
            self._draw_empty_graph()
        else:
            self._draw_graph()
        
        # Rafraîchir le canvas
        self.canvas.draw()
    
    def _draw_empty_graph(self):
        """
        Dessine un graphe vide avec un message d'accueil
        """
        self.ax.text(0.5, 0.5, 
                    "🔍 Chronosense v0.1\n\nGraphe d'Investigation Vide\n\nAjoutez des artéfacts pour commencer",
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.ax.transAxes,
                    fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.ax.set_title("Graphe d'Investigation DFIR", fontsize=14, fontweight='bold')
    
    def _draw_graph(self):
        """
        Dessine le graphe avec NetworkX et Matplotlib
        """
        # Calculer la disposition des nœuds
        if self.get_node_count() == 1:
            # Un seul nœud au centre
            pos = {list(self.graph.nodes())[0]: (0.5, 0.5)}
        elif self.get_node_count() <= 10:
            # Disposition circulaire pour les petits graphes
            pos = nx.circular_layout(self.graph)
        else:
            # Disposition spring pour les graphes plus grands
            pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        # Préparer les couleurs des nœuds
        node_colors = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id].get('type', 'default')
            color = self.node_colors.get(node_type, self.node_colors['default'])
            node_colors.append(color)
        
        # Dessiner les arêtes
        nx.draw_networkx_edges(
            self.graph, pos, ax=self.ax,
            edge_color='gray',
            width=2,
            alpha=0.6
        )
        
        # Dessiner les nœuds
        nx.draw_networkx_nodes(
            self.graph, pos, ax=self.ax,
            node_color=node_colors,
            node_size=1000,
            alpha=0.8
        )
        
        # Ajouter les labels (artéfacts)
        labels = {}
        for node_id in self.graph.nodes():
            artifact = self.id_to_artifact[node_id]
            # Tronquer les labels longs
            if len(artifact) > 15:
                labels[node_id] = artifact[:12] + "..."
            else:
                labels[node_id] = artifact
        
        nx.draw_networkx_labels(
            self.graph, pos, labels, ax=self.ax,
            font_size=8,
            font_weight='bold'
        )
        
        # Configuration de l'affichage
        self.ax.set_title(f"Graphe d'Investigation - {self.get_node_count()} artéfacts, {self.get_edge_count()} liens", 
                         fontsize=12, fontweight='bold')
        self.ax.axis('off')
        
        # Ajuster les marges
        self.figure.tight_layout()
    
    def _detect_artifact_type(self, artifact):
        """
        Détecte automatiquement le type d'un artéfact
        
        Args:
            artifact (str): L'artéfact à analyser
            
        Returns:
            str: Le type détecté
        """
        artifact_lower = artifact.lower()
        
        # Patterns pour différents types
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        hash_pattern = r'^[a-fA-F0-9]{32,128}$'  # MD5, SHA1, SHA256, etc.
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        
        if re.match(ip_pattern, artifact):
            return 'ip'
        elif re.match(hash_pattern, artifact):
            return 'hash'
        elif re.match(domain_pattern, artifact):
            return 'domain'
        elif '.' in artifact and any(ext in artifact_lower for ext in ['.exe', '.dll', '.bat', '.ps1', '.doc', '.pdf']):
            return 'file'
        elif any(proc in artifact_lower for proc in ['powershell', 'cmd', 'rundll32', 'regsvr32', 'svchost']):
            return 'process'
        else:
            return 'default'
    
    def _generate_node_description(self, artifact, artifact_type):
        """
        Génère une description pour un nœud
        
        Args:
            artifact (str): L'artéfact
            artifact_type (str): Le type d'artéfact
            
        Returns:
            str: Description du nœud
        """
        descriptions = {
            'ip': f"Adresse IP: {artifact}",
            'hash': f"Hash cryptographique: {artifact}",
            'file': f"Fichier: {artifact}",
            'process': f"Processus: {artifact}",
            'domain': f"Domaine: {artifact}",
            'default': f"Artéfact: {artifact}"
        }
        
        return descriptions.get(artifact_type, f"Artéfact: {artifact}")
    
    def _get_type_emoji(self, artifact_type):
        """
        Retourne l'emoji correspondant au type d'artéfact
        
        Args:
            artifact_type (str): Le type d'artéfact
            
        Returns:
            str: L'emoji correspondant
        """
        emojis = {
            'ip': '🌐',
            'hash': '🔐',
            'file': '📄',
            'process': '⚙️',
            'domain': '🌍',
            'default': '🔍'
        }
        
        return emojis.get(artifact_type, '🔍')
