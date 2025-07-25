#!/usr/bin/env python3
"""
Пример использования системы анализа конкурентов
"""

import asyncio
from agents.competitor_agent import CompetitorAgent
from config.settings import load_config


async def main():
    """Демонстрация работы агента"""
    
    # Загружаем конфигурацию
    config = load_config('config/default.yaml')
    
    # Создаем агента
    agent = CompetitorAgent(config)
    
    # Список компаний для анализа
    companies = [
        "Tesla",
        "OpenAI", 
        "Stripe"
    ]
    
    print("🔍 Запуск анализа конкурентов...")
    
    for company in companies:
        print(f"\n📊 Анализируем: {company}")
        
        try:
            # Запускаем анализ
            results = await agent.analyze_competitor(
                company_name=company,
                output_dir=f"reports/{company.lower()}"
            )
            
            print(f"✅ Анализ {company} завершен успешно")
            
            # Выводим краткую статистику
            website_data = results.get('website_data', {})
            social_data = results.get('social_data', {})
            
            print(f"   📱 Подписчиков в соцсетях: {social_data.get('summary', {}).get('total_followers', 0)}")
            print(f"   🌐 Технологий на сайте: {len(website_data.get('technologies', []))}")
            print(f"   📦 Продуктов найдено: {len(website_data.get('products', []))}")
            
        except Exception as e:
            print(f"❌ Ошибка при анализе {company}: {e}")
    
    print("\n🎉 Анализ всех компаний завершен!")
    print("📁 Отчеты сохранены в папке reports/")


if __name__ == "__main__":
    asyncio.run(main())
