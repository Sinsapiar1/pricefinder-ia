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
        print(f"\n🔍 Buscando: '{product_name}'")
        print(f"   Sitios a buscar: {', '.join(Config.TARGET_SITES)}")
        print(f"   Productos por sitio: hasta {self.max_results}")
        
        all_products = []
        for site in Config.TARGET_SITES:
            try:
                print(f"\n  📡 Buscando en {site}...")
                products = self._search_site(site, product_name)
                all_products.extend(products)
                if products:
                    print(f"  ✅ {site}: {len(products)} productos encontrados")
                else:
                    print(f"  ⚠️ {site}: No se encontraron productos")
                time.sleep(1)  # Pausa entre sitios para no sobrecargar
            except Exception as e:
                print(f"  ❌ Error en {site}: {str(e)[:100]}")
                continue
        
        print(f"\n📊 Total encontrados: {len(all_products)} productos de {len(Config.TARGET_SITES)} tiendas")
        return all_products
    
    def _search_site(self, site, product_name):
        products = []
        search_query = product_name.replace(" ", "+")
        
        search_urls = {
            'amazon.com': f'https://www.amazon.com/s?k={search_query}',
            'walmart.com': f'https://www.walmart.com/search?q={search_query}',
            'ebay.com': f'https://www.ebay.com/sch/i.html?_nkw={search_query}',
            'bestbuy.com': f'https://www.bestbuy.com/site/searchpage.jsp?st={search_query}'
        }
        
        target_url = search_urls.get(site)
        if not target_url:
            return products
        
        # Configuración óptima de ScraperAPI por tienda
        scraper_params = {
            'api_key': self.api_key,
            'url': target_url,
        }
        
        # Amazon: Simple y efectivo (sin parámetros extra)
        if 'amazon' in site:
            scraper_params['country_code'] = 'us'
            # Amazon funciona perfecto así
        
        # eBay: Configuración especial para mejor compatibilidad
        elif 'ebay' in site:
            scraper_params['country_code'] = 'us'
            scraper_params['keep_headers'] = 'true'
            # eBay a veces necesita render también
            scraper_params['render'] = 'false'  # Explícitamente false primero
        
        # Walmart: Necesita render JS + parámetros especiales
        elif 'walmart' in site:
            scraper_params['render'] = 'true'
            scraper_params['country_code'] = 'us'
            scraper_params['wait_for_selector'] = '[data-automation-id="product-title"]'
        
        # BestBuy: Necesita render JS
        elif 'bestbuy' in site:
            scraper_params['render'] = 'true'
            scraper_params['country_code'] = 'us'
            scraper_params['wait_for_selector'] = '.sku-title'
        
        # Construir URL de ScraperAPI
        scraper_url = 'http://api.scraperapi.com'
        
        try:
            print(f"    📡 Request URL: {scraper_url}")
            print(f"    📋 Target: {target_url}")
            print(f"    ⚙️ Params: {scraper_params}")
            
            response = requests.get(scraper_url, params=scraper_params, timeout=self.timeout)
            print(f"    ✓ Response status: {response.status_code}")
            print(f"    📦 Content length: {len(response.content)} bytes")
            
            if response.status_code == 200:
                # Verificar que hay contenido
                if len(response.content) < 1000:
                    print(f"    ⚠ Respuesta muy pequeña, probablemente bloqueada")
                    print(f"    Contenido: {response.text[:500]}")
                
                soup = BeautifulSoup(response.content, 'html5lib')
                
                if 'amazon.com' in site:
                    products = self._parse_amazon(soup, site)
                    print(f"    ✓ Amazon parseado: {len(products)} productos")
                elif 'walmart.com' in site:
                    products = self._parse_walmart(soup, site)
                    print(f"    ✓ Walmart parseado: {len(products)} productos")
                elif 'ebay.com' in site:
                    products = self._parse_ebay(soup, site)
                    print(f"    ✓ eBay parseado: {len(products)} productos")
                elif 'bestbuy.com' in site:
                    products = self._parse_bestbuy(soup, site)
                    print(f"    ✓ BestBuy parseado: {len(products)} productos")
            else:
                print(f"    ⚠ Status code no exitoso: {response.status_code}")
                
                # FALLBACK STRATEGY
                # Si falló, intentar estrategia alternativa
                if 'ebay' in site and scraper_params.get('render') == 'false':
                    # eBay falló sin render, intentar CON render
                    print(f"    → eBay: Reintentando CON render...")
                    scraper_params['render'] = 'true'
                    response = requests.get(scraper_url, params=scraper_params, timeout=self.timeout)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html5lib')
                        products = self._parse_ebay(soup, site)
                        print(f"    ✓ eBay parseado (con render): {len(products)} productos")
                
                elif 'render' in scraper_params and scraper_params['render'] == 'true':
                    # Walmart/BestBuy falló con render, intentar SIN render
                    print(f"    → Reintentando sin render para ahorrar créditos...")
                    scraper_params['render'] = 'false'
                    if 'session_number' in scraper_params:
                        del scraper_params['session_number']
                    if 'wait_for_selector' in scraper_params:
                        del scraper_params['wait_for_selector']
                    
                    response = requests.get(scraper_url, params=scraper_params, timeout=self.timeout)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html5lib')
                        
                        if 'walmart.com' in site:
                            products = self._parse_walmart(soup, site)
                            print(f"    ✓ Walmart parseado (sin render): {len(products)} productos")
                        elif 'bestbuy.com' in site:
                            products = self._parse_bestbuy(soup, site)
                            print(f"    ✓ BestBuy parseado (sin render): {len(products)} productos")
        except requests.Timeout:
            print(f"    ⏱️ Timeout después de {self.timeout}s - Sitio muy lento")
        except Exception as e:
            print(f"    ✗ Error en scraping: {str(e)[:150]}")
        
        return products[:self.max_results]
    
    def _parse_amazon(self, soup, site):
        products = []
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"    Amazon: Encontrados {len(items)} items en HTML")
        
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
        """Parser REAL para Walmart.com"""
        products = []
        
        # Walmart usa diferentes estructuras según el tipo de página
        # Intentar múltiples selectores
        items = soup.find_all('div', {'data-item-id': True})
        if not items:
            items = soup.find_all('div', class_=re.compile('search-result'))
        if not items:
            items = soup.find_all('div', {'data-testid': 'list-view'})
        
        print(f"    Walmart: Encontrados {len(items)} items en HTML")
        
        for item in items[:self.max_results]:
            try:
                # Buscar nombre
                name_elem = item.find('span', {'data-automation-id': 'product-title'})
                if not name_elem:
                    name_elem = item.find('a', {'link-identifier': True})
                if not name_elem:
                    name_elem = item.find('span', class_=re.compile('product-title'))
                if not name_elem:
                    continue
                
                # Buscar precio
                price_elem = item.find('span', {'data-automation-id': 'product-price'})
                if not price_elem:
                    price_elem = item.find('div', class_=re.compile('price'))
                if not price_elem:
                    continue
                
                # Buscar link
                link_elem = item.find('a', href=True)
                if not link_elem:
                    continue
                
                try:
                    # Extraer precio
                    price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                    match = re.search(r'(\d+\.?\d*)', price_text)
                    if match:
                        price = float(match.group(1))
                    else:
                        continue
                except:
                    continue
                
                # Construir URL
                href = link_elem['href']
                if href.startswith('/'):
                    product_url = f"https://www.walmart.com{href}"
                elif href.startswith('http'):
                    product_url = href
                else:
                    product_url = f"https://www.walmart.com/{href}"
                
                products.append({
                    'tienda': site,
                    'nombre_crudo': name_elem.text.strip(),
                    'precio': price,
                    'url': product_url,
                    'reviews': 4.0
                })
                print(f"    ✓ Walmart producto: {name_elem.text.strip()[:50]}... - ${price}")
            except Exception as e:
                print(f"    ⚠ Error parseando item de Walmart: {str(e)[:50]}")
                continue
        
        return products
    
    def _parse_ebay(self, soup, site):
        """Parser REAL para eBay.com - MEJORADO con múltiples selectores"""
        products = []
        
        # eBay tiene varias estructuras dependiendo de la vista
        items = soup.find_all('li', class_='s-item')
        if not items:
            items = soup.find_all('div', class_='s-item')
        if not items:
            items = soup.find_all('li', class_=re.compile('s-item'))
        if not items:
            # Fallback: buscar cualquier item con enlace y precio
            items = soup.find_all('div', class_=re.compile('item'))
        
        print(f"    eBay: Encontrados {len(items)} items en HTML")
        
        # Debug: Ver qué clases hay
        if items:
            first_item = items[0] if len(items) > 0 else None
            if first_item:
                print(f"    eBay: Primer item classes: {first_item.get('class', [])}")
        
        productos_encontrados = 0
        for idx, item in enumerate(items):
            if productos_encontrados >= self.max_results:
                break
                
            try:
                # Buscar nombre con MÚLTIPLES selectores
                name_elem = item.find('h3', class_='s-item__title')
                if not name_elem:
                    name_elem = item.find('div', class_='s-item__title')
                if not name_elem:
                    name_elem = item.find('h3')
                if not name_elem:
                    name_elem = item.find('span', class_=re.compile('title'))
                if not name_elem:
                    print(f"    eBay item {idx}: No se encontró nombre")
                    continue
                
                nombre_texto = name_elem.text.strip()
                
                # Saltar "Shop on eBay" y otros items especiales
                if 'shop on ebay' in nombre_texto.lower() or len(nombre_texto) < 10:
                    print(f"    eBay item {idx}: Item especial, saltando")
                    continue
                
                # Buscar precio con MÚLTIPLES selectores
                price_elem = item.find('span', class_='s-item__price')
                if not price_elem:
                    price_elem = item.find('span', class_=re.compile('price'))
                if not price_elem:
                    price_elem = item.find('div', class_=re.compile('price'))
                if not price_elem:
                    print(f"    eBay item {idx}: No se encontró precio")
                    continue
                
                # Buscar link
                link_elem = item.find('a', class_='s-item__link', href=True)
                if not link_elem:
                    link_elem = item.find('a', href=True)
                if not link_elem:
                    print(f"    eBay item {idx}: No se encontró link")
                    continue
                
                try:
                    # Extraer precio (puede tener "to" para rangos)
                    price_text = price_elem.text.replace('$', '').replace(',', '').strip()
                    # Limpiar texto extra
                    price_text = price_text.replace('USD', '').replace('Free shipping', '').strip()
                    
                    # Si hay rango (ej: "$100 to $200"), tomar el primero
                    if 'to' in price_text.lower():
                        price_text = price_text.lower().split('to')[0].strip()
                    
                    match = re.search(r'(\d+\.?\d*)', price_text)
                    if match:
                        price = float(match.group(1))
                        if price < 1:  # Precio inválido
                            print(f"    eBay item {idx}: Precio inválido: ${price}")
                            continue
                    else:
                        print(f"    eBay item {idx}: No se pudo extraer precio de '{price_text}'")
                        continue
                except Exception as price_error:
                    print(f"    eBay item {idx}: Error en precio: {str(price_error)[:50]}")
                    continue
                
                # URL de eBay
                product_url = link_elem['href']
                if not product_url.startswith('http'):
                    product_url = f"https://www.ebay.com{product_url}"
                
                # Producto válido encontrado
                products.append({
                    'tienda': site,
                    'nombre_crudo': nombre_texto,
                    'precio': price,
                    'url': product_url,
                    'reviews': 4.0
                })
                productos_encontrados += 1
                print(f"    ✓ eBay producto {productos_encontrados}: {nombre_texto[:50]}... - ${price}")
                
            except Exception as e:
                print(f"    ⚠ eBay item {idx} error general: {str(e)[:100]}")
                continue
        
        print(f"    eBay: Total productos válidos: {len(products)}")
        return products
    
    def _parse_target(self, soup, site):
        """Target no implementado aún"""
        return []
