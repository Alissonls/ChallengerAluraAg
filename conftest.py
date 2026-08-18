"""
conftest.py — Configuração global do pytest para o Nexus AI
"""
import sys
import os

# Injeta o backend no path para todos os testes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
