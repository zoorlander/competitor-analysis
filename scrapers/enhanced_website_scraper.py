"""Улучшенный скрапер для анализа веб-сайтов конкурентов"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse, quote
import re
import time
from datetime import datetime


class EnhancedWebsiteScraper:
    """Улучшенный скрапер для глубокого анализа сайтов"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.delay = config.get('delay', 1)
        self.timeout = config.get('timeout', 30)
        self.user_agent = config.get('user_agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        self.max_pages = config.get('max_pages', 5)
        
    async def scrape_company_site(self, company_name: str) -> Dict[str, Any]:
        """Комплексный анализ сайта компании"""
        
        print(f"🔍 Ищем официальный сайт {company_name}...")
        
        # 1. Находим официальный сайт
        website_url = await self._find_company_website(company_name)
        
        if not website_url:
            return {'error': f'Не удалось найти сайт для {company_name}'}
        
        print(f"✅ Найден сайт: {website_url}")
        print(f"📊 Анализируем структуру сайта...")
        
        # 2. Собираем данные с главной страницы
        main_page_data = await self._scrape_main_page(website_url)
        
        # 3. Анализируем дополнительные страницы
        print(f"📄 Ищем дополнительные страницы...")
        additional_pages = await self._scrape_additional_pages(website_url)
        
        # 4. Технический анализ
        print(f"🔧 Технический анализ...")
        tech_analysis = await self._technical_analysis(website_url)
        
        # Объединяем все данные
        result = {
            'url': website_url,
            'company': company_name,
            'timestamp': datetime.now().isoformat(),
            'main_page': main_page_data,
            'additional_pages': additional_pages,
            'technical': tech_analysis,
            'summary': self._generate_summary(main_page_data, additional_pages, tech_analysis)
        }
        
        return result
    
    async def _find_company_website(self, company_name: str) -> Optional[str]:
        """Поиск официального сайта через поисковики"""
        
        # Пробуем распространенные паттерны URL
        common_patterns = [
            f"https://www.{company_name.lower().replace(' ', '')}.com",
            f"https://{company_name.lower().replace(' ', '')}.com",
            f"https://www.{company_name.lower().replace(' ', '')}.io",
            f"https://{company_name.lower().replace(' ', '')}.io"
        ]
        
        for url in common_patterns:
            if await self._verify_website(url):
                return url
        
        # Если не нашли, используем DuckDuckGo поиск
        search_query = f'"{company_name}" official website'
        found_url = await self._search_duckduckgo(search_query)
        if found_url and await self._verify_website(found_url):
            return found_url
        
        return None
    
    async def _search_duckduckgo(self, query: str) -> Optional[str]:
        """Поиск через DuckDuckGo"""
        
        try:
            # Используем DuckDuckGo Instant Answer API (бесплатно)
            search_url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
            
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': self.user_agent}
                
                async with session.get(search_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Проверяем результаты
                        if data.get('AbstractURL'):
                            return data['AbstractURL']
                        
                        # Проверяем Related Topics
                        for topic in data.get('RelatedTopics', []):
                            if isinstance(topic, dict) and topic.get('FirstURL'):
                                url = topic['FirstURL']
                                if self._is_valid_company_url(url, query.split()[0]):
                                    return url
                                    
        except Exception as e:
            print(f"Ошибка поиска в DuckDuckGo: {e}")
        
        return None
    
    def _is_valid_company_url(self, url: str, company_name: str) -> bool:
        """Проверяем, что URL похож на официальный сайт компании"""
        
        domain = urlparse(url).netloc.lower()
        company_clean = company_name.lower().replace(' ', '').replace('"', '')
        
        # Исключаем социальные сети и агрегаторы
        excluded_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 
                          'youtube.com', 'wikipedia.org', 'crunchbase.com', 'glassdoor.com']
        
        for excluded in excluded_domains:
            if excluded in domain:
                return False
        
        # Проверяем, содержит ли домен название компании
        return company_clean in domain
    
    async def _verify_website(self, url: str) -> bool:
        """Проверяем доступность сайта"""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': self.user_agent}
                async with session.head(url, headers=headers, timeout=10) as response:
                    return response.status in [200, 301, 302]
        except:
            return False
    
    async def _scrape_main_page(self, url: str) -> Dict[str, Any]:
        """Детальный анализ главной страницы"""
        
        data = {
            'title': '',
            'description': '',
            'h1_tags': [],
            'navigation_menu': [],
            'call_to_actions': [],
            'social_links': [],
            'contact_info': {},
            'value_propositions': [],
            'testimonials': [],
            'pricing_mentioned': False,
            'technologies': [],
            'forms': [],
            'images_count': 0,
            'links_analysis': {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': self.user_agent}
                
                async with session.get(url, headers=headers, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Базовая информация
                        data['title'] = soup.find('title').get_text().strip() if soup.find('title') else ''
                        
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        data['description'] = meta_desc.get('content', '').strip() if meta_desc else ''
                        
                        # H1 заголовки
                        data['h1_tags'] = [h1.get_text().strip() for h1 in soup.find_all('h1')]
                        
                        # Навигационное меню
                        data['navigation_menu'] = self._extract_navigation(soup)
                        
                        # Call-to-action кнопки
                        data['call_to_actions'] = self._extract_cta_buttons(soup)
                        
                        # Социальные ссылки
                        data['social_links'] = self._extract_social_links(soup)
                        
                        # Контактная информация
                        data['contact_info'] = self._extract_contact_info(soup)
                        
                        # Value propositions
                        data['value_propositions'] = self._extract_value_props(soup)
                        
                        # Отзывы и testimonials
                        data['testimonials'] = self._extract_testimonials(soup)
                        
                        # Упоминания цен
                        data['pricing_mentioned'] = self._check_pricing_mentions(soup)
                        
                        # Технологии
                        data['technologies'] = self._detect_technologies(soup, html)
                        
                        # Формы
                        data['forms'] = self._extract_forms(soup)
                        
                        # Подсчет элементов
                        data['images_count'] = len(soup.find_all('img'))
                        
                        # Анализ ссылок
                        data['links_analysis'] = self._analyze_links(soup, url)
                        
        except Exception as e:
            data['error'] = str(e)
        
        await asyncio.sleep(self.delay)  # Задержка между запросами
        return data
    
    def _extract_navigation(self, soup: BeautifulSoup) -> List[str]:
        """Извлечение пунктов главного меню"""
        
        nav_items = []
        nav_selectors = ['nav', '.nav', '.navigation', '.menu', '.header-menu']
        
        for selector in nav_selectors:
            nav_element = soup.select_one(selector)
            if nav_element:
                links = nav_element.find_all('a')
                for link in links:
                    text = link.get_text().strip()
                    if text and len(text) < 50:
                        nav_items.append(text)
                break
        
        return list(set(nav_items))[:10]  # Топ-10 уникальных пунктов
    
    def _extract_cta_buttons(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение Call-to-Action кнопок"""
        
        cta_buttons = []
        cta_selectors = [
            '.btn', '.button', '.cta',
            'a[href*="signup"]', 'a[href*="trial"]', 'a[href*="demo"]'
        ]
        
        for selector in cta_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                href = element.get('href', '')
                
                if text and len(text) < 100:
                    cta_buttons.append({
                        'text': text,
                        'url': href,
                        'type': self._categorize_cta(text, href)
                    })
        
        return cta_buttons[:10]
    
    def _categorize_cta(self, text: str, href: str) -> str:
        """Категоризация типа CTA"""
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sign up', 'register', 'join']):
            return 'signup'
        elif any(word in text_lower for word in ['demo', 'trial', 'try']):
            return 'trial'
        elif any(word in text_lower for word in ['contact', 'call']):
            return 'contact'
        elif any(word in text_lower for word in ['pricing', 'price']):
            return 'pricing'
        else:
            return 'other'
    
    def _extract_social_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение ссылок на социальные сети"""
        
        social_links = []
        social_platforms = {
            'twitter.com': 'Twitter',
            'linkedin.com': 'LinkedIn', 
            'facebook.com': 'Facebook',
            'instagram.com': 'Instagram',
            'youtube.com': 'YouTube',
            'github.com': 'GitHub'
        }
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '').lower()
            
            for platform_domain, platform_name in social_platforms.items():
                if platform_domain in href:
                    social_links.append({
                        'platform': platform_name,
                        'url': link.get('href')
                    })
                    break
        
        return social_links
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Извлечение контактной информации"""
        
        contact = {
            'emails': [],
            'phones': [],
            'contact_page': None
        }
        
        text_content = soup.get_text()
        
        # Email адреса
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text_content)
        contact['emails'] = list(set(emails))[:5]  # Первые 5 уникальных
        
        # Телефоны
        phone_pattern = r'\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        phones = re.findall(phone_pattern, text_content)
        contact['phones'] = list(set(phones))[:3]  # Первые 3 уникальных
        
        # Ссылка на страницу контактов
        contact_links = soup.find_all('a', href=True)
        for link in contact_links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            if 'contact' in href or 'contact' in text:
                contact['contact_page'] = link.get('href')
                break
        
        return contact
    
    def _extract_value_props(self, soup: BeautifulSoup) -> List[str]:
        """Извлечение ценностных предложений"""
        
        value_props = []
        headers = soup.find_all(['h1', 'h2', 'h3'])
        
        for header in headers:
            text = header.get_text().strip()
            if 20 <= len(text) <= 200:
                value_props.append(text)
        
        return value_props[:5]
    
    def _extract_testimonials(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Извлечение отзывов клиентов"""
        
        testimonials = []
        testimonial_selectors = ['.testimonial', '.review', '.quote']
        
        for selector in testimonial_selectors:
            elements = soup.select(selector)
            for element in elements:
                quote_text = element.get_text().strip()
                
                if quote_text and len(quote_text) > 20:
                    testimonials.append({
                        'text': quote_text[:200] + '...' if len(quote_text) > 200 else quote_text,
                        'author': 'Unknown'
                    })
        
        return testimonials[:3]
    
    def _check_pricing_mentions(self, soup: BeautifulSoup) -> bool:
        """Проверяем упоминания цен на главной странице"""
        
        text_content = soup.get_text().lower()
        pricing_keywords = ['price', 'pricing', 'cost', 'free', 'trial', '$', '€']
        
        return any(keyword in text_content for keyword in pricing_keywords)
    
    def _detect_technologies(self, soup: BeautifulSoup, html: str) -> List[str]:
        """Определение используемых технологий"""
        
        technologies = []
        
        # Анализ JavaScript библиотек
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '').lower()
            
            if 'react' in src:
                technologies.append('React')
            elif 'vue' in src:
                technologies.append('Vue.js')
            elif 'angular' in src:
                technologies.append('Angular')
            elif 'jquery' in src:
                technologies.append('jQuery')
            elif 'bootstrap' in src:
                technologies.append('Bootstrap')
        
        # Google Analytics
        if 'gtag' in html or 'ga(' in html:
            technologies.append('Google Analytics')
        
        return list(set(technologies))
    
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Анализ форм на сайте"""
        
        forms = []
        form_elements = soup.find_all('form')
        
        for form in form_elements:
            form_data = {
                'fields_count': len(form.find_all(['input', 'select', 'textarea'])),
                'has_email_field': bool(form.find('input', {'type': 'email'})),
                'purpose': 'unknown'
            }
            
            # Определяем назначение формы
            form_text = form.get_text().lower()
            if 'newsletter' in form_text or 'subscribe' in form_text:
                form_data['purpose'] = 'newsletter'
            elif 'contact' in form_text:
                form_data['purpose'] = 'contact'
            elif 'login' in form_text or 'signin' in form_text:
                form_data['purpose'] = 'login'
            
            forms.append(form_data)
        
        return forms
    
    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, int]:
        """Анализ ссылок на странице"""
        
        all_links = soup.find_all('a', href=True)
        base_domain = urlparse(base_url).netloc
        
        internal_count = 0
        external_count = 0
        
        for link in all_links:
            href = link.get('href')
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain == base_domain:
                    internal_count += 1
                else:
                    external_count += 1
            else:
                internal_count += 1  # Относительные ссылки считаем внутренними
        
        return {
            'internal_links': internal_count,
            'external_links': external_count,
            'total_links': len(all_links)
        }
