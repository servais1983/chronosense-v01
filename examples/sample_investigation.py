#!/usr/bin/env python3
"""
Chronosense v0.1 - Exemple d'Investigation
Démontre l'utilisation de Chronosense pour une investigation DFIR complète

Auteur: Généré automatiquement
Version: 0.1
"""

import sys
import os
import time

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph_manager import GraphManager
from ai_manager import AIManager

def run_sample_investigation():
    """
    Exécute un exemple d'investigation DFIR avec Chronosense
    """
    print("🔍 Chronosense v0.1 - Exemple d'Investigation DFIR")
    print("=" * 60)
    print()
    
    # Initialiser les gestionnaires
    print("📋 Initialisation des composants...")
    graph_manager = GraphManager()
    ai_manager = AIManager()
    
    print(f"✅ GraphManager initialisé")
    print(f"✅ AIManager initialisé (mode: {ai_manager.mode})")
    print()
    
    # Scénario d'investigation : Attaque APT simulée
    print("🎯 Scénario: Investigation d'une attaque APT suspectée")
    print("📅 Contexte: Détection d'activités suspectes sur le réseau d'entreprise")
    print()
    
    # Phase 1: Collecte d'artéfacts initiaux
    print("📊 Phase 1: Collecte d'artéfacts initiaux")
    print("-" * 40)
    
    initial_artifacts = [
        "192.168.1.150",  # IP suspecte interne
        "powershell.exe",  # Processus suspect
        "8.8.8.8",  # DNS externe
        "malicious-domain.com",  # Domaine suspect
        "evil.exe"  # Fichier suspect
    ]
    
    for artifact in initial_artifacts:
        try:
            node_id = graph_manager.add_node(artifact)
            artifact_type = graph_manager.graph.nodes[node_id]['type']
            print(f"  ➕ Ajouté: {artifact} (type: {artifact_type})")
            time.sleep(0.5)  # Simulation du temps de traitement
        except Exception as e:
            print(f"  ❌ Erreur avec {artifact}: {e}")
    
    print(f"\n📈 Statistiques: {graph_manager.get_node_count()} artéfacts collectés")
    print()
    
    # Phase 2: Établissement de relations
    print("📊 Phase 2: Établissement de relations entre artéfacts")
    print("-" * 50)
    
    relationships = [
        ("192.168.1.150", "powershell.exe", "executed_on"),
        ("powershell.exe", "8.8.8.8", "connected_to"),
        ("powershell.exe", "malicious-domain.com", "resolved"),
        ("malicious-domain.com", "evil.exe", "downloaded"),
        ("evil.exe", "192.168.1.150", "installed_on")
    ]
    
    for artifact1, artifact2, relationship in relationships:
        try:
            graph_manager.add_edge(artifact1, artifact2, relationship)
            print(f"  🔗 Lien: {artifact1} --[{relationship}]--> {artifact2}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ Erreur de liaison {artifact1} <-> {artifact2}: {e}")
    
    print(f"\n📈 Statistiques: {graph_manager.get_edge_count()} relations établies")
    print()
    
    # Phase 3: Analyse du graphe
    print("📊 Phase 3: Analyse du graphe d'investigation")
    print("-" * 45)
    
    summary = graph_manager.get_graph_summary()
    print(summary)
    print()
    
    # Phase 4: Génération d'hypothèses IA
    print("📊 Phase 4: Génération d'hypothèses avec l'IA")
    print("-" * 45)
    
    print("🧠 Analyse en cours...")
    graph_description = graph_manager.get_graph_description()
    
    print("📝 Description du graphe pour l'IA:")
    print(graph_description)
    print()
    
    print("🤖 Génération d'hypothèses...")
    hypotheses = ai_manager.generate_hypotheses(graph_description)
    
    print("📋 Hypothèses générées:")
    print(hypotheses)
    print()
    
    # Phase 5: Artéfacts supplémentaires
    print("📊 Phase 5: Découverte d'artéfacts supplémentaires")
    print("-" * 50)
    
    additional_artifacts = [
        "a1b2c3d4e5f6789012345678901234567890abcd",  # Hash suspect
        "cmd.exe",  # Autre processus
        "192.168.1.200",  # Autre IP compromise
        "backdoor.dll",  # Fichier de persistance
        "c2-server.net"  # Serveur C&C
    ]
    
    for artifact in additional_artifacts:
        try:
            node_id = graph_manager.add_node(artifact)
            artifact_type = graph_manager.graph.nodes[node_id]['type']
            print(f"  ➕ Découvert: {artifact} (type: {artifact_type})")
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ Erreur avec {artifact}: {e}")
    
    # Nouvelles relations
    new_relationships = [
        ("evil.exe", "a1b2c3d4e5f6789012345678901234567890abcd", "has_hash"),
        ("evil.exe", "cmd.exe", "spawned"),
        ("cmd.exe", "192.168.1.200", "connected_to"),
        ("backdoor.dll", "192.168.1.150", "installed_on"),
        ("192.168.1.200", "c2-server.net", "communicates_with")
    ]
    
    for artifact1, artifact2, relationship in new_relationships:
        try:
            graph_manager.add_edge(artifact1, artifact2, relationship)
            print(f"  🔗 Nouveau lien: {artifact1} --[{relationship}]--> {artifact2}")
            time.sleep(0.2)
        except Exception as e:
            print(f"  ❌ Erreur de liaison: {e}")
    
    print()
    
    # Phase 6: Analyse finale
    print("📊 Phase 6: Analyse finale du graphe étendu")
    print("-" * 45)
    
    final_summary = graph_manager.get_graph_summary()
    print(final_summary)
    print()
    
    # Nouvelle analyse IA avec le graphe complet
    print("🤖 Analyse IA finale avec le graphe complet...")
    final_description = graph_manager.get_graph_description()
    final_hypotheses = ai_manager.generate_hypotheses(final_description)
    
    print("📋 Hypothèses finales:")
    print(final_hypotheses)
    print()
    
    # Résumé de l'investigation
    print("📊 Résumé de l'Investigation")
    print("=" * 40)
    print(f"🔍 Artéfacts analysés: {graph_manager.get_node_count()}")
    print(f"🔗 Relations identifiées: {graph_manager.get_edge_count()}")
    print(f"🧠 Mode IA utilisé: {ai_manager.mode}")
    print()
    
    # Types d'artéfacts détectés
    types_count = {}
    for node_id in graph_manager.graph.nodes():
        node_type = graph_manager.graph.nodes[node_id].get('type', 'unknown')
        types_count[node_type] = types_count.get(node_type, 0) + 1
    
    print("📋 Types d'artéfacts détectés:")
    for artifact_type, count in types_count.items():
        print(f"  • {artifact_type.title()}: {count}")
    
    print()
    print("✅ Investigation d'exemple terminée avec succès!")
    print("💡 Utilisez ces patterns pour vos propres investigations.")

