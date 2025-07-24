"""Анализатор контента с использованием AI"""

import asyncio
from typing import Dict, List, Any
import openai


class ContentAnalyzer:
    """Анализ контента с помощью ИИ"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.openai_key = config.get('openai_api_key', '')
        self.model = config.get('openai_model', 'gpt-4')
    
    async def analyze(self, website_data: Dict, social_data: Dict) -> Dict[str, Any]:
        """Комплексный анализ собранного контента"""
        
        analysis = {
            'sentiment': self._analyze_sentiment(website_data, social_data),
            'key_topics': self._extract_topics(website_data, social_data),
            'brand_positioning': self._analyze_positioning(website_data),
            'content_strategy': self._analyze_content_strategy(social_data),
            'competitive_advantages': self._find_advantages(website_data)
        }
        
        return analysis
    
    def _analyze_sentiment(self, website_data: Dict, social_data: Dict) -> Dict[str, float]:
        """Анализ тональности контента"""
        # Упрощенный анализ - в реальности использовать OpenAI API
        return {
            'website_sentiment': 0.7,  # положительная
            'social_sentiment': 0.6,
            'overall_sentiment': 0.65
        }
    
    def _extract_topics(self, website_data: Dict, social_data: Dict) -> List[str]:
        """Извлечение ключевых тем"""
        topics = []
        
        # Из ключевых слов сайта
        if website_data.get('keywords'):
            topics.extend(website_data['keywords'][:5])
        
        # Из заголовков контента
        if website_data.get('content_sections'):
            topics.extend([
                section['title'] 
                for section in website_data['content_sections'][:3]
            ])
        
        return topics
    
    def _analyze_positioning(self, website_data: Dict) -> Dict[str, str]:
        """Анализ позиционирования бренда"""
        return {
            'value_proposition': website_data.get('description', ''),
            'target_audience': 'Определяется на основе контента',
            'brand_voice': 'Профессиональный'
        }
    
    def _analyze_content_strategy(self, social_data: Dict) -> Dict[str, Any]:
        """Анализ контент-стратегии в соцсетях"""
        return {
            'posting_frequency': 'Средняя активность',
            'engagement_rate': 3.2,
            'content_types': ['Новости', 'Продукты', 'Инсайты'],
            'best_performing_platform': social_data.get('summary', {}).get('most_active_platform', '')
        }
    
    def _find_advantages(self, website_data: Dict) -> List[str]:
        """Поиск конкурентных преимуществ"""
        advantages = []
        
        if website_data.get('products'):
            advantages.append('Широкая линейка продуктов')
        
        if website_data.get('technologies'):
            advantages.append(f'Использует современные технологии: {", ".join(website_data["technologies"])}')
        
        return advantages
