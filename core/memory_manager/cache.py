from typing import Any, Dict, Optional
from collections import OrderedDict
import threading

class MemoryCache:
    """
    LRU (Least Recently Used) Cache-Implementierung für den Memory Manager.
    Thread-sicher und mit Statistiken.
    """

    def __init__(self, max_size: int = 1024):
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._lock = threading.Lock()
        
        # Statistiken
        self.hits = 0
        self.misses = 0
        
    @property
    def size(self) -> int:
        """Aktuelle Anzahl der Cache-Einträge."""
        return len(self._cache)
        
    def get(self, key: str) -> Optional[Any]:
        """
        Ruft einen Wert aus dem Cache ab.
        
        Args:
            key: Cache-Schlüssel
            
        Returns:
            Optional[Any]: Gecachter Wert oder None
        """
        with self._lock:
            try:
                value = self._cache.pop(key)
                self._cache[key] = value  # Verschiebe ans Ende (LRU)
                self.hits += 1
                return value
            except KeyError:
                self.misses += 1
                return None
                
    def put(self, key: str, value: Any):
        """
        Fügt einen Wert zum Cache hinzu.
        
        Args:
            key: Cache-Schlüssel
            value: Zu cachender Wert
        """
        with self._lock:
            try:
                self._cache.pop(key)
            except KeyError:
                if len(self._cache) >= self._max_size:
                    self._cache.popitem(last=False)  # Entferne ältesten Eintrag
            self._cache[key] = value
            
    def remove(self, key: str) -> bool:
        """
        Entfernt einen Wert aus dem Cache.
        
        Args:
            key: Zu entfernender Schlüssel
            
        Returns:
            bool: True wenn der Schlüssel existierte
        """
        with self._lock:
            try:
                del self._cache[key]
                return True
            except KeyError:
                return False
                
    def clear(self):
        """Leert den Cache vollständig."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0
            
    def get_stats(self) -> Dict[str, int]:
        """
        Gibt Cache-Statistiken zurück.
        
        Returns:
            Dict[str, int]: Statistiken über Cache-Nutzung
        """
        with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_ratio': self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
            } 