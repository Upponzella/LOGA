import os
import json
import logging
import shutil
from datetime import datetime
from typing import Any, Dict, Optional, List
from .cache import MemoryCache

class MemoryManager:
    """
    Zentrales Speicherverwaltungssystem für LOGA.
    Verwaltet Kern- und Archivdaten mit Caching und Backup.
    """

    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config = self._load_config()
        self._setup_logging()
        
        self.cache = MemoryCache(self.config['performance']['cache_size'])
        self.index = self._load_index()
        
    def _load_config(self) -> dict:
        """Lädt die Systemkonfiguration."""
        try:
            config_path = os.path.join(self.base_path, 'config.yaml')
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.critical(f"Kritischer Fehler beim Laden der Speicherkonfiguration: {str(e)}")
            raise

    def _setup_logging(self):
        """Initialisiert das Memory-Logging."""
        log_dir = os.path.join(self.base_path, self.config['logging']['directory'])
        os.makedirs(log_dir, exist_ok=True)
        
        self.logger = logging.getLogger('memory')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(
            os.path.join(log_dir, 'memory.log'),
            encoding='utf-8'
        )
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - [MEMORY] - %(message)s')
        )
        self.logger.addHandler(handler)

    def _load_index(self) -> dict:
        """Lädt den Speicherindex."""
        try:
            index_path = os.path.join(self.base_path, 'memory/core/index.json')
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {'core': {}, 'archive': {}}
        except Exception as e:
            self.logger.error(f"Fehler beim Laden des Index: {str(e)}")
            return {'core': {}, 'archive': {}}

    def _save_index(self):
        """Speichert den aktualisierten Index."""
        try:
            index_path = os.path.join(self.base_path, 'memory/core/index.json')
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern des Index: {str(e)}")

    def store(self, key: str, data: Any, permanent: bool = False) -> bool:
        """
        Speichert Daten im Speichersystem.
        
        Args:
            key: Eindeutiger Schlüssel
            data: Zu speichernde Daten
            permanent: Ob die Daten permanent gespeichert werden sollen
            
        Returns:
            bool: Erfolg der Operation
        """
        try:
            # Cache aktualisieren
            self.cache.put(key, data)
            
            if permanent:
                # Permanente Speicherung
                storage_path = os.path.join(
                    self.base_path,
                    'memory/core',
                    f"{key}.json"
                )
                with open(storage_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                # Index aktualisieren
                self.index['core'][key] = {
                    'path': storage_path,
                    'timestamp': datetime.now().isoformat(),
                    'size': os.path.getsize(storage_path)
                }
                self._save_index()
            
            self.logger.info(f"Daten gespeichert: {key} (permanent={permanent})")
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern von {key}: {str(e)}")
            return False

    def retrieve(self, key: str) -> Optional[Any]:
        """
        Ruft Daten aus dem Speichersystem ab.
        
        Args:
            key: Schlüssel der Daten
            
        Returns:
            Optional[Any]: Die gespeicherten Daten oder None
        """
        try:
            # Versuche Cache-Zugriff
            cached_data = self.cache.get(key)
            if cached_data is not None:
                self.logger.debug(f"Cache-Treffer: {key}")
                return cached_data
            
            # Versuche permanenten Speicher
            if key in self.index['core']:
                file_path = self.index['core'][key]['path']
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.cache.put(key, data)
                self.logger.debug(f"Daten aus Speicher geladen: {key}")
                return data
                
            # Versuche Archiv
            if key in self.index['archive']:
                return self._retrieve_from_archive(key)
            
            self.logger.warning(f"Daten nicht gefunden: {key}")
            return None
            
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von {key}: {str(e)}")
            return None

    def _retrieve_from_archive(self, key: str) -> Optional[Any]:
        """Ruft Daten aus dem Archiv ab."""
        try:
            archive_path = self.index['archive'][key]['path']
            with open(archive_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen aus dem Archiv: {key}: {str(e)}")
            return None

    def archive(self, key: str) -> bool:
        """
        Verschiebt Daten ins Archiv.
        
        Args:
            key: Schlüssel der zu archivierenden Daten
            
        Returns:
            bool: Erfolg der Operation
        """
        try:
            if key not in self.index['core']:
                self.logger.warning(f"Keine Daten zum Archivieren gefunden: {key}")
                return False
            
            source_path = self.index['core'][key]['path']
            archive_path = os.path.join(
                self.base_path,
                'memory/archive',
                f"{key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            # Datei ins Archiv verschieben
            shutil.move(source_path, archive_path)
            
            # Index aktualisieren
            self.index['archive'][key] = {
                'path': archive_path,
                'timestamp': datetime.now().isoformat(),
                'original_timestamp': self.index['core'][key]['timestamp']
            }
            del self.index['core'][key]
            
            # Cache leeren
            self.cache.remove(key)
            
            self._save_index()
            self.logger.info(f"Daten archiviert: {key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler beim Archivieren von {key}: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """
        Löscht Daten aus dem Speichersystem.
        
        Args:
            key: Schlüssel der zu löschenden Daten
            
        Returns:
            bool: Erfolg der Operation
        """
        try:
            # Cache leeren
            self.cache.remove(key)
            
            # Aus Kernspeicher löschen
            if key in self.index['core']:
                os.remove(self.index['core'][key]['path'])
                del self.index['core'][key]
                self._save_index()
                self.logger.info(f"Daten gelöscht: {key}")
                return True
                
            self.logger.warning(f"Keine Daten zum Löschen gefunden: {key}")
            return False
            
        except Exception as e:
            self.logger.error(f"Fehler beim Löschen von {key}: {str(e)}")
            return False

    def list_keys(self, include_archived: bool = False) -> List[str]:
        """
        Listet alle verfügbaren Schlüssel auf.
        
        Args:
            include_archived: Ob archivierte Schlüssel einbezogen werden sollen
            
        Returns:
            List[str]: Liste der Schlüssel
        """
        keys = list(self.index['core'].keys())
        if include_archived:
            keys.extend(self.index['archive'].keys())
        return keys

    def get_stats(self) -> Dict[str, Any]:
        """
        Gibt Statistiken über den Speicherverbrauch zurück.
        
        Returns:
            Dict[str, Any]: Speicherstatistiken
        """
        stats = {
            'core_items': len(self.index['core']),
            'archive_items': len(self.index['archive']),
            'cache_size': self.cache.size,
            'cache_hits': self.cache.hits,
            'cache_misses': self.cache.misses
        }
        
        # Berechne Gesamtgröße
        total_size = 0
        for item in self.index['core'].values():
            total_size += item['size']
        stats['total_size'] = total_size
        
        return stats

    def cleanup(self):
        """Führt Aufräumarbeiten durch."""
        self.cache.clear()
        self._save_index() 
