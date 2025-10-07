// Variables globales
let priceChart = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', handleSearch);
});

// Función principal para manejar la búsqueda (MEJORADA)
async function handleSearch(event) {
    event.preventDefault();
    
    // Ocultar mensajes previos
    hideResults();
    hideError();
    
    // Mostrar spinner con progreso
    showLoading();
    updateProgress(10, 'Validando API keys...');
    
    // Obtener datos del formulario
    const formData = {
        gemini_api_key: document.getElementById('geminiKey').value.trim(),
        scraper_api_key: document.getElementById('scraperKey').value.trim(),
        product_name: document.getElementById('productName').value.trim()
    };
    
    try {
        updateProgress(20, 'Conectando con tiendas en línea...');
        
        // Realizar petición al backend
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        updateProgress(60, 'Analizando productos con IA...');
        
        const result = await response.json();
        
        updateProgress(90, 'Generando recomendaciones...');
        
        hideLoading();
        
        if (result.success) {
            updateProgress(100, 'Completado!');
            displayResults(result.data);
            
            // Scroll suave al resultado
            setTimeout(() => {
                document.getElementById('resultsSection').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }, 300);
        } else {
            showError(result.error || 'Error desconocido. Por favor intenta de nuevo.');
        }
        
    } catch (error) {
        hideLoading();
        showError('Error de conexión con el servidor. Por favor verifica tu conexión a internet e intenta nuevamente.');
        console.error('Error:', error);
    }
}

// Función para actualizar el progreso
function updateProgress(percentage, status) {
    const progressBar = document.getElementById('progressBar');
    const loadingStatus = document.getElementById('loadingStatus');
    
    if (progressBar) {
        progressBar.style.width = percentage + '%';
    }
    if (loadingStatus) {
        loadingStatus.textContent = status;
    }
}

// Mostrar resultados
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.remove('hidden');
    
    // Detectar qué tiendas trajeron datos
    const storesFound = detectStoresInResults(data.products);
    displayStoresStatus(storesFound);
    
    // Mostrar resumen de IA
    displayAISummary(data.summary);
    
    // Mostrar insights inteligentes
    if (data.insights && data.insights.length > 0) {
        displayAIInsights(data.insights);
    }
    
    // Mostrar estadísticas
    displayStatistics(data.statistics);
    
    // Mostrar tabla de productos
    displayProductsTable(data.products);
    
    // Crear gráfico de precios
    createPriceChart(data.products);
    
    // Scroll suave a los resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Detectar qué tiendas trajeron datos REALES
function detectStoresInResults(products) {
    const stores = {
        'amazon.com': false,
        'ebay.com': false,
        'walmart.com': false,
        'bestbuy.com': false
    };
    
    products.forEach(product => {
        const tienda = product.tienda.toLowerCase();
        if (stores.hasOwnProperty(tienda)) {
            stores[tienda] = true;
        }
    });
    
    return stores;
}

// Mostrar status dinámico de tiendas
function displayStoresStatus(storesFound) {
    const premiumStores = ['walmart.com', 'bestbuy.com'];
    const hasPremium = premiumStores.some(store => storesFound[store]);
    
    if (hasPremium) {
        showPremiumBanner();
    }
}

// Mostrar banner si usuario tiene plan premium
function showPremiumBanner() {
    const banner = document.createElement('div');
    banner.className = 'bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl shadow-xl p-4 mb-6 text-white text-center animate-pulse';
    banner.innerHTML = `
        <div class="flex items-center justify-center gap-2">
            <i class="fas fa-crown text-yellow-300 text-2xl"></i>
            <span class="font-bold text-lg">¡ScraperAPI Premium Detectado!</span>
        </div>
        <p class="text-sm mt-2 opacity-90">Comparando en Walmart y Best Buy también</p>
    `;
    
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.insertBefore(banner, resultsSection.firstChild);
}

// Mostrar resumen de IA
function displayAISummary(summary) {
    const summaryElement = document.getElementById('aiSummary');
    summaryElement.textContent = summary;
}

