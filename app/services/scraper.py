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
            print(f"    Response status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html5lib')
                
                if 'amazon.com' in site:
                    products = self._parse_amazon(soup, site)
                    print(f"    Amazon parseado: {len(products)} productos")
                elif 'bestbuy.com' in site:
                    products = self._parse_bestbuy(soup, site)
                    print(f"    BestBuy parseado: {len(products)} productos")
            else:
                print(f"    ⚠ Status code no exitoso: {response.status_code}")
        except Exception as e:
            print(f"    ✗ Error en scraping: {str(e)[:100]}")
        
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
                    # Extraer precio correctamente (ej: $1,299.99 → 1299.99)
                    price_text = price_whole.text.replace(',', '')
                    # Eliminar todo excepto números y punto decimal
                    price_text = ''.join(c for c in price_text if c.isdigit() or c == '.')
                    price = float(price_text)
                except:
                    continue
                
                # Construir URL completa y válida
                href = link_elem['href']
                if href.startswith('/'):
                    # Link relativo: /dp/B08N5WRWNW/ref=...
                    product_url = f"https://www.amazon.com{href}"
                elif href.startswith('http'):
                    # Link absoluto completo
                    product_url = href
                else:
                    # Otro caso: agregar dominio
                    product_url = f"https://www.amazon.com/{href}"
                
                # Limpiar parámetros innecesarios pero mantener /dp/ o /gp/
                if '/dp/' in product_url or '/gp/' in product_url:
                    # Link válido de producto
                    pass
                else:
                    # Si no tiene /dp/ o /gp/, mantener todo
                    pass
                
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
        
        # Intentar múltiples selectores (Best Buy cambia su HTML frecuentemente)
        items = soup.find_all('li', class_='sku-item')
        if not items:
            items = soup.find_all('div', class_='sku-item')
        if not items:
            items = soup.find_all('div', {'data-sku-id': True})
        
        print(f"    BestBuy: Encontrados {len(items)} items en HTML")
        
        for item in items[:self.max_results]:
            try:
                # Buscar nombre del producto con múltiples selectores
                name_elem = item.find('h4', class_='sku-title')
                if not name_elem:
                    name_elem = item.find('h4')
                if not name_elem:
                    name_elem = item.find('a', class_='v-fw-medium')
                if not name_elem:
                    continue
                
                # Buscar precio con múltiples selectores
                price_elem = item.find('span', {'aria-hidden': 'true'})
                if not price_elem:
                    price_elem = item.find('span', class_='priceView-customer-price')
                if not price_elem:
                    price_elem = item.find('span', class_='priceView-hero-price')
                if not price_elem:
                    continue
                
                # Buscar link
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                try:
                    # Extraer precio (ej: $1,299.99 → 1299.99)
                    price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                    # Buscar el primer número con o sin decimales
                    match = re.search(r'(\d+\.?\d*)', price_text)
                    if match:
                        price = float(match.group(1))
                    else:
                        continue
                except:
                    continue
                
                # Construir URL completa
                href = link_elem['href']
                if href.startswith('/'):
                    product_url = f"https://www.bestbuy.com{href}"
                elif href.startswith('http'):
                    product_url = href
                else:
                    product_url = f"https://www.bestbuy.com/{href}"
                
                products.append({
                    'tienda': site,
                    'nombre_crudo': name_elem.text.strip(),
                    'precio': price,
                    'url': product_url,
                    'reviews': 4.0
                })
                print(f"    ✓ BestBuy producto añadido: {name_elem.text.strip()[:50]}... - ${price}")
            except Exception as e:
                print(f"    ⚠ Error parseando item de BestBuy: {str(e)[:50]}")
                continue
        
        return products
    
    def _parse_walmart(self, soup, site):
        return []
    
    def _parse_ebay(self, soup, site):
        return []
    
    def _parse_target(self, soup, site):
        return []