def run_interactive_demo():
    """
    Démo interactive permettant à l'utilisateur d'ajouter ses propres artéfacts
    """
    print("🎮 Mode Démo Interactif")
    print("=" * 30)
    print("Ajoutez vos propres artéfacts pour tester Chronosense")
    print("Tapez 'quit' pour terminer, 'help' pour l'aide")
    print()
    
    graph_manager = GraphManager()
    ai_manager = AIManager()
    
    while True:
        artifact = input("🔍 Entrez un artéfact: ").strip()
        
        if artifact.lower() == 'quit':
            break
        elif artifact.lower() == 'help':
            print("\n💡 Exemples d'artéfacts:")
            print("  • IP: 192.168.1.1, 8.8.8.8")
            print("  • Hash: d41d8cd98f00b204e9800998ecf8427e")
            print("  • Fichier: malware.exe, trojan.dll")
            print("  • Processus: powershell.exe, cmd.exe")
            print("  • Domaine: malicious-site.com")
            print()
            continue
        elif not artifact:
            continue
        
        try:
            node_id = graph_manager.add_node(artifact)
            artifact_type = graph_manager.graph.nodes[node_id]['type']
            print(f"  ✅ Ajouté: {artifact} (type: {artifact_type})")
            
            # Afficher le résumé si on a plusieurs artéfacts
            if graph_manager.get_node_count() > 1:
                print(f"\n📊 Graphe actuel: {graph_manager.get_node_count()} artéfacts")
                
                # Proposer une analyse IA tous les 3 artéfacts
                if graph_manager.get_node_count() % 3 == 0:
                    analyze = input("🤖 Lancer l'analyse IA ? (y/n): ").lower()
                    if analyze == 'y':
                        description = graph_manager.get_graph_description()
                        hypotheses = ai_manager.generate_hypotheses(description)
                        print("\n" + hypotheses + "\n")
            
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    # Analyse finale
    if graph_manager.get_node_count() > 0:
        print("\n📊 Analyse finale:")
        summary = graph_manager.get_graph_summary()
        print(summary)
        
        description = graph_manager.get_graph_description()
        hypotheses = ai_manager.generate_hypotheses(description)
        print("\n🤖 Hypothèses finales:")
        print(hypotheses)
    
    print("\n👋 Merci d'avoir testé Chronosense!")

def main():
    """
    Point d'entrée principal pour les exemples
    """
    print("🔍 Chronosense v0.1 - Exemples d'Utilisation")
    print("=" * 50)
    print()
    print("Choisissez un mode:")
    print("1. Investigation d'exemple (automatique)")
    print("2. Démo interactive")
    print("3. Quitter")
    print()
    
    while True:
        choice = input("Votre choix (1-3): ").strip()
        
        if choice == '1':
            print()
            run_sample_investigation()
            break
        elif choice == '2':
            print()
            run_interactive_demo()
            break
        elif choice == '3':
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
