#!/usr/bin/env python3
"""
Главный модуль системы анализа конкурентов
"""

import click
import asyncio
from pathlib import Path

from agents.competitor_agent import CompetitorAgent
from config.settings import load_config


@click.command()
@click.option('--target', required=True, help='Название компании-конкурента для анализа')
@click.option('--config', default='config/default.yaml', help='Путь к файлу конфигурации')
@click.option('--output', default='reports/', help='Папка для сохранения отчетов')
def main(target: str, config: str, output: str):
    """Запуск анализа конкурента"""
    
    # Загрузка конфигурации
    config_data = load_config(config)
    
    # Создание агента
    agent = CompetitorAgent(config_data)
    
    # Запуск анализа
    click.echo(f"Начинаем анализ конкурента: {target}")
    
    try:
        # Асинхронный запуск анализа
        asyncio.run(agent.analyze_competitor(target, output))
        click.echo(f"Анализ завершен. Отчеты сохранены в {output}")
    except Exception as e:
        click.echo(f"Ошибка при анализе: {e}", err=True)
        return 1
    
    return 0


if __name__ == '__main__':
    main()