"""Скрапер для анализа веб-сайтов конкурентов"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
import re


class WebsiteScraper:
    """Скрапер для сбора данных с веб-сайтов"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = None
        self.driver = None
    
    async def scrape_company_site(self, company_name: str) -> Dict[str, Any]:
        """Скрапинг основного сайта компании"""
        
        # Поиск официального сайта
        website_url = await self._find_company_website(company_name)
        
        if not website_url:
            return {'error': f'Не удалось найти сайт для {company_name}'}
        
        # Сбор данных с сайта
        site_data = await self._scrape_website(website_url)
        
        return {
            'url': website_url,
            'company': company_name,
            **site_data
        }
    
    async def _find_company_website(self, company_name: str) -> Optional[str]:
        """Поиск официального сайта компании через поисковики"""
        # TODO: Реализовать поиск через Google/Bing API
        # Пока возвращаем заглушку
        return f"https://www.{company_name.lower().replace(' ', '')}.com"
    
    async def _scrape_website(self, url: str) -> Dict[str, Any]:
        """Скрапинг конкретного сайта"""
        
        data = {
            'title': '',
            'description': '',
            'keywords': [],
            'content_sections': [],
            'products': [],
            'pricing': [],
            'contact_info': {},
            'technologies': [],
            'meta_data': {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': self.config.get('user_agent', 'Mozilla/5.0')}
                timeout = aiohttp.ClientTimeout(total=self.config.get('timeout', 30))
                
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Извлечение базовой информации
                        data['title'] = soup.find('title').get_text() if soup.find('title') else ''
                        
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        data['description'] = meta_desc.get('content', '') if meta_desc else ''
                        
                        # Извлечение ключевых слов
                        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                        if meta_keywords:
                            data['keywords'] = [kw.strip() for kw in meta_keywords.get('content', '').split(',')]
                        
                        # Анализ контента
                        data['content_sections'] = self._extract_content_sections(soup)
                        
                        # Поиск информации о продуктах
                        data['products'] = self._extract_products(soup)
                        
                        # Поиск ценовой информации
                        data['pricing'] = self._extract_pricing(soup)
                        
                        # Контактная информация
                        data['contact_info'] = self._extract_contact_info(soup)
                        
                        # Анализ используемых технологий
                        data['technologies'] = self._detect_technologies(soup, html)
                        
        except Exception as e:
            data['error'] = str(e)
        
        return data
    
    def _extract_content_sections(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение основных секций контента"""
        sections = []
        
        # Поиск заголовков и связанного контента
        for header in soup.find_all(['h1', 'h2', 'h3']):
            section = {
                'level': header.name,
                'title': header.get_text().strip(),
                'content': ''
            }
            
            # Попытка найти связанный контент
            next_sibling = header.find_next_sibling()
            if next_sibling and next_sibling.name == 'p':
                section['content'] = next_sibling.get_text().strip()
            
            sections.append(section)
        
        return sections[:10]  # Ограничиваем количество секций
    
    def _extract_products(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение информации о продуктах"""
        products = []
        
        # Поиск продуктов по common patterns
        product_selectors = [
            '.product', '.service', '.offering',
            '[data-product]', '.product-card'
        ]
        
        for selector in product_selectors:
            elements = soup.select(selector)
            for el in elements[:5]:  # Ограничиваем количество
                product = {
                    'name': '',
                    'description': '',
                    'price': ''
                }
                
                # Попытка извлечь название
                name_el = el.find(['h1', 'h2', 'h3', 'h4', '.name', '.title'])
                if name_el:
                    product['name'] = name_el.get_text().strip()
                
                # Попытка извлечь описание
                desc_el = el.find(['p', '.description', '.desc'])
                if desc_el:
                    product['description'] = desc_el.get_text().strip()[:200]
                
                # Попытка извлечь цену
                price_el = el.find(['.price', '.cost', '[data-price]'])
                if price_el:
                    product['price'] = price_el.get_text().strip()
                
                if product['name']:  # Добавляем только если есть название
                    products.append(product)
        
        return products
    
    def _extract_pricing(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение ценовой информации"""
        pricing = []
        
        # Поиск ценовых планов
        price_selectors = [
            '.pricing-plan', '.price-card', '.plan',
            '[data-plan]', '.subscription'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for el in elements[:5]:
                plan = {
                    'name': '',
                    'price': '',
                    'features': []
                }
                
                # Название плана
                name_el = el.find(['h1', 'h2', 'h3', 'h4', '.plan-name'])
                if name_el:
                    plan['name'] = name_el.get_text().strip()
                
                # Цена
                price_el = el.find(['.price', '.cost', '.amount'])
                if price_el:
                    plan['price'] = price_el.get_text().strip()
                
                # Функции
                feature_els = el.find_all(['li', '.feature'])
                plan['features'] = [f.get_text().strip() for f in feature_els[:5]]
                
                if plan['price']:  # Добавляем только если есть цена
                    pricing.append(plan)
        
        return pricing
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Извлечение контактной информации"""
        contact = {
            'email': '',
            'phone': '',
            'address': ''
        }
        
        # Поиск email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, soup.get_text())
        if emails:
            contact['email'] = emails[0]
        
        # Поиск телефона
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        phones = re.findall(phone_pattern, soup.get_text())
        if phones:
            contact['phone'] = phones[0]
        
        # Поиск адреса (упрощенно)
        address_el = soup.find(['address', '.address', '.location'])
        if address_el:
            contact['address'] = address_el.get_text().strip()
        
        return contact
    
    def _detect_technologies(self, soup: BeautifulSoup, html: str) -> List[str]:
        """Определение используемых технологий"""
        technologies = []
        
        # Анализ скриптов
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '')
            
            if 'react' in src.lower():
                technologies.append('React')
            elif 'vue' in src.lower():
                technologies.append('Vue.js')
            elif 'angular' in src.lower():
                technologies.append('Angular')
            elif 'jquery' in src.lower():
                technologies.append('jQuery')
        
        # Анализ мета-тегов
        generator = soup.find('meta', attrs={'name': 'generator'})
        if generator:
            technologies.append(generator.get('content', ''))
        
        # Поиск популярных фреймворков по классам и ID
        if soup.find(class_=lambda x: x and 'bootstrap' in x.lower()):
            technologies.append('Bootstrap')
        
        return list(set(technologies))  # Убираем дубликаты
    
    async def close(self):
        """Закрытие ресурсов"""
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()