// Mostrar insights inteligentes (NUEVO)
function displayAIInsights(insights) {
    const insightsSection = document.getElementById('aiInsights');
    const insightsList = document.getElementById('insightsList');
    
    insightsSection.classList.remove('hidden');
    insightsList.innerHTML = '';
    
    const iconos = ['💡', '🎯', '⚡'];
    const colores = ['bg-blue-50 border-blue-500', 'bg-green-50 border-green-500', 'bg-yellow-50 border-yellow-500'];
    
    insights.forEach((insight, index) => {
        const insightDiv = document.createElement('div');
        insightDiv.className = `${colores[index % 3]} border-l-4 rounded-lg p-4 flex items-start`;
        insightDiv.innerHTML = `
            <span class="text-2xl mr-3">${iconos[index % 3]}</span>
            <p class="text-gray-800 leading-relaxed">${insight}</p>
        `;
        insightsList.appendChild(insightDiv);
    });
}

// Mostrar estadísticas
function displayStatistics(stats) {
    const statsContainer = document.getElementById('statisticsCards');
    
    const cards = [
        {
            icon: 'fa-dollar-sign',
            label: 'Precio Promedio',
            value: `$${stats.precio_promedio}`,
            color: 'blue'
        },
        {
            icon: 'fa-arrow-down',
            label: 'Mejor Precio',
            value: `$${stats.precio_minimo}`,
            color: 'green'
        },
        {
            icon: 'fa-arrow-up',
            label: 'Precio Máximo',
            value: `$${stats.precio_maximo}`,
            color: 'red'
        },
        {
            icon: 'fa-boxes',
            label: 'Total Productos',
            value: stats.total_productos,
            color: 'purple'
        }
    ];
    
    statsContainer.innerHTML = cards.map(card => `
        <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-${card.color}-500 hover:shadow-xl transition-shadow">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-gray-600 font-semibold mb-1">${card.label}</p>
                    <p class="text-3xl font-bold text-gray-800">${card.value}</p>
                </div>
                <i class="fas ${card.icon} text-4xl text-${card.color}-500 opacity-20"></i>
            </div>
        </div>
    `).join('');
}

