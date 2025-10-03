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

// Mostrar tabla de productos
function displayProductsTable(products) {
    const tableBody = document.getElementById('productsTableBody');
    
    // Ordenar productos por precio (ascendente)
    const sortedProducts = [...products].sort((a, b) => a.precio - b.precio);
    
    tableBody.innerHTML = sortedProducts.map(product => {
        const badgeClass = getBadgeClass(product.recomendacion);
        const starsHTML = getStarsHTML(product.reviews);
        
        return `
            <tr class="border-b hover:bg-gray-50 transition">
                <td class="px-6 py-4">
                    <span class="font-semibold text-gray-800">${product.tienda}</span>
                </td>
                <td class="px-6 py-4">
                    <p class="font-medium text-gray-900">${product.nombre_normalizado}</p>
                    <p class="text-xs text-gray-500 mt-1">${product.nombre_crudo}</p>
                </td>
                <td class="px-6 py-4 text-center">
                    <span class="text-2xl font-bold text-indigo-600">$${product.precio.toFixed(2)}</span>
                </td>
                <td class="px-6 py-4 text-center">
                    <div class="flex items-center justify-center space-x-1">
                        ${starsHTML}
                        <span class="text-sm text-gray-600 ml-2">${product.reviews.toFixed(1)}</span>
                    </div>
                </td>
                <td class="px-6 py-4 text-center">
                    <span class="px-3 py-1 rounded-full text-xs font-semibold ${badgeClass}">
                        ${product.recomendacion}
                    </span>
                    <p class="text-xs text-gray-600 mt-2">${product.razon || ''}</p>
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