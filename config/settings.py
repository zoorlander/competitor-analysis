"""Модуль для работы с конфигурацией"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """Загрузка конфигурации из YAML файла"""
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        # Создаем базовую конфигурацию если файл не существует
        return get_default_config()
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def get_default_config() -> Dict[str, Any]:
    """Базовая конфигурация по умолчанию"""
    
    return {
        'scraping': {
            'delay': 1,  # Задержка между запросами в секундах
            'timeout': 30,  # Таймаут запроса в секундах
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'max_pages': 10  # Максимальное количество страниц для анализа
        },
        'social': {
            'platforms': ['twitter', 'linkedin', 'facebook'],
            'max_posts': 50  # Максимальное количество постов для анализа
        },
        'analysis': {
            'openai_api_key': '',  # Ваш OpenAI API ключ
            'openai_model': 'gpt-4',
            'max_tokens': 2000,
            'languages': ['ru', 'en']
        },
        'market': {
            'search_engines': ['google', 'yandex'],
            'market_analysis_depth': 'medium'  # low, medium, high
        },
        'reports': {
            'format': 'html',  # html, pdf, json
            'include_charts': True,
            'language': 'ru'
        },
        'database': {
            'type': 'sqlite',  # sqlite, postgresql
            'path': 'data/competitors.db'  # для SQLite
        }
    }


def save_config(config: Dict[str, Any], config_path: str):
    """Сохранение конфигурации в YAML файл"""
    
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