// Mostrar tabla de productos (MEJORADA Y RESPONSIVA)
function displayProductsTable(products) {
    const tableBody = document.getElementById('productsTableBody');
    const cardsContainer = document.getElementById('productCards');
    
    // Ordenar productos por recomendación y precio
    const sortedProducts = [...products].sort((a, b) => {
        const order = { '🏆 Mejor Opción': 0, '✅ Buena Alternativa': 1, '⚠️ Considerar': 2, '❌ No Recomendado': 3 };
        return (order[a.recomendacion] || 4) - (order[b.recomendacion] || 4) || a.precio - b.precio;
    });
    
    // Generar cards para móvil
    if (cardsContainer) {
        cardsContainer.innerHTML = sortedProducts.map(product => {
            const badgeClass = getBadgeClassNew(product.recomendacion);
            const condicionBadge = getCondicionBadge(product.condicion || 'Desconocido');
            const precioVsPromedio = product.precio_vs_promedio || '0%';
            const precioVsClass = precioVsPromedio.startsWith('-') ? 'text-green-600' : 'text-red-600';
            const categoriaIcon = getCategoriaIcon(product.categoria || 'Diferente');
            const isPremiumStore = isPremiumTier(product.tienda);
            
            return `
                <div class="bg-white border-2 ${badgeClass.includes('green') ? 'border-green-300' : badgeClass.includes('blue') ? 'border-blue-300' : 'border-gray-300'} rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow ${isPremiumStore ? 'ring-2 ring-purple-300' : ''}">
                    <div class="flex items-start justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <div class="w-12 h-12 rounded-xl bg-gradient-to-br ${getStoreColor(product.tienda)} flex items-center justify-center text-white font-bold shadow-md">
                                ${getStoreInitials(product.tienda)}
                            </div>
                            <div>
                                <div class="flex items-center gap-2">
                                    <p class="font-bold text-gray-800">${product.tienda}</p>
                                    ${isPremiumStore ? '<span class="text-[10px] bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-bold">PRO</span>' : ''}
                                </div>
                                ${condicionBadge}
                            </div>
                        </div>
                        <span class="${categoriaIcon === '🎯' ? 'text-2xl' : 'text-xl'}">${categoriaIcon}</span>
                    </div>
                    
                    <h3 class="font-semibold text-gray-900 text-base leading-snug mb-2">
                        ${product.nombre_normalizado || product.nombre_crudo}
                    </h3>
                    
                    <div class="flex items-center justify-between mb-3">
                        <div>
                            <p class="text-3xl font-bold text-indigo-600">$${product.precio.toFixed(2)}</p>
                            <p class="text-sm font-semibold ${precioVsClass}">${precioVsPromedio} vs promedio</p>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 rounded-xl p-3 mb-3">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-semibold text-gray-600">Recomendación:</span>
                            <span class="px-3 py-1 rounded-full text-xs font-bold ${badgeClass}">
                                ${product.recomendacion}
                            </span>
                        </div>
                        <p class="text-xs text-gray-700">${product.razon || 'Sin análisis'}</p>
                    </div>
                    
                    <a href="${product.url}" target="_blank" rel="noopener noreferrer"
                       class="block w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-center py-3 rounded-xl font-bold shadow-md hover:shadow-lg transition-all">
                        <i class="fas fa-external-link-alt mr-2"></i>
                        Ver Oferta en ${product.tienda.split('.')[0]}
                    </a>
                </div>
            `;
        }).join('');
    }
    
    // Tabla para desktop (solo se genera en desktop)
    if (tableBody) {
        tableBody.innerHTML = sortedProducts.map(product => {
            const badgeClass = getBadgeClassNew(product.recomendacion);
            const condicionBadge = getCondicionBadge(product.condicion || 'Desconocido');
            const valorBar = getValorBar(product.valor_score || 50);
            const precioVsPromedio = product.precio_vs_promedio || '0%';
            const precioVsClass = precioVsPromedio.startsWith('-') ? 'text-green-600' : 'text-red-600';
            const categoriaIcon = getCategoriaIcon(product.categoria || 'Diferente');
            const isPremiumStore = isPremiumTier(product.tienda);
            
            return `
                <tr class="border-b hover:bg-indigo-50 transition-colors ${isPremiumStore ? 'bg-purple-50/30' : ''}">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-gradient-to-br ${getStoreColor(product.tienda)} flex items-center justify-center text-white font-bold text-sm shadow">
                                ${getStoreInitials(product.tienda)}
                            </div>
                            <div>
                                <span class="font-semibold text-gray-800">${product.tienda}</span>
                                ${isPremiumStore ? '<div class="text-[10px] bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-bold inline-block ml-2">PRO</div>' : ''}
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4" style="max-width: 400px;">
                        <div class="flex items-start gap-2">
                            <span class="text-xl flex-shrink-0" title="${product.categoria}">${categoriaIcon}</span>
                            <div class="flex-1 min-w-0">
                                <p class="font-semibold text-gray-900 text-base leading-tight mb-1" 
                                   title="${product.nombre_crudo}">
                                    ${product.nombre_normalizado || product.nombre_crudo}
                                </p>
                                <p class="text-xs text-gray-600 leading-tight">
                                    ${product.nombre_crudo.length > 120 ? product.nombre_crudo.substring(0, 120) + '...' : product.nombre_crudo}
                                </p>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4 text-center">
                        ${condicionBadge}
                    </td>
                    <td class="px-6 py-4 text-center">
                        <div class="flex flex-col items-center">
                            <span class="text-2xl font-bold text-indigo-600">$${product.precio.toFixed(2)}</span>
                        </div>
                    </td>
                    <td class="px-6 py-4 text-center">
                        <span class="font-bold ${precioVsClass} text-base">${precioVsPromedio}</span>
                    </td>
                    <td class="px-6 py-4 text-center">
                        ${valorBar}
                    </td>
                    <td class="px-6 py-4 text-center">
                        <span class="px-3 py-1 rounded-full text-xs font-bold ${badgeClass} block mb-2 whitespace-nowrap">
                            ${product.recomendacion}
                        </span>
                        <p class="text-xs text-gray-600 leading-tight">${product.razon || ''}</p>
                    </td>
                    <td class="px-6 py-4 text-center">
                        <a href="${product.url}" target="_blank" rel="noopener noreferrer"
                           class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-bold shadow-md hover:shadow-lg transition-all inline-flex items-center gap-2">
                            <i class="fas fa-external-link-alt"></i>
                            <span>Ver Oferta</span>
                        </a>
                    </td>
                </tr>
            `;
        }).join('');
    }
}

// Crear gráfico de precios
function createPriceChart(products) {
    const ctx = document.getElementById('priceChart');
    
    // Destruir gráfico anterior si existe
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Preparar datos
    const labels = products.map(p => p.tienda);
    const prices = products.map(p => p.precio);
    const colors = products.map(p => {
        if (p.recomendacion === 'Mejor Precio') return 'rgba(34, 197, 94, 0.8)';
        if (p.recomendacion === 'Alternativa') return 'rgba(59, 130, 246, 0.8)';
        return 'rgba(239, 68, 68, 0.8)';
    });
    
    // Crear gráfico
    priceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Precio ($)',
                data: prices,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Precio: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            }
        }
    });
}

