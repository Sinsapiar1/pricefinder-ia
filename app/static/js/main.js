// Variables globales
let priceChart = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', handleSearch);
});

// Función principal para manejar la búsqueda
async function handleSearch(event) {
    event.preventDefault();
    
    // Ocultar mensajes previos
    hideResults();
    hideError();
    
    // Mostrar spinner
    showLoading();
    
    // Obtener datos del formulario
    const formData = {
        gemini_api_key: document.getElementById('geminiKey').value.trim(),
        scraper_api_key: document.getElementById('scraperKey').value.trim(),
        product_name: document.getElementById('productName').value.trim()
    };
    
    try {
        // Realizar petición al backend
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (result.success) {
            displayResults(result.data);
        } else {
            showError(result.error || 'Error desconocido');
        }
        
    } catch (error) {
        hideLoading();
        showError('Error de conexión con el servidor. Verifica que el servidor esté corriendo.');
        console.error('Error:', error);
    }
}

// Mostrar resultados
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.remove('hidden');
    
    // Mostrar resumen de IA
    displayAISummary(data.summary);
    
    // Mostrar insights inteligentes (NUEVO)
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

// Mostrar tabla de productos (MEJORADA CON NUEVOS CAMPOS)
function displayProductsTable(products) {
    const tableBody = document.getElementById('productsTableBody');
    
    // Ordenar productos por recomendación y precio
    const sortedProducts = [...products].sort((a, b) => {
        const order = { '🏆 Mejor Opción': 0, '✅ Buena Alternativa': 1, '⚠️ Considerar': 2, '❌ No Recomendado': 3 };
        return (order[a.recomendacion] || 4) - (order[b.recomendacion] || 4) || a.precio - b.precio;
    });
    
    tableBody.innerHTML = sortedProducts.map(product => {
        const badgeClass = getBadgeClassNew(product.recomendacion);
        const condicionBadge = getCondicionBadge(product.condicion || 'Desconocido');
        const valorBar = getValorBar(product.valor_score || 50);
        const precioVsPromedio = product.precio_vs_promedio || '0%';
        const precioVsClass = precioVsPromedio.startsWith('-') ? 'text-green-600' : 'text-red-600';
        const categoriaIcon = getCategoriaIcon(product.categoria || 'Diferente');
        
        // Tooltip con especificaciones
        const especsTooltip = (product.especificaciones_detectadas && product.especificaciones_detectadas.length > 0)
            ? product.especificaciones_detectadas.join(', ')
            : 'N/A';
        
        return `
            <tr class="border-b hover:bg-gray-50 transition">
                <td class="px-6 py-4">
                    <span class="font-semibold text-gray-800">${product.tienda}</span>
                </td>
                <td class="px-6 py-4">
                    <div class="flex items-start">
                        <span class="text-xl mr-2" title="${product.categoria}">${categoriaIcon}</span>
                        <div>
                            <p class="font-medium text-gray-900">${product.nombre_normalizado || product.nombre_crudo}</p>
                            <p class="text-xs text-gray-500 mt-1" title="${especsTooltip}">${product.nombre_crudo}</p>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4 text-center">
                    ${condicionBadge}
                </td>
                <td class="px-6 py-4 text-center">
                    <span class="text-2xl font-bold text-indigo-600">$${product.precio.toFixed(2)}</span>
                </td>
                <td class="px-6 py-4 text-center">
                    <span class="font-semibold ${precioVsClass}">${precioVsPromedio}</span>
                </td>
                <td class="px-6 py-4 text-center">
                    ${valorBar}
                </td>
                <td class="px-6 py-4 text-center">
                    <span class="px-3 py-1 rounded-full text-xs font-semibold ${badgeClass} block mb-2">
                        ${product.recomendacion}
                    </span>
                    <p class="text-xs text-gray-600">${product.razon || ''}</p>
                </td>
                <td class="px-6 py-4 text-center">
                    <a href="${product.url}" target="_blank" 
                       class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition inline-flex items-center space-x-2">
                        <i class="fas fa-external-link-alt"></i>
                        <span>Ver Oferta</span>
                    </a>
                </td>
            </tr>
        `;
    }).join('');
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