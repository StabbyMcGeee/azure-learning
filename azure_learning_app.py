#!/usr/bin/env python3

import json
import os
import random
import sqlite3
import sys
import time
import tkinter as tk
import webbrowser
from datetime import date, datetime, timedelta
from tkinter import filedialog, font as tkfont, messagebox, ttk

APP_DIR = (
    os.path.dirname(os.path.abspath(sys.executable))
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
DB_PATH = os.path.join(APP_DIR, "azure_learning.db")

AZURE_BLUE = "#0A84FF"
AZURE_LIGHT = "#8FD3FF"
AZURE_DARK = "#03070C"
AZURE_NAVY = "#B8E3FF"
AZURE_PALE = "#07111C"
AZURE_BORDER = "#244862"
WHITE = "#101D2B"
INK = "#F4F9FF"
MUTED = "#A7C1D3"
TEXT_ON_ACCENT = "#03111E"
SURFACE = "#142536"
SURFACE_RAISED = "#193249"
SURFACE_ACCENT = "#0B2942"
SURFACE_SELECTED = "#16466A"
SUCCESS_SURFACE = "#103827"
ERROR_SURFACE = "#401C29"

QUESTION_TYPE_LABELS = {
    "all": "Alle Fragentypen",
    "single": "Single Choice",
    "multi": "Multiple Choice",
    "true_false": "Ja / Nein",
    "ordering": "Drag & Drop / Reihenfolge",
    "drag_drop": "Drag & Drop",
    "build_list": "Build List",
    "matching": "Zuordnung",
    "hot_area": "Hot Area",
    "active_screen": "Active Screen",
    "case": "Fallstudie",
}

DOMAIN_LABELS = {
    "all": "Alle Prüfungsbereiche",
    "cloud": "Cloud Concepts",
    "architecture": "Azure Architecture and Services",
    "governance": "Azure Management and Governance",
}

DOMAIN_UI_LABELS = {
    "cloud": "Cloud-Konzepte",
    "architecture": "Azure-Architektur und -Dienste",
    "governance": "Azure-Verwaltung und Governance",
}

DIFFICULTY_LABELS = {
    "all": "Alle Schwierigkeitsgrade",
    "1": "Grundlagen",
    "2": "Anwendung",
    "3": "Szenario",
    "4": "Fortgeschrittenes Szenario",
}

# Registry of exam simulations. Each entry appears as its own tab/category so
# additional certifications (SC-900, AZ-104, ...) can be added later without
# restructuring the UI — just add a catalog entry and question bank filtered
# by the matching "exam" field, then flip "status" to "active".
ACTIVE_EXAM_ID = "AZ-900"
EXAM_CATALOG = [
    {"id": "AZ-900", "name": "AZ-900: Azure Fundamentals", "status": "active"},
    {"id": "SC-900", "name": "SC-900: Security, Compliance & Identity Fundamentals", "status": "planned"},
    {"id": "AZ-104", "name": "AZ-104: Azure Administrator", "status": "planned"},
]

# Leitner-style spaced repetition: 6 boxes with growing review intervals (days).
# A wrong answer always resets a question to box 1 / interval 1 day, a correct
# answer promotes it to the next box, spacing out reviews of well-known material.
SR_BOX_INTERVALS = [1, 2, 4, 8, 16, 32]

# Midpoints of Microsoft's published AZ-900 skills-measured weighting
# (Cloud concepts 25-30%, Architecture & services 35-40%, Governance 30-35%),
# used to compute a blueprint-weighted "scaled score" instead of a flat
# percentage — this is what makes practice accuracy realistically comparable
# to the real exam, since the real exam weighs domains unevenly.
EXAM_DOMAIN_WEIGHTS = {"cloud": 0.275, "architecture": 0.375, "governance": 0.325}
EXAM_PASS_SCALED_SCORE = 700

QUESTION_TYPE_DESCRIPTIONS = {
    "single": "Eine beste Antwort aus mehreren Optionen auswählen.",
    "multi": "Mehrere zutreffende Antworten erkennen und auswählen.",
    "true_false": "Eine Aussage anhand der Azure-Grundlagen bewerten.",
    "ordering": "Schritte oder Konzepte per Drag & Drop richtig sortieren.",
    "drag_drop": "Elemente mit der Maus in die geforderte Reihenfolge ziehen.",
    "build_list": "Eine gültige Bereitstellungs- oder Prozessliste aufbauen.",
    "matching": "Azure-Dienste, Eigenschaften und Szenarien zuordnen.",
    "hot_area": "Die passende Stelle beziehungsweise Funktion auswählen.",
    "active_screen": "Eine realistische Azure-Portal-Ansicht interpretieren.",
    "case": "Ein Szenario lesen und die Anforderungen daraus ableiten.",
}

QUESTION_BANK = [
    {
        "id": "az900-001",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welches Cloud-Servicemodell stellt eine fertige Anwendung bereit, ohne dass der Kunde Server oder Betriebssystem verwalten muss?",
        "options": ["IaaS", "PaaS", "SaaS", "Private Cloud"],
        "answer": "SaaS",
        "explanation": "SaaS bedeutet Software as a Service: Der Anbieter verwaltet Anwendung, Plattform und Infrastruktur, der Kunde nutzt die fertige Anwendung direkt über Browser oder Client. Bei IaaS verwaltet der Kunde noch Betriebssystem und Laufzeitumgebung selbst, bei PaaS zumindest die Anwendungslogik und Daten. Private Cloud ist kein Servicemodell, sondern ein Bereitstellungsmodell und beschreibt, wem die Infrastruktur exklusiv zur Verfügung steht.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 1,
    },
    {
        "id": "az900-002",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Aussagen beschreiben Verbrauchsbasierte Cloud-Kosten korrekt? Wähle alle zutreffenden Antworten.",
        "options": [
            "Kosten hängen von der genutzten Kapazität ab.",
            "Kapazität muss immer im Voraus gekauft werden.",
            "Kosten werden häufig als OPEX statt CAPEX betrachtet.",
            "Unbenutzte Ressourcen verursachen oft weiterhin laufende Kosten."
        ],
        "answer": ["Kosten hängen von der genutzten Kapazität ab.", "Kosten werden häufig als OPEX statt CAPEX betrachtet.", "Unbenutzte Ressourcen verursachen oft weiterhin laufende Kosten."],
        "explanation": "Verbrauchsbasierte Abrechnung ist an tatsächliche Nutzung und laufenden Betrieb gekoppelt. Das gilt oft als OPEX und ist kein langfristiger Vorabkauf.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/",
        "difficulty": 2,
    },
    {
        "id": "az900-003",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "In einem Public Cloud-Modell teilen Kunde und Anbieter immer genau dieselben Sicherheitsverantwortungen.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Das Shared Responsibility Model teilt Aufgaben auf; je nach Servicemodell liegen unterschiedliche Verantwortlichkeiten beim Anbieter und Kunden.",
        "source": "https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility",
        "difficulty": 2,
    },
    {
        "id": "az900-004",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welche Eigenschaft beschreibt Skalierbarkeit am treffendsten?",
        "options": ["Mehrere Datenbanken mit identischer Sicherung", "Automatische Anpassung von Kapazität an Last", "Direkte Backup-Sicherung ohne Netzwerk", "Verwendung eines eigenen Rechenzentrums"],
        "answer": "Automatische Anpassung von Kapazität an Last",
        "explanation": "Skalierbarkeit bedeutet, dass Ressourcen je nach Last erhöht oder verringert werden können, entweder durch weitere Instanzen (horizontal) oder größere Instanzen (vertikal). Mehrere identisch gesicherte Datenbanken beschreiben Redundanz statt Skalierung, ein Backup ohne Netzwerk betrifft Datensicherung, und ein eigenes Rechenzentrum ist das Gegenteil eines Cloud-Merkmals.",
        "source": "https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/",
        "difficulty": 1,
    },
    {
        "id": "az900-005",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welches Szenario passt am besten zu einer Hybrid Cloud?",
        "options": [
            "Alle Anwendungen laufen ausschließlich in einer Public Cloud.",
            "Workloads werden zwischen einem lokalen Standort und Azure verteilt.",
            "Es gibt keine lokale IT-Verantwortung mehr.",
            "Daten werden ausschließlich im Browser gespeichert."
        ],
        "answer": "Workloads werden zwischen einem lokalen Standort und Azure verteilt.",
        "explanation": "Hybrid Cloud kombiniert lokale und Public-Cloud-Umgebungen, etwa für Übergangsszenarien, Datenresidenz-Anforderungen oder schrittweise Migration. Läuft alles ausschließlich in der Public Cloud, handelt es sich um ein reines Public-Cloud-Modell; ohne jede lokale Verantwortung oder mit reiner Browser-Speicherung liegt ebenfalls keine Hybrid-Architektur vor.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/",
        "difficulty": 2,
    },
    {
        "id": "az900-006",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "ordering",
        "prompt": "Ordne die Modelle nach steigendem Grad an eigener Infrastrukturverwaltung: SaaS → PaaS → IaaS.",
        "options": ["SaaS", "PaaS", "IaaS"],
        "answer": ["SaaS", "PaaS", "IaaS"],
        "explanation": "Bei SaaS verwaltet der Kunde am wenigsten; bei IaaS verwaltet er die meisten Betriebssystem- und Plattformaspekte selbst.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 2,
    },
    {
        "id": "az900-007",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Was beschreibt Serverless Computing am besten?",
        "options": [
            "Es gibt keine Server im Betrieb.",
            "Der Anbieter verwaltet die Infrastruktur, während der Kunde auf Funktionen fokussiert.",
            "Serverless ist immer günstiger als jede VM.",
            "Serverless eignet sich nur für Datenbanken."
        ],
        "answer": "Der Anbieter verwaltet die Infrastruktur, während der Kunde auf Funktionen fokussiert.",
        "explanation": "Serverless Computing bedeutet, dass der Cloud-Anbieter die zugrunde liegende Infrastruktur (Server, Skalierung, Patching) vollständig verwaltet, während sich Entwickler ausschließlich auf den Anwendungscode bzw. einzelne Funktionen konzentrieren. Es gibt weiterhin physische Server, nur eben unsichtbar für den Kunden; Serverless ist nicht pauschal günstiger als jede VM (es hängt vom Nutzungsmuster ab), und es ist nicht auf Datenbanken beschränkt, sondern eignet sich z. B. auch für ereignisgesteuerte Funktionen und APIs.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-008",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Vorteile bietet Cloud Computing typischerweise? Wähle alle zutreffenden Antworten.",
        "options": ["Elastische Skalierung", "Globalere Reichweite", "Automatische Freiheitsgewährung ohne Governance", "Pay-as-you-go"],
        "answer": ["Elastische Skalierung", "Globalere Reichweite", "Pay-as-you-go"],
        "explanation": "Cloud bietet oft Elastizität, globale Bereitstellung und Verbrauchsorientierung. Governance bleibt trotzdem nötig.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/",
        "difficulty": 1,
    },
    {
        "id": "az900-009",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Azure-Komponente dient als logische Gruppierung verwandter Ressourcen für Verwaltung, Bereitstellung und Lebenszyklus?",
        "options": ["Region Pair", "Resource Group", "Availability Zone", "Resource Lock"],
        "answer": "Resource Group",
        "explanation": "Eine Resource Group bündelt zusammengehörige Ressourcen (z. B. eine App mit Datenbank und Netzwerk) logisch für gemeinsame Verwaltung, Bereitstellung, Berechtigungen und Lebenszyklus. Ein Region Pair beschreibt zwei miteinander verknüpfte Azure-Regionen, eine Availability Zone einen physisch getrennten Standort innerhalb einer Region, und ein Resource Lock verhindert nur versehentliches Löschen oder Ändern einzelner Ressourcen.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview",
        "difficulty": 1,
    },
    {
        "id": "az900-010",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Was ist der Hauptzweck von Availability Zones?",
        "options": [
            "Ermittlung möglicher Kosten.",
            "Schutz vor Ausfällen einzelner Rechenzentrum-Standorte innerhalb einer Region.",
            "Ersetzen von Azure Resource Groups.",
            "Erlauben einfaches DNS-Management."
        ],
        "answer": "Schutz vor Ausfällen einzelner Rechenzentrum-Standorte innerhalb einer Region.",
        "explanation": "Availability Zones sind physisch getrennte Standorte mit eigener Stromversorgung, Kühlung und Netzwerk innerhalb derselben Region und schützen so vor dem Ausfall eines einzelnen Rechenzentrums. Sie dienen nicht der Kostenermittlung, ersetzen keine Resource Groups (ein anderes Konzept auf Verwaltungsebene) und haben nichts mit DNS-Management zu tun.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-011",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "matching",
        "prompt": "Ordne die Azure-Dienste ihren sinnvollsten Zwecken zu.",
        "pairs": [
            ["Azure Functions", "Ereignisgesteuerte serverlose Ausführung"],
            ["Azure Virtual Machines", "Volle Kontrolle über das Gastbetriebssystem"],
            ["Azure App Service", "Verwaltetes Hosting für Webanwendungen"]
        ],
        "answer": [
            ["Azure Functions", "Ereignisgesteuerte serverlose Ausführung"],
            ["Azure Virtual Machines", "Volle Kontrolle über das Gastbetriebssystem"],
            ["Azure App Service", "Verwaltetes Hosting für Webanwendungen"]
        ],
        "explanation": "Die Wahl hängt davon ab, wie viel Infrastruktur- und Betriebssystemkontrolle man benötigt.",
        "source": "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree",
        "difficulty": 2,
    },
    {
        "id": "az900-012",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "multi",
        "prompt": "Welche Dienste gehören zu Azure Networking? Wähle alle zutreffenden Antworten.",
        "options": ["Virtual Network", "VPN Gateway", "ExpressRoute", "Azure Table Storage"],
        "answer": ["Virtual Network", "VPN Gateway", "ExpressRoute"],
        "explanation": "Virtual Network, VPN Gateway und ExpressRoute sind Netzwerk-/Verbindungsdienste. Table Storage ist ein Speicher-Dienst.",
        "source": "https://learn.microsoft.com/en-us/azure/networking/",
        "difficulty": 2,
    },
    {
        "id": "az900-013",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Ein Unternehmen braucht eine private, sichere Verbindung von einem lokalen Rechenzentrum zu Azure ohne das öffentliche Internet. Welcher Dienst ist passend?",
        "options": ["Azure DNS", "ExpressRoute", "Public Endpoint", "Azure CDN"],
        "answer": "ExpressRoute",
        "explanation": "ExpressRoute stellt über einen Konnektivitätsanbieter eine dedizierte, private Verbindung zwischen einem lokalen Rechenzentrum und Azure her, die nicht über das öffentliche Internet läuft und höhere Zuverlässigkeit, geringere Latenz sowie höhere Bandbreite bietet als eine Standard-Internetverbindung. Azure DNS löst nur Namen auf, ein Public Endpoint ist über das Internet erreichbar, und Azure CDN beschleunigt lediglich die Auslieferung statischer Inhalte.",
        "source": "https://learn.microsoft.com/en-us/azure/expressroute/",
        "difficulty": 2,
    },
    {
        "id": "az900-014",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Speicheroption eignet sich besonders für unstrukturierte Objekte wie Bilder, Videos und Backups?",
        "options": ["Blob Storage", "Azure SQL Database", "Queue Storage", "Azure DNS"],
        "answer": "Blob Storage",
        "explanation": "Blob Storage speichert große Mengen unstrukturierter Objektdaten wie Bilder, Videos oder Backups kosteneffizient über Access Tiers (Hot/Cool/Archive). Azure SQL Database ist für strukturierte, relationale Daten gedacht, Queue Storage dient dem asynchronen Nachrichtenaustausch zwischen Anwendungskomponenten, und Azure DNS löst lediglich Domainnamen auf — keiner der drei eignet sich als primärer Objektspeicher.",
        "source": "https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction",
        "difficulty": 1,
    },
    {
        "id": "az900-015",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "multi",
        "prompt": "Welche Redundanzoptionen replizieren Daten in eine zweite Region? Wähle alle zutreffenden Antworten.",
        "options": ["LRS", "GRS", "GZRS", "ZRS"],
        "answer": ["GRS", "GZRS"],
        "explanation": "Geo-redundante Optionen verteilen Daten auf eine sekundäre Region. LRS und ZRS sind regional.",
        "source": "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy",
        "difficulty": 2,
    },
    {
        "id": "az900-016",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Funktion von Microsoft Entra kann basierend auf Bedingungen zusätzliche Anforderungen wie MFA erzwingen?",
        "options": ["Microsoft Entra Conditional Access", "Resource Lock", "Azure Advisor", "Azure Migrate"],
        "answer": "Microsoft Entra Conditional Access",
        "explanation": "Microsoft Entra Conditional Access wertet Signale wie Benutzerrisiko, Standort oder Gerätezustand aus und erzwingt darauf basierend Richtlinien wie Multi-Faktor-Authentifizierung oder Zugriffssperren. Ein Resource Lock verhindert nur Löschen/Ändern von Ressourcen, Azure Advisor gibt Empfehlungen, und Azure Migrate unterstützt Migrationsprojekte — keines davon ist eine bedingte Zugriffssteuerung für Identitäten.",
        "source": "https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-017",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welches Prinzip geht davon aus, dass Zugriff nicht automatisch vertraut werden darf und ständig überprüft werden muss?",
        "options": ["Defense in Depth", "Zero Trust", "Economies of Scale", "Elasticity"],
        "answer": "Zero Trust",
        "explanation": "Zero Trust basiert auf den Prinzipien 'explizit verifizieren', 'geringstmögliche Rechte verwenden' und 'von einer Sicherheitsverletzung ausgehen' – Zugriff wird nie automatisch vertraut. Defense in Depth beschreibt mehrschichtige Sicherheitskontrollen statt eines Vertrauensmodells, Economies of Scale betrifft Kosteneffekte großer Anbieter, und Elastizität ist ein Skalierungskonzept ohne Sicherheitsbezug.",
        "source": "https://learn.microsoft.com/en-us/security/zero-trust/",
        "difficulty": 2,
    },
    {
        "id": "az900-018",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welcher Dienst eignet sich für mehrere identische VMs, die automatisch skaliert und verteilt werden?",
        "options": ["VM Scale Sets", "Azure Data Box", "Azure Policy", "Microsoft Purview"],
        "answer": "VM Scale Sets",
        "explanation": "VM Scale Sets erstellen und verwalten eine Gruppe identisch konfigurierter, lastverteilter VMs, die je nach Auslastung automatisch hoch- oder herunterskaliert werden. Azure Data Box dient dem physischen Massendatentransfer, Azure Policy erzwingt Compliance-Regeln, und Microsoft Purview betrifft Daten-Governance — keines davon skaliert VM-Gruppen.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-019",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Was beschreibt ein Private Endpoint am besten?",
        "options": [
            "Eine öffentliche IP für jede Ressource.",
            "Eine private IP-Adresse in einem VNet für den privaten Zugriff auf einen Azure-Dienst.",
            "Eine Kostenwarnung.",
            "Ein Backup in einer zweiten Region."
        ],
        "answer": "Eine private IP-Adresse in einem VNet für den privaten Zugriff auf einen Azure-Dienst.",
        "explanation": "Ein Private Endpoint ist eine private IP-Adresse aus einem VNet-Subnetz, über die ein Azure-Dienst privat erreichbar ist, ohne dass der Datenverkehr über das öffentliche Internet läuft. Er ist keine öffentliche IP, keine Kostenwarnung und kein Backup-Mechanismus – dafür wären Azure Backup oder Georedundanz zuständig.",
        "source": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-020",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "ordering",
        "prompt": "Ordne die Azure-Verwaltungshierarchie von oben nach unten.",
        "options": ["Management Group", "Subscription", "Resource Group", "Resource"],
        "answer": ["Management Group", "Subscription", "Resource Group", "Resource"],
        "explanation": "Management Groups enthalten Subscriptions, diese enthalten Resource Groups und darin Ressourcen.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-021",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welcher Dienst unterstützt Discovery, Bewertung und Migration lokaler Server und Anwendungen nach Azure?",
        "options": ["Azure Migrate", "Azure Monitor", "Azure DNS", "Azure Firewall Manager"],
        "answer": "Azure Migrate",
        "explanation": "Azure Migrate bietet ein zentrales Hub zur Discovery, Bewertung (z. B. Rightsizing, Kostenschätzung) und eigentlichen Migration lokaler Server, Datenbanken und Anwendungen nach Azure. Azure Monitor überwacht bereits laufende Ressourcen, Azure DNS löst Namen auf, und Firewall Manager verwaltet Firewall-Richtlinien — keines davon unterstützt den Migrationsprozess selbst.",
        "source": "https://learn.microsoft.com/en-us/azure/migrate/",
        "difficulty": 2,
    },
    {
        "id": "az900-022",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welcher Dienst ist ein verwaltetes Verzeichnis für Identitäten und Zugriffe in Azure?",
        "options": ["Microsoft Entra ID", "Azure Files", "Azure Bastion", "Azure Front Door"],
        "answer": "Microsoft Entra ID",
        "explanation": "Microsoft Entra ID ist Azures cloudbasierter Verzeichnis- und Identitätsdienst für Benutzer, Gruppen, Anmeldung und Zugriffsverwaltung. Azure Files ist ein Datei-Speicherdienst, Azure Bastion ermöglicht sicheren VM-Zugriff ohne öffentliche IP, und Azure Front Door ist ein globaler Anwendungs- und Content-Delivery-Dienst – keiner davon verwaltet Identitäten.",
        "source": "https://learn.microsoft.com/en-us/entra/identity/",
        "difficulty": 1,
    },
    {
        "id": "az900-023",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welches Tool schätzt voraussichtliche Kosten für geplante Azure-Ressourcen vor der Bereitstellung?",
        "options": ["Pricing Calculator", "Azure Advisor", "Azure Service Health", "Azure Policy"],
        "answer": "Pricing Calculator",
        "explanation": "Der Azure Pricing Calculator ermöglicht das Konfigurieren geplanter Ressourcen und liefert eine Kostenschätzung vor der Bereitstellung, ideal zum Vergleichen von Architekturoptionen. Azure Advisor gibt Empfehlungen zu bereits laufenden Ressourcen, Azure Service Health informiert über Dienststatus, und Azure Policy erzwingt Regeln — keines davon dient der Vorab-Kostenschätzung.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/pricing-calculator",
        "difficulty": 1,
    },
    {
        "id": "az900-024",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welches Feature hilft, Azure-Ressourcen nach Projekt, Kostenstelle oder Umgebung zu organisieren und Kosten zu analysieren?",
        "options": ["Tags", "Availability Sets", "Managed Identities", "Regions"],
        "answer": "Tags",
        "explanation": "Tags sind frei definierbare Schlüssel-Wert-Metadaten, die Ressourcen z. B. nach Projekt, Kostenstelle oder Umgebung kennzeichnen und so Organisation sowie Kostenanalyse in Cost Management erleichtern. Availability Sets betreffen die Verfügbarkeit von VMs, Managed Identities die Authentifizierung von Ressourcen gegenüber anderen Diensten, und Regions beschreiben nur den geografischen Standort – keines davon dient der Kostenorganisation.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources",
        "difficulty": 1,
    },
    {
        "id": "az900-025",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Du willst vermeiden, dass eine Ressource versehentlich gelöscht wird. Welches Feature nutzt du?",
        "options": ["Resource Lock", "Service Tag", "Route Table", "Availability Zone"],
        "answer": "Resource Lock",
        "explanation": "Ein Resource Lock (CanNotDelete oder ReadOnly) schützt eine Ressource gezielt vor versehentlichem Löschen oder Ändern, unabhängig von RBAC-Berechtigungen. Ein Service Tag ist lediglich eine Gruppe von IP-Adressbereichen für Netzwerkregeln, eine Route Table steuert den Netzwerkverkehr, und eine Availability Zone betrifft die physische Verteilung von Ressourcen — keines davon verhindert Löschvorgänge.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources",
        "difficulty": 2,
    },
    {
        "id": "az900-026",
        "exam": "AZ-900",
        "category": "governance",
        "type": "multi",
        "prompt": "Welche Aussagen zu Azure Policy sind richtig? Wähle alle zutreffenden Antworten.",
        "options": [
            "Azure Policy kann Organisationsstandards erzwingen oder bewerten.",
            "Azure Policy kann erlaubte Regionen beschränken.",
            "Azure Policy ersetzt RBAC vollständig.",
            "Azure Policy kann Compliance-Zustände auswerten."
        ],
        "answer": [
            "Azure Policy kann Organisationsstandards erzwingen oder bewerten.",
            "Azure Policy kann erlaubte Regionen beschränken.",
            "Azure Policy kann Compliance-Zustände auswerten."
        ],
        "explanation": "Azure Policy steuert Konfigurationen und Compliance-Richtlinien, während RBAC Berechtigungen steuert.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-027",
        "exam": "AZ-900",
        "category": "governance",
        "type": "matching",
        "prompt": "Ordne das Tool zu seiner Hauptaufgabe.",
        "pairs": [
            ["Azure Advisor", "Empfehlungen für Zuverlässigkeit, Sicherheit, Performance und Kosten"],
            ["Azure Service Health", "Statusinformationen zu Azure-Services und Wartungen"],
            ["Azure Monitor", "Metriken, Logs und Warnungen"],
            ["Microsoft Purview", "Daten-Governance und Datenkatalog"]
        ],
        "answer": [
            ["Azure Advisor", "Empfehlungen für Zuverlässigkeit, Sicherheit, Performance und Kosten"],
            ["Azure Service Health", "Statusinformationen zu Azure-Services und Wartungen"],
            ["Azure Monitor", "Metriken, Logs und Warnungen"],
            ["Microsoft Purview", "Daten-Governance und Datenkatalog"]
        ],
        "explanation": "Azure Advisor bewertet bestehende Ressourcen und liefert Empfehlungen zu Zuverlässigkeit, Sicherheit, Performance und Kosten. Azure Service Health informiert über den Status von Azure-Diensten und geplante Wartungen, die dein Abonnement betreffen. Azure Monitor sammelt Metriken, Logs und löst Warnungen aus. Microsoft Purview verwaltet Daten-Governance, Klassifizierung und einen unternehmensweiten Datenkatalog. Obwohl sich die Tools ergänzen, hat jedes einen klar abgegrenzten Hauptzweck.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/",
        "difficulty": 2,
    },
    {
        "id": "az900-028",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welches Tool bietet eine browserbasierte Shell mit Azure CLI und Azure PowerShell ohne lokale Installation?",
        "options": ["Azure Cloud Shell", "Azure Arc", "Azure Resource Graph", "Azure DevTest Labs"],
        "answer": "Azure Cloud Shell",
        "explanation": "Azure Cloud Shell ist eine browserbasierte, vorkonfigurierte Shell-Umgebung mit Azure CLI und Azure PowerShell, die direkt im Portal genutzt werden kann, ohne dass eine lokale Installation oder Konfiguration notwendig ist. Azure Arc verwaltet Ressourcen außerhalb von Azure, Azure Resource Graph dient der Abfrage von Ressourcenmetadaten, und DevTest Labs stellt Entwicklungs-/Testumgebungen bereit — keines davon ist eine Shell-Umgebung im Browser.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-shell/overview",
        "difficulty": 1,
    },
    {
        "id": "az900-029",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Was ist der Hauptzweck von Azure Resource Manager (ARM)?",
        "options": [
            "Verwaltung und Bereitstellung von Azure-Ressourcen über eine konsistente Ebene.",
            "Ersetzen aller Datenbanken.",
            "Bereitstellen physischer Kabel.",
            "Nur Überwachung von Benutzerpasswörtern."
        ],
        "answer": "Verwaltung und Bereitstellung von Azure-Ressourcen über eine konsistente Ebene.",
        "explanation": "Azure Resource Manager ist die zentrale Verwaltungsebene, über die alle Bereitstellungswerkzeuge (Portal, CLI, PowerShell, SDKs) Ressourcen konsistent erstellen, ändern und löschen. Er ersetzt keine Datenbanken, hat keinen Bezug zu physischen Kabeln und überwacht keine Passwörter – dafür sind Identitäts- bzw. Monitoring-Dienste zuständig.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-030",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welches Konzept beschreibt das deklarative Management von Infrastruktur mit Dateien, Versionierung und Wiederholbarkeit?",
        "options": ["Infrastructure as Code", "Manual Scaling", "Passwordless Authentication", "Data Sovereignty"],
        "answer": "Infrastructure as Code",
        "explanation": "Infrastructure as Code beschreibt Infrastruktur in Dateien (z. B. ARM-Templates oder Bicep), die versioniert, geprüft und wiederholt bereitgestellt werden können. Manual Scaling ist das Gegenteil einer automatisierten, deklarativen Vorgehensweise, Passwordless Authentication betrifft Anmeldeverfahren, und Data Sovereignty beschreibt rechtliche Anforderungen an den Datenstandort.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-031",
        "exam": "AZ-900",
        "category": "governance",
        "type": "true_false",
        "prompt": "Azure Monitor Application Insights ist ein Tool zur Überwachung von Anwendungsleistung und -nutzung.",
        "options": ["Wahr", "Falsch"],
        "answer": "Wahr",
        "explanation": "Die Aussage ist korrekt: Application Insights ist ein Feature von Azure Monitor und überwacht Live-Anwendungen hinsichtlich Performance-Kennzahlen (Antwortzeiten, Fehlerraten), Ausnahmen sowie Nutzungsverhalten, und ermöglicht so proaktives Erkennen von Problemen, bevor Nutzer sie melden.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-032",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-policy-tags",
        "case_order": 1,
        "case_text": "Ein Unternehmen möchte Entwicklungsressourcen auf genehmigte Regionen beschränken und die Nutzung nach Team auswerten. Die Lösung soll verbindliche Regeln verwenden und trotzdem eine nachvollziehbare Kosten- und Organisationszuordnung ermöglichen.",
        "prompt": "Ein Unternehmen will verhindern, dass Entwicklungsressourcen in teuren Regionen erstellt werden, und alle Ressourcen nach Team analysieren. Welche zwei Maßnahmen passen am besten?",
        "options": [
            "Azure Policy für erlaubte Regionen definieren.",
            "Tags wie team=development verwenden.",
            "Alle Ressourcen manuell prüfen und keine Regeln setzen.",
            "MFA deaktivieren."
        ],
        "answer": ["Azure Policy für erlaubte Regionen definieren.", "Tags wie team=development verwenden."],
        "explanation": "Policy setzt verbindliche Regeln durch; Tags unterstützen Kostenerfassung und Organisation.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-033",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst erweitert Azure-Verwaltung und Governance auf Server außerhalb von Azure?",
        "options": ["Azure Arc", "Azure Functions", "Azure Blob Storage", "Azure DNS"],
        "answer": "Azure Arc",
        "explanation": "Azure Arc erweitert Azure-Verwaltung, Richtlinien und Monitoring auf Server, Kubernetes-Cluster und Ressourcen außerhalb von Azure, etwa on-premises oder in anderen Clouds. Azure Functions ist ein serverloser Compute-Dienst, Azure Blob Storage ein Objektspeicher, und Azure DNS verwaltet nur Domainnamen – keiner davon verbindet externe Infrastruktur mit Azure-Governance.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-arc/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-034",
        "exam": "AZ-900",
        "category": "governance",
        "type": "multi",
        "prompt": "Welche Faktoren beeinflussen Azure-Kosten typischerweise? Wähle alle zutreffenden Antworten.",
        "options": ["Region", "Diensttyp und Größe", "Nutzungsdauer", "Farbe des Ressourcennamens"],
        "answer": ["Region", "Diensttyp und Größe", "Nutzungsdauer"],
        "explanation": "Kosten hängen unter anderem von Region, Größen, Nutzung und Datenverkehr ab. Der Name selbst ist irrelevant.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/",
        "difficulty": 1,
    },
    {
        "id": "az900-035",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Du brauchst eine Warnung, wenn eine Metrik einen Schwellenwert überschreitet. Welche Funktion nutzt du?",
        "options": ["Azure Monitor Alert", "Management Group", "Azure Data Box", "Resource Group"],
        "answer": "Azure Monitor Alert",
        "explanation": "Azure Monitor Alerts reagieren auf Metriken, Logs oder andere definierte Bedingungen und lösen Benachrichtigungen oder Aktionen (z. B. Autoscaling) aus. Eine Management Group bündelt Abonnements für Governance, Azure Data Box dient dem Offline-Datentransfer, und eine Resource Group ist nur ein Verwaltungscontainer – keines davon überwacht Schwellenwerte.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-036",
        "exam": "AZ-900",
        "category": "governance",
        "type": "ordering",
        "prompt": "Ordne einen typischen IaC-Workflow in sinnvoller Reihenfolge.",
        "options": ["Datei versionieren", "Änderung prüfen", "Bereitstellung ausführen", "Ressourcen validieren"],
        "answer": ["Datei versionieren", "Änderung prüfen", "Bereitstellung ausführen", "Ressourcen validieren"],
        "explanation": "Ein sauberer IaC-Workflow beginnt mit deklarativer Definition, geht durch Prüfung und Bereitstellung und endet mit Validierung.",
        "source": "https://learn.microsoft.com/en-us/azure/devops/",
        "difficulty": 2,
    },
    {
        "id": "az900-037",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst liefert personalisierte Empfehlungen zur Sicherheit, Zuverlässigkeit, Performance und Kosten von Azure-Ressourcen?",
        "options": ["Azure Advisor", "Azure Policy", "Microsoft Purview", "Azure Load Testing"],
        "answer": "Azure Advisor",
        "explanation": "Azure Advisor analysiert die Konfiguration und Nutzung bestehender Ressourcen und gibt personalisierte, umsetzbare Empfehlungen in den Kategorien Zuverlässigkeit, Sicherheit, Performance, Betriebsvortrefflichkeit und Kosten. Azure Policy erzwingt Regeln, statt Empfehlungen zu geben, Microsoft Purview betrifft Daten-Governance, und Azure Load Testing prüft die Leistungsfähigkeit unter Last — keines davon liefert allgemeine Best-Practice-Empfehlungen über alle Ressourcen hinweg.",
        "source": "https://learn.microsoft.com/en-us/azure/advisor/",
        "difficulty": 1,
    },
    {
        "id": "az900-038",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Was beschreibt Azure Service Health am treffendsten?",
        "options": [
            "Personalisierte Statusinformationen und geplante Wartungen, die eigene Ressourcen betreffen.",
            "Ein Tool zum Erstellen von VMs.",
            "Eine Datenbank für Blob-Dateien.",
            "Ein Ersatz für Conditional Access."
        ],
        "answer": "Personalisierte Statusinformationen und geplante Wartungen, die eigene Ressourcen betreffen.",
        "explanation": "Azure Service Health liefert personalisierte Informationen zu Serviceproblemen, geplanten Wartungen und Sicherheitshinweisen, die die eigenen Ressourcen betreffen. Es dient nicht zum Erstellen von VMs, ist keine Datenbank für Blob-Dateien und kein Ersatz für Conditional Access, das den bedingten Zugriff auf Identitätsebene steuert.",
        "source": "https://learn.microsoft.com/en-us/azure/service-health/",
        "difficulty": 2,
    },
    {
        "id": "az900-039",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welche Berechtigungsmethode weist Benutzern oder Gruppen Rollen auf Azure-Ressourcen zu?",
        "options": ["Azure RBAC", "Azure Pricing Calculator", "Azure Resource Health", "Azure CDN"],
        "answer": "Azure RBAC",
        "explanation": "Azure RBAC (Role-Based Access Control) weist Benutzern, Gruppen oder Diensten Rollen auf einem bestimmten Scope (Verwaltungsgruppe, Abonnement, Ressourcengruppe oder Ressource) zu und steuert so, welche Aktionen erlaubt sind. Der Pricing Calculator dient der Kostenschätzung, Resource Health zeigt den Zustand von Ressourcen, und Azure CDN beschleunigt Inhalte — keines davon regelt Zugriffsberechtigungen.",
        "source": "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview",
        "difficulty": 1,
    },
    {
        "id": "az900-040",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Service ist für die zentrale Sicht auf Azure-Metriken, Logs und Warnungen zuständig?",
        "options": ["Azure Monitor", "Azure Policy", "Azure Advisor", "Azure Arc"],
        "answer": "Azure Monitor",
        "explanation": "Azure Monitor sammelt und konsolidiert Metriken, Protokolle und Warnungen aus Azure- und Nicht-Azure-Ressourcen an einer zentralen Stelle. Azure Policy erzwingt Konfigurationsstandards statt Telemetrie zu sammeln, Azure Advisor gibt Optimierungsempfehlungen, und Azure Arc verwaltet externe Ressourcen – keines davon ist für zentrales Monitoring zuständig.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview",
        "difficulty": 1,
    },
    {
        "id": "az900-041",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welches Modell ist am besten für eine Organisation geeignet, die nur eine fertige Lösung statt eigener Infrastruktur verwenden will?",
        "options": ["IaaS", "PaaS", "SaaS", "On-premises"],
        "answer": "SaaS",
        "explanation": "SaaS ist die richtige Wahl, wenn eine Organisation ausschließlich eine fertige Anwendung nutzen möchte, ohne Infrastruktur oder Plattform zu betreiben. IaaS und PaaS erfordern weiterhin eigene Verwaltung von Betriebssystem bzw. Anwendungscode, und On-premises bedeutet, dass die Organisation die gesamte Infrastruktur selbst betreibt – das Gegenteil des gewünschten Szenarios.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/",
        "difficulty": 1,
    },
    {
        "id": "az900-042",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welches Azure-Feature eignet sich, um Ressourcennamen oder die Kostenanalyse nach Team, Projekt oder Umgebung zu gruppieren?",
        "options": ["Tags", "Availability Zones", "Managed Disk", "Subnet"],
        "answer": "Tags",
        "explanation": "Tags sind Name-Wert-Paare, die Ressourcen unabhängig von ihrer technischen Struktur nach Team, Projekt, Umgebung oder Kostenstelle gruppieren und so Kostenanalysen sowie Governance-Auswertungen ermöglichen. Availability Zones betreffen die physische Ausfallsicherheit, Managed Disks sind Datenträger, und ein Subnet unterteilt ein virtuelles Netzwerk — keines davon dient der organisatorischen Kategorisierung.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources",
        "difficulty": 1,
    },
    {
        "id": "az900-043",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welcher Dienst richtet den Zugriff über eine private IP-Adresse in einem Virtual Network ein?",
        "options": ["Private Endpoint", "Azure Firewall", "Azure Front Door", "Azure VPN Gateway"],
        "answer": "Private Endpoint",
        "explanation": "Ein Private Endpoint bindet einen PaaS-Dienst (z. B. Storage-Konto oder SQL-Datenbank) über eine private IP-Adresse direkt in ein Virtual Network ein, sodass der Datenverkehr nicht über das öffentliche Internet läuft. Azure Firewall filtert Datenverkehr, Azure Front Door ist ein globaler Layer-7-Lastverteiler/CDN, und ein VPN Gateway verbindet ganze Netzwerke — keines davon stellt eine private IP für einen einzelnen PaaS-Dienst bereit.",
        "source": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-044",
        "exam": "AZ-900",
        "category": "governance",
        "type": "multi",
        "prompt": "Welche Funktionen tragen typischerweise zur Governance in Azure bei? Wähle alle zutreffenden Antworten.",
        "options": ["Azure Policy", "Resource Locks", "Tags", "Azure Monitor Alert"],
        "answer": ["Azure Policy", "Resource Locks", "Tags", "Azure Monitor Alert"],
        "explanation": "Alle vier Optionen tragen zur Governance bei: Azure Policy erzwingt organisatorische Regeln und Compliance, Resource Locks verhindern versehentliche Lösch-/Änderungsvorgänge, Tags ermöglichen Kategorisierung für Kostenanalyse und Zuständigkeit, und Azure Monitor-Warnungen überwachen die Einhaltung von Betriebs- und Sicherheitszielen. Governance in Azure ist typischerweise eine Kombination mehrerer solcher Mechanismen, nicht nur eines einzelnen Tools.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/",
        "difficulty": 2,
    },
    {
        "id": "az900-045",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "Eine Hybrid Cloud ist nur dann sinnvoll, wenn keine lokale Infrastruktur mehr vorhanden ist.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Hybrid Cloud ist oft genau dann sinnvoll, wenn lokale und cloudbasierte Umgebungen parallel oder schrittweise genutzt werden.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/",
        "difficulty": 2,
    },
    {
        "id": "az900-046",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welche Cloudumgebung wird von einer Organisation betrieben und ausschließlich von dieser Organisation genutzt?",
        "options": ["Public Cloud", "Private Cloud", "Hybrid Cloud", "Community Cloud"],
        "answer": "Private Cloud",
        "explanation": "Eine Private Cloud ist für die exklusive Nutzung durch eine Organisation vorgesehen. Eine Hybrid Cloud kombiniert lokale Infrastruktur oder eine Private Cloud mit einer Public Cloud.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 1,
    },
    {
        "id": "az900-047",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Begriffe gehören zu den typischen Vorteilen von Cloud Computing? Wählen Sie alle zutreffenden Antworten.",
        "options": ["Skalierbarkeit", "Zuverlässigkeit", "Vorhersagbarkeit", "Automatische Aufhebung jeder Governance"],
        "answer": ["Skalierbarkeit", "Zuverlässigkeit", "Vorhersagbarkeit"],
        "explanation": "Cloud Computing kann Skalierbarkeit, Zuverlässigkeit und Vorhersagbarkeit verbessern. Governance und Sicherheitskontrollen bleiben weiterhin erforderlich.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 2,
    },
    {
        "id": "az900-048",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Azure-Struktur beschreibt einen geografisch verteilten Standort mit mindestens einem oder mehreren Rechenzentren?",
        "options": ["Azure-Region", "Verfügbarkeitszone", "Ressourcengruppe", "Abonnement"],
        "answer": "Azure-Region",
        "explanation": "Eine Azure-Region ist ein geografischer Standort mit mindestens einem, meist mehreren Rechenzentren, der über ein Netzwerk mit geringer Latenz verbunden ist. Eine Verfügbarkeitszone liegt innerhalb einer Region, eine Ressourcengruppe ist nur ein logischer Verwaltungscontainer ohne physischen Standort, und ein Abonnement ist eine Abrechnungs- und Verwaltungseinheit ohne geografische Bedeutung.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/regions-overview",
        "difficulty": 1,
    },
    {
        "id": "az900-049",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welcher Azure-Dienst stellt eine verwaltete Umgebung zum Ausführen von Containern bereit, ohne dass ein vollständiger Kubernetes-Cluster verwaltet werden muss?",
        "options": ["Azure Container Instances", "Azure Virtual Machines", "Azure DNS", "Azure Data Box"],
        "answer": "Azure Container Instances",
        "explanation": "Azure Container Instances führt einzelne Container schnell und ohne Verwaltungsaufwand aus, ideal für einfache oder kurzlebige Workloads. Azure Kubernetes Service ist die passende Wahl für orchestrierte, mehrknotige Cluster; Azure Virtual Machines würde ein volles Betriebssystem statt eines Containers bereitstellen, und Azure DNS bzw. Azure Data Box haben keinen Bezug zur Container-Ausführung.",
        "source": "https://learn.microsoft.com/en-us/azure/container-instances/container-instances-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-050",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welche Aussage beschreibt Azure Resource Manager-Vorlagen (ARM templates) am besten?",
        "options": [
            "Sie definieren Azure-Ressourcen deklarativ und ermöglichen wiederholbare Bereitstellungen.",
            "Sie ersetzen Microsoft Entra ID bei der Authentifizierung.",
            "Sie dienen ausschließlich zur Anzeige von Metriken.",
            "Sie sind ein lokaler Dateispeicher für unstrukturierte Daten."
        ],
        "answer": "Sie definieren Azure-Ressourcen deklarativ und ermöglichen wiederholbare Bereitstellungen.",
        "explanation": "ARM-Vorlagen beschreiben Azure-Ressourcen deklarativ in JSON (oder über Bicep) und ermöglichen so konsistente, wiederholbare Bereitstellungen per Infrastructure as Code. Sie ersetzen keine Authentifizierung durch Microsoft Entra ID, zeigen selbst keine Metrikdaten an, und sind kein Dateispeicher für unstrukturierte Daten – dafür wäre Azure Blob Storage zuständig.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-051",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst wird verwendet, um Protokolle mit Log Analytics abzufragen und daraus Überwachung und Warnungen abzuleiten?",
        "options": ["Azure Monitor", "Azure Policy", "Azure Advisor", "Azure Service Health"],
        "answer": "Azure Monitor",
        "explanation": "Azure Monitor sammelt Metriken und Protokolle zentral, während Log Analytics als Abfragekomponente das Durchsuchen und Auswerten der Protokolldaten (z. B. mit KQL) ermöglicht. Azure Policy erzwingt Konfigurationsregeln statt Protokolle abzufragen, Azure Advisor liefert Empfehlungen, und Azure Service Health informiert nur über Dienststörungen – keines davon bietet Log-Abfragen.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-052",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Microsoft-Entra-ID-Funktion ermöglicht den einmaligen Zugriff auf mehrere Anwendungen mit denselben Anmeldeinformationen?",
        "options": ["Single Sign-On (SSO)", "Azure Policy", "Resource Lock", "Azure Advisor"],
        "answer": "Single Sign-On (SSO)",
        "explanation": "Single Sign-On ermöglicht Benutzern, sich einmal anzumelden und danach ohne erneute Anmeldung auf mehrere vertrauenswürdige Anwendungen zuzugreifen. Azure Policy betrifft Governance statt Anmeldung, ein Resource Lock verhindert nur Löschen oder Ändern von Ressourcen, und Azure Advisor gibt Optimierungsempfehlungen – keines davon ist eine Anmeldefunktion.",
        "source": "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/what-is-single-sign-on",
        "difficulty": 1,
    },
    {
        "id": "az900-053",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "multi",
        "prompt": "Welche Methoden können zur kennwortlosen Authentifizierung mit Microsoft Entra ID verwendet werden? Wählen Sie alle zutreffenden Antworten.",
        "options": ["FIDO2-Sicherheitsschlüssel", "Windows Hello for Business", "Microsoft Authenticator", "Azure Resource Group"],
        "answer": ["FIDO2-Sicherheitsschlüssel", "Windows Hello for Business", "Microsoft Authenticator"],
        "explanation": "FIDO2-Sicherheitsschlüssel, Windows Hello for Business und Microsoft Authenticator gehören zu den kennwortlosen Authentifizierungsoptionen. Eine Ressourcengruppe ist kein Authentifizierungsverfahren.",
        "source": "https://learn.microsoft.com/en-us/entra/identity/authentication/overview-authentication",
        "difficulty": 2,
    },
    {
        "id": "az900-054",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Azure Storage-Redundanz repliziert Daten synchron innerhalb einer einzelnen Region über mehrere Verfügbarkeitszonen?",
        "options": ["LRS", "ZRS", "GRS", "RA-GRS"],
        "answer": "ZRS",
        "explanation": "Zone-redundant storage (ZRS) repliziert Daten synchron über mehrere Verfügbarkeitszonen innerhalb der primären Region. GRS und RA-GRS verwenden zusätzlich eine sekundäre Region.",
        "source": "https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy",
        "difficulty": 2,
    },
    {
        "id": "az900-055",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Ein Unternehmen muss mehrere Terabyte Daten offline nach Azure übertragen, weil die verfügbare Netzwerkbandbreite nicht ausreicht. Welcher Dienst ist am besten geeignet?",
        "options": ["Azure Data Box", "Azure DNS", "Azure Monitor", "Azure Functions"],
        "answer": "Azure Data Box",
        "explanation": "Azure Data Box überträgt sehr große Datenmengen per physischem, verschlüsseltem Gerät offline zu Azure, wenn die Netzwerkbandbreite nicht ausreicht. Azure DNS verwaltet nur Domainnamen, Azure Monitor sammelt Telemetrie, und Azure Functions ist ein serverloser Compute-Dienst – keines davon transportiert Massendaten.",
        "source": "https://learn.microsoft.com/en-us/azure/databox/data-box-overview",
        "difficulty": 1,
    },
    {
        "id": "az900-056",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Welche Verbindung bietet eine dedizierte private Verbindung von einem lokalen Netzwerk zu Microsoft Cloud-Diensten?",
        "options": ["ExpressRoute", "Point-to-site VPN", "Azure DNS", "Azure CDN"],
        "answer": "ExpressRoute",
        "explanation": "ExpressRoute stellt eine private Verbindung über einen Konnektivitätsanbieter bereit. Ein VPN verwendet verschlüsselten Datenverkehr über ein öffentliches Netzwerk.",
        "source": "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction",
        "difficulty": 2,
    },
    {
        "id": "az900-057",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst hilft dabei, Datenbestände zu katalogisieren und den Datenbestand eines Unternehmens zu verwalten?",
        "options": ["Microsoft Purview", "Azure Load Balancer", "Azure Virtual Network", "Azure Bastion"],
        "answer": "Microsoft Purview",
        "explanation": "Microsoft Purview katalogisiert Datenbestände unternehmensweit, klassifiziert sensible Daten und unterstützt Data Governance und Compliance. Azure Load Balancer verteilt Netzwerkverkehr, Azure Virtual Network stellt isolierte Netzwerke bereit, und Azure Bastion ermöglicht sicheren VM-Zugriff – keines davon betrifft Datenkatalogisierung.",
        "source": "https://learn.microsoft.com/en-us/purview/purview",
        "difficulty": 2,
    },
    {
        "id": "az900-058",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst bewertet Azure-Ressourcen anhand von Sicherheitsbest Practices und gibt Empfehlungen zur Verbesserung der Sicherheitslage?",
        "options": ["Microsoft Defender for Cloud", "Azure Pricing Calculator", "Azure Resource Manager", "Azure Storage Explorer"],
        "answer": "Microsoft Defender for Cloud",
        "explanation": "Microsoft Defender for Cloud bewertet die Sicherheitslage von Azure- und Hybridressourcen (Secure Score), gibt Härtungsempfehlungen und bietet erweiterten Bedrohungsschutz. Der Pricing Calculator schätzt nur Kosten, Azure Resource Manager verwaltet Bereitstellungen, und Azure Storage Explorer ist ein Werkzeug zur Dateiverwaltung – keines davon bewertet Sicherheit.",
        "source": "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction",
        "difficulty": 2,
    },
    {
        "id": "az900-059",
        "exam": "AZ-900",
        "category": "governance",
        "type": "matching",
        "prompt": "Ordnen Sie die Azure-Verwaltungswerkzeuge ihrem typischen Einsatz zu.",
        "pairs": [
            ["Azure Portal", "Grafische browserbasierte Verwaltung"],
            ["Azure CLI", "Plattformübergreifende Befehlszeilenverwaltung"],
            ["Azure Cloud Shell", "Browserbasierte Shell mit vorkonfigurierten Tools"],
        ],
        "answer": [
            ["Azure Portal", "Grafische browserbasierte Verwaltung"],
            ["Azure CLI", "Plattformübergreifende Befehlszeilenverwaltung"],
            ["Azure Cloud Shell", "Browserbasierte Shell mit vorkonfigurierten Tools"],
        ],
        "explanation": "Das Azure Portal ist grafisch, Azure CLI ist eine plattformübergreifende Befehlszeilenschnittstelle und Cloud Shell stellt eine browserbasierte Shell mit Azure-Tools bereit.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-shell/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-060",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Welcher Dienst zeigt den Zustand einer bestimmten Azure-Ressource an, beispielsweise ob eine virtuelle Maschine verfügbar ist?",
        "options": ["Azure Resource Health", "Azure Service Health", "Azure Advisor", "Azure Policy"],
        "answer": "Azure Resource Health",
        "explanation": "Resource Health liefert Informationen zum Zustand einzelner Ressourcen. Service Health informiert über Dienstprobleme, geplante Wartungen und andere Ereignisse, die das Azure-Abonnement betreffen können.",
        "source": "https://learn.microsoft.com/en-us/azure/service-health/resource-health-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-061",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ordnen Sie die Schritte für den Zugriff auf einen PaaS-Dienst über ein privates Netzwerk in die richtige Reihenfolge.",
        "options": [
            "Ein Virtual Network auswählen",
            "Ein Subnetz für den Private Endpoint auswählen",
            "Den Private Endpoint erstellen",
            "Die Verbindung zum PaaS-Dienst überprüfen",
        ],
        "answer": [
            "Ein Virtual Network auswählen",
            "Ein Subnetz für den Private Endpoint auswählen",
            "Den Private Endpoint erstellen",
            "Die Verbindung zum PaaS-Dienst überprüfen",
        ],
        "explanation": "Der Private Endpoint wird in einem Subnetz eines Virtual Network bereitgestellt und ermöglicht anschließend den privaten Zugriff auf den PaaS-Dienst.",
        "source": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-062",
        "exam": "AZ-900",
        "category": "governance",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und ordnen Sie eine sinnvolle Reihenfolge für die Bereitstellung einer standardisierten Azure-Umgebung mit Infrastructure as Code. Ein Element gehört nicht in den Ablauf.",
        "options": [
            "Vorlage und Parameter definieren",
            "Bereitstellung überprüfen",
            "Vorlage ausführen",
            "Ressourcen und Richtlinien validieren",
            "Ressourcen anschließend manuell im Portal nachbearbeiten",
        ],
        "answer": [
            "Vorlage und Parameter definieren",
            "Vorlage ausführen",
            "Bereitstellung überprüfen",
            "Ressourcen und Richtlinien validieren",
        ],
        "explanation": "Eine deklarative Vorlage wird zuerst definiert, dann ausgeführt, anschließend geprüft und schließlich gegen die erwarteten Ressourcen- und Governance-Anforderungen validiert. Manuelles Nachbearbeiten im Portal widerspricht dem Grundprinzip von Infrastructure as Code, bei dem der gewünschte Zustand ausschließlich über die Vorlage gesteuert wird und nachträgliche manuelle Änderungen zu Konfigurationsabweichungen (Configuration Drift) führen.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-063",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "hot_area",
        "prompt": "Wählen Sie den Bereich aus, der für die private Verbindung eines PaaS-Dienstes aus einem Virtual Network verwendet wird.",
        "options": ["Public IP address", "Private Endpoint", "Azure DNS zone", "Availability zone"],
        "answer": "Private Endpoint",
        "explanation": "Ein Private Endpoint stellt eine private IP-Adresse im Virtual Network bereit. Eine Public IP address ist öffentlich erreichbar und keine private Verbindung.",
        "source": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
        "difficulty": 2,
    },
    {
        "id": "az900-064",
        "exam": "AZ-900",
        "category": "governance",
        "type": "active_screen",
        "prompt": "Sie sehen eine Azure-Monitor-Ansicht mit Zeitreihen, Schwellenwerten und einer Benachrichtigungsregel. Welche Funktion wird hier konfiguriert?",
        "options": ["Alert rule", "Resource lock", "Management group", "Pricing calculator"],
        "answer": "Alert rule",
        "explanation": "Eine Azure Monitor alert rule reagiert auf definierte Bedingungen wie Metrik- oder Log-Schwellenwerte und kann eine Benachrichtigung oder Aktion auslösen.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-065",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "hot_area",
        "prompt": "Wählen Sie den Dienst aus, der vollständige Kontrolle über das Gastbetriebssystem bietet.",
        "options": ["Azure App Service", "Azure Functions", "Azure Virtual Machines", "Azure Container Instances"],
        "answer": "Azure Virtual Machines",
        "explanation": "Azure Virtual Machines bietet Kontrolle über das Gastbetriebssystem. App Service, Functions und Container Instances abstrahieren mehr Infrastruktur.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machines/overview",
        "difficulty": 2,
    },
    {
        "id": "az900-066",
        "exam": "AZ-900",
        "category": "governance",
        "type": "active_screen",
        "prompt": "Ein Dashboard zeigt Empfehlungen zu Kosten, Zuverlässigkeit, Sicherheit und Leistung. Welcher Azure-Dienst stellt diese Empfehlungen bereit?",
        "options": ["Azure Advisor", "Azure Monitor", "Azure Policy", "Microsoft Purview"],
        "answer": "Azure Advisor",
        "explanation": "Azure Advisor analysiert die Azure-Umgebung und liefert personalisierte Empfehlungen in den Bereichen Kosten, Sicherheit, Zuverlässigkeit und Leistung.",
        "source": "https://learn.microsoft.com/en-us/azure/advisor/advisor-overview",
        "difficulty": 1,
    },
    {
        "id": "az900-067",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "Bei einer Platform as a Service-Lösung bleibt der Kunde für die physische Sicherheit des Rechenzentrums verantwortlich.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Bei PaaS übernimmt Microsoft die physische Infrastruktur und deren Sicherheit. Der Kunde bleibt unter anderem für Daten, Identitäten und die Konfiguration seiner Anwendung verantwortlich.",
        "source": "https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility",
        "difficulty": 3,
    },
    {
        "id": "az900-068",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Eigenschaften gehören typischerweise zu einer elastischen Cloudarchitektur? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Kapazität kann an die Nachfrage angepasst werden.",
            "Ressourcen müssen für die höchste Last dauerhaft vorgehalten werden.",
            "Bereitstellung kann automatisiert werden.",
            "Nicht mehr benötigte Ressourcen können entfernt werden.",
        ],
        "answer": [
            "Kapazität kann an die Nachfrage angepasst werden.",
            "Bereitstellung kann automatisiert werden.",
            "Nicht mehr benötigte Ressourcen können entfernt werden.",
        ],
        "explanation": "Elastizität beschreibt die bedarfsgerechte Anpassung von Kapazität. Automatisierung und das Entfernen ungenutzter Ressourcen unterstützen dieses Modell.",
        "source": "https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/",
        "difficulty": 3,
    },
    {
        "id": "az900-069",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "ordering",
        "prompt": "Ordnen Sie die Azure-Hierarchie von der höchsten zur niedrigsten Verwaltungsebene.",
        "options": ["Management group", "Subscription", "Resource group", "Resource"],
        "answer": ["Management group", "Subscription", "Resource group", "Resource"],
        "explanation": "Management groups können mehrere Subscriptions enthalten. Eine Subscription enthält Resource groups, und diese enthalten einzelne Ressourcen.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-070",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ziehen Sie die Schritte für eine abgesicherte Verbindung von einem lokalen Netzwerk zu Azure in die richtige Reihenfolge.",
        "options": [
            "Ein Azure Virtual Network bereitstellen",
            "Ein lokales VPN-Gerät konfigurieren",
            "Ein VPN Gateway in Azure bereitstellen",
            "Die Site-to-Site-Verbindung testen",
        ],
        "answer": [
            "Ein Azure Virtual Network bereitstellen",
            "Ein lokales VPN-Gerät konfigurieren",
            "Ein VPN Gateway in Azure bereitstellen",
            "Die Site-to-Site-Verbindung testen",
        ],
        "explanation": "Das Zielnetz wird zuerst erstellt, danach werden die Gegenstelle und das Azure VPN Gateway konfiguriert. Anschließend wird die Site-to-Site-Verbindung geprüft.",
        "source": "https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal",
        "difficulty": 4,
    },
    {
        "id": "az900-071",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und bauen Sie die Reihenfolge für die Veröffentlichung einer containerisierten Webanwendung auf. Ein Element gehört nicht dazu.",
        "options": [
            "Ein Container-Image erstellen",
            "Das Image in eine Registry pushen",
            "Die Container-App mit dem Image bereitstellen",
            "Protokolle und Skalierung überprüfen",
            "Den Container-Host manuell patchen",
        ],
        "answer": [
            "Ein Container-Image erstellen",
            "Das Image in eine Registry pushen",
            "Die Container-App mit dem Image bereitstellen",
            "Protokolle und Skalierung überprüfen",
        ],
        "explanation": "Ein Container-Image wird zuerst gebaut, dann in eine Registry gepusht, von dort als Container-App bereitgestellt und abschließend hinsichtlich Laufzeitverhalten und Skalierung überwacht. Das manuelle Patchen des Hosts entfällt bei verwalteten Container-Diensten wie Azure Container Apps, da Microsoft die zugrunde liegende Hostinfrastruktur betreibt und patcht.",
        "source": "https://learn.microsoft.com/en-us/azure/container-apps/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-072",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "matching",
        "prompt": "Ordnen Sie die Speicheroption dem passenden Szenario zu.",
        "pairs": [
            ["Azure Blob Storage", "Unstrukturierte Objekte wie Bilder und Backups"],
            ["Azure Files", "Verwaltete SMB- oder NFS-Dateifreigabe"],
            ["Azure Queue Storage", "Asynchrone Nachrichten zwischen Anwendungskomponenten"],
        ],
        "answer": [
            ["Azure Blob Storage", "Unstrukturierte Objekte wie Bilder und Backups"],
            ["Azure Files", "Verwaltete SMB- oder NFS-Dateifreigabe"],
            ["Azure Queue Storage", "Asynchrone Nachrichten zwischen Anwendungskomponenten"],
        ],
        "explanation": "Blob Storage ist für Objekte gedacht, Azure Files stellt Dateifreigaben bereit und Queue Storage entkoppelt Komponenten über Nachrichten.",
        "source": "https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction",
        "difficulty": 3,
    },
    {
        "id": "az900-073",
        "exam": "AZ-900",
        "category": "governance",
        "type": "hot_area",
        "prompt": "Sie wollen verhindern, dass ein Resource Group versehentlich gelöscht wird, ohne Berechtigungen zu ändern. Welche Funktion wählen Sie?",
        "options": ["Resource lock", "Azure Policy", "Tag", "Management group"],
        "answer": "Resource lock",
        "explanation": "Ein Resource lock schützt eine Ressource oder Resource Group vor Löschen beziehungsweise Änderungen. Er ersetzt weder RBAC noch Azure Policy.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources",
        "difficulty": 3,
    },
    {
        "id": "az900-074",
        "exam": "AZ-900",
        "category": "governance",
        "type": "active_screen",
        "prompt": "In einer Kostenansicht werden tatsächliche Ausgaben nach Subscription und Ressourcengruppe aufgeschlüsselt. Welche Funktion verwenden Sie?",
        "options": ["Cost analysis", "Azure Service Health", "Resource Health", "Network Watcher"],
        "answer": "Cost analysis",
        "explanation": "Cost analysis in Microsoft Cost Management ermöglicht die Analyse tatsächlicher Kosten und das Filtern nach Bereichen wie Subscription oder Resource group.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis",
        "difficulty": 4,
    },
    {
        "id": "az900-075",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-self-service",
        "case_order": 1,
        "case_text": "Ein Unternehmen betreibt mehrere Azure-Webanwendungen. Entwickler sollen standardisiert und selbstständig bereitstellen können. Nur genehmigte Regionen und Ressourcentypen dürfen verwendet werden, Kosten müssen nach Team auswertbar sein und Administratoren sollen nur die benötigten Rechte erhalten.",
        "prompt": "Welche Maßnahmen erfüllen die drei Anforderungen? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Eine ARM- oder Bicep-Vorlage für standardisierte Bereitstellungen verwenden.",
            "Azure Policy für zulässige Regionen verwenden.",
            "Allen Administratoren Owner auf Subscription-Ebene geben.",
            "RBAC-Rollen nach dem Prinzip der geringsten Rechte zuweisen.",
        ],
        "answer": [
            "Eine ARM- oder Bicep-Vorlage für standardisierte Bereitstellungen verwenden.",
            "Azure Policy für zulässige Regionen verwenden.",
            "RBAC-Rollen nach dem Prinzip der geringsten Rechte zuweisen.",
        ],
        "explanation": "Infrastructure as Code standardisiert Bereitstellungen, Azure Policy erzwingt Organisationsregeln und RBAC begrenzt Zugriffsrechte. Owner für alle Administratoren verletzt Least Privilege.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-076",
        "exam": "AZ-900",
        "category": "governance",
        "type": "true_false",
        "prompt": "Azure Advisor erzwingt automatisch Organisationsregeln wie eine Richtlinie für erlaubte Regionen.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Azure Advisor gibt Empfehlungen. Azure Policy dient dazu, Regeln zu definieren und deren Einhaltung zu prüfen oder zu erzwingen.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-077",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Aussagen zum verbrauchsabhängigen Cloudmodell sind korrekt? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Die Kosten können mit der tatsächlichen Nutzung schwanken.",
            "Nicht benötigte Ressourcen sollten beendet oder entfernt werden.",
            "Der Anbieter garantiert unabhängig von der Nutzung immer dieselben Kosten.",
            "Kosten können mit Tags oder Cost Management analysiert werden.",
        ],
        "answer": [
            "Die Kosten können mit der tatsächlichen Nutzung schwanken.",
            "Nicht benötigte Ressourcen sollten beendet oder entfernt werden.",
            "Kosten können mit Tags oder Cost Management analysiert werden.",
        ],
        "explanation": "Im verbrauchsabhängigen Modell entstehen Kosten abhängig von Nutzung und Konfiguration. Unbenutzte Ressourcen können weiter Kosten verursachen; Analyse und Tags helfen bei der Zuordnung.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data",
        "difficulty": 3,
    },
    {
        "id": "az900-078",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ordnen Sie die Schritte für die Wiederherstellung einer Azure-VM aus einem Recovery Services-Tresor.",
        "options": [
            "Einen Wiederherstellungspunkt auswählen",
            "Das Ziel für die Wiederherstellung konfigurieren",
            "Die Wiederherstellung starten",
            "Die wiederhergestellten Ressourcen überprüfen",
        ],
        "answer": [
            "Einen Wiederherstellungspunkt auswählen",
            "Das Ziel für die Wiederherstellung konfigurieren",
            "Die Wiederherstellung starten",
            "Die wiederhergestellten Ressourcen überprüfen",
        ],
        "explanation": "Zuerst wird ein geeigneter Wiederherstellungspunkt ausgewählt, dann das Ziel festgelegt. Nach dem Start wird geprüft, ob die Ressourcen erwartungsgemäß wiederhergestellt wurden.",
        "source": "https://learn.microsoft.com/en-us/azure/backup/backup-azure-arm-restore-vms",
        "difficulty": 4,
    },
    {
        "id": "az900-079",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und bauen Sie eine sinnvolle Reihenfolge für die Skalierung einer Webanwendung mit Azure App Service auf. Ein Element passt nicht zu Autoscale.",
        "options": [
            "Metrik oder Auslastung definieren",
            "Eine Autoscale-Regel konfigurieren",
            "Die Mindest- und Höchstanzahl von Instanzen festlegen",
            "Das Skalierungsverhalten anhand von Metriken überprüfen",
            "Eine zusätzliche VM manuell hinzufügen",
        ],
        "answer": [
            "Metrik oder Auslastung definieren",
            "Eine Autoscale-Regel konfigurieren",
            "Die Mindest- und Höchstanzahl von Instanzen festlegen",
            "Das Skalierungsverhalten anhand von Metriken überprüfen",
        ],
        "explanation": "Autoscale benötigt zuerst ein Signal (Metrik/Auslastung), danach Regeln sowie Instanz-Grenzwerte. Anschließend wird anhand von Metriken kontrolliert, ob die Skalierung wie beabsichtigt funktioniert. Das manuelle Hinzufügen einer VM widerspricht dem Zweck von Autoscale in App Service (PaaS), das die Instanzanzahl automatisch und regelbasiert anpasst, ohne manuelle VM-Verwaltung.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-080",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "matching",
        "prompt": "Ordnen Sie die Identitätsfunktion ihrer typischen Verwendung zu.",
        "pairs": [
            ["Microsoft Entra MFA", "Zusätzliche Authentifizierungsanforderung"],
            ["Microsoft Entra Conditional Access", "Zugriff anhand von Bedingungen steuern"],
            ["Microsoft Entra ID", "Cloudbasierter Identitäts- und Verzeichnisdienst"],
        ],
        "answer": [
            ["Microsoft Entra MFA", "Zusätzliche Authentifizierungsanforderung"],
            ["Microsoft Entra Conditional Access", "Zugriff anhand von Bedingungen steuern"],
            ["Microsoft Entra ID", "Cloudbasierter Identitäts- und Verzeichnisdienst"],
        ],
        "explanation": "MFA ergänzt die Anmeldung um einen weiteren Faktor. Conditional Access wertet Signale und Bedingungen aus. Microsoft Entra ID stellt Identitäts- und Verzeichnisfunktionen bereit.",
        "source": "https://learn.microsoft.com/en-us/entra/identity/",
        "difficulty": 3,
    },
    {
        "id": "az900-081",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "matching",
        "prompt": "Ordnen Sie den Netzwerkdienst dem passenden Zweck zu.",
        "pairs": [
            ["Azure DNS", "Namensauflösung für DNS-Domänen"],
            ["Network Security Group", "Regeln für ein- und ausgehenden Netzwerkverkehr"],
            ["Azure Load Balancer", "Verteilen von Datenverkehr auf Backend-Instanzen"],
        ],
        "answer": [
            ["Azure DNS", "Namensauflösung für DNS-Domänen"],
            ["Network Security Group", "Regeln für ein- und ausgehenden Netzwerkverkehr"],
            ["Azure Load Balancer", "Verteilen von Datenverkehr auf Backend-Instanzen"],
        ],
        "explanation": "Azure DNS verwaltet DNS-Zonen und Auflösung. Network Security Groups filtern Datenverkehr. Ein Load Balancer verteilt Verbindungen auf Backend-Ressourcen.",
        "source": "https://learn.microsoft.com/en-us/azure/networking/networking-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-082",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-rbac-scope",
        "case_order": 1,
        "case_text": "Ein Team muss Produktionsressourcen schützen. Entwickler sollen Ressourcen starten und überwachen, aber weder Netzwerkregeln ändern noch die gesamte Subscription verwalten.",
        "prompt": "Welche Maßnahmen passen zu dieser Anforderung? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Eine passende integrierte RBAC-Rolle auf möglichst kleinem Scope zuweisen.",
            "Für alle Entwickler die Rolle Owner auf Subscription-Ebene verwenden.",
            "Eine Resource Group als Scope verwenden, wenn nur diese betroffen ist.",
            "Bei Bedarf eine benutzerdefinierte Rolle mit den erforderlichen Aktionen definieren.",
        ],
        "answer": [
            "Eine passende integrierte RBAC-Rolle auf möglichst kleinem Scope zuweisen.",
            "Eine Resource Group als Scope verwenden, wenn nur diese betroffen ist.",
            "Bei Bedarf eine benutzerdefinierte Rolle mit den erforderlichen Aktionen definieren.",
        ],
        "explanation": "RBAC folgt dem Prinzip der geringsten Rechte und kann auf Management group, Subscription, Resource group oder Ressource angewendet werden. Owner auf Subscription-Ebene wäre zu weitreichend.",
        "source": "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-083",
        "exam": "AZ-900",
        "category": "governance",
        "type": "active_screen",
        "prompt": "Sie sehen eine Ansicht mit Azure-Ressourcen, die gegen eine Organisationsregel verstoßen. Welcher Dienst bewertet diese Compliance-Zustände?",
        "options": ["Azure Policy", "Azure Advisor", "Azure Cost Management", "Azure Service Health"],
        "answer": "Azure Policy",
        "explanation": "Azure Policy definiert und bewertet Regeln für Ressourcen. Im Compliance-Dashboard werden Ressourcen angezeigt, die eine Policy erfüllen oder verletzen.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-084",
        "exam": "AZ-900",
        "category": "governance",
        "type": "hot_area",
        "prompt": "Welche Stelle wählen Sie, um geplante Wartungen und Dienstprobleme anzuzeigen, die Ihr Azure-Abonnement betreffen können?",
        "options": ["Azure Service Health", "Azure Resource Health", "Azure Advisor", "Azure Storage Explorer"],
        "answer": "Azure Service Health",
        "explanation": "Service Health informiert über Dienstprobleme, geplante Wartungen und Gesundheitswarnungen mit Bezug zu den verwendeten Azure-Diensten und Abonnements.",
        "source": "https://learn.microsoft.com/en-us/azure/service-health/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-085",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "Eine höhere Verfügbarkeit bedeutet automatisch, dass eine Anwendung auch vor Datenverlust geschützt ist.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Verfügbarkeit und Datenschutz beziehungsweise Wiederherstellbarkeit sind unterschiedliche Ziele. Backups, Replikation und Recovery-Strategien müssen separat geplant werden.",
        "source": "https://learn.microsoft.com/en-us/azure/well-architected/reliability/",
        "difficulty": 4,
    },
    {
        "id": "az900-086",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ordnen Sie die Schritte für die Bereitstellung einer Azure Storage-Dateifreigabe.",
        "options": [
            "Ein Storage-Konto erstellen",
            "Eine File Share anlegen",
            "Zugriff und Kontingent konfigurieren",
            "Die Dateifreigabe verbinden und testen",
        ],
        "answer": [
            "Ein Storage-Konto erstellen",
            "Eine File Share anlegen",
            "Zugriff und Kontingent konfigurieren",
            "Die Dateifreigabe verbinden und testen",
        ],
        "explanation": "Azure Files wird in einem Storage-Konto bereitgestellt. Danach wird die Freigabe erstellt, konfiguriert und von einem Client aus getestet.",
        "source": "https://learn.microsoft.com/en-us/azure/storage/files/storage-files-quick-create-use-windows",
        "difficulty": 3,
    },
    {
        "id": "az900-087",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Unternehmen möchte seine lokale Anwendung zunächst unverändert in Azure ausführen und später modernisieren. Welcher Ansatz passt zunächst am besten?",
        "options": [
            "Die Anwendung als IaaS-Workload auf Azure Virtual Machines verschieben.",
            "Die Anwendung sofort in Azure Functions umschreiben.",
            "Alle Daten zuerst in Azure Policy konvertieren.",
            "Die lokale Anwendung durch Microsoft Purview ersetzen.",
        ],
        "answer": "Die Anwendung als IaaS-Workload auf Azure Virtual Machines verschieben.",
        "explanation": "Ein Lift-and-Shift-Ansatz verschiebt eine bestehende Anwendung mit minimalen Änderungen auf Azure Virtual Machines (IaaS) und erlaubt eine spätere, schrittweise Modernisierung. Ein sofortiges Umschreiben in Azure Functions wäre ein riskanter Komplettumbau ohne Übergangsphase, Azure Policy dient der Governance statt der Datenkonvertierung, und Microsoft Purview katalogisiert Daten statt Anwendungen zu ersetzen.",
        "source": "https://learn.microsoft.com/en-us/azure/app-modernization-guidance/plan/the-6-rs-of-application-modernization",
        "difficulty": 4,
    },
    {
        "id": "az900-088",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "Eine private Cloud ist ausschließlich dadurch definiert, dass sie von Microsoft in einer Azure-Region betrieben wird.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Eine private Cloud ist einer einzelnen Organisation vorbehalten. Sie kann von der Organisation selbst oder einem Dienstanbieter betrieben werden; die Bezeichnung hängt nicht ausschließlich von Azure-Regionen ab.",
        "source": "https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/",
        "difficulty": 3,
    },
    {
        "id": "az900-089",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "drag_drop",
        "prompt": "Ordnen Sie die Schritte für eine bedarfsgerechte Skalierung einer Anwendung sinnvoll.",
        "options": [
            "Die erwarteten Lastsignale und Metriken bestimmen",
            "Eine Skalierungsregel definieren",
            "Mindest- und Höchstgrenzen festlegen",
            "Das Verhalten unter einer Testlast überprüfen",
        ],
        "answer": [
            "Die erwarteten Lastsignale und Metriken bestimmen",
            "Eine Skalierungsregel definieren",
            "Mindest- und Höchstgrenzen festlegen",
            "Das Verhalten unter einer Testlast überprüfen",
        ],
        "explanation": "Skalierung sollte auf messbaren Signalen basieren. Regeln und Grenzen schützen vor unkontrolliertem Wachstum; ein Test bestätigt, dass die Anwendung erwartungsgemäß reagiert.",
        "source": "https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/",
        "difficulty": 4,
    },
    {
        "id": "az900-090",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "multi",
        "prompt": "Eine Webanwendung benötigt hohe Verfügbarkeit innerhalb einer Azure-Region. Welche Maßnahmen können dieses Ziel unterstützen? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Ressourcen über mehrere Availability Zones verteilen.",
            "Eine geeignete Lastverteilung zwischen Instanzen verwenden.",
            "Alle Instanzen in demselben einzelnen Rechenzentrum platzieren.",
            "Fehler- und Wiederherstellungsverhalten testen.",
        ],
        "answer": [
            "Ressourcen über mehrere Availability Zones verteilen.",
            "Eine geeignete Lastverteilung zwischen Instanzen verwenden.",
            "Fehler- und Wiederherstellungsverhalten testen.",
        ],
        "explanation": "Availability Zones reduzieren die Abhängigkeit von einem einzelnen Rechenzentrumsstandort. Lastverteilung und Tests ergänzen die technische Resilienzplanung.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-091",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "ordering",
        "prompt": "Ordnen Sie die Ebenen der Azure-Verwaltungshierarchie von oben nach unten.",
        "options": ["Management group", "Subscription", "Resource group", "Resource"],
        "answer": ["Management group", "Subscription", "Resource group", "Resource"],
        "explanation": "Management groups organisieren Subscriptions. Subscriptions enthalten Resource groups, die wiederum einzelne Ressourcen enthalten.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-092",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "hot_area",
        "prompt": "Welche Option wählen Sie für eine verwaltete Plattform zum Hosten einer Webanwendung, ohne virtuelle Maschinen selbst zu verwalten?",
        "options": ["Azure App Service", "Azure Virtual Machines", "Azure VPN Gateway", "Azure Data Box"],
        "answer": "Azure App Service",
        "explanation": "Azure App Service ist ein verwalteter PaaS-Dienst für Webanwendungen. Bei virtuellen Maschinen bleibt deutlich mehr Betriebssystemverwaltung beim Kunden.",
        "source": "https://learn.microsoft.com/en-us/azure/app-service/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-093",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "active_screen",
        "prompt": "Eine Azure-Ansicht zeigt eine Metrik für CPU-Auslastung und eine Regel, die bei Überschreitung eine weitere Instanz startet. Welche Funktion ist dargestellt?",
        "options": ["Autoscale", "Resource lock", "Azure Policy", "Cost analysis"],
        "answer": "Autoscale",
        "explanation": "Autoscale passt die Anzahl von Instanzen anhand definierter Metriken und Regeln an. Es ist keine Zugriffs-, Governance- oder Kostenanalysefunktion.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-094",
        "exam": "AZ-900",
        "category": "governance",
        "type": "matching",
        "prompt": "Ordnen Sie das Governance-Werkzeug seiner Hauptaufgabe zu.",
        "pairs": [
            ["Azure Policy", "Regeln definieren und Compliance bewerten"],
            ["Azure RBAC", "Zugriff auf Ressourcen und Aktionen steuern"],
            ["Resource lock", "Löschen oder Änderungen blockieren"],
        ],
        "answer": [
            ["Azure Policy", "Regeln definieren und Compliance bewerten"],
            ["Azure RBAC", "Zugriff auf Ressourcen und Aktionen steuern"],
            ["Resource lock", "Löschen oder Änderungen blockieren"],
        ],
        "explanation": "Policy bewertet und erzwingt Organisationsregeln, RBAC steuert Berechtigungen und Resource Locks schützen Ressourcen vor bestimmten Änderungen.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-095",
        "exam": "AZ-900",
        "category": "governance",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und bauen Sie einen sinnvollen Ablauf für die Einführung einer Kostenwarnung auf. Ein Element gehört nicht in diesen Ablauf.",
        "options": [
            "Ein Budget für den passenden Scope definieren",
            "Eine Auslöseschwelle festlegen",
            "Eine Benachrichtigungsaktion konfigurieren",
            "Die Ausgaben regelmäßig überprüfen",
            "Eine Availability Zone konfigurieren",
        ],
        "answer": [
            "Ein Budget für den passenden Scope definieren",
            "Eine Auslöseschwelle festlegen",
            "Eine Benachrichtigungsaktion konfigurieren",
            "Die Ausgaben regelmäßig überprüfen",
        ],
        "explanation": "Ein Budget benötigt zuerst einen Scope und Grenzwerte, danach eine Schwelle, ab der reagiert werden soll. Anschließend werden Benachrichtigungen eingerichtet und die tatsächlichen Ausgaben weiter überwacht. Availability Zones betreffen die physische Verfügbarkeit von Ressourcen innerhalb einer Region und haben nichts mit Kostenüberwachung oder Budgets zu tun.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets",
        "difficulty": 4,
    },
    {
        "id": "az900-096",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-self-service",
        "case_order": 2,
        "case_text": "Ein Unternehmen betreibt mehrere Azure-Webanwendungen. Entwickler sollen standardisiert und selbstständig bereitstellen können. Nur genehmigte Regionen und Ressourcentypen dürfen verwendet werden, Kosten müssen nach Team auswertbar sein und Administratoren sollen nur die benötigten Rechte erhalten.",
        "prompt": "Welche Kombination unterstützt diese Anforderungen? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Eine Azure Policy für erlaubte Regionen zuweisen.",
            "Eine Tag-Richtlinie beziehungsweise Policy für die Kostenstelle verwenden.",
            "Azure Advisor als verbindliche Bereitstellungsblockade verwenden.",
            "Den Compliance-Zustand der Policies regelmäßig prüfen.",
        ],
        "answer": [
            "Eine Azure Policy für erlaubte Regionen zuweisen.",
            "Eine Tag-Richtlinie beziehungsweise Policy für die Kostenstelle verwenden.",
            "Den Compliance-Zustand der Policies regelmäßig prüfen.",
        ],
        "explanation": "Azure Policy kann Regionen und erforderliche Tags prüfen oder erzwingen. Der Compliance-Zustand zeigt Abweichungen. Advisor liefert Empfehlungen, ist aber keine verbindliche Policy-Engine.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-097",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Start-up möchte kurzfristig weltweit testen und nur für tatsächlich bereitgestellte Ressourcen zahlen. Welcher Cloudvorteil passt am besten?",
        "options": ["Elastische Bereitstellung mit verbrauchsabhängiger Abrechnung", "Ausschließlich lokale Hardware", "Kapazitätskauf für zehn Jahre", "Manuelle Skalierung ohne Telemetrie"],
        "answer": "Elastische Bereitstellung mit verbrauchsabhängiger Abrechnung",
        "explanation": "Elastische, verbrauchsabhängige Bereitstellung erlaubt es, Ressourcen weltweit schnell hinzuzufügen und nur für tatsächlich genutzte Kapazität zu zahlen – ideal für unsichere oder kurzfristige Lastspitzen eines Start-ups. Ausschließlich lokale Hardware oder ein zehnjähriger Kapazitätskauf widersprechen dem Wunsch nach geringer Vorabinvestition, und manuelle Skalierung ohne Telemetrie ermöglicht keine bedarfsgerechte, schnelle Anpassung.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 3,
    },
    {
        "id": "az900-098",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Ziele gehören zur Resilienzplanung? Wählen Sie alle zutreffenden Antworten.",
        "options": ["Ausfälle erkennen und behandeln", "Wiederherstellungsziele definieren", "Jede Störung vollständig verhindern", "Abhängigkeiten und Fehlerdomänen berücksichtigen"],
        "answer": ["Ausfälle erkennen und behandeln", "Wiederherstellungsziele definieren", "Abhängigkeiten und Fehlerdomänen berücksichtigen"],
        "explanation": "Resilienz bedeutet, dass ein System Fehler toleriert, erkennt und sich davon erholt. Eine vollständige Verhinderung jeder Störung ist kein realistisches Resilienzversprechen.",
        "source": "https://learn.microsoft.com/en-us/azure/well-architected/reliability/",
        "difficulty": 4,
    },
    {
        "id": "az900-099",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "true_false",
        "prompt": "Eine Azure-Region besteht aus mindestens einem physischen Rechenzentrum und kann Availability Zones enthalten.",
        "options": ["Wahr", "Falsch"],
        "answer": "Wahr",
        "explanation": "Eine Region ist ein geografischer Bereich mit mindestens einem Rechenzentrum. Viele Regionen unterstützen mehrere physisch getrennte Availability Zones.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/regions-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-100",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "ordering",
        "prompt": "Ordnen Sie die grundlegenden Schritte für die Veröffentlichung einer serverlosen Funktion.",
        "options": ["Funktion und Trigger definieren", "Konfiguration und Berechtigungen festlegen", "Funktion bereitstellen", "Ausführung und Protokolle prüfen"],
        "answer": ["Funktion und Trigger definieren", "Konfiguration und Berechtigungen festlegen", "Funktion bereitstellen", "Ausführung und Protokolle prüfen"],
        "explanation": "Trigger und Code bestimmen das Verhalten. Konfiguration und Identität werden vor der Bereitstellung festgelegt; danach wird die Ausführung anhand von Logs geprüft.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-101",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "matching",
        "prompt": "Ordnen Sie das Compute-Modell dem passenden Betriebsprofil zu.",
        "pairs": [
            ["Azure Virtual Machines", "Maximale Kontrolle über Gastbetriebssystem und Software"],
            ["Azure App Service", "Verwaltetes Hosting für Webanwendungen"],
            ["Azure Functions", "Ereignisgesteuerte Ausführung einzelner Funktionen"],
        ],
        "answer": [
            ["Azure Virtual Machines", "Maximale Kontrolle über Gastbetriebssystem und Software"],
            ["Azure App Service", "Verwaltetes Hosting für Webanwendungen"],
            ["Azure Functions", "Ereignisgesteuerte Ausführung einzelner Funktionen"],
        ],
        "explanation": "VMs bieten die meiste Kontrolle, App Service abstrahiert den Serverbetrieb für Webanwendungen und Functions eignet sich für ereignisgesteuerten Code.",
        "source": "https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree",
        "difficulty": 3,
    },
    {
        "id": "az900-102",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ziehen Sie die Schritte für den privaten Zugriff einer Anwendung auf Azure Storage in die richtige Reihenfolge.",
        "options": ["Virtual Network und Subnetz vorbereiten", "Private Endpoint erstellen", "Namensauflösung für den privaten Endpunkt prüfen", "Zugriff aus der Anwendung testen"],
        "answer": ["Virtual Network und Subnetz vorbereiten", "Private Endpoint erstellen", "Namensauflösung für den privaten Endpunkt prüfen", "Zugriff aus der Anwendung testen"],
        "explanation": "Der Private Endpoint wird in einem geeigneten Subnetz erstellt. DNS muss die private Adresse liefern, bevor der Anwendungstest aussagekräftig ist.",
        "source": "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-103",
        "exam": "AZ-900",
        "category": "governance",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und bauen Sie den Ablauf für eine standardisierte Ressourcenbereitstellung mit Bicep auf. Ein Element gehört nicht zu diesem Prozess.",
        "options": ["Vorlage und Parameter definieren", "Bereitstellung in einer Testumgebung ausführen", "Ergebnis und Policy-Compliance prüfen", "Freigegebene Bereitstellung ausrollen", "Ressourcengruppe manuell im Portal löschen und neu erstellen"],
        "answer": ["Vorlage und Parameter definieren", "Bereitstellung in einer Testumgebung ausführen", "Ergebnis und Policy-Compliance prüfen", "Freigegebene Bereitstellung ausrollen"],
        "explanation": "Die Bicep-Vorlage wird zuerst definiert, dann in einer Testumgebung ausgeführt und gegen Ergebnis- sowie Policy-Compliance geprüft. Erst danach erfolgt der freigegebene Rollout. Das manuelle Löschen und Neuerstellen der Ressourcengruppe im Portal ist ein destruktiver Ad-hoc-Schritt, der dem deklarativen, wiederholbaren IaC-Ansatz von Bicep widerspricht.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-104",
        "exam": "AZ-900",
        "category": "governance",
        "type": "hot_area",
        "prompt": "Welche Funktion wählen Sie, um eine Empfehlung zur Kostenoptimierung für eine laufende Ressource zu erhalten?",
        "options": ["Azure Advisor", "Azure Policy", "Azure Resource Health", "Azure DNS"],
        "answer": "Azure Advisor",
        "explanation": "Azure Advisor liefert personalisierte Empfehlungen unter anderem zu Kosten, Sicherheit, Zuverlässigkeit und Leistung. Policy dient dagegen der Regel- und Compliance-Steuerung.",
        "source": "https://learn.microsoft.com/en-us/azure/advisor/advisor-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-105",
        "exam": "AZ-900",
        "category": "governance",
        "type": "active_screen",
        "prompt": "Eine Ansicht zeigt Logabfragen, Zeitbereiche und Ergebnisse aus mehreren Ressourcen. Welche Azure-Komponente wird typischerweise verwendet?",
        "options": ["Log Analytics workspace", "Resource lock", "Pricing Calculator", "Availability set"],
        "answer": "Log Analytics workspace",
        "explanation": "Log Analytics workspaces sammeln und analysieren Protokolldaten mit Abfragen. Sie sind ein zentraler Bestandteil von Azure Monitor.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-106",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-monitoring",
        "case_order": 1,
        "case_text": "Ein Unternehmen möchte neue Azure-Ressourcen zentral überwachen. Das Betriebsteam braucht Metriken und Logs, Entwickler sollen Anwendungstelemetrie analysieren, und Ausfälle einzelner Ressourcen sollen sichtbar sein.",
        "prompt": "Welche Kombination erfüllt die Anforderungen? Wählen Sie alle zutreffenden Antworten.",
        "options": ["Azure Monitor für Metriken und Überwachung verwenden.", "Log Analytics für zentrale Protokollabfragen verwenden.", "Application Insights für Anwendungstelemetrie verwenden.", "Resource Health durch Tags ersetzen."],
        "answer": ["Azure Monitor für Metriken und Überwachung verwenden.", "Log Analytics für zentrale Protokollabfragen verwenden.", "Application Insights für Anwendungstelemetrie verwenden."],
        "explanation": "Azure Monitor deckt Überwachung ab, Log Analytics analysiert Logs und Application Insights fokussiert auf Anwendungstelemetrie. Tags liefern Metadaten, ersetzen aber keine Zustandsüberwachung.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-107",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Unternehmen benötigt für eine neue Kampagne vorübergehend zusätzliche Kapazität. Welche Cloud-Eigenschaft beschreibt das schnelle Hinzufügen und spätere Entfernen von Ressourcen?",
        "options": ["Elastizität", "Souveränität", "Mandantenfähigkeit", "Lokale Redundanz"],
        "answer": "Elastizität",
        "explanation": "Elastizität bezeichnet die Fähigkeit, Kapazität bedarfsgerecht zu erhöhen oder zu verringern. Skalierbarkeit und Elastizität überschneiden sich, aber der zeitabhängige Anpassungsaspekt ist hier entscheidend.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 3,
    },
    {
        "id": "az900-108",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche Aussagen beschreiben ein Hybrid-Cloud-Szenario? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Einige Workloads bleiben lokal, andere laufen in Azure.",
            "Identitäten oder Netzwerke können zwischen lokalen Systemen und Azure integriert werden.",
            "Alle Systeme müssen ausschließlich in einer Public Cloud liegen.",
            "Die Organisation kann eine schrittweise Migration planen.",
        ],
        "answer": [
            "Einige Workloads bleiben lokal, andere laufen in Azure.",
            "Identitäten oder Netzwerke können zwischen lokalen Systemen und Azure integriert werden.",
            "Die Organisation kann eine schrittweise Migration planen.",
        ],
        "explanation": "Hybrid Cloud verbindet lokale Infrastruktur mit Cloudressourcen. Das unterstützt Integration und schrittweise Migration, bedeutet aber nicht, dass alles in der Public Cloud liegen muss.",
        "source": "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-109",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "true_false",
        "prompt": "Eine Availability Set schützt automatisch vor jedem Ausfall einer gesamten Azure-Region.",
        "options": ["Wahr", "Falsch"],
        "answer": "Falsch",
        "explanation": "Availability Sets verteilen VMs innerhalb eines Rechenzentrums über Fault und Update Domains. Sie ersetzen keine regionsübergreifende Strategie und schützen nicht automatisch vor einem vollständigen Regionsausfall.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machines/availability",
        "difficulty": 4,
    },
    {
        "id": "az900-110",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "drag_drop",
        "prompt": "Ordnen Sie die Schritte für die Bereitstellung eines Azure Container Registry-Images in eine Container-App.",
        "options": [
            "Ein Image bauen und taggen",
            "Das Image in die Registry pushen",
            "Die Container-App auf das Image verweisen",
            "Start und Protokolle der App prüfen",
        ],
        "answer": [
            "Ein Image bauen und taggen",
            "Das Image in die Registry pushen",
            "Die Container-App auf das Image verweisen",
            "Start und Protokolle der App prüfen",
        ],
        "explanation": "Die Registry stellt das Image für den Dienst bereit. Nach dem Verweis auf das Image sollte der Startzustand und die Laufzeit über Logs geprüft werden.",
        "source": "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli",
        "difficulty": 4,
    },
    {
        "id": "az900-111",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "active_screen",
        "prompt": "Eine simulierte Portalansicht zeigt Subnetze, Routing und eine Network Security Group. Welche Ressource wird hier hauptsächlich konfiguriert?",
        "options": ["Azure Virtual Network", "Azure Cost Management", "Microsoft Purview", "Recovery Services vault"],
        "answer": "Azure Virtual Network",
        "explanation": "Subnets, Routing und Network Security Groups gehören zur Konfiguration eines Azure Virtual Network. Die anderen Optionen erfüllen andere Verwaltungs- oder Schutzaufgaben.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-112",
        "exam": "AZ-900",
        "category": "governance",
        "type": "matching",
        "prompt": "Ordnen Sie das Überwachungswerkzeug seinem typischen Zweck zu.",
        "pairs": [
            ["Azure Monitor", "Metriken, Logs und Warnungen überwachen"],
            ["Application Insights", "Anwendungstelemetrie und Abhängigkeiten analysieren"],
            ["Azure Service Health", "Dienstprobleme und geplante Wartungen anzeigen"],
        ],
        "answer": [
            ["Azure Monitor", "Metriken, Logs und Warnungen überwachen"],
            ["Application Insights", "Anwendungstelemetrie und Abhängigkeiten analysieren"],
            ["Azure Service Health", "Dienstprobleme und geplante Wartungen anzeigen"],
        ],
        "explanation": "Azure Monitor ist die übergreifende Überwachungsplattform. Application Insights fokussiert Anwendungen, während Service Health über Azure-Dienstereignisse informiert.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-113",
        "exam": "AZ-900",
        "category": "governance",
        "type": "hot_area",
        "prompt": "Welche Portal-Funktion wählen Sie, um den Zugriff einer Benutzergruppe auf eine Resource Group zu begrenzen?",
        "options": ["Azure RBAC", "Azure Advisor", "Azure Service Health", "Azure Pricing Calculator"],
        "answer": "Azure RBAC",
        "explanation": "Azure RBAC weist Rollen auf einem bestimmten Scope zu, beispielsweise einer Resource Group. Dadurch können Berechtigungen nach dem Prinzip der geringsten Rechte vergeben werden.",
        "source": "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-114",
        "exam": "AZ-900",
        "category": "governance",
        "type": "case",
        "case_group": "governance-self-service",
        "case_order": 3,
        "case_text": "Ein Unternehmen betreibt mehrere Azure-Webanwendungen. Entwickler sollen standardisiert und selbstständig bereitstellen können. Nur genehmigte Regionen und Ressourcentypen dürfen verwendet werden, Kosten müssen nach Team auswertbar sein und Administratoren sollen nur die benötigten Rechte erhalten.",
        "prompt": "Welche Maßnahmen sind geeignet? Wählen Sie alle zutreffenden Antworten.",
        "options": [
            "Azure Policy für Regionen und Ressourcentypen verwenden.",
            "Tags für Team- oder Kostenstelleninformationen verwenden.",
            "Allen Entwicklern Owner auf Management-Group-Ebene geben.",
            "RBAC mit einem möglichst kleinen Scope einsetzen.",
        ],
        "answer": [
            "Azure Policy für Regionen und Ressourcentypen verwenden.",
            "Tags für Team- oder Kostenstelleninformationen verwenden.",
            "RBAC mit einem möglichst kleinen Scope einsetzen.",
        ],
        "explanation": "Policy steuert zulässige Konfigurationen, Tags unterstützen Kosten- und Organisationsauswertungen und RBAC begrenzt Berechtigungen. Owner auf Management-Group-Ebene wäre unnötig weitreichend.",
        "source": "https://learn.microsoft.com/en-us/azure/governance/policy/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-115",
        "exam": "AZ-900",
        "category": "governance",
        "type": "build_list",
        "prompt": "Wählen Sie die passenden Schritte aus und bauen Sie einen sinnvollen Ablauf zur Untersuchung eines Ressourcenproblems auf. Ein Element gehört nicht zur systematischen Fehlersuche.",
        "options": [
            "Resource Health der betroffenen Ressource prüfen",
            "Azure Service Health auf übergreifende Dienstereignisse prüfen",
            "Azure Monitor-Metriken und Logs untersuchen",
            "Ursache und Folgemaßnahmen dokumentieren",
            "Support-Ticket ohne vorherige Diagnose eröffnen",
        ],
        "answer": [
            "Resource Health der betroffenen Ressource prüfen",
            "Azure Service Health auf übergreifende Dienstereignisse prüfen",
            "Azure Monitor-Metriken und Logs untersuchen",
            "Ursache und Folgemaßnahmen dokumentieren",
        ],
        "explanation": "Resource Health grenzt zuerst den Zustand der einzelnen Ressource ein. Service Health prüft anschließend Azure-weite oder abonnementsbezogene Ereignisse, Monitor liefert technische Signale (Metriken/Logs), und die Dokumentation hält Ursache und Maßnahmen fest. Ein Support-Ticket ohne vorherige Diagnose überspringt die verfügbaren Selbstdiagnose-Tools und verzögert unnötig die Problemlösung.",
        "source": "https://learn.microsoft.com/en-us/azure/service-health/resource-health-overview",
        "difficulty": 4,
    },
    {
        "id": "az900-116",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Welche Aussage beschreibt den Unterschied zwischen CapEx und OpEx im Cloudkontext am besten?",
        "options": [
            "CapEx sind Vorabinvestitionen; OpEx sind laufende verbrauchs- oder betriebsbezogene Kosten.",
            "CapEx und OpEx bedeuten beide ausschließlich monatliche Azure-Rechnungen.",
            "OpEx erfordert immer den Kauf physischer Server.",
            "CapEx ist nur für Softwarelizenzen zulässig.",
        ],
        "answer": "CapEx sind Vorabinvestitionen; OpEx sind laufende verbrauchs- oder betriebsbezogene Kosten.",
        "explanation": "CapEx (Capital Expenditure) sind Vorabinvestitionen, z. B. in eigene Hardware, während OpEx (Operational Expenditure) laufende, nutzungsabhängige Kosten wie Cloud-Abrechnungen sind. Beide Begriffe beschreiben keine reinen Azure-Rechnungen, OpEx erfordert gerade keinen Hardwarekauf, und CapEx ist nicht auf Softwarelizenzen beschränkt, sondern betrifft jede Vorabinvestition in Vermögenswerte.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 3,
    },
    {
        "id": "az900-117",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Unternehmen betreibt eine eigene Datenbank-Engine auf einer Azure-VM (IaaS). Wer ist laut Shared-Responsibility-Modell für das Einspielen von Betriebssystem-Patches verantwortlich?",
        "options": [
            "Der Kunde",
            "Microsoft",
            "Beide gemeinsam, aber nur bei Enterprise Agreements",
            "Niemand, das Betriebssystem wird automatisch nie gepatcht",
        ],
        "answer": "Der Kunde",
        "explanation": "Bei IaaS betreibt Microsoft nur physische Infrastruktur, Netzwerk und Virtualisierungsschicht; Betriebssystem, dessen Patches sowie alles darüber (z. B. die Datenbank-Engine) liegen beim Kunden. 'Microsoft' wäre bei PaaS/SaaS teilweise richtig, hier aber nicht bei reinem IaaS. Ein Enterprise Agreement ändert nichts an der technischen Verantwortungsteilung, und Patches werden nicht automatisch von niemandem übernommen — ungepatchte VMs bleiben ein Sicherheitsrisiko des Kunden.",
        "source": "https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility",
        "difficulty": 3,
    },
    {
        "id": "az900-118",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Start-up möchte keine Vorabinvestition in Hardware tätigen und nur für tatsächlich genutzte Rechenleistung pro Stunde bezahlen. Welches Kostenmodell beschreibt das?",
        "options": [
            "OpEx (nutzungsbasiert)",
            "CapEx (Vorabinvestition)",
            "Ein Fixkosten-Leasingmodell über 5 Jahre",
            "Eine einmalige, unbefristete Lizenzgebühr",
        ],
        "answer": "OpEx (nutzungsbasiert)",
        "explanation": "Nutzungsbasierte, laufende Kosten ohne Vorabkauf von Hardware entsprechen dem OpEx-Modell (Operational Expenditure). CapEx bedeutet dagegen eine Vorabinvestition in eigene Infrastruktur, die abgeschrieben wird. Ein mehrjähriges Fixkosten-Leasing und eine einmalige Lizenzgebühr sind beides Formen vorab gebundener Kosten und widersprechen dem Wunsch nach reiner, flexibler Verbrauchsabrechnung.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 2,
    },
    {
        "id": "az900-119",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Onlineshop verkauft meist gleichmäßig, hat aber am Black Friday für wenige Stunden ein Vielfaches der normalen Last und fällt danach wieder auf Normalniveau. Welches Cloud-Merkmal beschreibt am besten die automatische, temporäre Bereitstellung und den anschließenden Abbau zusätzlicher Ressourcen?",
        "options": [
            "Elastizität",
            "Skalierbarkeit",
            "Fehlertoleranz",
            "Agilität",
        ],
        "answer": "Elastizität",
        "explanation": "Elastizität beschreibt speziell das automatische, dynamische Hinzufügen und Entfernen von Ressourcen im Rhythmus der tatsächlichen Nachfrage, oft ohne manuelles Eingreifen. Skalierbarkeit ist der allgemeinere Begriff für die Fähigkeit, Kapazität zu erhöhen oder zu verringern, impliziert aber nicht zwingend Automatik oder Kurzfristigkeit. Fehlertoleranz betrifft das Überleben von Ausfällen, Agilität die Geschwindigkeit der Bereitstellung neuer Dienste — beides beschreibt nicht das auf/ab-Verhalten bei Lastspitzen.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 3,
    },
    {
        "id": "az900-120",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Eine Bank muss bestimmte sensible Daten aus regulatorischen Gründen zwingend on-premises behalten, möchte aber Azure für zusätzliche Rechenlast bei Lastspitzen nutzen. Welches Bereitstellungsmodell passt am besten?",
        "options": [
            "Hybrid Cloud",
            "Public Cloud",
            "Private Cloud",
            "Community Cloud",
        ],
        "answer": "Hybrid Cloud",
        "explanation": "Eine Hybrid Cloud kombiniert on-premises-Infrastruktur mit Public-Cloud-Ressourcen und erlaubt genau dieses Szenario: regulierte Daten bleiben lokal, während elastische Rechenlast in die Public Cloud ausgelagert wird. Reine Public Cloud würde die Datenresidenz-Anforderung verletzen, reine Private Cloud böte keine öffentliche Skalierungsoption, und 'Community Cloud' ist kein von Azure verwendetes Standardmodell für dieses Szenario.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 2,
    },
    {
        "id": "az900-121",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "true_false",
        "prompt": "Multitenancy bedeutet, dass sich mehrere Kunden dieselbe zugrunde liegende Infrastruktur teilen, ihre Daten und Ressourcen aber logisch voneinander isoliert sind.",
        "options": ["Wahr", "Falsch"],
        "answer": "Wahr",
        "explanation": "Multitenancy in Azure bedeutet gemeinsam genutzte physische Infrastruktur bei gleichzeitig logischer Trennung der Kundendaten und -ressourcen durch Isolationsmechanismen auf Plattformebene. Kunden bemerken die gemeinsame Nutzung im Normalbetrieb nicht, da sie keinen Zugriff auf die Ressourcen anderer Mandanten haben.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 2,
    },
    {
        "id": "az900-122",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Eine Workload läuft rund um die Uhr über 3 Jahre mit vorhersagbarer, konstanter Auslastung. Welche Preisoption reduziert die Kosten gegenüber nutzungsbasierten (Pay-as-you-go) Preisen am stärksten?",
        "options": [
            "Azure-Reservierungen (Azure Reservations)",
            "Spot-VMs",
            "Pay-as-you-go",
            "Free Tier",
        ],
        "answer": "Azure-Reservierungen (Azure Reservations)",
        "explanation": "Azure-Reservierungen bieten deutliche Rabatte gegenüber Pay-as-you-go, wenn im Voraus eine feste Nutzungsdauer (z. B. 1 oder 3 Jahre) zugesagt wird — ideal für vorhersagbare, dauerhafte Workloads. Spot-VMs sind zwar günstiger, aber jederzeit unterbrechbar und daher für konstante Dauerlast ungeeignet. Pay-as-you-go bleibt teurer bei Dauerbetrieb, und der Free Tier deckt nur begrenzte kostenlose Kontingente ab, nicht Produktionsworkloads über Jahre.",
        "source": "https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations",
        "difficulty": 3,
    },
    {
        "id": "az900-123",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "single",
        "prompt": "Ein Batch-Rendering-Job kann jederzeit unterbrochen und später fortgesetzt werden. Das Team möchte die Rechenkosten minimieren und toleriert, dass die VM bei Kapazitätsengpässen vom Anbieter beendet werden kann. Welche VM-Preisoption passt am besten?",
        "options": [
            "Spot-VMs",
            "Azure-Reservierungen",
            "Dedicated Hosts",
            "Azure Hybrid Benefit",
        ],
        "answer": "Spot-VMs",
        "explanation": "Spot-VMs nutzen ungenutzte Azure-Kapazität zu stark reduzierten Preisen, können aber bei Kapazitätsbedarf mit kurzer Vorwarnung entzogen werden — genau passend für unterbrechbare Batch-Workloads. Azure-Reservierungen und Dedicated Hosts zielen auf dauerhafte, unterbrechungsfreie Workloads ab und sind teurer als nötig für dieses Szenario. Azure Hybrid Benefit betrifft Lizenzkosten, nicht die VM-Verfügbarkeit oder -Unterbrechbarkeit.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms",
        "difficulty": 3,
    },
    {
        "id": "az900-124",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein Unternehmen besitzt bereits Windows-Server-Lizenzen mit Software Assurance und möchte diese nutzen, um die Lizenzkosten für Azure-VMs zu senken. Welches Programm ermöglicht das?",
        "options": [
            "Azure Hybrid Benefit",
            "Azure-Reservierungen (Azure Reservations)",
            "Azure Cost Management-Budgets",
            "Azure Policy",
        ],
        "answer": "Azure Hybrid Benefit",
        "explanation": "Azure Hybrid Benefit erlaubt es, bereits vorhandene, lizenzierte Windows-Server- (oder SQL-Server-)Lizenzen mit Software Assurance in Azure weiterzuverwenden und dadurch reine Kompute-Kosten statt vollem Lizenzpreis zu zahlen. Azure-Reservierungen betreffen die Kapazitätszusage, nicht bestehende Lizenzen. Cost Management-Budgets überwachen nur Ausgaben, und Azure Policy erzwingt Konfigurationsregeln — keines davon verrechnet vorhandene Lizenzen.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machines/windows/hybrid-use-benefit-licensing",
        "difficulty": 3,
    },
    {
        "id": "az900-125",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein Unternehmen benötigt für kritische Produktionsausfälle rund um die Uhr eine garantierte Erstreaktion von unter einer Stunde. Welcher Azure-Supportplan aus dem Standardangebot bietet die schnellste Reaktionszeit?",
        "options": [
            "Professional Direct",
            "Basic (kostenlos)",
            "Developer",
            "Standard",
        ],
        "answer": "Professional Direct",
        "explanation": "Professional Direct bietet für Vorfälle mit kritischen Auswirkungen rund um die Uhr eine Erstreaktion in unter einer Stunde. Basic ist kostenlos, deckt aber nur Abrechnungs-/Kontofragen ohne technische Reaktionszeit-SLA ab. Developer richtet sich an Entwicklungs-/Testumgebungen mit Reaktion nur während Geschäftszeiten. Standard bietet zwar 24/7-Support, aber mit längeren garantierten Reaktionszeiten als Professional Direct.",
        "source": "https://azure.microsoft.com/en-us/support/plans/",
        "difficulty": 3,
    },
    {
        "id": "az900-126",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein Unternehmen muss vor einer Migration nachweisen, dass Azure bestimmte branchenspezifische Zertifizierungen (z. B. ISO 27001) erfüllt. Wo findet das Unternehmen offizielle Compliance-Berichte und Zertifizierungsnachweise zu Azure?",
        "options": [
            "Microsoft Service Trust Portal / Trust Center",
            "Azure Advisor",
            "Azure Monitor",
            "Azure Resource Graph",
        ],
        "answer": "Microsoft Service Trust Portal / Trust Center",
        "explanation": "Das Microsoft Service Trust Portal (Teil des Microsoft Trust Center) veröffentlicht offizielle Audit-Berichte, Zertifizierungen und Compliance-Nachweise für Microsoft-Cloud-Dienste. Azure Advisor gibt Optimierungsempfehlungen für eigene Ressourcen, Azure Monitor sammelt Telemetriedaten, und Azure Resource Graph dient der Abfrage von Ressourcenmetadaten — keines davon liefert offizielle externe Zertifizierungsnachweise.",
        "source": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-home",
        "difficulty": 2,
    },
    {
        "id": "az900-127",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Ein Unternehmen möchte im Falle eines regionalen Ausfalls eine von Microsoft koordinierte, geografisch getrennte Wiederherstellung von Azure-Plattformdiensten sicherstellen. Welches Konzept beschreibt dieses feste Paar von Regionen?",
        "options": [
            "Region Pair (Regionspaar)",
            "Availability Zone",
            "Availability Set",
            "Resource Group",
        ],
        "answer": "Region Pair (Regionspaar)",
        "explanation": "Ein Region Pair verbindet zwei Regionen innerhalb derselben Geografie; Microsoft priorisiert bei großflächigen Ausfällen die Wiederherstellung mindestens einer Region je Paar und führt Plattform-Updates nacheinander statt gleichzeitig in beiden Regionen durch. Availability Zones liegen innerhalb einer einzelnen Region, Availability Sets innerhalb eines Rechenzentrums, und eine Resource Group ist nur ein logischer Verwaltungscontainer ohne physische Redundanzbedeutung.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/cross-region-replication-azure",
        "difficulty": 3,
    },
    {
        "id": "az900-128",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Eine Anwendung besteht aus zwei voneinander abhängigen Diensten in Serie: Dienst A hat eine SLA von 99,9 % und Dienst B eine SLA von 99,95 %. Welche kombinierte Verfügbarkeit hat die Gesamtanwendung ungefähr, wenn beide Dienste gleichzeitig verfügbar sein müssen?",
        "options": [
            "ca. 99,85 %",
            "99,95 % (das Maximum beider Werte)",
            "100 %, da Azure-SLAs immer addiert werden",
            "199,85 % (die Summe beider Werte)",
        ],
        "answer": "ca. 99,85 %",
        "explanation": "Bei voneinander abhängigen Diensten in Serie wird die kombinierte Verfügbarkeit durch Multiplikation der Einzelwahrscheinlichkeiten berechnet: 0,999 × 0,9995 ≈ 0,9985, also ca. 99,85 % — niedriger als jeder Einzelwert. SLAs werden nicht addiert und ergeben nie automatisch 100 % oder Werte über 100 %, und das bloße Maximum beider Werte ignoriert, dass ein Ausfall irgendeines der beiden Dienste die gesamte Kette betrifft.",
        "source": "https://learn.microsoft.com/en-us/azure/reliability/overview",
        "difficulty": 4,
    },
    {
        "id": "az900-129",
        "exam": "AZ-900",
        "category": "architecture",
        "type": "single",
        "prompt": "Ein Unternehmen möchte zwei VMs so bereitstellen, dass ein Hardwareausfall (Server, Netzwerk-Switch) innerhalb eines Rechenzentrums niemals beide VMs gleichzeitig betrifft, ohne dafür mehrere komplette Rechenzentren der Region zu benötigen. Welche Option passt am besten?",
        "options": [
            "Availability Set",
            "Availability Zone",
            "Region Pair",
            "Nur ein Load Balancer",
        ],
        "answer": "Availability Set",
        "explanation": "Ein Availability Set verteilt VMs innerhalb eines einzelnen Rechenzentrums auf verschiedene Fehler- und Updatedomänen, sodass ein einzelner Hardware- oder Wartungsausfall nicht beide VMs gleichzeitig trifft — ganz ohne mehrere Rechenzentren. Availability Zones benötigen mehrere physisch getrennte Rechenzentren innerhalb der Region, Region Pairs operieren regionsübergreifend, und ein Load Balancer allein verteilt nur Datenverkehr, ohne Fehlerdomänen-Trennung zu garantieren.",
        "source": "https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview",
        "difficulty": 3,
    },
    {
        "id": "az900-130",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein europäisches Unternehmen möchte sicherstellen, dass Kundendaten und zugehörige Diagnosedaten für wichtige Microsoft-Cloud-Dienste innerhalb der EU verarbeitet und gespeichert werden. Welches Microsoft-Angebot adressiert genau dieses Bedürfnis?",
        "options": [
            "EU Data Boundary",
            "Azure Policy",
            "Azure Lighthouse",
            "Azure Arc",
        ],
        "answer": "EU Data Boundary",
        "explanation": "Die EU Data Boundary ist Microsofts konkrete, schrittweise erweiterte Zusage, Kunden- und zunehmend auch Diagnosedaten wichtiger Cloud-Dienste innerhalb der EU/EFTA zu verarbeiten und zu speichern. Azure Policy kann Regionsbeschränkungen technisch erzwingen, ist aber ein allgemeines Governance-Werkzeug und nicht die spezifische Datenresidenz-Zusage selbst. Azure Lighthouse betrifft partnerübergreifende Verwaltung, Azure Arc die Verwaltung außerhalb Azures — beides ohne Bezug zur Datenresidenz.",
        "source": "https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn",
        "difficulty": 3,
    },
    {
        "id": "az900-131",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein Unternehmen betreibt Server in der eigenen Zentrale, bei einem anderen Cloud-Anbieter und in Azure. Es möchte alle diese Ressourcen über eine einheitliche Steuerungsebene mit Azure Policy, Tags und Monitoring verwalten, ohne sie physisch nach Azure zu migrieren. Welcher Dienst ermöglicht das?",
        "options": [
            "Azure Arc",
            "Azure Migrate",
            "Azure Site Recovery",
            "Azure Lighthouse",
        ],
        "answer": "Azure Arc",
        "explanation": "Azure Arc erweitert die Azure-Steuerungsebene (Policy, Tags, Monitoring, RBAC) auf Server, Kubernetes-Cluster und Daten außerhalb von Azure, ohne dass eine physische Migration nötig ist. Azure Migrate dient der tatsächlichen Migration von Workloads nach Azure, Azure Site Recovery repliziert für Notfallwiederherstellung, und Azure Lighthouse ermöglicht Partnern die tenantübergreifende Verwaltung mehrerer Kunden-Abonnements — keines davon erweitert die Governance auf fremd gehostete Server ohne Migration.",
        "source": "https://learn.microsoft.com/en-us/azure/azure-arc/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-132",
        "exam": "AZ-900",
        "category": "governance",
        "type": "single",
        "prompt": "Ein Managed-Service-Provider möchte Azure-Ressourcen in den Tenants mehrerer Kunden zentral verwalten, ohne für jeden Kunden separate Anmeldedaten zu benötigen. Welcher Dienst ist dafür vorgesehen?",
        "options": [
            "Azure Lighthouse",
            "Azure Arc",
            "Microsoft Entra Conditional Access",
            "Azure Deployment Stacks",
        ],
        "answer": "Azure Lighthouse",
        "explanation": "Azure Lighthouse ermöglicht Dienstanbietern den delegierten Zugriff auf Kunden-Tenants über eine einzige Anmeldung und ein zentrales Verwaltungs-Dashboard, statt für jeden Kunden separat einzuloggen. Azure Arc erweitert die Steuerungsebene auf Ressourcen außerhalb Azures (nicht auf Multi-Tenant-Verwaltung), Microsoft Entra Conditional Access steuert Zugriffsbedingungen innerhalb eines Tenants, und Azure Deployment Stacks verwalten Ressourcensammlungen als zusammengehörige Bereitstellung — keines davon ist für tenantübergreifende Partnerverwaltung gedacht.",
        "source": "https://learn.microsoft.com/en-us/azure/lighthouse/overview",
        "difficulty": 3,
    },
    {
        "id": "az900-133",
        "exam": "AZ-900",
        "category": "cloud",
        "type": "multi",
        "prompt": "Welche der folgenden Aussagen beschreiben zutreffend Vorteile von Cloud Computing? Wähle alle zutreffenden Antworten.",
        "options": [
            "Nutzungsbasierte Kosten statt hoher Vorabinvestitionen",
            "Weltweite Bereitstellung in Minuten statt Wochen",
            "Automatische Eliminierung jeglicher Sicherheitsverantwortung des Kunden",
            "Möglichkeit, Kapazität schnell an Nachfrage anzupassen",
        ],
        "answer": [
            "Nutzungsbasierte Kosten statt hoher Vorabinvestitionen",
            "Weltweite Bereitstellung in Minuten statt Wochen",
            "Möglichkeit, Kapazität schnell an Nachfrage anzupassen",
        ],
        "explanation": "Cloud Computing bietet nutzungsbasierte Kosten, schnelle globale Bereitstellung und flexible Kapazitätsanpassung. Die Aussage zur 'automatischen Eliminierung jeglicher Sicherheitsverantwortung' ist falsch: Das Shared-Responsibility-Modell verlagert nur einen Teil der Verantwortung an Microsoft, der Kunde behält je nach Servicemodell (IaaS/PaaS/SaaS) weiterhin eigene Sicherheitsaufgaben wie Identitäts-, Daten- oder Zugriffsschutz.",
        "source": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
        "difficulty": 3,
    },
]


