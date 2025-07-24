"""Генератор отчетов по анализу конкурентов"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ReportGenerator:
    """Генерация отчетов в различных форматах"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.format = config.get('format', 'html')
        self.language = config.get('language', 'ru')
    
    async def generate_report(self, analysis_data: Dict[str, Any], output_dir: str):
        """Генерация основного отчета"""
        
        # Создаем папку для отчетов
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Генерируем отчеты в разных форматах
        if self.format == 'html':
            await self._generate_html_report(analysis_data, output_path)
        
        await self._generate_json_report(analysis_data, output_path)
        await self._generate_summary(analysis_data, output_path)
    
    async def _generate_html_report(self, data: Dict, output_path: Path):
        """Генерация HTML отчета"""
        
        company_name = data.get('company', 'Unknown')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Анализ конкурента: {company_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 30px 0; padding: 20px; border-left: 4px solid #007acc; }}
        .metric {{ background: #f9f9f9; padding: 10px; margin: 10px 0; border-radius: 3px; }}
        .recommendation {{ background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Анализ конкурента: {company_name}</h1>
        <p><strong>Дата анализа:</strong> {timestamp}</p>
    </div>
    
    <div class="section">
        <h2>📊 Основные метрики</h2>
        {self._format_website_metrics(data.get('website_data', {}))}
        {self._format_social_metrics(data.get('social_data', {}))}
    </div>
    
    <div class="section">
        <h2>🎯 Анализ контента</h2>
        {self._format_content_analysis(data.get('content_analysis', {}))}
    </div>
    
    <div class="section">
        <h2>🏪 Рыночный анализ</h2>
        {self._format_market_analysis(data.get('market_analysis', {}))}
    </div>
    
    <div class="section">
        <h2>💡 Рекомендации</h2>
        {self._format_recommendations(data.get('market_analysis', {}).get('recommendations', []))}
    </div>
</body>
</html>
        """
        
        # Сохраняем HTML файл
        html_file = output_path / f"{company_name}_analysis.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _format_website_metrics(self, website_data: Dict) -> str:
        """Форматирование метрик сайта"""
        if not website_data:
            return "<p>Данные о сайте недоступны</p>"
        
        return f"""
        <div class="metric">
            <strong>Сайт:</strong> {website_data.get('url', 'N/A')}<br>
            <strong>Заголовок:</strong> {website_data.get('title', 'N/A')}<br>
            <strong>Описание:</strong> {website_data.get('description', 'N/A')}<br>
            <strong>Продукты:</strong> {len(website_data.get('products', []))} найдено<br>
            <strong>Технологии:</strong> {', '.join(website_data.get('technologies', []))}
        </div>
        """
    
    def _format_social_metrics(self, social_data: Dict) -> str:
        """Форматирование метрик соцсетей"""
        if not social_data:
            return "<p>Данные о социальных сетях недоступны</p>"
        
        summary = social_data.get('summary', {})
        return f"""
        <div class="metric">
            <strong>Общее количество подписчиков:</strong> {summary.get('total_followers', 0)}<br>
            <strong>Наиболее активная платформа:</strong> {summary.get('most_active_platform', 'N/A')}<br>
            <strong>Платформы:</strong> {', '.join(social_data.get('platforms', {}).keys())}
        </div>
        """
    
    def _format_content_analysis(self, content_analysis: Dict) -> str:
        """Форматирование анализа контента"""
        if not content_analysis:
            return "<p>Анализ контента недоступен</p>"
        
        topics = content_analysis.get('key_topics', [])
        sentiment = content_analysis.get('sentiment', {})
        
        return f"""
        <div class="metric">
            <strong>Ключевые темы:</strong> {', '.join(topics[:5])}<br>
            <strong>Общая тональность:</strong> {sentiment.get('overall_sentiment', 0):.2f}<br>
            <strong>Позиционирование:</strong> {content_analysis.get('brand_positioning', {}).get('value_proposition', 'N/A')}
        </div>
        """
    
    def _format_market_analysis(self, market_analysis: Dict) -> str:
        """Форматирование рыночного анализа"""
        if not market_analysis:
            return "<p>Рыночный анализ недоступен</p>"
        
        position = market_analysis.get('market_position', {})
        competitors = market_analysis.get('competitors', [])
        
        competitors_html = ""
        for comp in competitors[:3]:
            competitors_html += f"<li><strong>{comp.get('name')}:</strong> {comp.get('market_share')} - {comp.get('strengths')}</li>"
        
        return f"""
        <div class="metric">
            <strong>Рыночная позиция:</strong> {position.get('market_share', 'N/A')}<br>
            <strong>Сегмент:</strong> {position.get('market_segment', 'N/A')}<br>
            <strong>Основные конкуренты:</strong>
            <ul>{competitors_html}</ul>
        </div>
        """
    
    def _format_recommendations(self, recommendations: list) -> str:
        """Форматирование рекомендаций"""
        if not recommendations:
            return "<p>Рекомендации не сгенерированы</p>"
        
        rec_html = ""
        for i, rec in enumerate(recommendations, 1):
            rec_html += f'<div class="recommendation">{i}. {rec}</div>'
        
        return rec_html
    
    async def _generate_json_report(self, data: Dict, output_path: Path):
        """Генерация JSON отчета для API интеграции"""
        
        json_file = output_path / f"{data.get('company', 'unknown')}_data.json"
        
        # Добавляем метаинформацию
        data['meta'] = {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'format': 'competitor_analysis'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    async def _generate_summary(self, data: Dict, output_path: Path):
        """Генерация краткого резюме"""
        company_name = data.get('company', 'Unknown')
        
        summary = f"""
# Краткое резюме: {company_name}

## Ключевые находки:
- Подписчиков в соцсетях: {data.get('social_data', {}).get('summary', {}).get('total_followers', 0)}
- Продуктов на сайте: {len(data.get('website_data', {}).get('products', []))}
- Используемые технологии: {len(data.get('website_data', {}).get('technologies', []))}

## Главные рекомендации:
"""
        
        recommendations = data.get('market_analysis', {}).get('recommendations', [])
        for i, rec in enumerate(recommendations[:3], 1):
            summary += f"{i}. {rec}\n"
        
        summary_file = output_path / f"{company_name}_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
