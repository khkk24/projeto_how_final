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
from .ml_classifier import AccidentSeverityClassifier
from .ml_visualizer import MLVisualizer

__all__ = [
    "DataLoader",
    "DataCleaner",
    "DataExplorer",
    "StatisticalAnalyzer",
    "Visualizer",
    "InsightGenerator",
    "AccidentSeverityClassifier",
    "MLVisualizer",
]
