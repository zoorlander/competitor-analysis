"""Основной агент для анализа конкурентов"""

import asyncio
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime

from scrapers.website_scraper import WebsiteScraper
from scrapers.social_scraper import SocialScraper
from analyzers.content_analyzer import ContentAnalyzer
from analyzers.market_analyzer import MarketAnalyzer
from reports.report_generator import ReportGenerator


class CompetitorAgent:
    """Главный агент для комплексного анализа конкурентов"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.website_scraper = WebsiteScraper(config.get('scraping', {}))
        self.social_scraper = SocialScraper(config.get('social', {}))
        self.content_analyzer = ContentAnalyzer(config.get('analysis', {}))
        self.market_analyzer = MarketAnalyzer(config.get('market', {}))
        self.report_generator = ReportGenerator(config.get('reports', {}))
    
    async def analyze_competitor(self, company_name: str, output_dir: str) -> Dict[str, Any]:
        """Полный анализ конкурента"""
        
        results = {
            'company': company_name,
            'website_data': {},
            'social_data': {},
            'content_analysis': {},
            'market_analysis': {},
            'timestamp': datetime.now()
        }
        
        # 1. Сбор данных с веб-сайта
        print(f"Анализируем веб-сайт {company_name}...")
        website_data = await self.website_scraper.scrape_company_site(company_name)
        results['website_data'] = website_data
        
        # 2. Сбор данных из социальных сетей
        print(f"Анализируем социальные сети {company_name}...")
        social_data = await self.social_scraper.scrape_social_profiles(company_name)
        results['social_data'] = social_data
        
        # 3. Анализ контента
        print("Анализируем собранный контент...")
        content_analysis = await self.content_analyzer.analyze(
            website_data, social_data
        )
        results['content_analysis'] = content_analysis
        
        # 4. Рыночный анализ
        print("Проводим рыночный анализ...")
        market_analysis = await self.market_analyzer.analyze(
            company_name, results
        )
        results['market_analysis'] = market_analysis
        
        # 5. Генерация отчета
        print("Генерируем отчет...")
        await self.report_generator.generate_report(results, output_dir)
        
        return results
    
    async def schedule_analysis(self, companies: List[str], schedule: str):
        """Запланированный анализ нескольких конкурентов"""
        # TODO: Реализовать планировщик
        pass