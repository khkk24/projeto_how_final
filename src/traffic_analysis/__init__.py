"""
traffic_analysis package: outils POO pour charger, nettoyer, explorer, analyser et visualiser
les données d'accidents de transit.
"""
from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .data_explorer import DataExplorer
from .statistical_analyzer import StatisticalAnalyzer
from .visualizer import Visualizer
from .insight_generator import InsightGenerator

__all__ = [
    "DataLoader",
    "DataCleaner",
    "DataExplorer",
    "StatisticalAnalyzer",
    "Visualizer",
    "InsightGenerator",
]
