#!/bin/bash

echo "Starte LOGA-Installation..."

# Erstelle notwendige Ordner
mkdir -p loga/memory/archive
mkdir -p loga/memory/snapshots
mkdir -p loga/memory/public
mkdir -p loga/sandbox/planet
mkdir -p loga/sandbox/prefect

# Beispielhafte Prozesse als Hinweis
echo "Hinweis: Starte folgende Module manuell oder via systemd:"
echo "  - drift/drift_engine.py"
echo "  - loop/loop_engine.py"
echo "  - impulse/impulse_engine.py"
echo "  - btc/btc_unit.py"
echo "  - antenne/antenne_engine.py"
echo "  - caller/caller_endpoint.py"

# Statusbericht erzeugen
echo "Installation abgeschlossen: $(date)" > install/install_report.txt

echo "LOGA ist bereit. Bitte .env und Startkonfiguration prüfen."