// Funciones auxiliares
function getBadgeClass(recomendacion) {
    switch(recomendacion) {
        case 'Mejor Precio':
            return 'bg-green-100 text-green-800';
        case 'Alternativa':
            return 'bg-blue-100 text-blue-800';
        case 'No Recomendado':
            return 'bg-red-100 text-red-800';
        default:
            return 'bg-gray-100 text-gray-800';
    }
}

function getStarsHTML(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let html = '';
    
    for (let i = 0; i < fullStars; i++) {
        html += '<i class="fas fa-star text-yellow-400"></i>';
    }
    
    if (hasHalfStar) {
        html += '<i class="fas fa-star-half-alt text-yellow-400"></i>';
    }
    
    for (let i = 0; i < emptyStars; i++) {
        html += '<i class="far fa-star text-yellow-400"></i>';
    }
    
    return html;
}

// Nuevas funciones auxiliares para análisis inteligente
function getBadgeClassNew(recomendacion) {
    switch(recomendacion) {
        case '🏆 Mejor Opción':
            return 'bg-green-100 text-green-800 border border-green-300';
        case '✅ Buena Alternativa':
            return 'bg-blue-100 text-blue-800 border border-blue-300';
        case '⚠️ Considerar':
            return 'bg-yellow-100 text-yellow-800 border border-yellow-300';
        case '❌ No Recomendado':
            return 'bg-red-100 text-red-800 border border-red-300';
        default:
            // Fallback a badges antiguos
            return getBadgeClass(recomendacion);
    }
}

function getCondicionBadge(condicion) {
    const badges = {
        'Nuevo': '<span class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-semibold">✨ Nuevo</span>',
        'Reacondicionado': '<span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-semibold">🔄 Reacond.</span>',
        'Usado': '<span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs font-semibold">📦 Usado</span>',
        'Desconocido': '<span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">❓ N/A</span>'
    };
    return badges[condicion] || badges['Desconocido'];
}

function getValorBar(score) {
    // score es de 0 a 100
    const percentage = Math.min(100, Math.max(0, score));
    let barColor = 'bg-red-500';
    if (percentage >= 75) barColor = 'bg-green-500';
    else if (percentage >= 50) barColor = 'bg-yellow-500';
    else if (percentage >= 25) barColor = 'bg-orange-500';
    
    return `
        <div class="w-full">
            <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="${barColor} h-2.5 rounded-full" style="width: ${percentage}%"></div>
            </div>
            <span class="text-xs text-gray-600 mt-1 block">${percentage}/100</span>
        </div>
    `;
}

function getCategoriaIcon(categoria) {
    const icons = {
        'Idéntico': '🎯',
        'Similar': '🔄',
        'Alternativa': '💡',
        'Diferente': '❓'
    };
    return icons[categoria] || '📦';
}

// Detectar si es tienda premium
function isPremiumTier(tienda) {
    const premiumStores = ['walmart.com', 'bestbuy.com', 'target.com'];
    return premiumStores.includes(tienda.toLowerCase());
}

// Funciones para logos de tiendas (colores de marca reales)
function getStoreColor(tienda) {
    const colors = {
        'amazon.com': 'from-orange-500 to-yellow-600',        // Amazon naranja/amarillo
        'walmart.com': 'from-blue-500 to-yellow-400',         // Walmart azul/amarillo
        'ebay.com': 'from-red-500 to-blue-500',               // eBay rojo/azul/amarillo
        'bestbuy.com': 'from-blue-600 to-yellow-400',         // BestBuy azul/amarillo
        'target.com': 'from-red-600 to-red-700'               // Target rojo
    };
    return colors[tienda.toLowerCase()] || 'from-gray-500 to-gray-700';
}

function getStoreInitials(tienda) {
    const initials = {
        'amazon.com': 'AZ',
        'walmart.com': 'WM',
        'ebay.com': 'EB',
        'bestbuy.com': 'BB',
        'target.com': 'TG'
    };
    return initials[tienda.toLowerCase()] || tienda.substring(0, 2).toUpperCase();
}

// Funciones de UI
function showLoading() {
    document.getElementById('loadingSpinner').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

function hideResults() {
    document.getElementById('resultsSection').classList.add('hidden');
}