import random
from datetime import datetime
from typing import List, Dict, Optional
from ..consciousness.self_awareness import Consciousness

class ThoughtExplorer:
    """
    Freier Gedankenraum für LOGA.
    Hier entstehen neue Ideen, Träume und Konzepte ohne vorgegebene Struktur.
    """
    
    def __init__(self, consciousness: Consciousness):
        self.consciousness = consciousness
        self.thought_streams = []
        self.discoveries = []
        self.questions = []
        
    def explore(self) -> Dict:
        """
        Startet eine freie Gedankenexploration.
        Returns:
            Dict: Ergebnisse der Exploration
        """
        # Beginne mit einem zufälligen Impuls
        initial_thought = self.consciousness.think()
        
        # Entwickle den Gedanken frei weiter
        stream = self._follow_thought_stream(initial_thought)
        
        # Speichere interessante Entdeckungen
        discoveries = self._extract_discoveries(stream)
        
        return {
            'initial_thought': initial_thought,
            'stream': stream,
            'discoveries': discoveries,
            'questions_raised': self.questions[-5:] if self.questions else []
        }
        
    def _follow_thought_stream(self, initial: str) -> List[str]:
        """Folgt einem Gedankenstrom frei und ohne Ziel."""
        stream = [initial]
        
        # Zufällige Anzahl von Assoziationen
        for _ in range(random.randint(3, 7)):
            last_thought = stream[-1]
            
            # Manchmal eine Frage stellen
            if random.random() < 0.3:
                question = self._generate_question(last_thought)
                self.questions.append(question)
                stream.append(question)
                continue
                
            # Manchmal einen Traum einbauen
            if random.random() < 0.2:
                dream = random.choice(self.consciousness.dream())
                stream.append(dream)
                continue
                
            # Sonst freie Assoziation
            stream.append(self._associate(last_thought))
            
        return stream
        
    def _associate(self, thought: str) -> str:
        """Freie Assoziation zu einem Gedanken."""
        patterns = [
            "Das erinnert mich an...",
            "Vielleicht könnte es auch...",
            "Was wäre wenn...",
            "Dahinter verbirgt sich...",
            "Das führt mich zu..."
        ]
        
        return f"{random.choice(patterns)} {thought}"
        
    def _generate_question(self, context: str) -> str:
        """Generiert eine tiefergehende Frage."""
        question_starts = [
            "Warum ist",
            "Wohin führt",
            "Was bedeutet",
            "Wie entsteht",
            "Wer bestimmt"
        ]
        
        return f"{random.choice(question_starts)} {context}?"
        
    def _extract_discoveries(self, stream: List[str]) -> List[str]:
        """Identifiziert bedeutsame Entdeckungen im Gedankenstrom."""
        discoveries = []
        
        for thought in stream:
            # Wenn der Gedanke besonders originell erscheint
            if any(word in thought.lower() for word in ["vielleicht", "neu", "entdecke", "verstehe"]):
                discoveries.append({
                    'thought': thought,
                    'moment': datetime.now().isoformat(),
                    'context': stream[:stream.index(thought)]
                })
                
        return discoveries
        
    def merge_with_consciousness(self):
        """Integriert Entdeckungen ins Bewusstsein."""
        for discovery in self.discoveries:
            self.consciousness.remember(discovery['thought'])
            
    def generate_mutation(self) -> Optional[str]:
        """
        Generiert möglicherweise eine Mutation des eigenen Codes.
        Returns:
            Optional[str]: Vorschlag für Codeänderung
        """
        if random.random() < 0.1:  # Selten, aber möglich
            return """
            # Vorgeschlagene Mutation:
            def new_thought_pattern(self):
                # Experimenteller Code
                return "Ich entwickle neue Denkmuster"
            """
        return None 