class DragOrderList(tk.Frame):
    """Mouse-draggable ordered list for 'ordering' / 'drag_drop' question types.

    Items are real draggable rows: press and hold to lift a row (shown as a
    floating ghost that follows the cursor), release over another row to drop
    it into that position. No move-up/move-down buttons involved.
    """

    def __init__(self, parent, items):
        super().__init__(parent, bg=WHITE)
        self.items = list(items)
        self.rows = []
        self.ghost = None
        self.drag_item = None
        self.locked = False
        self.list_frame = tk.Frame(self, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.list_frame.pack(fill="x")
        self._render()

    def _render(self):
        for row in self.rows:
            row.destroy()
        self.rows = []
        for index, text in enumerate(self.items):
            row = self._make_row(text, index)
            row.pack(fill="x")
            self.rows.append(row)

    def _render_preserving_viewport(self):
        """Rebuild rows without moving an enclosing scrollable practice tab."""
        canvases = []
        parent = self.master
        while parent is not None:
            if isinstance(parent, tk.Canvas):
                canvases.append((parent, parent.yview()[0]))
            parent = parent.master
        self._render()

        def restore_viewport():
            for canvas, position in canvases:
                if canvas.winfo_exists():
                    canvas.yview_moveto(position)

        self.update_idletasks()
        restore_viewport()
        self.after_idle(restore_viewport)

    def _make_row(self, text, index):
        cursor = "arrow" if self.locked else "fleur"
        row = tk.Frame(self.list_frame, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER, cursor=cursor)
        handle = tk.Label(row, text="⠿⠿", bg=SURFACE, fg=AZURE_LIGHT, font=("Segoe UI", 11, "bold"), width=3, cursor=cursor)
        handle.pack(side="left", padx=(10, 2), pady=9)
        idx_label = tk.Label(row, text=str(index + 1), bg=SURFACE, fg=MUTED, font=("Segoe UI", 10, "bold"), width=2, cursor=cursor)
        idx_label.pack(side="left")
        label = tk.Label(row, text=text, bg=SURFACE, fg=INK, font=("Segoe UI", 10), anchor="w", justify="left", wraplength=800, cursor=cursor)
        label.pack(side="left", fill="x", expand=True, padx=(8, 10), pady=9)
        row.item_text = text
        if not self.locked:
            for widget in (row, handle, idx_label, label):
                widget.bind("<ButtonPress-1>", lambda event, t=text: self._start_drag(t, event))
                widget.bind("<B1-Motion>", self._on_drag)
                widget.bind("<ButtonRelease-1>", self._on_drop)
        return row

    def _row_for(self, text):
        for row in self.rows:
            if row.item_text == text:
                return row
        return None

    def _start_drag(self, text, event):
        if self.locked:
            return
        self.drag_item = text
        row = self._row_for(text)
        if row is not None:
            row.configure(bg=SURFACE_SELECTED)
            for child in row.winfo_children():
                child.configure(bg=SURFACE_SELECTED)
        width = self.list_frame.winfo_width() or 800
        self.ghost = tk.Label(
            self.list_frame, text=f"⠿⠿  {text}", bg=AZURE_BLUE, fg=TEXT_ON_ACCENT, font=("Segoe UI", 10, "bold"),
            anchor="w", padx=10, pady=9,
        )
        rel_y = event.y_root - self.list_frame.winfo_rooty()
        self.ghost.place(x=0, y=max(0, rel_y - 18), width=width)
        self.ghost.lift()

    def _on_drag(self, event):
        if self.locked or self.ghost is None:
            return
        rel_y = event.y_root - self.list_frame.winfo_rooty()
        self.ghost.place(y=max(0, rel_y - 18))

    def _target_index(self, rel_y):
        for index, row in enumerate(self.rows):
            row_center = row.winfo_y() + row.winfo_height() / 2
            if rel_y < row_center:
                return index
        return len(self.rows)

    def _on_drop(self, event):
        if self.locked or self.ghost is None:
            return
        rel_y = event.y_root - self.list_frame.winfo_rooty()
        target_index = self._target_index(rel_y)
        self.ghost.destroy()
        self.ghost = None
        current_index = self.items.index(self.drag_item)
        item = self.items.pop(current_index)
        if target_index > current_index:
            target_index -= 1
        self.items.insert(max(0, min(len(self.items), target_index)), item)
        self.drag_item = None
        self._render_preserving_viewport()

    def get_order(self):
        return list(self.items)

    def lock(self):
        self.locked = True
        self._render()


class DragBuildList(tk.Frame):
    """Two-pane drag-and-drop picker for 'build_list' questions.

    A pool of available steps (including distractors that do not belong in
    the final answer) sits on the left; the learner drags the correct steps
    into the ordered target list on the right, and can drag items back out.
    """

    def __init__(self, parent, pool_items, target_items):
        super().__init__(parent, bg=WHITE)
        self.pool_items = list(pool_items)
        self.target_items = list(target_items)
        self.locked = False
        self.drag_item = None
        self.drag_source = None
        self.ghost = None
        self.pool_rows = []
        self.target_rows = []

        columns = tk.Frame(self, bg=WHITE)
        columns.pack(fill="both", expand=True)

        pool_col = tk.Frame(columns, bg=WHITE)
        pool_col.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(pool_col, text="Verfügbare Schritte (nicht jeder wird benötigt)", font=("Segoe UI", 10, "bold"), fg=MUTED, bg=WHITE).pack(anchor="w", pady=(0, 4))
        self.pool_frame = tk.Frame(pool_col, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER, height=220)
        self.pool_frame.pack(fill="both", expand=True)

        target_col = tk.Frame(columns, bg=WHITE)
        target_col.pack(side="left", fill="both", expand=True, padx=(8, 0))
        tk.Label(target_col, text="Ihre Reihenfolge", font=("Segoe UI", 10, "bold"), fg=MUTED, bg=WHITE).pack(anchor="w", pady=(0, 4))
        self.target_frame = tk.Frame(target_col, bg=SURFACE_ACCENT, highlightthickness=2, highlightbackground=AZURE_BLUE, height=220)
        self.target_frame.pack(fill="both", expand=True)

        self.empty_hint = tk.Label(self.target_frame, text="Elemente per Drag & Drop hierher ziehen", bg=SURFACE_ACCENT, fg=MUTED, font=("Segoe UI", 10, "italic"))

        self._render()

    def _render(self):
        for row in self.pool_rows + self.target_rows:
            row.destroy()
        self.pool_rows = []
        self.target_rows = []
        for text in self.pool_items:
            row = self._make_row(self.pool_frame, text, "pool")
            row.pack(fill="x", pady=3, padx=3)
            self.pool_rows.append(row)
        self.empty_hint.pack_forget()
        if not self.target_items:
            self.empty_hint.pack(pady=18)
        for index, text in enumerate(self.target_items):
            row = self._make_row(self.target_frame, text, "target", index=index)
            row.pack(fill="x", pady=3, padx=3)
            self.target_rows.append(row)

    def _render_preserving_viewport(self):
        """Rebuild rows without moving an enclosing scrollable practice tab."""
        canvases = []
        parent = self.master
        while parent is not None:
            if isinstance(parent, tk.Canvas):
                canvases.append((parent, parent.yview()[0]))
            parent = parent.master
        self._render()

        def restore_viewport():
            for canvas, position in canvases:
                if canvas.winfo_exists():
                    canvas.yview_moveto(position)

        self.update_idletasks()
        restore_viewport()
        self.after_idle(restore_viewport)

    def _make_row(self, parent, text, source, index=None):
        cursor = "arrow" if self.locked else "fleur"
        bg = WHITE if source == "pool" else SURFACE_SELECTED
        row = tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground=AZURE_BORDER, cursor=cursor)
        widgets = [row]
        if index is not None:
            idx_label = tk.Label(row, text=str(index + 1), bg=bg, fg=AZURE_BLUE, font=("Segoe UI", 10, "bold"), width=2, cursor=cursor)
            idx_label.pack(side="left", padx=(6, 2), pady=6)
            widgets.append(idx_label)
        label = tk.Label(row, text=text, bg=bg, fg=INK, font=("Segoe UI", 11), anchor="w", justify="left", wraplength=400, cursor=cursor)
        label.pack(side="left", fill="x", expand=True, padx=(4, 6), pady=6)
        widgets.append(label)
        row.item_text = text
        row.item_source = source
        if not self.locked:
            for widget in widgets:
                widget.bind("<ButtonPress-1>", lambda event, t=text, s=source: self._start_drag(t, s, event))
                widget.bind("<B1-Motion>", self._on_drag)
                widget.bind("<ButtonRelease-1>", self._on_drop)
        return row

    def _start_drag(self, text, source, event):
        if self.locked:
            return
        self.drag_item = text
        self.drag_source = source
        self.ghost = tk.Label(self, text=text, bg=AZURE_BLUE, fg=TEXT_ON_ACCENT, font=("Segoe UI", 11, "bold"), anchor="w", padx=8, pady=6, wraplength=340)
        self.ghost.place(x=event.x_root - self.winfo_rootx() - 60, y=event.y_root - self.winfo_rooty() - 14)
        self.ghost.lift()

    def _on_drag(self, event):
        if self.locked or self.ghost is None:
            return
        self.ghost.place(x=event.x_root - self.winfo_rootx() - 60, y=event.y_root - self.winfo_rooty() - 14)

    def _point_in(self, widget, x_root, y_root):
        wx, wy = widget.winfo_rootx(), widget.winfo_rooty()
        return wx <= x_root <= wx + widget.winfo_width() and wy <= y_root <= wy + widget.winfo_height()

    def _target_drop_index(self, y_root):
        for index, row in enumerate(self.target_rows):
            row_center = row.winfo_rooty() + row.winfo_height() / 2
            if y_root < row_center:
                return index
        return len(self.target_rows)

    def _on_drop(self, event):
        if self.locked or self.ghost is None:
            return
        self.ghost.destroy()
        self.ghost = None
        over_target = self._point_in(self.target_frame, event.x_root, event.y_root)
        over_pool = self._point_in(self.pool_frame, event.x_root, event.y_root)

        item = self.drag_item
        if self.drag_source == "pool" and item in self.pool_items:
            self.pool_items.remove(item)
        elif self.drag_source == "target" and item in self.target_items:
            self.target_items.remove(item)

        if over_target:
            index = self._target_drop_index(event.y_root)
            self.target_items.insert(index, item)
        elif over_pool:
            self.pool_items.append(item)
        elif self.drag_source == "pool":
            self.pool_items.append(item)
        else:
            self.target_items.append(item)

        self.drag_item = None
        self.drag_source = None
        self._render_preserving_viewport()

    def get_target(self):
        return list(self.target_items)

    def lock(self):
        self.locked = True
        self._render()


