#!/usr/bin/env python3
"""
Tests unitaires pour GraphManager
Chronosense v0.1

Auteur: Généré automatiquement
Version: 0.1
"""

import unittest
import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph_manager import GraphManager

class TestGraphManager(unittest.TestCase):
    """
    Tests unitaires pour la classe GraphManager
    """
    
    def setUp(self):
        """
        Configuration avant chaque test
        """
        self.graph_manager = GraphManager()
    
    def tearDown(self):
        """
        Nettoyage après chaque test
        """
        self.graph_manager.clear_graph()
    
    def test_initialization(self):
        """
        Test de l'initialisation du GraphManager
        """
        self.assertIsNotNone(self.graph_manager.graph)
        self.assertEqual(self.graph_manager.get_node_count(), 0)
        self.assertEqual(self.graph_manager.get_edge_count(), 0)
        self.assertEqual(self.graph_manager.node_counter, 0)
    
    def test_add_single_node(self):
        """
        Test d'ajout d'un seul nœud
        """
        artifact = "192.168.1.1"
        node_id = self.graph_manager.add_node(artifact)
        
        self.assertEqual(self.graph_manager.get_node_count(), 1)
        self.assertIn(artifact, self.graph_manager.artifact_to_id)
        self.assertIn(node_id, self.graph_manager.id_to_artifact)
        self.assertEqual(self.graph_manager.id_to_artifact[node_id], artifact)
    
    def test_add_multiple_nodes(self):
        """
        Test d'ajout de plusieurs nœuds
        """
        artifacts = ["192.168.1.1", "malware.exe", "powershell.exe"]
        
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        self.assertEqual(self.graph_manager.get_node_count(), len(artifacts))
        
        for artifact in artifacts:
            self.assertIn(artifact, self.graph_manager.artifact_to_id)
    
    def test_add_duplicate_node(self):
        """
        Test d'ajout d'un nœud en double (doit lever une exception)
        """
        artifact = "192.168.1.1"
        self.graph_manager.add_node(artifact)
        
        with self.assertRaises(ValueError):
            self.graph_manager.add_node(artifact)
    
    def test_artifact_type_detection(self):
        """
        Test de la détection automatique des types d'artéfacts
        """
        test_cases = [
            ("192.168.1.1", "ip"),
            ("8.8.8.8", "ip"),
            ("d41d8cd98f00b204e9800998ecf8427e", "hash"),
            ("malware.exe", "file"),
            ("powershell.exe", "process"),
            ("malicious-site.com", "domain"),
            ("unknown_artifact", "default")
        ]
        
        for artifact, expected_type in test_cases:
            detected_type = self.graph_manager._detect_artifact_type(artifact)
            self.assertEqual(detected_type, expected_type, 
                           f"Type incorrect pour {artifact}: attendu {expected_type}, obtenu {detected_type}")
    
    def test_add_edge(self):
        """
        Test d'ajout d'arêtes entre nœuds
        """
        artifact1 = "192.168.1.1"
        artifact2 = "malware.exe"
        
        self.graph_manager.add_node(artifact1)
        self.graph_manager.add_node(artifact2)
        self.graph_manager.add_edge(artifact1, artifact2, "connected")
        
        self.assertEqual(self.graph_manager.get_edge_count(), 1)
    
    def test_add_edge_nonexistent_nodes(self):
        """
        Test d'ajout d'arête avec des nœuds inexistants
        """
        with self.assertRaises(ValueError):
            self.graph_manager.add_edge("nonexistent1", "nonexistent2")
    
    def test_remove_node(self):
        """
        Test de suppression de nœud
        """
        artifact = "192.168.1.1"
        self.graph_manager.add_node(artifact)
        self.assertEqual(self.graph_manager.get_node_count(), 1)
        
        self.graph_manager.remove_node(artifact)
        self.assertEqual(self.graph_manager.get_node_count(), 0)
        self.assertNotIn(artifact, self.graph_manager.artifact_to_id)
    
    def test_remove_nonexistent_node(self):
        """
        Test de suppression d'un nœud inexistant
        """
        with self.assertRaises(ValueError):
            self.graph_manager.remove_node("nonexistent")
    
    def test_clear_graph(self):
        """
        Test de nettoyage complet du graphe
        """
        # Ajouter quelques nœuds et arêtes
        artifacts = ["192.168.1.1", "malware.exe", "powershell.exe"]
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        self.graph_manager.add_edge(artifacts[0], artifacts[1])
        self.graph_manager.add_edge(artifacts[1], artifacts[2])
        
        # Vérifier que le graphe n'est pas vide
        self.assertGreater(self.graph_manager.get_node_count(), 0)
        self.assertGreater(self.graph_manager.get_edge_count(), 0)
        
        # Nettoyer
        self.graph_manager.clear_graph()
        
        # Vérifier que tout est vide
        self.assertEqual(self.graph_manager.get_node_count(), 0)
        self.assertEqual(self.graph_manager.get_edge_count(), 0)
        self.assertEqual(len(self.graph_manager.artifact_to_id), 0)
        self.assertEqual(len(self.graph_manager.id_to_artifact), 0)
        self.assertEqual(self.graph_manager.node_counter, 0)
    
    def test_get_all_nodes(self):
        """
        Test de récupération de tous les nœuds
        """
        artifacts = ["192.168.1.1", "malware.exe", "powershell.exe"]
        
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        all_nodes = self.graph_manager.get_all_nodes()
        self.assertEqual(len(all_nodes), len(artifacts))
        
        for artifact in artifacts:
            self.assertIn(artifact, all_nodes)
    
    def test_graph_summary(self):
        """
        Test de génération du résumé du graphe
        """
        # Graphe vide
        summary = self.graph_manager.get_graph_summary()
        self.assertIn("Graphe vide", summary)
        
        # Graphe avec des nœuds
        artifacts = ["192.168.1.1", "malware.exe"]
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        summary = self.graph_manager.get_graph_summary()
        self.assertIn("Statistiques", summary)
        self.assertIn("Types d'artéfacts", summary)
        self.assertIn("Artéfacts détectés", summary)
    
    def test_graph_description(self):
        """
        Test de génération de la description pour l'IA
        """
        # Graphe vide
        description = self.graph_manager.get_graph_description()
        self.assertIn("Aucun artéfact", description)
        
        # Graphe avec des nœuds
        artifacts = ["192.168.1.1", "malware.exe", "powershell.exe"]
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        # Ajouter une connexion
        self.graph_manager.add_edge(artifacts[0], artifacts[1])
        
        description = self.graph_manager.get_graph_description()
        self.assertIn("Artéfacts détectés", description)
        self.assertIn("Connexions identifiées", description)
        
        for artifact in artifacts:
            self.assertIn(artifact, description)
    
    def test_node_colors(self):
        """
        Test de la configuration des couleurs de nœuds
        """
        expected_colors = ['ip', 'hash', 'file', 'process', 'domain', 'default']
        
        for color_type in expected_colors:
            self.assertIn(color_type, self.graph_manager.node_colors)
            self.assertTrue(self.graph_manager.node_colors[color_type].startswith('#'))
    
    def test_get_type_emoji(self):
        """
        Test de récupération des emojis par type
        """
        test_cases = [
            ('ip', '🌐'),
            ('hash', '🔐'),
            ('file', '📄'),
            ('process', '⚙️'),
            ('domain', '🌍'),
            ('unknown', '🔍')
        ]
        
        for artifact_type, expected_emoji in test_cases:
            emoji = self.graph_manager._get_type_emoji(artifact_type)
            self.assertEqual(emoji, expected_emoji)
    
    def test_generate_node_description(self):
        """
        Test de génération de description de nœud
        """
        test_cases = [
            ("192.168.1.1", "ip", "Adresse IP: 192.168.1.1"),
            ("malware.exe", "file", "Fichier: malware.exe"),
            ("powershell.exe", "process", "Processus: powershell.exe")
        ]
        
        for artifact, artifact_type, expected_desc in test_cases:
            description = self.graph_manager._generate_node_description(artifact, artifact_type)
            self.assertEqual(description, expected_desc)

