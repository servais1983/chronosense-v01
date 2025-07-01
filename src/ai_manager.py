#!/usr/bin/env python3
"""
Chronosense v0.1 - Gestionnaire d'IA
Gère la communication avec le modèle Phi-3 local et la génération d'hypothèses

Auteur: Généré automatiquement
Version: 0.1 (Preuve de Concept)
"""

import json
import requests
from datetime import datetime
import time

# Import conditionnel pour Transformers (Hugging Face)
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers non disponible. Utilisation du mode simulation.")

class AIManager:
    """
    Gestionnaire d'IA pour l'analyse d'investigation DFIR
    Intègre le modèle Microsoft Phi-3 en local
    """
    
    def __init__(self):
        """
        Initialise le gestionnaire d'IA
        """
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        
        # Configuration
        self.max_tokens = 512
        self.temperature = 0.7
        self.api_url = "http://localhost:11434/api/generate"  # URL pour Ollama local
        
        # Mode de fonctionnement
        self.mode = "simulation"  # "transformers", "api", "simulation"
        
        # Initialiser le modèle
        self._initialize_model()
        
        print(f"AIManager initialisé en mode: {self.mode}")
    
    def _initialize_model(self):
        """
        Initialise le modèle Phi-3 selon la méthode disponible
        """
        # Essayer d'abord avec Transformers (Hugging Face)
        if TRANSFORMERS_AVAILABLE:
            try:
                print("🔄 Tentative de chargement du modèle Phi-3 via Transformers...")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    trust_remote_code=True,
                    torch_dtype="auto",
                    device_map="auto"
                )
                
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    max_new_tokens=self.max_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                self.mode = "transformers"
                print("✅ Modèle Phi-3 chargé avec succès via Transformers")
                return
                
            except Exception as e:
                print(f"❌ Erreur lors du chargement via Transformers: {e}")
        
        # Essayer avec une API locale (Ollama, etc.)
        try:
            print("🔄 Tentative de connexion à l'API locale...")
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                self.mode = "api"
                print("✅ API locale détectée (Ollama)")
                return
        except Exception as e:
            print(f"❌ API locale non disponible: {e}")
        
        # Mode simulation par défaut
        self.mode = "simulation"
        print("⚠️ Mode simulation activé - Aucun modèle IA réel disponible")
    
    def generate_hypotheses(self, graph_description):
        """
        Génère des hypothèses d'investigation basées sur le graphe
        
        Args:
            graph_description (str): Description textuelle du graphe
            
        Returns:
            str: Hypothèses générées par l'IA
        """
        # Construire le prompt structuré
        prompt = self._build_investigation_prompt(graph_description)
        
        # Générer la réponse selon le mode disponible
        if self.mode == "transformers":
            return self._generate_with_transformers(prompt)
        elif self.mode == "api":
            return self._generate_with_api(prompt)
        else:
            return self._generate_simulation(graph_description)
    
    def _build_investigation_prompt(self, graph_description):
        """
        Construit le prompt structuré pour l'analyse DFIR
        
        Args:
            graph_description (str): Description du graphe d'investigation
            
        Returns:
            str: Prompt formaté pour l'IA
        """
        prompt = f"""En tant qu'expert en analyse DFIR (Digital Forensics and Incident Response), analyse les artéfacts suivants issus d'une investigation en cours.

**Artéfacts connus :**
{graph_description}

**Ta mission :**
1. Génère 2 hypothèses plausibles sur le type d'attaque en cours, basées sur les TTPs du framework MITRE ATT&CK.
2. Pour chaque hypothèse, propose 1 action d'investigation concrète et immédiate que l'analyste devrait entreprendre pour la valider ou l'invalider.

Présente ta réponse de manière claire et concise.

**Réponse :**"""
        
        return prompt
    
    def _generate_with_transformers(self, prompt):
        """
        Génère une réponse avec le modèle Transformers
        
        Args:
            prompt (str): Le prompt à traiter
            
        Returns:
            str: Réponse générée
        """
        try:
            print("🧠 Génération avec Transformers...")
            
            # Générer la réponse
            outputs = self.pipeline(
                prompt,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                return_full_text=False
            )
            
            response = outputs[0]['generated_text'].strip()
            
            # Post-traitement
            response = self._post_process_response(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return f"Erreur lors de la génération d'hypothèses: {e}"
    
    def _generate_with_api(self, prompt):
        """
        Génère une réponse via API locale (Ollama)
        
        Args:
            prompt (str): Le prompt à traiter
            
        Returns:
            str: Réponse générée
        """
        try:
            print("🧠 Génération via API locale...")
            
            payload = {
                "model": "phi3",  # Nom du modèle dans Ollama
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '')
                return self._post_process_response(generated_text)
            else:
                return f"Erreur API: {response.status_code} - {response.text}"
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération via API: {e}")
            return f"Erreur lors de la génération d'hypothèses: {e}"
    
    def _generate_simulation(self, graph_description):
        """
        Génère une réponse simulée pour les tests
        
        Args:
            graph_description (str): Description du graphe
            
        Returns:
            str: Réponse simulée
        """
        print("🎭 Génération en mode simulation...")
        
        # Analyser les types d'artéfacts présents
        has_ip = 'ip:' in graph_description.lower() or any(x in graph_description for x in ['192.168', '10.', '172.', '8.8.8.8'])
        has_file = 'fichier:' in graph_description.lower() or '.exe' in graph_description.lower()
        has_process = 'processus:' in graph_description.lower() or 'powershell' in graph_description.lower()
        has_hash = 'hash:' in graph_description.lower() or len([x for x in graph_description.split() if len(x) >= 32 and all(c in '0123456789abcdefABCDEF' for c in x)]) > 0
        
        # Générer des hypothèses basées sur les artéfacts détectés
        hypotheses = []
        
        if has_ip and has_process:
            hypotheses.append({
                "title": "Hypothèse 1: Exfiltration de données via PowerShell",
                "description": "Les artéfacts suggèrent une possible exfiltration de données utilisant PowerShell pour communiquer avec des serveurs externes.",
                "mitre_ttp": "T1041 (Exfiltration Over C2 Channel), T1059.001 (PowerShell)",
                "action": "Analyser les logs réseau pour identifier les connexions sortantes et examiner l'historique des commandes PowerShell."
            })
        
        if has_file and has_hash:
            hypotheses.append({
                "title": "Hypothèse 2: Déploiement de malware",
                "description": "La présence de fichiers exécutables avec des hash spécifiques indique un possible déploiement de malware.",
                "mitre_ttp": "T1204 (User Execution), T1105 (Ingress Tool Transfer)",
                "action": "Vérifier les hash contre des bases de données de malware (VirusTotal, MISP) et analyser le comportement des fichiers."
            })
        
        if not hypotheses:
            # Hypothèses génériques
            hypotheses = [
                {
                    "title": "Hypothèse 1: Reconnaissance initiale",
                    "description": "Les artéfacts collectés suggèrent une phase de reconnaissance ou de découverte du réseau.",
                    "mitre_ttp": "T1083 (File and Directory Discovery), T1057 (Process Discovery)",
                    "action": "Examiner les logs système pour identifier les activités de découverte et corréler avec d'autres événements suspects."
                },
                {
                    "title": "Hypothèse 2: Persistance système",
                    "description": "Les éléments détectés pourraient indiquer une tentative d'établissement de persistance sur le système.",
                    "mitre_ttp": "T1547 (Boot or Logon Autostart Execution), T1053 (Scheduled Task/Job)",
                    "action": "Vérifier les mécanismes de démarrage automatique et les tâches planifiées pour détecter des modifications suspectes."
                }
            ]
        
        # Formater la réponse
        response_parts = []
        response_parts.append("🤖 **ANALYSE IA - HYPOTHÈSES D'INVESTIGATION**")
        response_parts.append("=" * 50)
        response_parts.append("")
        
        for i, hypothesis in enumerate(hypotheses, 1):
            response_parts.append(f"**{hypothesis['title']}**")
            response_parts.append("")
            response_parts.append(f"📋 **Description:** {hypothesis['description']}")
            response_parts.append("")
            response_parts.append(f"🎯 **TTPs MITRE ATT&CK:** {hypothesis['mitre_ttp']}")
            response_parts.append("")
            response_parts.append(f"🔍 **Action recommandée:** {hypothesis['action']}")
            response_parts.append("")
            response_parts.append("-" * 40)
            response_parts.append("")
        
        response_parts.append("💡 **Note:** Cette analyse est générée en mode simulation.")
        response_parts.append("Pour une analyse complète, configurez le modèle Phi-3 local.")
        response_parts.append("")
        response_parts.append(f"⏰ Analyse générée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        
        return "\n".join(response_parts)
    
    def _post_process_response(self, response):
        """
        Post-traite la réponse de l'IA
        
        Args:
            response (str): Réponse brute de l'IA
            
        Returns:
            str: Réponse nettoyée et formatée
        """
        # Nettoyer la réponse
        response = response.strip()
        
        # Ajouter un timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y à %H:%M:%S')
        response += f"\n\n⏰ Analyse générée le {timestamp}"
        
        return response
    
    def get_model_info(self):
        """
        Retourne les informations sur le modèle utilisé
        
        Returns:
            dict: Informations sur le modèle
        """
        return {
            "model_name": self.model_name,
            "mode": self.mode,
            "available": self.mode != "simulation",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
    
    def test_connection(self):
        """
        Teste la connexion au modèle d'IA
        
        Returns:
            bool: True si la connexion fonctionne
        """
        try:
            test_prompt = "Test de connexion. Réponds simplement 'OK'."
            
            if self.mode == "transformers":
                outputs = self.pipeline(test_prompt, max_new_tokens=10, do_sample=False)
                return "ok" in outputs[0]['generated_text'].lower()
            
            elif self.mode == "api":
                payload = {
                    "model": "phi3",
                    "prompt": test_prompt,
                    "stream": False,
                    "options": {"num_predict": 10}
                }
                response = requests.post(self.api_url, json=payload, timeout=30)
                return response.status_code == 200
            
            else:
                return True  # Mode simulation toujours disponible
                
        except Exception as e:
            print(f"❌ Test de connexion échoué: {e}")
            return False


class PromptTemplates:
    """
    Templates de prompts pour différents types d'analyses DFIR
    """
    
    @staticmethod
    def investigation_analysis(artifacts):
        """
        Template pour l'analyse d'investigation générale
        """
        return f"""En tant qu'expert en analyse DFIR, analyse les artéfacts suivants:

{artifacts}

Fournis:
1. Deux hypothèses d'attaque basées sur MITRE ATT&CK
2. Des actions d'investigation concrètes pour chaque hypothèse
3. Une évaluation du niveau de criticité (Faible/Moyen/Élevé/Critique)

Réponds de manière structurée et professionnelle."""
    
    @staticmethod
    def malware_analysis(file_artifacts):
        """
        Template pour l'analyse de malware
        """
        return f"""Analyse les indicateurs de malware suivants:

{file_artifacts}

Détermine:
1. Le type de malware probable
2. Les techniques d'évasion possibles
3. Les IOCs à surveiller
4. Les mesures de containment recommandées"""
    
    @staticmethod
    def network_analysis(network_artifacts):
        """
        Template pour l'analyse réseau
        """
        return f"""Analyse les artéfacts réseau suivants:

{network_artifacts}

Évalue:
1. Les patterns de communication suspects
2. Les indicateurs de C2 (Command & Control)
3. Les signes d'exfiltration de données
4. Les recommandations de monitoring réseau"""