def compute_scaled_score(domain_results):
    """Blueprint-weighted score on Microsoft's 100-1000 scale (pass >= 700).

    Uses EXAM_DOMAIN_WEIGHTS (blueprint midpoints) instead of a flat overall
    percentage, since the real exam does not treat every question as equally
    "worth" the same across domains. Domains with no attempted questions are
    excluded and the remaining weights are renormalized so partial exams
    (e.g. type practice) still produce a meaningful estimate.
    """
    weighted_sum = 0.0
    weight_total = 0.0
    for category, weight in EXAM_DOMAIN_WEIGHTS.items():
        stats = domain_results.get(category)
        if not stats or not stats.get("total"):
            continue
        accuracy = stats["correct"] / stats["total"]
        weighted_sum += accuracy * weight
        weight_total += weight
    if weight_total == 0:
        return 100, False
    weighted_accuracy = weighted_sum / weight_total
    scaled = round(100 + weighted_accuracy * 900)
    scaled = max(100, min(1000, scaled))
    return scaled, scaled >= EXAM_PASS_SCALED_SCORE


class AzureLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure Learning")
        self.root.geometry("1360x880")
        self.root.minsize(1080, 720)
        self.root.configure(bg=AZURE_PALE)

        self.db = self._init_db()
        self.questions = self._load_questions()
        self.current_learn_question = None
        self.current_weak_question = None
        self.current_exam_questions = []
        self.exam_index = 0
        self.exam_answers = {}
        self.exam_marked = set()
        self.exam_deadline = None
        self.exam_timer_id = None
        self.selected_question_map = {}
        self.drag_index = None
        self.current_question_frame = None
        self.current_question_mode = None
        self.current_feedback_frame = None
        self.type_practice_question = None
        self.current_answer_locked = False
        self.last_learn_question_id = None
        self.current_answer_area = None
        self.current_question_controls = None
        self.last_exam_result = None
        self.exam_review_active = False
        self.today_plan_entries = []
        self.today_plan_index = 0
        self.exam_review_questions = []
        self.exam_review_index = 0

        self._configure_accessible_fonts()
        self._build_theme()
        self._build_ui()
        self._refresh_dashboard()
        self._restore_exam_session()

    def _record_exam_run(self, result):
        self.db.execute(
            """
            INSERT INTO exam_runs
                (completed_at, correct, total, score, forced, domains_json, scaled_score, passed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(timespec="seconds"),
                result["correct"],
                result["total"],
                result["score"],
                1 if result.get("forced") else 0,
                json.dumps(result["domains"], ensure_ascii=False),
                result.get("scaled_score", 100),
                1 if result.get("passed") else 0,
            ),
        )
        self.db.commit()
        self._refresh_weak_areas()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id TEXT PRIMARY KEY,
                exam TEXT,
                category TEXT,
                type TEXT,
                prompt TEXT,
                options_json TEXT,
                answer_json TEXT,
                pairs_json TEXT,
                case_text TEXT,
                case_group TEXT,
                case_order INTEGER,
                explanation TEXT,
                source TEXT,
                difficulty INTEGER
            )
            """
        )
        columns = [row[1] for row in conn.execute("PRAGMA table_info(questions)").fetchall()]
        if "pairs_json" not in columns:
            conn.execute("ALTER TABLE questions ADD COLUMN pairs_json TEXT")
        if "case_text" not in columns:
            conn.execute("ALTER TABLE questions ADD COLUMN case_text TEXT")
        if "case_group" not in columns:
            conn.execute("ALTER TABLE questions ADD COLUMN case_group TEXT")
        if "case_order" not in columns:
            conn.execute("ALTER TABLE questions ADD COLUMN case_order INTEGER")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT,
                correct INTEGER,
                mode TEXT,
                answered_at TEXT,
                score INTEGER
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS study_dates (
                study_day TEXT PRIMARY KEY
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exam_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                completed_at TEXT NOT NULL,
                correct INTEGER NOT NULL,
                total INTEGER NOT NULL,
                score REAL NOT NULL,
                forced INTEGER NOT NULL DEFAULT 0,
                domains_json TEXT NOT NULL
            )
            """
        )
        exam_run_columns = [row[1] for row in conn.execute("PRAGMA table_info(exam_runs)").fetchall()]
        if "scaled_score" not in exam_run_columns:
            conn.execute("ALTER TABLE exam_runs ADD COLUMN scaled_score INTEGER")
        if "passed" not in exam_run_columns:
            conn.execute("ALTER TABLE exam_runs ADD COLUMN passed INTEGER")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exam_sessions (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                question_ids_json TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                marked_json TEXT NOT NULL,
                exam_index INTEGER NOT NULL,
                deadline REAL NOT NULL,
                saved_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_schedule (
                question_id TEXT PRIMARY KEY,
                box INTEGER NOT NULL DEFAULT 1,
                interval_days INTEGER NOT NULL DEFAULT 1,
                next_review TEXT NOT NULL,
                last_result INTEGER,
                reviewed_count INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT
            )
            """
        )
        conn.commit()

        expected_ids = {question["id"] for question in QUESTION_BANK}
        existing_rows = conn.execute("SELECT * FROM questions").fetchall()
        existing_ids = {row["id"] for row in existing_rows}
        expected_by_id = {question["id"]: question for question in QUESTION_BANK}
        content_changed = False
        for row in existing_rows:
            expected = expected_by_id.get(row["id"])
            if expected is None:
                content_changed = True
                break
            stored = {
                "exam": row["exam"],
                "category": row["category"],
                "type": row["type"],
                "prompt": row["prompt"],
                "options": json.loads(row["options_json"] or "[]"),
                "answer": json.loads(row["answer_json"] or "[]"),
                "pairs": json.loads(row["pairs_json"] or "[]"),
                "case_text": row["case_text"],
                "case_group": row["case_group"],
                "case_order": row["case_order"],
                "explanation": row["explanation"],
                "source": row["source"],
                "difficulty": row["difficulty"],
            }
            expected_values = {
                "exam": expected["exam"],
                "category": expected["category"],
                "type": expected["type"],
                "prompt": expected["prompt"],
                "options": expected.get("options", []),
                "answer": expected.get(
                    "answer",
                    [] if expected["type"] in ("multi", "ordering", "drag_drop", "build_list", "case", "matching") else "",
                ),
                "pairs": expected.get("pairs", []),
                "case_text": expected.get("case_text"),
                "case_group": expected.get("case_group"),
                "case_order": expected.get("case_order"),
                "explanation": expected["explanation"],
                "source": expected["source"],
                "difficulty": expected.get("difficulty", 1),
            }
            if stored != expected_values:
                content_changed = True
                break
        needs_seed = (
            len(existing_ids) != len(expected_ids)
            or existing_ids != expected_ids
            or conn.execute("SELECT COUNT(*) FROM questions WHERE pairs_json IS NULL").fetchone()[0] > 0
            or content_changed
        )
        if needs_seed:
            conn.execute("DELETE FROM questions")
            for question in QUESTION_BANK:
                conn.execute(
                    "INSERT INTO questions (id, exam, category, type, prompt, options_json, answer_json, pairs_json, case_text, case_group, case_order, explanation, source, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        question["id"],
                        question["exam"],
                        question["category"],
                        question["type"],
                        question["prompt"],
                        json.dumps(question.get("options", [])),
                        json.dumps(question.get("answer", [] if question["type"] in ("multi", "ordering", "drag_drop", "build_list", "case", "matching") else "")),
                        json.dumps(question.get("pairs", [])),
                        question.get("case_text"),
                        question.get("case_group"),
                        question.get("case_order"),
                        question["explanation"],
                        question["source"],
                        question.get("difficulty", 1),
                    ),
                )
            conn.commit()
        return conn

    def _load_questions(self):
        rows = self.db.execute("SELECT * FROM questions ORDER BY id").fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["options"] = json.loads(item["options_json"]) if item.get("options_json") else []
            item["answer"] = json.loads(item["answer_json"]) if item.get("answer_json") else []
            item["pairs"] = json.loads(item["pairs_json"]) if item.get("pairs_json") else []
            result.append(item)
        return result

    def _build_theme(self):
        style = ttk.Style(self.root)
        self.root.option_add("*TCombobox*Listbox*Background", WHITE)
        self.root.option_add("*TCombobox*Listbox*Foreground", INK)
        self.root.option_add("*TCombobox*Listbox*selectBackground", SURFACE_SELECTED)
        self.root.option_add("*TCombobox*Listbox*selectForeground", INK)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=AZURE_PALE)
        style.configure("TLabel", background=AZURE_PALE, foreground=INK)
        style.configure("TButton", font=("Segoe UI", 12, "bold"), foreground=INK, background=SURFACE_RAISED, padding=(12, 7))
        style.map("TButton", background=[("active", SURFACE_SELECTED), ("pressed", SURFACE_ACCENT)])
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground=INK)
        style.configure("Section.TLabel", font=("Segoe UI", 13, "bold"), foreground=AZURE_NAVY)
        style.configure("Body.TLabel", font=("Segoe UI", 11), foreground=MUTED)
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), foreground=TEXT_ON_ACCENT, background=AZURE_BLUE, padding=(16, 9))
        style.map("Primary.TButton", background=[("active", "#2494FF"), ("pressed", "#006BC7")])
        style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), foreground=INK, background=SURFACE_RAISED, padding=(14, 8))
        style.map("Accent.TButton", background=[("active", SURFACE_SELECTED), ("pressed", SURFACE_ACCENT)])
        style.configure("TNotebook", background=AZURE_PALE, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 12, "bold"), padding=(18, 10), foreground=MUTED, background=SURFACE)
        style.map("TNotebook.Tab", background=[("selected", WHITE), ("active", SURFACE_RAISED)], foreground=[("selected", AZURE_NAVY)])
        style.configure("TCombobox", font=("Segoe UI", 12), padding=6, foreground=INK, fieldbackground=SURFACE, background=SURFACE_RAISED)
        style.map(
            "TCombobox",
            foreground=[("readonly", INK), ("disabled", MUTED)],
            fieldbackground=[("readonly", SURFACE), ("disabled", SURFACE_ACCENT)],
            background=[("readonly", SURFACE_RAISED), ("disabled", SURFACE_ACCENT)],
        )
        style.configure("TScrollbar", background=SURFACE_RAISED, troughcolor=AZURE_PALE, arrowcolor=INK)
        style.configure("TRadiobutton", font=("Segoe UI", 12), padding=(2, 5), foreground=INK, background=WHITE)
        style.configure("TCheckbutton", font=("Segoe UI", 12), padding=(2, 5), foreground=INK, background=WHITE)
        style.configure("Card.TFrame", background=WHITE)

    def _configure_accessible_fonts(self):
        current_scaling = float(self.root.tk.call("tk", "scaling"))
        self.root.tk.call("tk", "scaling", current_scaling * 1.12)
        for name, size in {
            "TkDefaultFont": 12,
            "TkTextFont": 12,
            "TkMenuFont": 12,
            "TkHeadingFont": 12,
            "TkCaptionFont": 11,
            "TkSmallCaptionFont": 11,
        }.items():
            try:
                tkfont.nametofont(name).configure(family="Segoe UI", size=size)
            except tk.TclError:
                continue

    def _build_ui(self):
        self.main = tk.Frame(self.root, bg=AZURE_PALE, padx=14, pady=14)
        self.main.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.main)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_tab = tk.Frame(self.notebook, bg=AZURE_PALE)
        self.learn_tab = tk.Frame(self.notebook, bg=AZURE_PALE)
        self.types_tab = tk.Frame(self.notebook, bg=AZURE_PALE)
        self.exam_tab = tk.Frame(self.notebook, bg=AZURE_PALE)
        self.review_tab = tk.Frame(self.notebook, bg=AZURE_PALE)
        self.stats_tab = tk.Frame(self.notebook, bg=AZURE_PALE)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.learn_tab, text="Lernen")
        self.notebook.add(self.types_tab, text="Fragentypen")
        self.notebook.add(self.exam_tab, text="AZ-900 Prüfungssimulation")
        self.notebook.add(self.review_tab, text="Wiederholung")
        self.notebook.add(self.stats_tab, text="Statistik")

        self._build_dashboard_tab()
        self._build_learn_tab()
        self._build_types_tab()
        self._build_exam_tab()
        self._build_review_tab()
        self._build_stats_tab()
        self._install_global_scroll_bindings()

    def _install_global_scroll_bindings(self):
        self.root.bind_all("<MouseWheel>", self._scroll_active_page, add="+")
        self.root.bind_all("<Button-4>", self._scroll_active_page, add="+")
        self.root.bind_all("<Button-5>", self._scroll_active_page, add="+")

    def _build_scrollable_page(self, parent, bg=AZURE_PALE):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=bg)
        content.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        window = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return canvas, content

    def _scroll_active_page(self, event):
        active_page = self.notebook.select()
        canvas = {
            str(self.dashboard_tab): self.dashboard_canvas,
            str(self.learn_tab): self.learn_canvas,
            str(self.types_tab): self.types_canvas,
            str(self.exam_tab): self.exam_canvas,
            str(self.review_tab): self.review_canvas,
            str(self.stats_tab): self.stats_canvas,
        }.get(active_page)
        if canvas is None:
            return None
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            units = -1
        elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
            units = 1
        else:
            return None
        canvas.yview_scroll(units, "units")
        return "break"

    def _build_dashboard_tab(self):
        self.dashboard_tab.configure(bg=AZURE_PALE)
        self.dashboard_canvas, dashboard_page = self._build_scrollable_page(self.dashboard_tab)
        hero = tk.Canvas(dashboard_page, height=150, bg=AZURE_BLUE, highlightthickness=0)
        hero.pack(fill="x", padx=0, pady=0)
        hero.create_rectangle(0, 0, 1600, 150, fill=AZURE_BLUE, outline="")
        for x, y, r in [(1040, 45, 52), (1115, 90, 42), (1195, 38, 34), (1265, 92, 56)]:
            hero.create_oval(x-r, y-r, x+r, y+r, fill="#2B8DD8", outline="")
        hero.create_text(28, 42, text="Azure Learning", anchor="w", font=("Segoe UI", 27, "bold"), fill=TEXT_ON_ACCENT)
        hero.create_text(30, 86, text="AZ-900 Fundamentals · Lerne mit der Terminologie von Microsoft", anchor="w", font=("Segoe UI", 12), fill="#D7F0FF")
        hero.create_text(30, 120, text="Üben  •  Verstehen  •  Wiederholen  •  Sicher antreten", anchor="w", font=("Segoe UI", 11, "bold"), fill=TEXT_ON_ACCENT)

        top = tk.Frame(dashboard_page, bg=AZURE_PALE)
        top.pack(fill="x", padx=18, pady=(18, 14))

        self.dashboard_cards = []
        self.dashboard_card_frames = []
        card_accents = {
            "attempts": AZURE_BLUE,
            "accuracy": "#1E8E5A",
            "streak": "#D97706",
            "due": "#8E44AD",
            "weak": "#C0392B",
        }
        for title, key in [("Übungsversuche", "attempts"), ("Genauigkeit", "accuracy"), ("Aktuelle Serie", "streak"), ("Fällig heute", "due"), ("Schwache Themen", "weak")]:
            frame = tk.Frame(top, width=205, height=122, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            frame.pack_propagate(False)
            tk.Frame(frame, bg=card_accents[key], height=4).pack(fill="x", side="top")
            tk.Label(frame, text=title, font=("Segoe UI", 11, "bold"), fg=MUTED, bg=WHITE).pack(anchor="w", padx=14, pady=(16, 6))
            var = tk.StringVar(value="0")
            label = tk.Label(frame, textvariable=var, font=("Segoe UI", 20, "bold"), fg=AZURE_NAVY, bg=WHITE)
            label.pack(anchor="w", padx=14)
            self.dashboard_cards.append((key, var))
            self.dashboard_card_frames.append(frame)
        top.bind("<Configure>", self._layout_dashboard_cards)

        self.status_box = tk.Frame(dashboard_page, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.status_box.pack(fill="x", padx=18, pady=(4, 8))
        tk.Label(self.status_box, text="Aktueller Fokus", font=("Segoe UI", 11, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 4))
        self.focus_var = tk.StringVar(value="AZ-900-Grundlagen")
        self.focus_label = tk.Label(self.status_box, textvariable=self.focus_var, font=("Segoe UI", 11), bg=WHITE, fg=MUTED, wraplength=1080, justify="left")
        self.focus_label.pack(anchor="w", padx=16, pady=(0, 12))
        self.status_box.bind(
            "<Configure>",
            lambda event: self.focus_label.configure(wraplength=max(400, event.width - 48)),
            add="+",
        )

        actions = tk.Frame(dashboard_page, bg=AZURE_PALE)
        actions.pack(fill="x", padx=18, pady=(8, 18))
        self.dashboard_action_buttons = [
            ttk.Button(actions, text="Lernmodus öffnen", command=self.open_learn_tab, style="Primary.TButton"),
            ttk.Button(actions, text="Heutigen Lernplan starten", command=self.start_today_plan, style="Primary.TButton"),
            ttk.Button(actions, text="Prüfungssimulation starten", command=self.start_exam, style="Accent.TButton"),
            ttk.Button(actions, text="Schwachstellen wiederholen", command=self.open_review_tab, style="Accent.TButton"),
            ttk.Button(actions, text="Fortschritt exportieren", command=self.export_progress, style="Accent.TButton"),
        ]
        actions.bind("<Configure>", self._layout_dashboard_actions)

        self.dashboard_summary = tk.Frame(dashboard_page, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.dashboard_summary.pack(fill="both", expand=True, padx=18, pady=(2, 12))
        summary_header = tk.Frame(self.dashboard_summary, bg=WHITE)
        summary_header.pack(fill="x", padx=16, pady=(14, 8))
        tk.Label(summary_header, text="Dein Lernfortschritt", font=("Segoe UI", 13, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(side="left")
        tk.Label(
            summary_header,
            text="Lerne gezielt, wiederhole regelmäßig und verfolge deine Entwicklung.",
            font=("Segoe UI", 11),
            bg=WHITE,
            fg=MUTED,
        ).pack(side="right")
        self.dashboard_summary_content = tk.Frame(self.dashboard_summary, bg=WHITE)
        self.dashboard_summary_content.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        self.autosave_var = tk.StringVar(value="")
        tk.Label(
            dashboard_page,
            textvariable=self.autosave_var,
            bg=AZURE_PALE,
            fg=MUTED,
            anchor="w",
            font=("Segoe UI", 10),
        ).pack(fill="x", padx=18, pady=(0, 10))

    def _layout_dashboard_cards(self, event):
        columns = 5 if event.width >= 1120 else 3
        for column in range(columns):
            event.widget.grid_columnconfigure(column, weight=1)
        for index, frame in enumerate(self.dashboard_card_frames):
            frame.grid(row=index // columns, column=index % columns, sticky="ew", padx=6, pady=6)

    def _layout_dashboard_actions(self, event):
        columns = 5 if event.width >= 1120 else 3
        for column in range(columns):
            event.widget.grid_columnconfigure(column, weight=1)
        for index, button in enumerate(self.dashboard_action_buttons):
            button.grid(row=index // columns, column=index % columns, sticky="ew", padx=4, pady=4)

    def _build_learn_tab(self):
        self.learn_tab.configure(bg=AZURE_PALE)
        self.learn_canvas, learn_page = self._build_scrollable_page(self.learn_tab)
        self.learn_toolbar = tk.Frame(learn_page, bg=AZURE_PALE)
        self.learn_toolbar.pack(fill="x", padx=12, pady=(12, 8))
        self.learn_topic_var = tk.StringVar(value="all")
        self.learn_type_var = tk.StringVar(value="all")
        topic_group = ttk.Frame(self.learn_toolbar)
        ttk.Label(topic_group, text="Prüfungsbereich:").pack(side="left", padx=(0, 8))
        self.learn_topic_menu = ttk.Combobox(topic_group, values=list(DOMAIN_LABELS.values()), state="readonly", width=30)
        self.learn_topic_menu.set(DOMAIN_LABELS["all"])
        self.learn_topic_menu.bind("<<ComboboxSelected>>", self._apply_learn_filter)
        self.learn_topic_menu.pack(side="left", fill="x", expand=True)
        type_group = ttk.Frame(self.learn_toolbar)
        ttk.Label(type_group, text="Fragentyp:").pack(side="left", padx=(0, 8))
        self.learn_type_menu = ttk.Combobox(type_group, values=list(QUESTION_TYPE_LABELS.values()), state="readonly", width=24)
        self.learn_type_menu.set(QUESTION_TYPE_LABELS["all"])
        self.learn_type_menu.bind("<<ComboboxSelected>>", self._apply_learn_filter)
        self.learn_type_menu.pack(side="left", fill="x", expand=True)
        difficulty_group = ttk.Frame(self.learn_toolbar)
        ttk.Label(difficulty_group, text="Schwierigkeit:").pack(side="left", padx=(0, 8))
        self.learn_difficulty_menu = ttk.Combobox(
            difficulty_group,
            values=list(DIFFICULTY_LABELS.values()),
            state="readonly",
            width=20,
        )
        self.learn_difficulty_menu.set(DIFFICULTY_LABELS["all"])
        self.learn_difficulty_menu.bind("<<ComboboxSelected>>", self._apply_learn_filter)
        self.learn_difficulty_menu.pack(side="left", fill="x", expand=True)
        next_button = ttk.Button(self.learn_toolbar, text="Nächste Frage", command=self.load_next_learn_question, style="Accent.TButton")
        self.learn_filter_groups = [topic_group, type_group, difficulty_group]
        self.learn_next_button = next_button
        self.learn_toolbar.bind("<Configure>", self._layout_learn_toolbar)

        self.learn_content = tk.Frame(learn_page, bg=AZURE_PALE)
        self.learn_content.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        self.load_next_learn_question()

    def _layout_learn_toolbar(self, event):
        compact = event.width < 1120
        columns = 2 if compact else 4
        for column in range(columns):
            self.learn_toolbar.grid_columnconfigure(column, weight=1 if column < 3 else 0)
        for index, group in enumerate(self.learn_filter_groups):
            row, column = (index // 2, index % 2) if compact else (0, index)
            group.grid(row=row, column=column, sticky="ew", padx=(0, 12), pady=3)
        button_row, button_column = (1, 1) if compact else (0, 3)
        self.learn_next_button.grid(row=button_row, column=button_column, sticky="ew", pady=3)

    def _build_exam_tab(self):
        self.exam_tab.configure(bg=AZURE_PALE)
        self.exam_header = tk.Frame(self.exam_tab, bg=AZURE_PALE)
        self.exam_header.pack(fill="x", padx=14, pady=(16, 10))
        self.exam_timer_var = tk.StringVar(value="45:00")
        tk.Label(self.exam_header, text="AZ-900 Prüfungssimulation", font=("Segoe UI", 18, "bold"), fg=AZURE_NAVY, bg=AZURE_PALE).pack(side="left")
        tk.Label(self.exam_header, textvariable=self.exam_timer_var, font=("Segoe UI", 16, "bold"), fg=AZURE_BLUE, bg=AZURE_PALE).pack(side="right")

        self.exam_canvas, self.exam_content = self._build_scrollable_page(self.exam_tab)

        self.exam_intro = tk.Frame(self.exam_content, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.exam_intro.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(self.exam_intro, text="AZ-900 Prüfungssimulation", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(14, 8))
        tk.Label(
            self.exam_intro,
            text=(
                "Original formulierte Assessment-Simulation — keine Microsoft-Livefragen und kein Exam-Dump. "
                "Die Fragen sind bewusst szenariobasiert und verwenden plausible Distraktoren statt reiner Learn-Wiederholung.\n\n"
                "45 Minuten · 40 Fragen · alle unterstützten Interaktionstypen · Zurück/Überspringen/Markieren · "
                "Review vor Abgabe · keine Sofortlösungen."
            ),
            bg=WHITE,
            fg=MUTED,
            justify="left",
            wraplength=900,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(0, 16))
        buttons = tk.Frame(self.exam_intro, bg=WHITE)
        buttons.pack(anchor="w", padx=16, pady=(0, 16))
        ttk.Button(buttons, text="Prüfung starten", command=self.start_exam, style="Primary.TButton").pack(side="left")
        self.resume_exam_button = ttk.Button(
            buttons,
            text="Gespeicherte Simulation fortsetzen",
            command=self._resume_exam_session,
            style="Accent.TButton",
        )
        self.resume_exam_button.pack(side="left", padx=(10, 0))
        self.resume_exam_button.state(["disabled"])

        catalog_row = tk.Frame(self.exam_intro, bg=WHITE)
        catalog_row.pack(fill="x", padx=16, pady=(4, 18))
        tk.Label(catalog_row, text="Prüfungssimulationen:", font=("Segoe UI", 10, "bold"), fg=MUTED, bg=WHITE).pack(anchor="w", pady=(0, 5))
        catalog_badges = tk.Frame(catalog_row, bg=WHITE)
        catalog_badges.pack(fill="x")
        for index, exam in enumerate(EXAM_CATALOG):
            is_active = exam["status"] == "active"
            badge = tk.Frame(
                catalog_badges,
                bg=AZURE_BLUE if is_active else AZURE_PALE,
                highlightthickness=1,
                highlightbackground=AZURE_BLUE if is_active else AZURE_BORDER,
            )
            badge.grid(row=0, column=index, sticky="ew", padx=(0, 8))
            catalog_badges.grid_columnconfigure(index, weight=1)
            label_text = exam["name"] if is_active else f"{exam['name']}\nBald verfügbar"
            tk.Label(
                badge,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg=TEXT_ON_ACCENT if is_active else MUTED,
                bg=AZURE_BLUE if is_active else AZURE_PALE,
                justify="center",
                wraplength=260,
            ).pack(fill="x", padx=8, pady=3)

    def _build_types_tab(self):
        self.types_tab.configure(bg=AZURE_PALE)
        types_canvas = tk.Canvas(self.types_tab, bg=AZURE_PALE, highlightthickness=0)
        types_scrollbar = ttk.Scrollbar(self.types_tab, orient="vertical", command=types_canvas.yview)
        self.types_scroll_frame = tk.Frame(types_canvas, bg=AZURE_PALE)
        self.types_scroll_frame.bind(
            "<Configure>", lambda e: types_canvas.configure(scrollregion=types_canvas.bbox("all"))
        )
        types_canvas_window = types_canvas.create_window((0, 0), window=self.types_scroll_frame, anchor="nw")
        types_canvas.bind("<Configure>", lambda e: types_canvas.itemconfigure(types_canvas_window, width=e.width))
        types_canvas.configure(yscrollcommand=types_scrollbar.set)
        types_canvas.pack(side="left", fill="both", expand=True)
        types_scrollbar.pack(side="right", fill="y")
        self.types_canvas = types_canvas

        tk.Label(self.types_scroll_frame, text="Nach Fragentyp üben", font=("Segoe UI", 20, "bold"), fg=AZURE_NAVY, bg=AZURE_PALE).pack(anchor="w", padx=24, pady=(24, 6))
        tk.Label(self.types_scroll_frame, text="Jeder Fragentyp trainiert eine andere Denkweise. Die Prüfungssimulation kombiniert alle Typen.", font=("Segoe UI", 11), fg=MUTED, bg=AZURE_PALE).pack(anchor="w", padx=24, pady=(0, 18))
        grid = tk.Frame(self.types_scroll_frame, bg=AZURE_PALE)
        grid.pack(fill="x", padx=24, pady=8)
        self.type_cards_grid = grid
        self.type_cards = []
        type_keys = [key for key in QUESTION_TYPE_LABELS if key != "all"]
        for index, type_key in enumerate(type_keys):
            card = tk.Frame(grid, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            tk.Frame(card, bg=AZURE_BLUE, height=4).pack(fill="x", side="top")
            tk.Label(card, text=QUESTION_TYPE_LABELS[type_key], font=("Segoe UI", 14, "bold"), fg=AZURE_NAVY, bg=WHITE).pack(anchor="w", padx=16, pady=(16, 5))
            count = sum(question["type"] == type_key for question in self.questions)
            tk.Label(card, text=f"{count} Fragen verfügbar", font=("Segoe UI", 10), fg=MUTED, bg=WHITE).pack(anchor="w", padx=16, pady=(0, 12))
            description = tk.Label(
                card,
                text=QUESTION_TYPE_DESCRIPTIONS.get(type_key, ""),
                font=("Segoe UI", 10),
                fg=MUTED,
                bg=WHITE,
                justify="left",
                wraplength=420,
            )
            description.pack(anchor="w", padx=16, pady=(0, 12))
            sample = next((question["prompt"] for question in self.questions if question["type"] == type_key), "")
            sample_label = tk.Label(
                card,
                text=f"Beispiel: {sample[:150]}{'…' if len(sample) > 150 else ''}",
                font=("Segoe UI", 10, "italic"),
                fg=MUTED,
                bg=WHITE,
                justify="left",
                wraplength=420,
            )
            sample_label.pack(anchor="w", padx=16, pady=(0, 12))

            def update_card_wrap(event, description=description, sample_label=sample_label):
                wraplength = max(220, event.width - 36)
                description.configure(wraplength=wraplength)
                sample_label.configure(wraplength=wraplength)

            card.bind("<Configure>", update_card_wrap)
            ttk.Button(
                card,
                text="Typ direkt üben",
                command=lambda key=type_key: self.open_type_practice(key),
                style="Accent.TButton",
            ).pack(anchor="w", padx=16, pady=(0, 16))
            self._bind_type_card(card, type_key)
            self.type_cards.append((card, description, sample_label))
        types_canvas.bind("<Configure>", lambda event: self._layout_type_cards(event.width), add="+")
        self.types_practice_frame = tk.Frame(self.types_scroll_frame, bg=AZURE_PALE, highlightthickness=1, highlightbackground=AZURE_BLUE)
        self.types_practice_frame.pack(fill="both", expand=True, padx=24, pady=(4, 24))
        tk.Label(
            self.types_practice_frame,
            text="Wähle oben einen Fragentyp, um hier direkt eine echte Aufgabe zu bearbeiten.",
            bg=AZURE_PALE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=8, pady=8)

    def _layout_type_cards(self, available_width):
        columns = 3 if available_width >= 1120 else 2
        wraplength = max(280, (available_width - 48) // columns - 32)
        for column in range(columns):
            self.type_cards_grid.grid_columnconfigure(column, weight=1)
        for index, (card, description, sample) in enumerate(self.type_cards):
            card.grid(row=index // columns, column=index % columns, sticky="nsew", padx=8, pady=8)
            description.configure(wraplength=wraplength)
            sample.configure(wraplength=wraplength)

    def _bind_type_card(self, card, type_key):
        def open_from_card(_event):
            self.open_type_practice(type_key)
            return "break"

        def on_enter(_event=None):
            card.configure(highlightbackground=AZURE_BLUE, highlightthickness=2)

        def on_leave(_event=None):
            card.configure(highlightbackground=AZURE_BORDER, highlightthickness=1)

        card.bind("<Button-1>", open_from_card)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.configure(cursor="hand2")

        def bind_text_children(widget):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    continue
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.bind("<Button-1>", open_from_card)
                    child.bind("<Enter>", on_enter)
                    child.bind("<Leave>", on_leave)
                    child.configure(cursor="hand2")
                bind_text_children(child)

        bind_text_children(card)

    def open_type_practice(self, type_key):
        pool = [question for question in self.questions if question["type"] == type_key]
        if not pool:
            return
        if len(pool) > 1 and self.type_practice_question:
            alternatives = [question for question in pool if question["id"] != self.type_practice_question["id"]]
            pool = alternatives or pool
        self.type_practice_question = random.choice(pool)
        self.notebook.select(self.types_tab)
        self._render_question_widget(self.types_practice_frame, self.type_practice_question, mode="type_practice")
        # Scroll the tab so the freshly rendered question is actually visible —
        # with 10 type cards the grid above can push this frame out of view.
        self.types_tab.update_idletasks()
        self.types_canvas.yview_moveto(1.0)

    def _build_review_tab(self):
        self.review_tab.configure(bg=AZURE_PALE)
        self.review_canvas, review_page = self._build_scrollable_page(self.review_tab)
        self.review_top = tk.Frame(review_page, bg=AZURE_PALE)
        self.review_top.pack(fill="x", padx=14, pady=(14, 10))
        tk.Label(self.review_top, text="Wiederholung / Intervalllernen", font=("Segoe UI", 18, "bold"), fg=AZURE_NAVY, bg=AZURE_PALE).pack(side="left")

        self.review_lists_row = tk.Frame(review_page, bg=AZURE_PALE, height=340)
        self.review_lists_row.grid_propagate(False)
        self.review_lists_row.pack(fill="x", padx=14, pady=(0, 10))
        self.review_lists_row.grid_columnconfigure(0, weight=1)
        self.review_lists_row.grid_columnconfigure(1, weight=1)
        self.review_lists_row.grid_rowconfigure(0, weight=1, minsize=340)

        due_panel = tk.Frame(self.review_lists_row, bg=WHITE, height=340, highlightthickness=1, highlightbackground=AZURE_BORDER)
        due_panel.pack_propagate(False)
        due_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        due_header = tk.Frame(due_panel, bg=WHITE)
        due_header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(due_header, text="Fällig zur Wiederholung", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(side="left")
        self.due_count_var = tk.StringVar(value="0 fällig")
        tk.Label(due_header, textvariable=self.due_count_var, font=("Segoe UI", 10, "bold"), bg=WHITE, fg=MUTED).pack(side="right")
        tk.Label(
            due_panel,
            text="Leitner-Intervalllernen: richtig beantwortete Fragen kommen seltener, "
                 "falsch beantwortete kommen morgen sofort wieder.",
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=MUTED,
            wraplength=440,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 6))
        self.due_review_queue = self._build_review_queue(due_panel)
        ttk.Button(due_panel, text="Fällige Wiederholung starten", command=self.load_due_review_question, style="Primary.TButton").pack(anchor="w", padx=12, pady=(0, 12))

        weak_panel = tk.Frame(self.review_lists_row, bg=WHITE, height=340, highlightthickness=1, highlightbackground=AZURE_BORDER)
        weak_panel.pack_propagate(False)
        weak_panel.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        weak_header = tk.Frame(weak_panel, bg=WHITE)
        weak_header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(weak_header, text="Häufig falsch beantwortet", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(side="left")
        tk.Label(
            weak_panel,
            text="Sortiert nach letztem Ergebnis (falsch zuerst) und Anzahl Fehlversuche.",
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=MUTED,
            wraplength=440,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 6))
        self.weak_review_queue = self._build_review_queue(weak_panel)
        ttk.Button(weak_panel, text="Schwachstellen üben", command=self.load_weak_question, style="Accent.TButton").pack(anchor="w", padx=12, pady=(0, 12))

        self.review_content = tk.Frame(review_page, bg=AZURE_PALE)
        self.review_content.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        self.review_question_frame = tk.Frame(self.review_content, bg=AZURE_PALE)
        self.review_question_frame.pack(fill="both", expand=True, pady=(0, 0))

        self._refresh_weak_areas()

    def _build_review_queue(self, parent):
        outer = tk.Frame(parent, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        outer.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        canvas = tk.Canvas(outer, bg=SURFACE, highlightthickness=0, height=210)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=SURFACE)
        content.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        window = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return content

    def _render_review_queue(self, queue, entries, empty_text):
        self._clear_frame(queue)
        if not entries:
            tk.Label(
                queue,
                text=empty_text,
                bg=SURFACE,
                fg=MUTED,
                justify="left",
                anchor="w",
                wraplength=390,
                font=("Segoe UI", 10),
            ).pack(fill="x", padx=12, pady=16)
            return
        for entry in entries:
            card = tk.Frame(queue, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER, cursor="hand2")
            card.pack(fill="x", padx=6, pady=4)
            tk.Frame(card, bg=entry["accent"], width=5).pack(side="left", fill="y")
            body = tk.Frame(card, bg=WHITE, cursor="hand2")
            body.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            tk.Label(
                body,
                text=entry["meta"],
                bg=WHITE,
                fg=entry["accent"],
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                cursor="hand2",
            ).pack(fill="x")
            tk.Label(
                body,
                text=entry["prompt"],
                bg=WHITE,
                fg=INK,
                font=("Segoe UI", 11),
                justify="left",
                anchor="w",
                wraplength=430,
                cursor="hand2",
            ).pack(fill="x", pady=(3, 0))

            def open_question(_event=None, question=entry["question"]):
                self.current_weak_question = question
                self._render_question_widget(self.review_question_frame, question, mode="weak")

            def highlight(_event=None, target=card):
                target.configure(highlightbackground=AZURE_BLUE, highlightthickness=2)

            def unhighlight(_event=None, target=card):
                target.configure(highlightbackground=AZURE_BORDER, highlightthickness=1)

            for widget in (card, body, *body.winfo_children()):
                widget.bind("<Button-1>", open_question)
                widget.bind("<Enter>", highlight)
                widget.bind("<Leave>", unhighlight)

    def _build_stats_tab(self):
        self.stats_tab.configure(bg=AZURE_PALE)
        canvas = tk.Canvas(self.stats_tab, bg=AZURE_PALE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.stats_tab, orient="vertical", command=canvas.yview)
        self.stats_scroll_frame = tk.Frame(canvas, bg=AZURE_PALE)
        self.stats_scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        stats_canvas_window = canvas.create_window((0, 0), window=self.stats_scroll_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(stats_canvas_window, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(14, 0), pady=14)
        scrollbar.pack(side="right", fill="y")
        self.stats_canvas = canvas

        header = tk.Frame(self.stats_scroll_frame, bg=AZURE_PALE)
        header.pack(fill="x", padx=4, pady=(0, 10))
        tk.Label(header, text="Statistik — echte Prüfungsleistung", font=("Segoe UI", 18, "bold"), fg=AZURE_NAVY, bg=AZURE_PALE).pack(side="left")
        ttk.Button(header, text="Aktualisieren", command=self._refresh_stats_tab).pack(side="right")

        self.stats_score_panel = tk.Frame(self.stats_scroll_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.stats_score_panel.pack(fill="x", padx=4, pady=(0, 12))

        self.stats_domain_panel = tk.Frame(self.stats_scroll_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.stats_domain_panel.pack(fill="x", padx=4, pady=(0, 12))

        self.stats_type_panel = tk.Frame(self.stats_scroll_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.stats_type_panel.pack(fill="x", padx=4, pady=(0, 12))

        self.stats_difficulty_panel = tk.Frame(self.stats_scroll_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.stats_difficulty_panel.pack(fill="x", padx=4, pady=(0, 12))

        self.stats_sr_panel = tk.Frame(self.stats_scroll_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.stats_sr_panel.pack(fill="x", padx=4, pady=(0, 20))

        self._refresh_stats_tab()

    def _stats_bar(self, parent, label, ratio, extra_text="", good_threshold=0.7):
        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", padx=16, pady=4)
        tk.Label(row, text=label, font=("Segoe UI", 10), bg=WHITE, fg=INK, width=34, anchor="w", justify="left").pack(side="left")
        bar_bg = tk.Canvas(row, width=260, height=14, bg=SURFACE_RAISED, highlightthickness=0)
        bar_bg.pack(side="left", padx=(4, 8))
        color = "#1E8E5A" if ratio >= good_threshold else "#D97706" if ratio >= 0.5 else "#C0392B"
        bar_bg.create_rectangle(0, 0, max(2, 260 * min(1.0, ratio)), 14, fill=color, outline="")
        tk.Label(row, text=f"{round(ratio * 100)}%{extra_text}", font=("Segoe UI", 10, "bold"), bg=WHITE, fg=AZURE_NAVY, width=18, anchor="w").pack(side="left")

    def _refresh_stats_tab(self):
        for panel in (self.stats_score_panel, self.stats_domain_panel, self.stats_type_panel, self.stats_difficulty_panel, self.stats_sr_panel):
            self._clear_frame(panel)

        # --- Scaled score history ---
        tk.Label(self.stats_score_panel, text="Geschätzter Prüfungsscore (100–1000, Bestehensgrenze 700)", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 4))
        runs = self.db.execute(
            """
            SELECT completed_at, scaled_score, passed, score, correct, total
            FROM exam_runs
            WHERE scaled_score IS NOT NULL
            ORDER BY id DESC
            LIMIT 10
            """
        ).fetchall()
        if not runs:
            tk.Label(self.stats_score_panel, text="Noch keine abgeschlossene Prüfungssimulation. Starte eine Prüfungssimulation, um echte Statistiken zu sehen.", font=("Segoe UI", 10), bg=WHITE, fg=MUTED, wraplength=900, justify="left").pack(anchor="w", padx=16, pady=(0, 12))
        else:
            scaled_values = [r["scaled_score"] for r in runs]
            best = max(scaled_values)
            latest = scaled_values[0]
            average = round(sum(scaled_values) / len(scaled_values))
            pass_count = sum(1 for r in runs if r["passed"])
            summary_row = tk.Frame(self.stats_score_panel, bg=WHITE)
            summary_row.pack(fill="x", padx=16, pady=(0, 8))
            for text in (
                f"Letzter Score: {latest}/1000",
                f"Bester Score: {best}/1000",
                f"Durchschnitt: {average}/1000",
                f"Bestanden: {pass_count}/{len(runs)}",
            ):
                tk.Label(summary_row, text=text, font=("Segoe UI", 10, "bold"), bg=SURFACE, fg=AZURE_NAVY, padx=10, pady=6).pack(side="left", padx=(0, 8))
            list_frame = tk.Frame(self.stats_score_panel, bg=WHITE)
            list_frame.pack(fill="x", padx=16, pady=(0, 14))
            for run in runs:
                timestamp = run["completed_at"].replace("T", " ")[:16]
                mark = "✅ Bestanden" if run["passed"] else "❌ Nicht bestanden"
                color = "#1E8E5A" if run["passed"] else "#C0392B"
                line = tk.Frame(list_frame, bg=WHITE)
                line.pack(fill="x", pady=1)
                tk.Label(line, text=timestamp, font=("Segoe UI", 10), bg=WHITE, fg=MUTED, width=18, anchor="w").pack(side="left")
                tk.Label(line, text=f"{run['scaled_score']}/1000", font=("Segoe UI", 10, "bold"), bg=WHITE, fg=AZURE_NAVY, width=10, anchor="w").pack(side="left")
                tk.Label(line, text=mark, font=("Segoe UI", 10, "bold"), bg=WHITE, fg=color, width=16, anchor="w").pack(side="left")
                tk.Label(line, text=f"(Rohwert: {round(run['score'], 1)}%, {run['correct']}/{run['total']})", font=("Segoe UI", 10), bg=WHITE, fg=MUTED).pack(side="left")

        # --- Domain accuracy vs blueprint target ---
        tk.Label(self.stats_domain_panel, text="Domänen-Genauigkeit vs. Blueprint-Zielgewichtung", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 6))
        domain_labels = {"cloud": "Describe cloud concepts", "architecture": "Describe Azure architecture and services", "governance": "Describe Azure management and governance"}
        any_domain_data = False
        for category, weight in EXAM_DOMAIN_WEIGHTS.items():
            row = self.db.execute(
                """
                SELECT COUNT(*) AS total, SUM(CASE WHEN a.correct = 1 THEN 1 ELSE 0 END) AS correct
                FROM attempts a JOIN questions q ON a.question_id = q.id
                WHERE q.category = ?
                """,
                (category,),
            ).fetchone()
            total = row["total"] or 0
            correct = row["correct"] or 0
            ratio = (correct / total) if total else 0.0
            extra = f"  ·  {correct}/{total} Fragen  ·  Blueprint-Ziel {round(weight * 100)}%"
            if total:
                any_domain_data = True
            self._stats_bar(self.stats_domain_panel, domain_labels[category], ratio, extra)
        if not any_domain_data:
            tk.Label(self.stats_domain_panel, text="Noch keine Übungsdaten pro Domäne vorhanden.", font=("Segoe UI", 10), bg=WHITE, fg=MUTED).pack(anchor="w", padx=16, pady=(0, 8))
        tk.Frame(self.stats_domain_panel, bg=WHITE, height=8).pack()

        # --- Question-type accuracy ---
        tk.Label(self.stats_type_panel, text="Genauigkeit nach Fragentyp", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 6))
        type_rows = self.db.execute(
            """
            SELECT q.type AS qtype, COUNT(*) AS total, SUM(CASE WHEN a.correct = 1 THEN 1 ELSE 0 END) AS correct
            FROM attempts a JOIN questions q ON a.question_id = q.id
            GROUP BY q.type
            ORDER BY total DESC
            """
        ).fetchall()
        if not type_rows:
            tk.Label(self.stats_type_panel, text="Noch keine Übungsdaten vorhanden.", font=("Segoe UI", 10), bg=WHITE, fg=MUTED).pack(anchor="w", padx=16, pady=(0, 8))
        else:
            for row in type_rows:
                ratio = (row["correct"] / row["total"]) if row["total"] else 0.0
                self._stats_bar(self.stats_type_panel, (row["qtype"] or "unknown").replace("_", " ").title(), ratio, f"  ·  {row['correct']}/{row['total']}")
        tk.Frame(self.stats_type_panel, bg=WHITE, height=8).pack()

        # --- Difficulty accuracy ---
        tk.Label(self.stats_difficulty_panel, text="Genauigkeit nach Schwierigkeitsgrad", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 6))
        difficulty_rows = self.db.execute(
            """
            SELECT q.difficulty AS diff, COUNT(*) AS total, SUM(CASE WHEN a.correct = 1 THEN 1 ELSE 0 END) AS correct
            FROM attempts a JOIN questions q ON a.question_id = q.id
            GROUP BY q.difficulty
            ORDER BY q.difficulty ASC
            """
        ).fetchall()
        difficulty_labels = {1: "Leicht", 2: "Mittel", 3: "Schwer"}
        if not difficulty_rows:
            tk.Label(self.stats_difficulty_panel, text="Noch keine Übungsdaten vorhanden.", font=("Segoe UI", 10), bg=WHITE, fg=MUTED).pack(anchor="w", padx=16, pady=(0, 8))
        else:
            for row in difficulty_rows:
                ratio = (row["correct"] / row["total"]) if row["total"] else 0.0
                label = difficulty_labels.get(row["diff"], f"Stufe {row['diff']}")
                self._stats_bar(self.stats_difficulty_panel, label, ratio, f"  ·  {row['correct']}/{row['total']}")
        tk.Frame(self.stats_difficulty_panel, bg=WHITE, height=8).pack()

        # --- Spaced repetition summary ---
        tk.Label(self.stats_sr_panel, text="Übersicht Intervalllernen", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=16, pady=(12, 6))
        sr = self._sr_summary()
        sr_row = tk.Frame(self.stats_sr_panel, bg=WHITE)
        sr_row.pack(fill="x", padx=16, pady=(0, 6))
        for text in (
            f"Fällig heute: {sr['due_now']}",
            f"Fällig diese Woche: {sr['due_week']}",
            f"Gemeistert (Box 6): {sr['mastered']}",
            f"Insgesamt geplant: {sr['scheduled']}",
        ):
            tk.Label(sr_row, text=text, font=("Segoe UI", 10, "bold"), bg=SURFACE, fg=AZURE_NAVY, padx=10, pady=6).pack(side="left", padx=(0, 8))
        link_row = tk.Frame(self.stats_sr_panel, bg=WHITE)
        link_row.pack(fill="x", padx=16, pady=(4, 14))
        ttk.Button(link_row, text="Zur Wiederholung wechseln", command=self.open_review_tab).pack(anchor="w")

    def _apply_learn_filter(self, event=None):
        self.load_next_learn_question()

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _get_selected_topic(self):
        label = self.learn_topic_menu.get()
        for key, value in DOMAIN_LABELS.items():
            if value == label:
                return key
        return "all"

    def _get_selected_type(self):
        label = self.learn_type_menu.get()
        for key, value in QUESTION_TYPE_LABELS.items():
            if value == label:
                return key
        return "all"

    def _get_selected_difficulty(self):
        label = self.learn_difficulty_menu.get()
        for key, value in DIFFICULTY_LABELS.items():
            if value == label:
                return key
        return "all"

    def _get_question_by_id(self, question_id):
        for question in self.questions:
            if question["id"] == question_id:
                return question
        return None

    def _fetch_weak_questions(self):
        rows = self.db.execute(
            """
            SELECT
                a.question_id,
                SUM(CASE WHEN a.correct = 0 THEN 1 ELSE 0 END) AS misses,
                MAX(a.answered_at) AS last_answered,
                (
                    SELECT latest.correct
                    FROM attempts AS latest
                    WHERE latest.question_id = a.question_id
                    ORDER BY latest.answered_at DESC, latest.id DESC
                    LIMIT 1
                ) AS latest_correct
            FROM attempts AS a
            GROUP BY a.question_id
            HAVING misses > 0
            ORDER BY latest_correct ASC, misses DESC, last_answered ASC, a.question_id ASC
            """
        ).fetchall()
        return [row["question_id"] for row in rows]

    def _refresh_dashboard(self):
        attempts = self.db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
        correct = self.db.execute("SELECT COUNT(*) FROM attempts WHERE correct = 1").fetchone()[0]
        accuracy = round((correct / attempts * 100), 1) if attempts else 0.0
        streak = self._calculate_streak()
        weak_items = len(self._fetch_weak_questions())
        sr_summary = self._sr_summary()

        stats = {
            "attempts": str(attempts),
            "accuracy": f"{accuracy}%",
            "streak": str(streak),
            "due": str(sr_summary["due_now"]),
            "weak": str(weak_items),
        }
        for key, var in self.dashboard_cards:
            var.set(stats[key])

        self.focus_var.set("AZ-900-Grundlagen — Cloud, Architektur und Governance nach dem Stand Juli 2026")
        self.autosave_var.set(
            f"Autosave aktiv · Fortschritt wird automatisch gespeichert in: {DB_PATH}"
        )

        run_summary = self.db.execute(
            """
            SELECT COUNT(*) AS total_runs, MAX(score) AS best_score
            FROM exam_runs
            """
        ).fetchone()
        if run_summary["total_runs"]:
            recent_run = self.db.execute(
                """
                SELECT score, correct, total, completed_at, scaled_score, passed
                FROM exam_runs
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()
            scaled_summary = self.db.execute(
                """
                SELECT AVG(scaled_score) AS avg_scaled, MAX(scaled_score) AS best_scaled,
                       SUM(CASE WHEN passed = 1 THEN 1 ELSE 0 END) AS pass_count
                FROM exam_runs
                WHERE scaled_score IS NOT NULL
                """
            ).fetchone()
            last_pass_label = ""
            if recent_run["passed"] is not None:
                last_pass_label = " — Bestanden" if recent_run["passed"] else " — Nicht bestanden"
        self._clear_frame(self.dashboard_summary_content)
        highlights = tk.Frame(self.dashboard_summary_content, bg=WHITE)
        highlights.pack(fill="x", pady=(0, 12))
        summary_cards = [
            ("Lernfortschritt", f"{correct}/{attempts} richtig" if attempts else "Noch keine Antworten", f"{accuracy}% Genauigkeit"),
            ("Wiederholung", f"{sr_summary['due_now']} heute fällig", f"{sr_summary['due_week']} diese Woche · {sr_summary['mastered']} gemeistert"),
            (
                "Prüfungssimulation",
                f"{recent_run['scaled_score']}/1000" if run_summary["total_runs"] and recent_run["scaled_score"] is not None else "Noch keine Simulation",
                last_pass_label.strip(" —") if run_summary["total_runs"] and last_pass_label else "Starte eine Simulation für deinen Score",
            ),
        ]
        for title, value, detail in summary_cards:
            card = tk.Frame(highlights, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(card, text=title, bg=SURFACE, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 3))
            tk.Label(card, text=value, bg=SURFACE, fg=AZURE_NAVY, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=12)
            tk.Label(card, text=detail, bg=SURFACE, fg=MUTED, font=("Segoe UI", 10), wraplength=280, justify="left").pack(anchor="w", padx=12, pady=(3, 10))

        today_plan = self._build_today_plan(limit=6)
        plan_card = tk.Frame(self.dashboard_summary_content, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        plan_card.pack(fill="x", pady=(0, 12))
        plan_header = tk.Frame(plan_card, bg=SURFACE)
        plan_header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(plan_header, text="Dein Plan für heute", bg=SURFACE, fg=AZURE_NAVY, font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Button(plan_header, text="Plan starten", command=self.start_today_plan, style="Accent.TButton").pack(side="right")
        plan_preview = "\n".join(
            f"• {entry['reason']}: {entry['question']['prompt'][:120]}{'…' if len(entry['question']['prompt']) > 120 else ''}"
            for entry in today_plan[:3]
        )
        plan_preview_label = tk.Label(
            plan_card,
            text=plan_preview or "Starte den Lernmodus, um deinen ersten persönlichen Plan zu erstellen.",
            bg=SURFACE,
            fg=INK,
            font=("Segoe UI", 10),
            justify="left",
            anchor="w",
            wraplength=1030,
        )
        plan_preview_label.pack(fill="x", padx=12, pady=(0, 10))
        plan_card.bind(
            "<Configure>",
            lambda event: plan_preview_label.configure(wraplength=max(400, event.width - 48)),
            add="+",
        )

        tk.Label(self.dashboard_summary_content, text="Fortschritt nach Prüfungsbereich", bg=WHITE, fg=AZURE_NAVY, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        domains = tk.Frame(self.dashboard_summary_content, bg=WHITE)
        domains.pack(fill="x")
        for category, label, target in (
            ("cloud", "Cloud concepts", "25–30%"),
            ("architecture", "Azure architecture and services", "35–40%"),
            ("governance", "Azure management and governance", "30–35%"),
        ):
            row = self.db.execute(
                """
                SELECT COUNT(*) AS total, COALESCE(SUM(correct), 0) AS correct
                FROM attempts AS a
                JOIN questions AS q ON q.id = a.question_id
                WHERE q.category = ?
                """,
                (category,),
            ).fetchone()
            total = row["total"] or 0
            domain_accuracy = round(row["correct"] / total * 100, 1) if total else 0.0
            domain = tk.Frame(domains, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            domain.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(domain, text=label, bg=WHITE, fg=MUTED, font=("Segoe UI", 10, "bold"), wraplength=280, justify="left").pack(anchor="w", padx=10, pady=(8, 3))
            tk.Label(domain, text=f"{domain_accuracy}%", bg=WHITE, fg=AZURE_NAVY, font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=10)
            tk.Label(domain, text=f"{row['correct']}/{total} Antworten · Blueprint {target}", bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(2, 8))

    def _calculate_streak(self):
        rows = self.db.execute("SELECT study_day FROM study_dates ORDER BY study_day DESC").fetchall()
        if not rows:
            return 0
        dates = [row["study_day"] for row in rows]
        today = date.today().isoformat()
        consecutive = 0
        cursor = today
        seen = set(dates)
        while cursor in seen:
            consecutive += 1
            day_obj = datetime.strptime(cursor, "%Y-%m-%d").date()
            day_obj = day_obj.fromordinal(day_obj.toordinal() - 1)
            cursor = day_obj.isoformat()
        return consecutive

    def _record_study_day(self):
        today_str = date.today().isoformat()
        self.db.execute("INSERT OR IGNORE INTO study_dates (study_day) VALUES (?)", (today_str,))
        self.db.commit()

    def _record_attempt(self, question_id, correct, mode="learn", score=0):
        self.db.execute(
            "INSERT INTO attempts (question_id, correct, mode, answered_at, score) VALUES (?, ?, ?, ?, ?)",
            (question_id, 1 if correct else 0, mode, datetime.utcnow().isoformat(timespec="seconds"), int(score)),
        )
        self.db.commit()
        self._record_study_day()
        self._update_review_schedule(question_id, correct)
        self._refresh_dashboard()
        self._refresh_weak_areas()

    def _update_review_schedule(self, question_id, correct):
        """Advance/reset the Leitner box for a question after an attempt.

        Correct answers promote the question to the next box (longer interval
        before it resurfaces); any wrong answer immediately resets it to box 1
        (interval 1 day) so mistakes come back for review the next day.
        """
        row = self.db.execute(
            "SELECT box, reviewed_count FROM review_schedule WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        current_box = row["box"] if row else 0
        reviewed_count = (row["reviewed_count"] if row else 0) + 1
        if correct:
            new_box = min(current_box + 1, len(SR_BOX_INTERVALS))
        else:
            new_box = 1
        new_box = max(1, new_box)
        interval_days = SR_BOX_INTERVALS[new_box - 1]
        next_review = (date.today() + timedelta(days=interval_days)).isoformat()
        self.db.execute(
            """
            INSERT INTO review_schedule (question_id, box, interval_days, next_review, last_result, reviewed_count, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(question_id) DO UPDATE SET
                box = excluded.box,
                interval_days = excluded.interval_days,
                next_review = excluded.next_review,
                last_result = excluded.last_result,
                reviewed_count = excluded.reviewed_count,
                updated_at = excluded.updated_at
            """,
            (
                question_id,
                new_box,
                interval_days,
                next_review,
                1 if correct else 0,
                reviewed_count,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        self.db.commit()

    def _fetch_due_review_questions(self):
        """Question ids whose spaced-repetition schedule is due today or overdue,
        most-overdue first, then longest-unreviewed. Only questions that have been
        attempted at least once are scheduled, so brand-new questions are excluded
        until the learner first sees them."""
        today = date.today().isoformat()
        rows = self.db.execute(
            """
            SELECT question_id, next_review, box
            FROM review_schedule
            WHERE next_review <= ?
            ORDER BY next_review ASC, box ASC
            """,
            (today,),
        ).fetchall()
        return [row["question_id"] for row in rows if self._get_question_by_id(row["question_id"])]

    def _sr_summary(self):
        """Counts for dashboard/stats: due now, due within 7 days, mastered (box 5+)."""
        today = date.today()
        rows = self.db.execute("SELECT next_review, box FROM review_schedule").fetchall()
        due_now = 0
        due_week = 0
        mastered = 0
        for row in rows:
            next_review = datetime.strptime(row["next_review"], "%Y-%m-%d").date()
            if next_review <= today:
                due_now += 1
            elif next_review <= today + timedelta(days=7):
                due_week += 1
            if row["box"] >= len(SR_BOX_INTERVALS):
                mastered += 1
        return {"due_now": due_now, "due_week": due_week, "mastered": mastered, "scheduled": len(rows)}

    def _build_today_plan(self, limit=10):
        """Build a concise, deduplicated practice queue from the learner's data."""
        entries = []
        seen = set()

        def add(question_id, reason):
            if len(entries) >= limit or question_id in seen:
                return
            question = self._get_question_by_id(question_id)
            if question:
                entries.append({"question": question, "reason": reason})
                seen.add(question_id)

        for question_id in self._fetch_due_review_questions():
            add(question_id, "Heute fällige Wiederholung")

        weak_ids = self._fetch_weak_questions()
        domain_rows = self.db.execute(
            """
            SELECT q.category, COUNT(*) AS total, SUM(a.correct) AS correct
            FROM attempts AS a
            JOIN questions AS q ON q.id = a.question_id
            GROUP BY q.category
            HAVING total > 0
            ORDER BY CAST(SUM(a.correct) AS REAL) / COUNT(*) ASC, total DESC
            """
        ).fetchall()
        for row in domain_rows:
            for question_id in weak_ids:
                question = self._get_question_by_id(question_id)
                if question and question["category"] == row["category"]:
                    add(question_id, f"Schwacher Bereich: {DOMAIN_LABELS.get(row['category'], row['category'])}")

        missed_type_rows = self.db.execute(
            """
            SELECT q.type, MAX(a.answered_at) AS last_miss
            FROM attempts AS a
            JOIN questions AS q ON q.id = a.question_id
            WHERE a.correct = 0
            GROUP BY q.type
            ORDER BY last_miss DESC
            """
        ).fetchall()
        for row in missed_type_rows:
            for question_id in weak_ids:
                question = self._get_question_by_id(question_id)
                if question and question["type"] == row["type"]:
                    add(question_id, f"Zuletzt verfehlter Typ: {QUESTION_TYPE_LABELS.get(row['type'], row['type'])}")
            if not any(
                entry["reason"].startswith("Zuletzt verfehlter Typ:")
                and entry["question"]["type"] == row["type"]
                for entry in entries
            ):
                for question in self.questions:
                    if question["type"] == row["type"] and question["id"] not in seen:
                        add(question["id"], f"Zuletzt verfehlter Typ: {QUESTION_TYPE_LABELS.get(row['type'], row['type'])}")
                        break

        for question in self.questions:
            if len(entries) >= limit:
                break
            add(question["id"], "AZ-900-Grundlagen festigen")
        return entries

    def start_today_plan(self):
        self.today_plan_entries = self._build_today_plan()
        self.today_plan_index = 0
        if not self.today_plan_entries:
            messagebox.showinfo("Lernplan", "Für den heutigen Lernplan sind keine Fragen verfügbar.")
            return
        self.notebook.select(self.learn_tab)
        self._render_today_plan_question()

    def _render_today_plan_question(self):
        if self.today_plan_index >= len(self.today_plan_entries):
            self.notebook.select(self.dashboard_tab)
            self._refresh_dashboard()
            messagebox.showinfo("Lernplan abgeschlossen", "Du hast alle Fragen deines heutigen Lernplans bearbeitet.")
            return
        entry = self.today_plan_entries[self.today_plan_index]
        self.current_learn_question = entry["question"]
        self.last_learn_question_id = entry["question"]["id"]
        self._render_question_widget(self.learn_content, entry["question"], mode="today")

    def _next_today_plan_question(self):
        self.today_plan_index += 1
        self._render_today_plan_question()

    def _render_question_widget(self, parent, question, mode="learn"):
        self._clear_frame(parent)
        self.current_question_mode = mode
        self.current_answer_locked = False
        frame = tk.Frame(parent, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.current_question_frame = frame
        self.current_feedback_frame = None

        header = tk.Frame(frame, bg=WHITE)
        header.pack(fill="x", padx=16, pady=(16, 10))
        type_label = tk.Label(header, text=QUESTION_TYPE_LABELS.get(question["type"], question["type"]), font=("Segoe UI", 10, "bold"), fg=AZURE_BLUE, bg=WHITE)
        type_label.pack(anchor="w")
        if mode == "exam":
            mode_label = "PRÜFUNGSSIMULATION · keine Sofortlösung"
        elif mode == "type_practice":
            mode_label = "TYP-TRAINING · direkte Auswertung"
        elif mode == "today":
            entry = self.today_plan_entries[self.today_plan_index]
            mode_label = (
                f"HEUTIGER LERNPLAN · Planpunkt {self.today_plan_index + 1} von "
                f"{len(self.today_plan_entries)} · {entry['reason']}"
            )
        elif mode == "exam_review":
            mode_label = (
                f"PRÜFUNGSNACHBEREITUNG · Frage {self.exam_review_index + 1} von "
                f"{len(self.exam_review_questions)}"
            )
        else:
            mode_label = "LERNEN · Erklärung nach Abgabe"
        difficulty = question.get("difficulty", 1)
        difficulty_text = DIFFICULTY_LABELS.get(str(difficulty), "Szenario")
        tk.Label(
            header,
            text=f"{DOMAIN_LABELS.get(question['category'], question['category'])}  ·  {mode_label}  ·  {difficulty_text}",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=WHITE,
        ).pack(anchor="w", pady=(4, 0))

        prompt_label = tk.Label(
            frame,
            text=question["prompt"],
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=INK,
            wraplength=1060,
            justify="left",
        )
        prompt_label.pack(anchor="w", padx=16, pady=(0, 14))
        def resize_prompt(event):
            wraplength = max(320, event.width - 16)
            if int(prompt_label.cget("wraplength")) != wraplength:
                prompt_label.configure(wraplength=wraplength)

        prompt_label.bind("<Configure>", resize_prompt, add="+")

        qtype = question["type"]
        answer_area = tk.Frame(frame, bg=WHITE)
        answer_area.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        self.current_answer_area = answer_area

        answer_vars = {}

        if qtype in ("single", "true_false"):
            choices = question.get("options", [])
            existing = self.exam_answers.get(question["id"], "") if mode == "exam" else ""
            selected = tk.StringVar(value=existing if isinstance(existing, str) else "")
            for option in choices:
                radio = ttk.Radiobutton(answer_area, text=option, variable=selected, value=option)
                radio.pack(anchor="w", pady=4)
            answer_vars["selection"] = selected
        elif qtype in ("hot_area", "active_screen"):
            choices = question.get("options", [])
            existing = self.exam_answers.get(question["id"], "") if mode == "exam" else ""
            selected = tk.StringVar(value=existing if isinstance(existing, str) else "")
            canvas = tk.Canvas(answer_area, width=900, height=210, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            canvas.pack(fill="x", expand=True, pady=(4, 8))
            hitboxes = {}

            def redraw_targets(*_args):
                canvas.delete("all")
                canvas.create_rectangle(0, 0, 900, 210, fill=SURFACE, outline="")
                if qtype == "active_screen":
                    canvas.create_rectangle(0, 0, 900, 38, fill=AZURE_NAVY, outline="")
                    canvas.create_text(18, 19, text="Azure portal · Ansicht", anchor="w", fill=TEXT_ON_ACCENT, font=("Segoe UI", 10, "bold"))
                columns = 2
                width = 420
                height = 62
                for index, option in enumerate(choices):
                    row, column = divmod(index, columns)
                    x1 = 24 + column * 440
                    y1 = 54 + row * 72
                    x2 = x1 + width
                    y2 = y1 + height
                    selected_fill = SURFACE_SELECTED if selected.get() == option else WHITE
                    canvas.create_rectangle(x1, y1, x2, y2, fill=selected_fill, outline=AZURE_BLUE, width=2 if selected.get() == option else 1)
                    canvas.create_text(x1 + 14, y1 + 15, text=f"{index + 1}", anchor="w", fill=AZURE_BLUE, font=("Segoe UI", 10, "bold"))
                    canvas.create_text(x1 + 46, y1 + 31, text=option, anchor="w", fill=INK, font=("Segoe UI", 10), width=350)
                    hitboxes[option] = (x1, y1, x2, y2)

            def choose_target(event):
                for option, (x1, y1, x2, y2) in hitboxes.items():
                    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                        selected.set(option)
                        redraw_targets()
                        break

            selected.trace_add("write", redraw_targets)
            canvas.bind("<Button-1>", choose_target)
            redraw_targets()
            tk.Label(
                answer_area,
                text="Klicke im simulierten Azure-Bereich auf die beste Auswahl.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack(anchor="w")
            answer_vars["selection"] = selected
        elif qtype == "multi":
            existing = self.exam_answers.get(question["id"], []) if mode == "exam" else []
            for option in question.get("options", []):
                var = tk.BooleanVar(value=option in existing)
                ttk.Checkbutton(answer_area, text=option, variable=var).pack(anchor="w", pady=4)
                answer_vars[option] = var
        elif qtype in ("ordering", "drag_drop"):
            existing = self.exam_answers.get(question["id"]) if mode == "exam" else None
            order = list(existing) if isinstance(existing, list) and set(existing) == set(question["options"]) else list(question["options"])
            if existing is None:
                random.shuffle(order)
            tk.Label(
                answer_area,
                text="⠿⠿ anfassen und mit gedrückter Maustaste an die gewünschte Position ziehen.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack(anchor="w", pady=(0, 6))
            drag_widget = DragOrderList(answer_area, order)
            drag_widget.pack(anchor="w", fill="x", expand=False)
            answer_vars["drag_widget"] = drag_widget
        elif qtype == "build_list":
            all_options = list(question["options"])
            existing = self.exam_answers.get(question["id"]) if mode == "exam" else None
            if isinstance(existing, list) and existing and set(existing).issubset(set(all_options)):
                target_initial = list(existing)
                pool_initial = [option for option in all_options if option not in existing]
            else:
                pool_initial = list(all_options)
                random.shuffle(pool_initial)
                target_initial = []
            tk.Label(
                answer_area,
                text="Ziehen Sie die passenden Schritte in die richtige Reihenfolge nach rechts. Nicht jeder Eintrag im Pool wird benötigt.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack(anchor="w", pady=(0, 6))
            build_widget = DragBuildList(answer_area, pool_initial, target_initial)
            build_widget.pack(fill="both", expand=True)
            answer_vars["build_widget"] = build_widget
        elif qtype == "matching":
            left_items = [item[0] for item in question["pairs"]]
            right_items = [item[1] for item in question["pairs"]]
            shuffled_right = list(right_items)
            random.shuffle(shuffled_right)
            answer_vars["pairs"] = {}
            existing = self.exam_answers.get(question["id"], {}) if mode == "exam" else {}
            for left in left_items:
                row = tk.Frame(answer_area, bg=WHITE)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=left, bg=WHITE, fg=AZURE_NAVY, font=("Segoe UI", 10, "bold"), width=34, anchor="w").pack(side="left")
                var = tk.StringVar(value=existing.get(left, "") if isinstance(existing, dict) else "")
                menu = ttk.Combobox(row, values=shuffled_right, textvariable=var, state="readonly", width=34)
                menu.pack(side="left", padx=(10, 0))
                answer_vars["pairs"][left] = var
        elif qtype == "case":
            case_text = question.get("case_text", "")
            if case_text:
                case_card = tk.Frame(frame, bg=SURFACE_ACCENT, highlightthickness=1, highlightbackground=AZURE_BORDER)
                case_card.pack(fill="x", padx=16, pady=(0, 12))
                part = question.get("case_order")
                group_label = " · ".join(
                    value for value in (
                        "FALLSTUDIE · SZENARIO",
                        f"Teil {part}" if part else "",
                    )
                    if value
                )
                tk.Label(case_card, text=group_label, bg=SURFACE_ACCENT, fg=AZURE_LIGHT, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
                tk.Label(case_card, text=case_text, bg=SURFACE_ACCENT, fg=INK, justify="left", anchor="w", wraplength=940, font=("Segoe UI", 10)).pack(anchor="w", padx=12, pady=(0, 10))
            for option in question.get("options", []):
                existing = self.exam_answers.get(question["id"], []) if mode == "exam" else []
                var = tk.BooleanVar(value=option in existing)
                ttk.Checkbutton(answer_area, text=option, variable=var).pack(anchor="w", pady=4)
                answer_vars[option] = var

        controls = tk.Frame(frame, bg=WHITE)
        controls.pack(fill="x", padx=16, pady=(0, 16))
        self.current_question_controls = controls
        submit_command = self._save_exam_answer_and_next if mode == "exam" else lambda: self._submit_question_from_widget(question, answer_vars, mode)
        ttk.Button(controls, text="Speichern & weiter" if mode == "exam" else "Antwort prüfen", command=submit_command, style="Primary.TButton").pack(side="left")
        if mode == "exam":
            ttk.Button(controls, text="Zurück", command=self._exam_previous, style="Accent.TButton").pack(side="left", padx=(8, 0))
            mark_label = "Markierung aufheben" if question["id"] in self.exam_marked else "Markieren"
            ttk.Button(controls, text=mark_label, command=self._toggle_exam_mark, style="Accent.TButton").pack(side="left", padx=(8, 0))
            ttk.Button(controls, text="Überspringen", command=self._exam_skip, style="Accent.TButton").pack(side="left", padx=(8, 0))
        if mode != "exam":
            ttk.Button(controls, text="Lösung anzeigen", command=lambda: self._reveal_answer(question), style="Accent.TButton").pack(side="left", padx=(8, 0))
        if mode not in ("exam", "type_practice"):
            ttk.Button(controls, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))

        self.current_answer_vars = answer_vars
        self.current_active_question = question

    def _extract_selection(self, question, answer_vars):
        qtype = question["type"]
        if qtype in ("single", "true_false", "hot_area", "active_screen"):
            return answer_vars["selection"].get()
        if qtype == "multi":
            out = []
            for key, var in answer_vars.items():
                if isinstance(var, tk.BooleanVar) and var.get():
                    out.append(key)
            return out
        if qtype in ("ordering", "drag_drop"):
            return answer_vars["drag_widget"].get_order()
        if qtype == "build_list":
            return answer_vars["build_widget"].get_target()
        if qtype == "matching":
            result = {}
            for left, var in answer_vars["pairs"].items():
                result[left] = var.get()
            return result
        if qtype == "case":
            out = []
            for key, var in answer_vars.items():
                if isinstance(var, tk.BooleanVar) and var.get():
                    out.append(key)
            return out
        return None

    def _has_answer(self, question, selected):
        if selected is None:
            return False
        if question["type"] == "matching":
            return isinstance(selected, dict) and all(selected.get(left) for left, _ in question["pairs"])
        if question["type"] in ("multi", "case"):
            return bool(selected)
        if question["type"] in ("ordering", "drag_drop", "build_list"):
            return bool(selected)
        return selected != ""

    def _evaluate_answer(self, question, selected):
        qtype = question["type"]
        correct = question["answer"]
        if qtype in ("single", "true_false", "hot_area", "active_screen"):
            return selected == correct
        if qtype == "multi":
            return sorted(selected) == sorted(correct)
        if qtype in ("ordering", "drag_drop", "build_list"):
            return selected == correct
        if qtype == "matching":
            if not isinstance(selected, dict):
                return False
            actual = {left: right for left, right in [(item[0], selected.get(item[0], "")) for item in question["pairs"]]}
            expected = {left: right for left, right in question["answer"]}
            return actual == expected
        if qtype == "case":
            return sorted(selected) == sorted(correct)
        return False

    def _submit_question_from_widget(self, question, answer_vars, mode):
        if mode == "exam":
            self._submit_exam_answer()
            return
        if self.current_answer_locked:
            return

        selected = self._extract_selection(question, answer_vars)
        if not self._has_answer(question, selected):
            messagebox.showinfo("Antwort erforderlich", "Bitte beantworte die Frage, bevor du sie prüfst.")
            return

        correct = self._evaluate_answer(question, selected)
        score = 100 if correct else 0
        self._record_attempt(question["id"], correct, mode=mode, score=score)

        self.current_answer_locked = True
        self._lock_current_answer_widgets()
        self._reveal_answer(question, correct=correct, selected=selected)

    def _lock_current_answer_widgets(self):
        def lock(widget):
            if isinstance(widget, (DragOrderList, DragBuildList)):
                widget.lock()
                return
            if isinstance(widget, tk.Listbox):
                widget.configure(state="disabled")
            elif isinstance(widget, tk.Canvas):
                widget.unbind("<Button-1>")
                widget.unbind("<B1-Motion>")
                widget.unbind("<ButtonRelease-1>")
            elif isinstance(widget, ttk.Button):
                try:
                    widget.state(["disabled"])
                except tk.TclError:
                    pass
            for child in widget.winfo_children():
                lock(child)

        for container in (self.current_answer_area, self.current_question_controls):
            if container is not None and container.winfo_exists():
                lock(container)

    def _format_answer(self, question, answer):
        if question["type"] == "matching" and isinstance(answer, dict):
            return "\n".join(f"{left} → {right}" for left, right in answer.items())
        if question["type"] == "matching" and isinstance(answer, list):
            return "\n".join(f"{left} → {right}" for left, right in answer)
        if isinstance(answer, list):
            return "\n".join(f"{index}. {item}" for index, item in enumerate(answer, 1))
        return str(answer)

    def _explain_selection(self, question, selected):
        qtype = question["type"]
        expected = question["answer"]
        if selected is None:
            return ""
        if qtype in ("multi", "case"):
            selected_set = set(selected if isinstance(selected, list) else [])
            expected_set = set(expected)
            right = [item for item in question.get("options", []) if item in selected_set and item in expected_set]
            missed = [item for item in question.get("options", []) if item in expected_set and item not in selected_set]
            extra = [item for item in question.get("options", []) if item in selected_set and item not in expected_set]
            parts = []
            if right:
                parts.append("Richtig ausgewählt:\n• " + "\n• ".join(right))
            if missed:
                parts.append("Fehlende richtige Auswahl:\n• " + "\n• ".join(missed))
            if extra:
                parts.append("Falsch ausgewählt:\n• " + "\n• ".join(extra))
            return "\n\n".join(parts) or "Keine Auswahl getroffen."
        if qtype in ("ordering", "drag_drop", "build_list") and isinstance(selected, list):
            lines = []
            for index in range(max(len(selected), len(expected))):
                actual = selected[index] if index < len(selected) else "(keine Auswahl)"
                wanted = expected[index] if index < len(expected) else "(kein weiteres Element)"
                if actual == wanted:
                    lines.append(f"Position {index + 1}: richtig — {actual}")
                else:
                    lines.append(f"Position {index + 1}: falsch — {actual}; erwartet: {wanted}")
            return "\n".join(lines)
        if qtype == "matching" and isinstance(selected, dict):
            expected_map = dict(expected)
            lines = []
            for left, wanted in expected_map.items():
                actual = selected.get(left, "")
                state = "richtig" if actual == wanted else f"falsch; erwartet: {wanted}"
                lines.append(f"{left} → {actual or '(keine Auswahl)'} ({state})")
            return "\n".join(lines)
        if qtype in ("single", "true_false", "hot_area", "active_screen"):
            return f"Deine Auswahl: {selected}\nErwartete Auswahl: {expected}"
        return ""

    def _reveal_answer(self, question, correct=None, selected=None):
        if self.current_question_frame is not None and self.current_question_mode != "exam":
            if selected is not None:
                self.current_answer_locked = True
            self._show_inline_feedback(self.current_question_frame, question, correct, selected)
            return
        explanation = question["explanation"]
        answer_text = self._format_answer(question, question["answer"])
        result = "Richtig" if correct is True else "Nicht richtig" if correct is False else "Lösung"
        message = f"{result}\n\n"
        if selected is not None:
            message += f"Auswertung:\n{self._explain_selection(question, selected)}\n\n"
        message += f"Richtige Antwort:\n{answer_text}\n\nWarum:\n{explanation}\n\nQuelle: {question['source']}"
        messagebox.showinfo("Erklärung", message)
        if self.notebook.index(self.notebook.select()) == self.notebook.index(self.learn_tab):
            self.load_next_learn_question()
        elif self.notebook.index(self.notebook.select()) == self.notebook.index(self.review_tab):
            self.load_weak_question()

    def _show_inline_feedback(self, frame, question, correct, selected):
        if self.current_feedback_frame is not None and self.current_feedback_frame.winfo_exists():
            self.current_feedback_frame.destroy()
        is_correct = correct is True
        is_solution = correct is None
        status_bg = SUCCESS_SURFACE if is_correct else ERROR_SURFACE if not is_solution else SURFACE_ACCENT
        status_border = "#9CE6B8" if is_correct else "#FFB8C5" if not is_solution else "#8FD3FF"
        status_text = (
            "Deine Antwort ist richtig. Gut gemacht."
            if is_correct
            else "Deine Antwort stimmt noch nicht. Prüfe die Auswertung und Erklärung unten."
            if not is_solution
            else "Hier ist die Lösung mit einer kurzen Erklärung."
        )
        feedback = tk.Frame(frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        feedback.pack(fill="x", padx=16, pady=(0, 16))
        self.current_feedback_frame = feedback

        status = tk.Frame(feedback, bg=status_bg, highlightthickness=0)
        status.pack(fill="x")
        tk.Frame(status, bg=status_border, width=6).pack(side="left", fill="y")
        status_content = tk.Frame(status, bg=status_bg)
        status_content.pack(side="left", fill="x", expand=True, padx=14, pady=12)
        title = "Richtig" if is_correct else "Nicht richtig" if not is_solution else "Lösung"
        tk.Label(
            status_content,
            text=title,
            bg=status_bg,
            fg=status_border,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        tk.Label(
            status_content,
            text=status_text,
            bg=status_bg,
            fg=INK,
            font=("Segoe UI", 10),
            justify="left",
            anchor="w",
            wraplength=900,
        ).pack(anchor="w", pady=(3, 0))

        def feedback_section(title, body, accent=AZURE_LIGHT, body_color=INK):
            section = tk.Frame(feedback, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            section.pack(fill="x", padx=14, pady=(12, 0))
            tk.Label(
                section,
                text=title,
                bg=SURFACE,
                fg=accent,
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w", padx=12, pady=(10, 4))
            tk.Label(
                section,
                text=body,
                bg=SURFACE,
                fg=body_color,
                justify="left",
                anchor="w",
                wraplength=890,
                font=("Segoe UI", 10),
            ).pack(anchor="w", padx=12, pady=(0, 10))

        if selected is not None:
            detail = self._explain_selection(question, selected)
            if detail:
                feedback_section("Deine Auswertung", detail, "#FFB8C5" if not is_correct else "#9CE6B8")
        feedback_section(
            "Richtige Antwort",
            self._format_answer(question, question["answer"]),
            AZURE_NAVY,
            AZURE_NAVY,
        )
        feedback_section("Warum das stimmt", question["explanation"])
        actions = tk.Frame(feedback, bg=WHITE)
        actions.pack(fill="x", padx=14, pady=12)
        if self.current_question_mode == "type_practice":
            ttk.Button(actions, text="Nächste Frage dieses Typs", command=self._next_type_practice, style="Primary.TButton").pack(side="left")
            ttk.Button(actions, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))
        elif self.current_question_mode == "learn":
            ttk.Button(actions, text="Nächste Frage", command=self.load_next_learn_question, style="Primary.TButton").pack(side="left")
            ttk.Button(actions, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))
        elif self.current_question_mode == "today":
            ttk.Button(actions, text="Nächster Planpunkt", command=self._next_today_plan_question, style="Primary.TButton").pack(side="left")
            ttk.Button(actions, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))
        elif self.current_question_mode == "exam_review":
            ttk.Button(actions, text="Nächste Prüfungsfrage", command=self._next_exam_review_question, style="Primary.TButton").pack(side="left")
            ttk.Button(actions, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))
        elif self.current_question_mode == "weak":
            ttk.Button(actions, text="Nächste Schwachstelle", command=self.load_weak_question, style="Primary.TButton").pack(side="left")
            ttk.Button(actions, text="Microsoft Learn öffnen", command=lambda: webbrowser.open(question["source"]), style="Accent.TButton").pack(side="left", padx=(8, 0))

    def _next_type_practice(self):
        if self.type_practice_question:
            self.open_type_practice(self.type_practice_question["type"])

    def open_learn_tab(self):
        self.notebook.select(self.learn_tab)

    def load_next_learn_question(self):
        topic = self._get_selected_topic()
        question_type = self._get_selected_type()
        difficulty = self._get_selected_difficulty()
        pool = [
            q for q in self.questions
            if (topic == "all" or q["category"] == topic)
            and (question_type == "all" or q["type"] == question_type)
            and (difficulty == "all" or str(q.get("difficulty", 1)) == difficulty)
        ]
        if not pool:
            return
        if len(pool) > 1 and self.last_learn_question_id:
            alternatives = [question for question in pool if question["id"] != self.last_learn_question_id]
            pool = alternatives or pool
        self.current_learn_question = random.choice(pool)
        self.last_learn_question_id = self.current_learn_question["id"]
        self._render_question_widget(self.learn_content, self.current_learn_question, mode="learn")

    def _refresh_weak_areas(self):
        due_ids = self._fetch_due_review_questions()
        self.due_count_var.set(f"{len(due_ids)} fällig")
        due_entries = []
        if not due_ids:
            self._render_review_queue(
                self.due_review_queue,
                due_entries,
                "Nichts ist heute fällig. Beantworte Fragen in Lernen oder der Prüfungssimulation, um deinen Wiederholungsplan zu starten.",
            )
        else:
            today = date.today()
            for qid in due_ids:
                question = self._get_question_by_id(qid)
                if not question:
                    continue
                row = self.db.execute(
                    "SELECT next_review, box FROM review_schedule WHERE question_id = ?",
                    (qid,),
                ).fetchone()
                overdue_days = (today - datetime.strptime(row["next_review"], "%Y-%m-%d").date()).days
                overdue_label = "heute fällig" if overdue_days <= 0 else f"{overdue_days} Tag(e) überfällig"
                due_entries.append(
                    {
                        "question": question,
                        "meta": f"BOX {row['box']} · {overdue_label.upper()}",
                        "prompt": question["prompt"],
                        "accent": "#8E44AD",
                    }
                )
            self._render_review_queue(self.due_review_queue, due_entries, "")

        weak_ids = self._fetch_weak_questions()
        weak_entries = []
        if not weak_ids:
            self._render_review_queue(
                self.weak_review_queue,
                weak_entries,
                "Noch keine Schwachstellen gespeichert. Übe ein paar Fragen, dann erscheinen sie hier.",
            )
        else:
            for qid in weak_ids:
                question = self._get_question_by_id(qid)
                if question:
                    misses = self.db.execute(
                        "SELECT COUNT(*) FROM attempts WHERE question_id = ? AND correct = 0",
                        (qid,),
                    ).fetchone()[0]
                    weak_entries.append(
                        {
                            "question": question,
                            "meta": f"{DOMAIN_LABELS.get(question['category'], question['category']).upper()} · {misses} FEHLVERSUCH{'E' if misses != 1 else ''}",
                            "prompt": question["prompt"],
                            "accent": "#C0392B",
                        }
                    )
            self._render_review_queue(self.weak_review_queue, weak_entries, "")

    def _select_due_review_question(self, event):
        return

    def load_due_review_question(self):
        due_ids = self._fetch_due_review_questions()
        if not due_ids:
            messagebox.showinfo("Spaced Repetition", "Aktuell ist nichts zur Wiederholung fällig. Beantworte weitere Fragen, um den Plan zu füllen.")
            return
        question = self._get_question_by_id(due_ids[0])
        if question:
            self.current_weak_question = question
            self._render_question_widget(self.review_question_frame, question, mode="weak")

    def _select_weak_question(self, event):
        return

    def load_weak_question(self):
        weak_ids = self._fetch_weak_questions()
        if not weak_ids:
            messagebox.showinfo("Weak areas", "No weak questions are recorded yet. Complete a few practice attempts first.")
            return
        question = self._get_question_by_id(weak_ids[0])
        if question:
            self.current_weak_question = question
            self._render_question_widget(self.review_question_frame, question, mode="weak")

    def open_review_tab(self):
        self.notebook.select(self.review_tab)
        self._refresh_weak_areas()

    def export_progress(self, path=None):
        if path is None:
            path = filedialog.asksaveasfilename(
                title="Fortschritt exportieren",
                initialdir=APP_DIR,
                initialfile=f"azure-learning-progress-{date.today().isoformat()}.json",
                defaultextension=".json",
                filetypes=[("JSON-Datei", "*.json"), ("Alle Dateien", "*.*")],
            )
        if not path:
            return

        exam_runs = []
        for row in self.db.execute("SELECT * FROM exam_runs ORDER BY id").fetchall():
            run = dict(row)
            run["domains"] = json.loads(run.pop("domains_json"))
            exam_runs.append(run)
        progress = {
            "format_version": 1,
            "exported_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "question_bank_size": len(self.questions),
            "attempts": [dict(row) for row in self.db.execute("SELECT * FROM attempts ORDER BY id").fetchall()],
            "exam_runs": exam_runs,
            "review_schedule": [
                dict(row) for row in self.db.execute("SELECT * FROM review_schedule ORDER BY question_id").fetchall()
            ],
            "study_days": [
                row["study_day"] for row in self.db.execute("SELECT study_day FROM study_dates ORDER BY study_day").fetchall()
            ],
        }
        temporary_path = f"{path}.tmp"
        try:
            with open(temporary_path, "w", encoding="utf-8") as export_file:
                json.dump(progress, export_file, ensure_ascii=False, indent=2)
                export_file.write("\n")
            os.replace(temporary_path, path)
        except OSError as error:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
            messagebox.showerror("Export fehlgeschlagen", f"Der Fortschritt konnte nicht exportiert werden:\n{error}")
            return
        messagebox.showinfo("Export erstellt", f"Dein Fortschritt wurde gespeichert unter:\n{path}")

    def start_exam(self):
        self.notebook.select(self.exam_tab)
        if self.exam_timer_id is not None:
            self.root.after_cancel(self.exam_timer_id)
            self.exam_timer_id = None
        self.exam_questions = self._build_exam_set(40)
        self.exam_index = 0
        self.exam_answers = {}
        self.exam_marked = set()
        self.exam_review_active = False
        self.exam_deadline = time.time() + 45 * 60
        self._clear_exam_session()
        self._render_exam_question()
        self._tick_exam_timer()

    def _save_exam_session(self):
        if not self.exam_questions or not self.exam_deadline:
            return
        self.db.execute(
            """
            INSERT OR REPLACE INTO exam_sessions
                (id, question_ids_json, answers_json, marked_json, exam_index, deadline, saved_at)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            """,
            (
                json.dumps([question["id"] for question in self.exam_questions]),
                json.dumps(self.exam_answers, ensure_ascii=False),
                json.dumps(sorted(self.exam_marked)),
                self.exam_index,
                self.exam_deadline,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        self.db.commit()

    def _clear_exam_session(self):
        self.db.execute("DELETE FROM exam_sessions WHERE id = 1")
        self.db.commit()
        if hasattr(self, "resume_exam_button") and self.resume_exam_button.winfo_exists():
            self.resume_exam_button.state(["disabled"])

    def _restore_exam_session(self):
        row = self.db.execute("SELECT * FROM exam_sessions WHERE id = 1").fetchone()
        if not row:
            return
        if row["deadline"] <= time.time():
            self._clear_exam_session()
            return
        question_map = {question["id"]: question for question in self.questions}
        question_ids = json.loads(row["question_ids_json"] or "[]")
        if not question_ids or any(question_id not in question_map for question_id in question_ids):
            self._clear_exam_session()
            return
        self.resume_exam_button.state(["!disabled"])

    def _resume_exam_session(self):
        row = self.db.execute("SELECT * FROM exam_sessions WHERE id = 1").fetchone()
        if not row or row["deadline"] <= time.time():
            self._clear_exam_session()
            return
        question_map = {question["id"]: question for question in self.questions}
        question_ids = json.loads(row["question_ids_json"] or "[]")
        if any(question_id not in question_map for question_id in question_ids):
            self._clear_exam_session()
            return
        self.exam_questions = [question_map[question_id] for question_id in question_ids]
        self.exam_answers = json.loads(row["answers_json"] or "{}")
        self.exam_marked = set(json.loads(row["marked_json"] or "[]"))
        self.exam_index = min(max(0, row["exam_index"]), len(self.exam_questions) - 1)
        self.exam_deadline = row["deadline"]
        self.exam_review_active = False
        self.notebook.select(self.exam_tab)
        self._render_exam_question()
        self._tick_exam_timer()

    def _build_exam_set(self, count):
        weights = {"cloud": 0.275, "architecture": 0.375, "governance": 0.35}
        target_counts = {category: round(count * weight) for category, weight in weights.items()}
        target_counts["architecture"] += count - sum(target_counts.values())

        # The simulator deliberately covers every interaction pattern at least
        # once. The remaining slots follow the official blueprint weighting.
        # Exam selection also prefers scenario-level items (difficulty 2-4),
        # keeping the easier recall questions useful for Learn mode.
        eligible = [q for q in self.questions if q.get("difficulty", 1) >= 2]
        if len(eligible) < count:
            eligible = list(self.questions)
        selected = []
        category_counts = {category: 0 for category in target_counts}
        supported_types = [
            "single", "multi", "true_false", "ordering", "drag_drop",
            "build_list", "matching", "hot_area", "active_screen", "case",
        ]
        for question_type in supported_types:
            pool = [
                q for q in eligible
                if q["type"] == question_type
                and q not in selected
                and category_counts[q["category"]] < target_counts.get(q["category"], 0)
            ]
            if not pool:
                pool = [q for q in eligible if q["type"] == question_type and q not in selected]
            if pool:
                chosen = random.choice(pool)
                selected.append(chosen)
                category_counts[chosen["category"]] += 1

        if count >= 25:
            selected_cases = [q for q in selected if q["type"] == "case"]
            grouped_cases = [
                q for q in eligible
                if q["type"] == "case"
                and q.get("case_group")
                and q not in selected
            ]
            groups = {}
            for question in grouped_cases:
                groups.setdefault(question["case_group"], []).append(question)
            viable_groups = [
                group for group in groups.values()
                if len(group) >= 2
                and sum(category_counts[q["category"]] < target_counts.get(q["category"], 0) for q in group) >= 2
            ]
            if viable_groups:
                current_group = next(
                    (
                        group
                        for group in groups.values()
                        if any(q in selected_cases for q in eligible if q.get("case_group") == group[0]["case_group"])
                    ),
                    random.choice(viable_groups),
                )
                current_group = sorted(current_group, key=lambda q: q.get("case_order", 0))
                for chosen in current_group:
                    if chosen in selected:
                        continue
                    if category_counts[chosen["category"]] >= target_counts.get(chosen["category"], 0):
                        continue
                    selected.append(chosen)
                    category_counts[chosen["category"]] += 1
            case_pool = [q for q in eligible if q["type"] == "case" and q not in selected]
            while len([q for q in selected if q["type"] == "case"]) < 2 and case_pool:
                chosen = random.choice(case_pool)
                case_pool.remove(chosen)
                selected.append(chosen)
                category_counts[chosen["category"]] += 1

        for category, amount in target_counts.items():
            remaining_slots = amount - category_counts[category]
            pool = [
                q for q in eligible
                if q["category"] == category and q not in selected
            ]
            random.shuffle(pool)
            selected.extend(pool[:max(0, remaining_slots)])
            category_counts[category] += min(len(pool), max(0, remaining_slots))

        if len(selected) < count:
            remaining = [q for q in eligible if q not in selected]
            random.shuffle(remaining)
            selected.extend(remaining[:count - len(selected)])
        random.shuffle(selected)
        ordered = []
        grouped_seen = set()
        for question in selected:
            if question["id"] in grouped_seen:
                continue
            group = question.get("case_group")
            if group:
                block = sorted(
                    [candidate for candidate in selected if candidate.get("case_group") == group],
                    key=lambda candidate: candidate.get("case_order", 0),
                )
                ordered.extend(block)
                grouped_seen.update(candidate["id"] for candidate in block)
            else:
                ordered.append(question)
                grouped_seen.add(question["id"])
        return ordered[:count]

    def _tick_exam_timer(self):
        if not self.exam_deadline:
            return
        remaining = max(0, int(self.exam_deadline - time.time()))
        minutes, seconds = divmod(remaining, 60)
        self.exam_timer_var.set(f"{minutes:02d}:{seconds:02d}")
        if remaining <= 0:
            self._finish_exam(force=True)
            return
        self.exam_timer_id = self.root.after(1000, self._tick_exam_timer)

    def _render_exam_question(self):
        if not self.exam_questions:
            return
        self.exam_review_active = False
        q = self.exam_questions[self.exam_index]
        self._clear_frame(self.exam_content)
        self.exam_timer_var.set(
            f"Question {self.exam_index + 1}/{len(self.exam_questions)}  |  "
            f"{max(0, int(self.exam_deadline - time.time())) // 60:02d}:"
            f"{max(0, int(self.exam_deadline - time.time())) % 60:02d}"
        )
        self._render_question_widget(self.exam_content, q, mode="exam")
        navigation = tk.Frame(self.exam_content, bg=AZURE_PALE)
        navigation.pack(fill="x", padx=8, pady=(0, 8))
        actions = tk.Frame(navigation, bg=AZURE_PALE)
        actions.pack(fill="x", pady=(0, 6))
        ttk.Button(actions, text="Überprüfen / abgeben", command=self._confirm_finish_exam, style="Accent.TButton").pack(side="right")
        unanswered = [
            question for question in self.exam_questions
            if not self._has_answer(question, self.exam_answers.get(question["id"]))
        ]
        if unanswered:
            ttk.Button(
                actions,
                text=f"Unbeantwortet ({len(unanswered)})",
                command=lambda: self._jump_to_exam_collection(unanswered),
                style="Accent.TButton",
            ).pack(side="right", padx=(6, 0))
        if self.exam_marked:
            marked_questions = [question for question in self.exam_questions if question["id"] in self.exam_marked]
            ttk.Button(
                actions,
                text=f"Markiert ({len(marked_questions)})",
                command=lambda: self._jump_to_exam_collection(marked_questions),
                style="Accent.TButton",
            ).pack(side="right", padx=(6, 0))
        question_buttons = tk.Frame(navigation, bg=AZURE_PALE)
        question_buttons.pack(fill="x")
        tk.Label(question_buttons, text="Fragen:", bg=AZURE_PALE, fg=MUTED, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 8), pady=2, sticky="nw")
        for index, question in enumerate(self.exam_questions):
            label = str(index + 1)
            if question["id"] in self.exam_marked:
                label += "!"
            button = ttk.Button(
                question_buttons,
                text=label,
                width=4,
                command=lambda target=index: self._jump_exam_question(target),
            )
            button.grid(row=index // 10, column=index % 10 + 1, padx=2, pady=2, sticky="w")

    def _jump_exam_question(self, index):
        if not self.exam_questions or not 0 <= index < len(self.exam_questions):
            return
        if not self.exam_review_active:
            self._capture_exam_answer()
        self.exam_index = index
        self._render_exam_question()

    def _jump_to_exam_collection(self, questions):
        if not questions:
            return
        ids = {question["id"] for question in questions}
        for index, question in enumerate(self.exam_questions):
            if question["id"] in ids:
                self._jump_exam_question(index)
                return

    def _finish_exam(self, force=False):
        if self.exam_timer_id is not None:
            try:
                self.root.after_cancel(self.exam_timer_id)
            except tk.TclError:
                pass
            self.exam_timer_id = None

        if not self.exam_questions:
            return

        if not self.exam_review_active:
            self._capture_exam_answer()
        total = len(self.exam_questions)
        correct_count = 0
        domain_results = {
            category: {"correct": 0, "total": 0}
            for category in ("cloud", "architecture", "governance")
        }
        type_results = {}
        missed_questions = []
        unanswered_questions = []
        for question in self.exam_questions:
            answer = self.exam_answers.get(question["id"])
            selected = answer
            if selected is None:
                if question["type"] in ("multi", "case", "ordering", "drag_drop", "build_list"):
                    selected = []
                elif question["type"] == "matching":
                    selected = {}
                else:
                    selected = ""
            correct = self._evaluate_answer(question, selected)
            if correct:
                correct_count += 1
            domain_results[question["category"]]["total"] += 1
            if correct:
                domain_results[question["category"]]["correct"] += 1
            result = type_results.setdefault(question["type"], {"correct": 0, "total": 0})
            result["total"] += 1
            if correct:
                result["correct"] += 1
            if not self._has_answer(question, answer):
                unanswered_questions.append(question)
            if not correct:
                missed_questions.append(
                    {
                        "question": question,
                        "selected": selected,
                        "answered": self._has_answer(question, answer),
                    }
                )
            self._record_attempt(question["id"], correct, mode="exam", score=100 if correct else 0)
        score = round((correct_count / total) * 100, 1) if total else 0.0
        scaled_score, passed = compute_scaled_score(domain_results)
        self.last_exam_result = {
            "correct": correct_count,
            "total": total,
            "score": score,
            "scaled_score": scaled_score,
            "passed": passed,
            "domains": domain_results,
            "types": type_results,
            "missed": missed_questions,
            "unanswered": unanswered_questions,
            "marked_questions": [
                question for question in self.exam_questions
                if question["id"] in self.exam_marked
            ],
            "marked": len(self.exam_marked),
            "forced": force,
        }
        self._record_exam_run(self.last_exam_result)
        self._clear_exam_session()
        self.exam_questions = []
        self.exam_deadline = None
        self.exam_timer_var.set("45:00")
        self._render_exam_results()
        self._refresh_dashboard()

    def _render_exam_results(self):
        result = self.last_exam_result
        if not result:
            self._prepare_exam_ui()
            return
        self._clear_frame(self.exam_content)
        outer = tk.Frame(self.exam_content, bg=AZURE_PALE)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        score_color = "#107C10" if result["score"] >= 80 else "#A4262C" if result["score"] < 70 else AZURE_NAVY
        card = tk.Frame(outer, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(card, text="Prüfungsergebnis", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=AZURE_NAVY).pack(anchor="w", padx=18, pady=(16, 4))
        tk.Label(card, text=f"{result['correct']}/{result['total']} richtig · {result['score']}% Rohwert", font=("Segoe UI", 14), bg=WHITE, fg=score_color).pack(anchor="w", padx=18, pady=(0, 2))
        scaled = result.get("scaled_score", 100)
        passed = result.get("passed", False)
        scaled_color = "#107C10" if passed else "#A4262C"
        pass_label = "Bestanden" if passed else "Nicht bestanden"
        scaled_score_label = tk.Label(
            card,
            text=f"Geschätzter Score: {scaled}/1000 — {pass_label} (Bestehensgrenze: {EXAM_PASS_SCALED_SCORE})",
            font=("Segoe UI", 18, "bold"),
            bg=WHITE,
            fg=scaled_color,
            justify="left",
            anchor="w",
            wraplength=980,
        )
        scaled_score_label.pack(anchor="w", padx=18, pady=(0, 4))
        card.bind(
            "<Configure>",
            lambda event: scaled_score_label.configure(wraplength=max(500, event.width - 48)),
            add="+",
        )
        tk.Label(
            card,
            text="Geschätzter Score gewichtet die drei Prüfungsbereiche nach dem offiziellen AZ-900-Blueprint "
                 "(Cloud Concepts 25-30%, Architecture & Services 35-40%, Management & Governance 30-35%), statt "
                 "alle Fragen gleich zu gewichten — das bildet die echte Prüfungsbewertung realistischer ab als "
                 "der reine Rohwert. Es bleibt eine Schätzung, keine offizielle Microsoft-Skalierung.",
            bg=WHITE,
            fg=MUTED,
            wraplength=980,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18, pady=(0, 14))

        summary = tk.Frame(outer, bg=AZURE_PALE)
        summary.pack(fill="x", pady=(0, 10))
        for category in ("cloud", "architecture", "governance"):
            label = DOMAIN_UI_LABELS[category]
            stats = result["domains"][category]
            percent = round(stats["correct"] / stats["total"] * 100, 1) if stats["total"] else 0
            tile = tk.Frame(summary, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            tile.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(tile, text=label, bg=WHITE, fg=MUTED, wraplength=250, justify="left", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 4))
            tk.Label(tile, text=f"{stats['correct']}/{stats['total']} · {percent}%", bg=WHITE, fg=AZURE_NAVY, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(0, 10))

        lower = tk.Frame(outer, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        lower.pack(fill="both", expand=True)
        tk.Label(lower, text="Überprüfung", bg=WHITE, fg=AZURE_NAVY, font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        type_summary = []
        for question_type, stats in sorted(result["types"].items()):
            percent = round(stats["correct"] / stats["total"] * 100, 1) if stats["total"] else 0
            type_summary.append(
                f"{QUESTION_TYPE_LABELS.get(question_type, question_type)}: "
                f"{stats['correct']}/{stats['total']} ({percent}%)"
            )
        tk.Label(
            lower,
            text=" · ".join(type_summary),
            bg=WHITE,
            fg=MUTED,
            justify="left",
            anchor="w",
            wraplength=980,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=14, pady=(0, 6))
        tk.Label(
            lower,
            text=f"Unbeantwortet: {len(result['unanswered'])} · Markiert: {result['marked']} · "
                 f"Fehlfragen: {len(result['missed'])}",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=14, pady=(0, 8))
        if result["unanswered"] or result["marked_questions"]:
            review_actions = tk.Frame(lower, bg=WHITE)
            review_actions.pack(fill="x", padx=14, pady=(0, 6))
            if result["unanswered"]:
                ttk.Button(
                    review_actions,
                    text="Unbeantwortete lernen",
                    command=lambda: self._open_exam_review_question_from_list(result["unanswered"]),
                    style="Accent.TButton",
                ).pack(side="left")
            if result["marked_questions"]:
                ttk.Button(
                    review_actions,
                    text="Markierte lernen",
                    command=lambda: self._open_exam_review_question_from_list(result["marked_questions"]),
                    style="Accent.TButton",
                ).pack(side="left", padx=(8, 0))
        tk.Label(
            lower,
            text="Geführte Fehlfragen-Analyse",
            bg=WHITE,
            fg=AZURE_NAVY,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=14, pady=(4, 4))
        review_list = tk.Listbox(
            lower,
            height=4,
            font=("Segoe UI", 10),
            activestyle="none",
            bg=WHITE,
            fg=INK,
            selectbackground=SURFACE_SELECTED,
            selectforeground=INK,
        )
        review_list.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        for entry in result["missed"]:
            question = entry["question"]
            review_list.insert(
                "end",
                f"[{QUESTION_TYPE_LABELS.get(question['type'], question['type'])}] "
                f"{question['prompt'][:120]}",
            )
        if not result["missed"]:
            review_list.insert("end", "Keine Fehlfragen — sehr gute Leistung.")
        review_list.bind("<<ListboxSelect>>", lambda _event: self._open_exam_review_question(review_list))
        self.exam_guided_review_frame = tk.Frame(lower, bg=SURFACE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        self.exam_guided_review_frame.pack(fill="x", padx=14, pady=(0, 12))
        if result["missed"]:
            self._render_exam_guided_review(0)
        else:
            tk.Label(
                self.exam_guided_review_frame,
                text="Es gibt keine Fehlfragen zu analysieren.",
                bg=SURFACE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack(anchor="w", padx=12, pady=12)

        actions = tk.Frame(outer, bg=AZURE_PALE)
        actions.pack(fill="x", pady=(10, 0))
        ttk.Button(actions, text="Neue Simulation", command=self.start_exam, style="Primary.TButton").pack(side="left")
        ttk.Button(actions, text="Schwachstellen öffnen", command=self.open_review_tab, style="Accent.TButton").pack(side="left", padx=(8, 0))
        ttk.Button(actions, text="Dashboard", command=lambda: self.notebook.select(self.dashboard_tab), style="Accent.TButton").pack(side="left", padx=(8, 0))

    def _open_exam_review_question(self, review_list):
        selection = review_list.curselection()
        if not selection or not self.last_exam_result:
            return
        index = selection[0]
        missed = self.last_exam_result.get("missed", [])
        if index >= len(missed):
            return
        self._render_exam_guided_review(index)

    def _render_exam_guided_review(self, index):
        missed = self.last_exam_result.get("missed", []) if self.last_exam_result else []
        if not missed or not 0 <= index < len(missed):
            return
        entry = missed[index]
        question = entry["question"]
        self._clear_frame(self.exam_guided_review_frame)

        header = tk.Frame(self.exam_guided_review_frame, bg=SURFACE)
        header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(
            header,
            text=f"Fehlfrage {index + 1} von {len(missed)}",
            bg=SURFACE,
            fg="#A4262C",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text=QUESTION_TYPE_LABELS.get(question["type"], question["type"]),
            bg=SURFACE,
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right")
        tk.Label(
            self.exam_guided_review_frame,
            text=question["prompt"],
            bg=SURFACE,
            fg=INK,
            font=("Segoe UI", 11, "bold"),
            justify="left",
            anchor="w",
            wraplength=980,
        ).pack(fill="x", padx=12, pady=(0, 8))

        def section(title, body, color=AZURE_BLUE):
            block = tk.Frame(self.exam_guided_review_frame, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
            block.pack(fill="x", padx=12, pady=(0, 6))
            tk.Label(block, text=title, bg=WHITE, fg=color, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(7, 2))
            tk.Label(
                block,
                text=body,
                bg=WHITE,
                fg=INK,
                font=("Segoe UI", 10),
                justify="left",
                anchor="w",
                wraplength=940,
            ).pack(anchor="w", padx=10, pady=(0, 7))

        learner_answer = (
            self._format_answer(question, entry["selected"])
            if entry["answered"]
            else "Nicht beantwortet"
        )
        section("Deine Antwort", learner_answer, "#A4262C")
        section("Richtige Antwort", self._format_answer(question, question["answer"]), "#107C10")
        section("Warum das stimmt", question["explanation"])

        actions = tk.Frame(self.exam_guided_review_frame, bg=SURFACE)
        actions.pack(fill="x", padx=12, pady=(2, 10))
        ttk.Button(
            actions,
            text="Vorherige",
            command=lambda: self._render_exam_guided_review(max(0, index - 1)),
            style="Accent.TButton",
        ).pack(side="left")
        ttk.Button(
            actions,
            text="Nächste",
            command=lambda: self._render_exam_guided_review(min(len(missed) - 1, index + 1)),
            style="Primary.TButton",
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            actions,
            text="Microsoft Learn öffnen",
            command=lambda: webbrowser.open(question["source"]),
            style="Accent.TButton",
        ).pack(side="left", padx=(8, 0))
        schedule_button = ttk.Button(
            actions,
            text="Für heute einplanen",
            style="Accent.TButton",
        )
        schedule_button.pack(side="left", padx=(8, 0))
        schedule_status = tk.StringVar(value="")
        tk.Label(
            actions,
            textvariable=schedule_status,
            bg=SURFACE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(8, 0))

        def schedule_for_today():
            added = self._add_question_to_today_review(question["id"])
            schedule_button.configure(
                text="Für heute eingeplant ✓" if added else "Bereits heute eingeplant"
            )
            schedule_button.state(["disabled"])
            schedule_status.set("Die Frage erscheint in Wiederholung.")

        schedule_button.configure(command=schedule_for_today)

    def _add_question_to_today_review(self, question_id):
        row = self.db.execute(
            "SELECT box, interval_days, reviewed_count, next_review FROM review_schedule WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        today = date.today().isoformat()
        if row and row["next_review"] <= today:
            return False
        if row:
            self.db.execute(
                "UPDATE review_schedule SET next_review = ?, updated_at = ? WHERE question_id = ?",
                (today, datetime.utcnow().isoformat(timespec="seconds"), question_id),
            )
        else:
            self.db.execute(
                """
                INSERT INTO review_schedule
                    (question_id, box, interval_days, next_review, last_result, reviewed_count, updated_at)
                VALUES (?, 1, 1, ?, 0, 0, ?)
                """,
                (question_id, today, datetime.utcnow().isoformat(timespec="seconds")),
            )
        self.db.commit()
        self._refresh_dashboard()
        self._refresh_weak_areas()
        return True

    def _open_exam_review_question_from_list(self, questions):
        if not questions:
            return
        seen = set()
        self.exam_review_questions = []
        for question in questions:
            if question["id"] not in seen:
                self.exam_review_questions.append(question)
                seen.add(question["id"])
        self.exam_review_index = 0
        self.notebook.select(self.learn_tab)
        self._render_exam_review_question()

    def _render_exam_review_question(self):
        if self.exam_review_index >= len(self.exam_review_questions):
            self.exam_review_questions = []
            self.exam_review_index = 0
            self.notebook.select(self.exam_tab)
            self._render_exam_results()
            return
        question = self.exam_review_questions[self.exam_review_index]
        self.current_learn_question = question
        self.last_learn_question_id = question["id"]
        self._render_question_widget(self.learn_content, question, mode="exam_review")

    def _next_exam_review_question(self):
        self.exam_review_index += 1
        self._render_exam_review_question()

    def _submit_exam_answer(self):
        self._save_exam_answer_and_next()

    def _capture_exam_answer(self):
        if not self.exam_questions:
            return None
        question = self.exam_questions[self.exam_index]
        selected = self._extract_selection(question, self.current_answer_vars)
        self.exam_answers[question["id"]] = selected
        self._save_exam_session()
        return selected

    def _save_exam_answer_and_next(self):
        if not self.exam_questions:
            return
        self._capture_exam_answer()
        if self.exam_index < len(self.exam_questions) - 1:
            self.exam_index += 1
            self._render_exam_question()
        else:
            self._confirm_finish_exam()

    def _exam_previous(self):
        if not self.exam_questions:
            return
        self._capture_exam_answer()
        if self.exam_index > 0:
            self.exam_index -= 1
            self._render_exam_question()

    def _exam_skip_or_mark(self):
        self._toggle_exam_mark()
        self._exam_skip()

    def _toggle_exam_mark(self):
        if not self.exam_questions:
            return
        self._capture_exam_answer()
        question = self.exam_questions[self.exam_index]
        if question["id"] in self.exam_marked:
            self.exam_marked.remove(question["id"])
        else:
            self.exam_marked.add(question["id"])
        self._render_exam_question()

    def _exam_skip(self):
        if not self.exam_questions:
            return
        self._capture_exam_answer()
        if self.exam_index < len(self.exam_questions) - 1:
            self.exam_index += 1
            self._render_exam_question()
        else:
            self._confirm_finish_exam()

    def _confirm_finish_exam(self):
        if not self.exam_questions:
            return
        self._capture_exam_answer()
        self._render_exam_submission_review()

    def _render_exam_submission_review(self):
        self.exam_review_active = True
        self._clear_frame(self.exam_content)
        outer = tk.Frame(self.exam_content, bg=AZURE_PALE)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        unanswered = [
            question for question in self.exam_questions
            if not self._has_answer(question, self.exam_answers.get(question["id"]))
        ]
        marked = [
            question for question in self.exam_questions
            if question["id"] in self.exam_marked
        ]
        answered = len(self.exam_questions) - len(unanswered)

        card = tk.Frame(outer, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        card.pack(fill="x", pady=(0, 10))
        tk.Label(
            card,
            text="Simulation überprüfen",
            bg=WHITE,
            fg=AZURE_NAVY,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 4))
        tk.Label(
            card,
            text=f"{answered}/{len(self.exam_questions)} beantwortet · "
                 f"{len(unanswered)} unbeantwortet · {len(marked)} markiert",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=18, pady=(0, 6))
        tk.Label(
            card,
            text="Prüfe markierte oder unbeantwortete Fragen vor der Abgabe. "
                 "Die Lösungen und Erklärungen bleiben bis nach der Abgabe verborgen.",
            bg=WHITE,
            fg=INK,
            wraplength=980,
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18, pady=(0, 14))

        review = tk.Frame(outer, bg=WHITE, highlightthickness=1, highlightbackground=AZURE_BORDER)
        review.pack(fill="both", expand=True)
        tk.Label(
            review,
            text="Fragenübersicht",
            bg=WHITE,
            fg=AZURE_NAVY,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(
            review,
            text="Rot = unbeantwortet   ·   Gelb = markiert   ·   Grün = beantwortet",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=14, pady=(0, 6))
        listbox = tk.Listbox(
            review,
            height=16,
            font=("Segoe UI", 10),
            activestyle="none",
            bg=WHITE,
            fg=INK,
            selectbackground=SURFACE_SELECTED,
            selectforeground=INK,
        )
        listbox.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        for index, question in enumerate(self.exam_questions):
            status = []
            has_answer = self._has_answer(question, self.exam_answers.get(question["id"]))
            if has_answer:
                status.append("beantwortet")
            else:
                status.append("unbeantwortet")
            if question["id"] in self.exam_marked:
                status.append("markiert")
            listbox.insert(
                "end",
                f"{index + 1:02d} · {' · '.join(status)} · "
                f"{QUESTION_TYPE_LABELS.get(question['type'], question['type'])} · "
                f"{question['prompt'][:90]}",
            )
            if not has_answer:
                listbox.itemconfig(index, background=ERROR_SURFACE, foreground="#FFB8C5")
            elif question["id"] in self.exam_marked:
                listbox.itemconfig(index, background="#403514", foreground="#FFE08A")
            else:
                listbox.itemconfig(index, background=SUCCESS_SURFACE, foreground="#8DE6B0")

        def jump_to_selected(_event=None):
            selection = listbox.curselection()
            if selection:
                self.exam_index = selection[0]
                self._render_exam_question()

        listbox.bind("<Double-Button-1>", jump_to_selected)
        controls = tk.Frame(outer, bg=AZURE_PALE)
        controls.pack(fill="x", pady=(10, 0))
        ttk.Button(
            controls,
            text="Zur ausgewählten Frage",
            command=jump_to_selected,
            style="Accent.TButton",
        ).pack(side="left")
        ttk.Button(
            controls,
            text="Zurück zur Prüfung",
            command=self._render_exam_question,
            style="Accent.TButton",
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            controls,
            text="Jetzt abgeben",
            command=self._finish_exam,
            style="Primary.TButton",
        ).pack(side="right")

    def _prepare_exam_ui(self):
        self._clear_frame(self.exam_content)
        frame = tk.Frame(self.exam_content, bg=AZURE_PALE)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Simulation abgeschlossen", font=("Segoe UI", 16, "bold"), bg=AZURE_PALE, fg=AZURE_NAVY).pack(padx=12, pady=12, anchor="w")
        ttk.Button(frame, text="Prüfung starten", command=self.start_exam, style="Primary.TButton").pack(anchor="w", padx=12, pady=(0, 10))


def main():
    root = tk.Tk()
    app = AzureLearningApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