class TestGraphManagerIntegration(unittest.TestCase):
    """
    Tests d'intégration pour GraphManager
    """
    
    def setUp(self):
        """
        Configuration avant chaque test
        """
        self.graph_manager = GraphManager()
    
    def test_complex_investigation_scenario(self):
        """
        Test d'un scénario d'investigation complexe
        """
        # Simuler une investigation APT
        artifacts = [
            "192.168.1.100",  # IP compromise
            "powershell.exe",  # Processus malveillant
            "evil.exe",  # Malware
            "c2-server.com",  # Serveur C&C
            "a1b2c3d4e5f6789012345678901234567890abcd",  # Hash
            "cmd.exe"  # Autre processus
        ]
        
        # Ajouter tous les artéfacts
        for artifact in artifacts:
            self.graph_manager.add_node(artifact)
        
        # Créer des relations logiques
        relationships = [
            ("192.168.1.100", "powershell.exe", "executed"),
            ("powershell.exe", "evil.exe", "downloaded"),
            ("evil.exe", "a1b2c3d4e5f6789012345678901234567890abcd", "has_hash"),
            ("evil.exe", "cmd.exe", "spawned"),
            ("cmd.exe", "c2-server.com", "connected_to")
        ]
        
        for artifact1, artifact2, relationship in relationships:
            self.graph_manager.add_edge(artifact1, artifact2, relationship)
        
        # Vérifications
        self.assertEqual(self.graph_manager.get_node_count(), len(artifacts))
        self.assertEqual(self.graph_manager.get_edge_count(), len(relationships))
        
        # Vérifier que la description contient tous les éléments
        description = self.graph_manager.get_graph_description()
        for artifact in artifacts:
            self.assertIn(artifact, description)
        
        # Vérifier le résumé
        summary = self.graph_manager.get_graph_summary()
        self.assertIn("IP: 1", summary)
        self.assertIn("File: 1", summary)
        self.assertIn("Process: 2", summary)
        self.assertIn("Domain: 1", summary)
        self.assertIn("Hash: 1", summary)

if __name__ == '__main__':
    # Configuration des tests
    unittest.TestLoader.sortTestMethodsUsing = None
    
    # Lancer les tests
    print("🧪 Tests unitaires pour GraphManager")
    print("=" * 40)
    
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests
    suite.addTests(loader.loadTestsFromTestCase(TestGraphManager))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphManagerIntegration))
    
    # Lancer les tests avec un runner verbeux
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 40)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Échecs:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Erreurs:")
        for test, traceback in result.errors:
            print(f"  • {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ Tous les tests ont réussi!")
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) ont échoué.")
        sys.exit(1)
