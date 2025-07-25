        except Exception as e:
            tech_data['error'] = str(e)
        
        return tech_data
    
    async def _check_url_exists(self, url: str) -> bool:
        """Проверяем существование URL"""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': self.user_agent}
                async with session.head(url, headers=headers, timeout=5) as response:
                    return response.status == 200
        except:
            return False
    
    def _generate_summary(self, main_page: Dict, additional_pages: Dict, technical: Dict) -> Dict[str, Any]:
        """Генерируем краткое резюме анализа"""
        
        summary = {
            'site_quality_score': 0,
            'key_findings': [],
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        score = 0
        
        # Оценка качества сайта (0-100)
        if main_page.get('title'):
            score += 10
        if main_page.get('description'):
            score += 10
        if main_page.get('h1_tags'):
            score += 10
        if main_page.get('call_to_actions'):
            score += 15
        if main_page.get('social_links'):
            score += 5
        if technical.get('https_enabled'):
            score += 10
        if technical.get('mobile_friendly'):
            score += 15
        if technical.get('load_time', 10) < 3:
            score += 15
        if additional_pages.get('pricing_page'):
            score += 10
        
        summary['site_quality_score'] = min(score, 100)
        
        # Ключевые находки
        if main_page.get('call_to_actions'):
            summary['key_findings'].append(f"Найдено {len(main_page['call_to_actions'])} призывов к действию")
        
        if main_page.get('technologies'):
            summary['key_findings'].append(f"Используемые технологии: {', '.join(main_page['technologies'][:3])}")
        
        if additional_pages.get('pricing_page'):
            pricing = additional_pages['pricing_page']
            if pricing.get('plans_found', 0) > 0:
                summary['key_findings'].append(f"Найдено {pricing['plans_found']} тарифных планов")
        
        # Сильные стороны
        if technical.get('https_enabled'):
            summary['strengths'].append("HTTPS включен")
        
        if technical.get('mobile_friendly'):
            summary['strengths'].append("Адаптивная версия для мобильных")
        
        if main_page.get('social_links'):
            summary['strengths'].append(f"Присутствие в {len(main_page['social_links'])} социальных сетях")
        
        # Слабые места
        if not main_page.get('description'):
            summary['weaknesses'].append("Отсутствует meta description")
        
        if not technical.get('has_sitemap'):
            summary['weaknesses'].append("Нет sitemap.xml")
        
        if technical.get('load_time', 0) > 5:
            summary['weaknesses'].append("Медленная загрузка страницы")
        
        # Рекомендации
        if not main_page.get('description'):
            summary['recommendations'].append("Добавить meta description для улучшения SEO")
        
        if len(main_page.get('call_to_actions', [])) < 2:
            summary['recommendations'].append("Увеличить количество призывов к действию")
        
        if not additional_pages.get('blog_page'):
            summary['recommendations'].append("Создать блог для контент-маркетинга")
        
        return summary
