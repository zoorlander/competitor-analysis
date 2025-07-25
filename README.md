# 🔍 Система анализа конкурентов

Автоматизированная система для комплексного анализа конкурентов с использованием веб-скрапинга, мониторинга социальных сетей и ИИ-аналитики.

## 🚀 Возможности

- **Веб-анализ**: Автоматический сбор данных с сайтов конкурентов
- **Социальные сети**: Мониторинг активности в Twitter, LinkedIn, Facebook, Instagram
- **ИИ-анализ**: Анализ контента и тональности с помощью OpenAI GPT-4
- **Рыночная аналитика**: SWOT-анализ и позиционирование
- **Отчеты**: Генерация HTML, JSON и Markdown отчетов
- **Планировщик**: Автоматические регулярные проверки

## 📁 Структура проекта

```
competitor-analysis/
├── agents/              # Основные агенты
│   ├── __init__.py
│   └── competitor_agent.py
├── scrapers/            # Модули веб-скрапинга
│   ├── __init__.py
│   ├── website_scraper.py
│   └── social_scraper.py
├── analyzers/           # ИИ-анализаторы
│   ├── __init__.py
│   ├── content_analyzer.py
│   └── market_analyzer.py
├── reports/             # Генерация отчетов
│   ├── __init__.py
│   └── report_generator.py
├── config/              # Конфигурация
│   ├── __init__.py
│   ├── settings.py
│   └── default.yaml
├── data/                # Хранение данных (создается автоматически)
├── requirements.txt     # Зависимости
├── main.py              # Основной скрипт
├── example.py           # Пример использования
└── README.md
```

## 🛠 Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/zoorlander/competitor-analysis.git
cd competitor-analysis
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте конфигурацию:**
```bash
cp config/default.yaml config/my_config.yaml
# Отредактируйте my_config.yaml, добавив API ключи
```

## ⚙️ Конфигурация

Основные настройки в `config/default.yaml`:

```yaml
analysis:
  openai_api_key: "your-openai-api-key"  # Обязательно для ИИ-анализа
  openai_model: "gpt-4"

social:
  platforms:
    - twitter
    - linkedin
    - facebook
  max_posts: 50

reports:
  format: "html"  # html, json, pdf
  language: "ru"
```

## 📋 Использование

### Командная строка

**Анализ одного конкурента:**
```bash
python main.py --target "Tesla"
```

**С кастомной конфигурацией:**
```bash
python main.py --target "OpenAI" --config config/my_config.yaml --output reports/openai/
```

### Программный интерфейс

```python
import asyncio
from agents.competitor_agent import CompetitorAgent
from config.settings import load_config

async def analyze_competitor():
    config = load_config('config/default.yaml')
    agent = CompetitorAgent(config)
    
    results = await agent.analyze_competitor(
        company_name="Tesla",
        output_dir="reports/tesla/"
    )
    
    print(f"Анализ завершен: {results['company']}")

asyncio.run(analyze_competitor())
```

### Пример массового анализа

```bash
python example.py
```

## 📊 Что анализируется

### Веб-сайт компании
- Заголовки и мета-описания
- Структура контента и разделы
- Информация о продуктах и ценах
- Контактные данные
- Используемые технологии
- SEO-метрики

### Социальные сети
- Количество подписчиков
- Активность постов
- Тональность контента
- Хештеги и упоминания
- Уровень вовлеченности

### Рыночный анализ
- Позиционирование бренда
- Конкурентные преимущества
- SWOT-анализ
- Рыночные тренды
- Рекомендации

## 📈 Типы отчетов

1. **HTML отчет** - Красивый интерактивный отчет с графиками
2. **JSON данные** - Структурированные данные для API
3. **Markdown резюме** - Краткое описание основных находок

Пример структуры отчета:
```
reports/tesla/
├── Tesla_analysis.html     # Основной HTML отчет
├── Tesla_data.json         # Сырые данные в JSON
└── Tesla_summary.md        # Краткое резюме
```

## 🔧 Расширение функциональности

### Добавление новых платформ

1. Расширьте `SocialScraper` в `scrapers/social_scraper.py`
2. Добавьте метод `_scrape_new_platform()`
3. Обновите конфигурацию

### Кастомные анализаторы

1. Создайте новый класс в `analyzers/`
2. Реализуйте метод `analyze()`
3. Интегрируйте в `CompetitorAgent`

### Новые форматы отчетов

1. Расширьте `ReportGenerator` в `reports/report_generator.py`
2. Добавьте метод `_generate_custom_report()`

## ⚠️ Ограничения и соображения

- **Rate limiting**: Встроенные задержки для соблюдения ограничений сайтов
- **Robots.txt**: Система уважает robots.txt файлы
- **API ключи**: Требуются для полной функциональности ИИ-анализа
- **Правовые аспекты**: Убедитесь в соблюдении ToS сайтов

## 🔐 Безопасность

- API ключи храните в переменных окружения
- Используйте `.env` файлы для локальной разработки  
- Не коммитьте конфиденциальные данные в Git

## 🤝 Развитие проекта

### Следующие шаги для улучшения:

1. **Интеграция с поисковыми API** (Google, Bing) для автоматического поиска сайтов
2. **Расширение социальных платформ** (TikTok, YouTube, Reddit)
3. **Добавление баз данных** для хранения исторических данных
4. **Веб-интерфейс** для управления анализом
5. **API сервер** для интеграции с другими системами
6. **Уведомления** (email, Slack, Telegram) о результатах
7. **Машинное обучение** для предиктивной аналитики

### Как внести вклад:

1. Fork репозитория
2. Создайте feature branch
3. Сделайте изменения с тестами
4. Отправьте Pull Request

## 📞 Поддержка

- **Issues**: Создавайте issue для багов и предложений
- **Discussions**: Обсуждение идей и вопросов
- **Wiki**: Документация и примеры

## 📄 Лицензия

MIT License - подробности в файле `LICENSE`

---

**⭐ Если проект полезен, поставьте звездочку!**
