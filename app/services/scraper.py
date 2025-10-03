import requests
from bs4 import BeautifulSoup
import time
import random
import hashlib
import re
from config import Config

class ProductScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.timeout = Config.REQUEST_TIMEOUT
        self.max_results = Config.MAX_RESULTS_PER_SITE
        
    def search_products(self, product_name):
        print(f"Buscando: {product_name}")
        USE_MOCK_DATA = False
        
        if USE_MOCK_DATA:
            print("Usando datos mock")
            return []
        
        all_products = []
        for site in Config.TARGET_SITES:
            try:
                print(f"  Buscando en {site}...")
                products = self._search_site(site, product_name)
                all_products.extend(products)
                print(f"  Encontrados {len(products)} productos")
                time.sleep(1)
            except Exception as e:
                print(f"  Error en {site}: {str(e)}")
                continue
        
        print(f"Total encontrados: {len(all_products)}")
        return all_products
    
    def _search_site(self, site, product_name):
        products = []
        search_urls = {
            'amazon.com': f'https://www.amazon.com/s?k={product_name.replace(" ", "+")}',
            'bestbuy.com': f'https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(" ", "+")}'
        }
        
        target_url = search_urls.get(site)
        if not target_url:
            return products
        
        scraper_url = f'http://api.scraperapi.com?api_key={self.api_key}&url={target_url}'
        
        try:
            response = requests.get(scraper_url, timeout=self.timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html5lib')
                
                if 'amazon.com' in site:
                    products = self._parse_amazon(soup, site)
                elif 'bestbuy.com' in site:
                    products = self._parse_bestbuy(soup, site)
        except Exception as e:
            print(f"    Error: {str(e)}")
        
        return products[:self.max_results]
    
    def _parse_amazon(self, soup, site):
        products = []
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items[:self.max_results]:
            try:
                name_elem = item.find('h2')
                if not name_elem:
                    continue
                
                price_elem = item.find('span', class_='a-price')
                if not price_elem:
                    continue
                
                price_whole = price_elem.find('span', class_='a-price-whole')
                if not price_whole:
                    continue
                
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                try:
                    price_text = price_whole.text.replace(',', '').replace('.', '')
                    price = float(price_text)
                except:
                    continue
                
                href = link_elem['href']
                if href.startswith('/'):
                    product_url = f"https://www.amazon.com{href.split('?')[0]}"
                else:
                    product_url = href.split('?')[0]
                
                rating_elem = item.find('span', class_='a-icon-alt')
                reviews = 4.0
                if rating_elem:
                    try:
                        reviews = float(rating_elem.text.split()[0])
                    except:
                        pass
                
                products.append({
                    'tienda': site,
                    'nombre_crudo': name_elem.text.strip(),
                    'precio': price,
                    'url': product_url,
                    'reviews': reviews
                })
            except:
                continue
        
        return products
    
    def _parse_bestbuy(self, soup, site):
        products = []
        items = soup.find_all('li', class_='sku-item')
        
        for item in items[:self.max_results]:
            try:
                name_elem = item.find('h4', class_='sku-title')
                if not name_elem:
                    continue
                
                price_elem = item.find('span', {'aria-hidden': 'true'})
                if not price_elem:
                    continue
                
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                try:
                    price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                    price = float(re.search(r'(\d+\.?\d*)', price_text).group(1))
                except:
                    continue
                
                href = link_elem['href']
                if href.startswith('/'):
                    product_url = f"https://www.bestbuy.com{href.split('?')[0]}"
                else:
                    product_url = href.split('?')[0]
                
                products.append({
                    'tienda': site,
                    'nombre_crudo': name_elem.text.strip(),
                    'precio': price,
                    'url': product_url,
                    'reviews': 4.0
                })
            except:
                continue
        
        return products
    
    def _parse_walmart(self, soup, site):
        return []
    
    def _parse_ebay(self, soup, site):
        return []
    
    def _parse_target(self, soup, site):
        return []
