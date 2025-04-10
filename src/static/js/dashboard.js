/**
 * DCortex Amazon Dashboard
 * Script principal para o dashboard de análise de produtos da Amazon
 * Autor: Arthur Ramos
 * Versão: 1.0.0
 */

// Variáveis globais
let progress = 0;
let currentTheme = localStorage.getItem('theme') || 'light';
let progressBar, loadingStatus, mainContent, loadingOverlay, errorMessage, errorText, productCount;

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa as referências aos elementos do DOM
    initDOMReferences();

    // Aplica o tema salvo
    applyTheme(currentTheme);

    // Adiciona listener para mudança de tema
    document.querySelector('.theme-toggle').addEventListener('click', toggleTheme);

    // Inicia a busca de dados
    fetchData();
});

/**
 * Inicializa as referências aos elementos do DOM
 */
function initDOMReferences() {
    progressBar = document.querySelector('.progress-bar');
    loadingStatus = document.getElementById('loading-status');
    mainContent = document.getElementById('main-content');
    loadingOverlay = document.getElementById('loading-overlay');
    errorMessage = document.getElementById('error-message');
    errorText = document.getElementById('error-text');
    productCount = document.getElementById('product-count');
}

/**
 * Aplica o tema especificado ao documento
 * @param {string} theme - O tema a ser aplicado ('light' ou 'dark')
 */
function applyTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    updateThemeIcon(theme);
}

/**
 * Alterna entre os temas claro e escuro
 */
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(currentTheme);
    localStorage.setItem('theme', currentTheme);
}

/**
 * Atualiza o ícone do botão de tema
 * @param {string} theme - O tema atual ('light' ou 'dark')
 */
function updateThemeIcon(theme = currentTheme) {
    const themeIcon = document.getElementById('theme-icon');
    if (theme === 'dark') {
        themeIcon.classList.remove('bi-sun-fill');
        themeIcon.classList.add('bi-moon-fill');
    } else {
        themeIcon.classList.remove('bi-moon-fill');
        themeIcon.classList.add('bi-sun-fill');
    }
}

/**
 * Atualiza a barra de progresso durante o carregamento
 */
function updateProgress() {
    if (progress < 95) {
        progress += Math.random() * 3;
        progressBar.style.width = `${progress}%`;

        // Atualiza o texto de status com mensagens mais detalhadas
        if (progress < 20) {
            loadingStatus.textContent = "Conectando ao serviço de dados...";
        } else if (progress < 40) {
            loadingStatus.textContent = "Coletando informações da Amazon...";
        } else if (progress < 60) {
            loadingStatus.textContent = "Processando dados com ColetorDadosAmazon...";
        } else if (progress < 80) {
            loadingStatus.textContent = "Analisando preços e avaliações...";
        } else {
            loadingStatus.textContent = "Preparando visualização...";
        }
    }
}

/**
 * Exibe mensagem de erro
 * @param {string} message - Mensagem de erro a ser exibida
 */
function showError(message) {
    loadingOverlay.style.display = 'none';
    mainContent.style.display = 'none';
    errorMessage.style.display = 'block';
    errorText.textContent = message;
}

/**
 * Formata um valor numérico como preço em reais
 * @param {number} price - Valor a ser formatado
 * @returns {string} - Valor formatado como preço
 */
function formatPrice(price) {
    // Verifica se o preço é um número válido
    if (price === undefined || price === null || isNaN(price)) {
        console.error('Preço inválido:', price);
        return 'R$ --';
    }
    return `R$ ${Number(price).toFixed(2)}`;
}

/**
 * Renderiza os cards de estatísticas
 * @param {Object} dados - Dados estatísticos para renderização
 */
function renderStatsCards(dados) {
    // Verifica se os dados estão presentes e são válidos
    if (!dados || typeof dados !== 'object') {
        console.error('Dados inválidos para renderStatsCards:', dados);
        return;
    }

    // Registra no console para debug
    console.log('Dados do gráfico:', dados);

    const media = dados.media !== undefined ? dados.media : 0;
    const minimo = dados.minimo !== undefined ? dados.minimo : 0;
    const maximo = dados.maximo !== undefined ? dados.maximo : 0;

    const statsCards = document.getElementById('stats-cards');
    statsCards.innerHTML = `
        <div class="col-md-4 fade-in delay-1">
            <div class="card stats-card">
                <div class="stats-icon">
                    <i class="bi bi-calculator"></i>
                </div>
                <h5 class="card-title">Preço Médio</h5>
                <div class="stats-value">
                    ${formatPrice(media)}
                </div>
                <div class="stats-label">Média dos preços dos produtos</div>
            </div>
        </div>
        <div class="col-md-4 fade-in delay-2">
            <div class="card stats-card success">
                <div class="stats-icon">
                    <i class="bi bi-graph-down-arrow"></i>
                </div>
                <h5 class="card-title">Preço Mais Baixo</h5>
                <div class="stats-value">
                    ${formatPrice(minimo)}
                </div>
                <div class="stats-label">Produto mais acessível</div>
            </div>
        </div>
        <div class="col-md-4 fade-in delay-3">
            <div class="card stats-card danger">
                <div class="stats-icon">
                    <i class="bi bi-graph-up-arrow"></i>
                </div>
                <h5 class="card-title">Preço Mais Alto</h5>
                <div class="stats-value">
                    ${formatPrice(maximo)}
                </div>
                <div class="stats-label">Produto mais caro</div>
            </div>
        </div>
    `;
}

/**
 * Renderiza a lista de produtos
 * @param {Array} produtos - Array de produtos para renderização
 */
function renderProducts(produtos) {
    const productsList = document.getElementById('products-list');

    // Atualiza o contador de produtos
    productCount.textContent = `${produtos.length} produtos`;
    console.log('Produtos recebidos:', produtos);

    productsList.innerHTML = produtos.map((produto, index) => {
        // Verifica e usa os campos corretos com fallbacks
        // Prioriza o formato do agente, mas suporta também o formato da API
        const nome = produto.titulo || produto.name || produto.nome || produto.título || 'Sem nome';
        const imagem = produto.imagem || produto.image_url || '';
        const url = produto.url_produto || produto.url || '#';
        const preco = produto.preco || produto.price || produto.preço || 0;
        const avaliacao = produto.rating || produto.avaliacao || produto.avaliação || 0;
        const posicao = produto.posição || produto.position || produto.posicao || index + 1;

        // Gera estrelas baseadas na avaliação
        const starsHtml = generateStars(avaliacao);

        // Adiciona animação com delay baseado no índice
        const delay = Math.min(index, 10) * 0.1;

        return `
        <div class="col-md-4 col-lg-3 fade-in" style="animation-delay: ${delay}s">
            <a href="${url}" target="_blank" class="card h-100">
                <div class="position-relative">
                    <img src="${imagem}" class="card-img-top product-image" alt="${nome}">
                    <span class="position-absolute top-0 start-0 badge bg-primary m-2">#${posicao}</span>
                </div>
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${nome}</h5>
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="rating">${starsHtml} ${avaliacao}</span>
                        </div>
                        <span class="price">${formatPrice(preco)}</span>
                    </div>
                </div>
            </a>
        </div>
        `;
    }).join('');
}

/**
 * Gera HTML para exibição de estrelas baseadas na avaliação
 * @param {number} rating - Valor da avaliação (0-5)
 * @returns {string} - HTML com as estrelas
 */
function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    let starsHtml = '';

    // Estrelas cheias
    for (let i = 0; i < fullStars; i++) {
        starsHtml += '<i class="bi bi-star-fill text-warning"></i>';
    }

    // Meia estrela
    if (halfStar) {
        starsHtml += '<i class="bi bi-star-half text-warning"></i>';
    }

    // Estrelas vazias
    for (let i = 0; i < emptyStars; i++) {
        starsHtml += '<i class="bi bi-star text-warning"></i>';
    }

    return starsHtml;
}

/**
 * Renderiza o gráfico de preços
 * @param {Object} dados - Dados para o gráfico
 */
function renderChart(dados) {
    // Verifica se os dados estão presentes e são válidos
    if (!dados || typeof dados !== 'object') {
        console.error('Dados inválidos para renderChart:', dados);
        return;
    }

    // Garante que os arrays existam
    const labels = Array.isArray(dados.labels) ? dados.labels : [];
    const precos = Array.isArray(dados.precos) ? dados.precos : [];

    // Filtra valores inválidos
    const validPrecos = precos.map(p => isNaN(p) ? 0 : Number(p));

    // Cores para o gráfico baseadas no tema atual
    const isDarkMode = document.documentElement.getAttribute('data-bs-theme') === 'dark';
    const gradientColors = isDarkMode ?
        ['rgba(76, 201, 240, 0.8)', 'rgba(72, 149, 239, 0.8)'] :
        ['rgba(67, 97, 238, 0.8)', 'rgba(58, 12, 163, 0.8)'];

    // Configuração do gráfico
    const ctx = document.getElementById('precoChart').getContext('2d');

    // Cria um gradiente
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, gradientColors[0]);
    gradient.addColorStop(1, gradientColors[1]);

    // Registra o plugin de datalabels
    Chart.register(ChartDataLabels);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Preço (R$)',
                data: validPrecos,
                backgroundColor: gradient,
                borderColor: 'transparent',
                borderRadius: 8,
                borderWidth: 0,
                hoverBackgroundColor: gradientColors[0],
                barPercentage: 0.7,
                categoryPercentage: 0.8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return 'R$ ' + value;
                        },
                        color: isDarkMode ? '#adb5bd' : '#6c757d'
                    },
                    title: {
                        display: true,
                        text: 'Preço (R$)',
                        color: isDarkMode ? '#f8f9fa' : '#2b2d42',
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: isDarkMode ? '#adb5bd' : '#6c757d'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: isDarkMode ? '#343a40' : 'rgba(255, 255, 255, 0.9)',
                    titleColor: isDarkMode ? '#f8f9fa' : '#2b2d42',
                    bodyColor: isDarkMode ? '#f8f9fa' : '#2b2d42',
                    borderColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                    borderWidth: 1,
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return formatPrice(context.raw);
                        }
                    }
                },
                datalabels: {
                    color: isDarkMode ? '#f8f9fa' : '#ffffff',
                    anchor: 'end',
                    align: 'top',
                    formatter: function(value) {
                        return formatPrice(value);
                    },
                    font: {
                        weight: 'bold',
                        size: 11
                    },
                    textShadow: '0 1px 2px rgba(0, 0, 0, 0.4)',
                    display: function(context) {
                        return context.dataIndex < 5; // Mostra apenas para os 5 primeiros itens
                    }
                }
            }
        }
    });
}

/**
 * Busca os dados da API
 * @returns {Promise<void>}
 */
async function fetchData() {
    // Reset UI
    resetUI();

    // Inicia a animação de carregamento
    const progressInterval = setInterval(updateProgress, 1000);

    try {
        // Busca os dados da API
        const data = await fetchDataFromAPI();

        if (data.success) {
            // Completa o progresso
            completeProgress();

            // Renderiza os dados
            renderData(data);

            // Mostra o conteúdo com animação
            showContent(progressInterval);
        } else {
            throw new Error(data.error || 'Erro ao carregar dados');
        }
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        clearInterval(progressInterval);
        showError(error.message);
    }
}

/**
 * Reseta a interface do usuário para o estado inicial de carregamento
 */
function resetUI() {
    progress = 0;
    progressBar.style.width = '0%';
    loadingOverlay.style.display = 'flex';
    loadingOverlay.style.opacity = '1';
    mainContent.style.display = 'none';
    errorMessage.style.display = 'none';
}

/**
 * Busca os dados da API
 * @returns {Promise<Object>} Dados da API
 */
async function fetchDataFromAPI() {
    console.log('Iniciando busca de dados...');
    const response = await fetch('/fetch-data');
    console.log('Resposta recebida:', response.status);

    const data = await response.json();
    console.log('Dados recebidos:', data);
    return data;
}

/**
 * Completa a barra de progresso
 */
function completeProgress() {
    progress = 100;
    progressBar.style.width = '100%';
}

/**
 * Renderiza todos os dados na interface
 * @param {Object} data - Dados a serem renderizados
 */
function renderData(data) {
    console.log('Dados recebidos:', data);

    // Verifica se os dados estão no formato esperado ou no formato do agente
    if (data.produtos && data.dados_grafico) {
        // Formato padrão da API
        console.log('Usando formato padrão da API');
        renderStatsCards(data.dados_grafico);
        renderProducts(data.produtos);
        renderChart(data.dados_grafico);
    } else if (Array.isArray(data)) {
        // Formato do agente (array de produtos)
        console.log('Usando formato do agente (array)');

        // Cria dados para o gráfico a partir dos produtos
        const dadosGrafico = processarDadosGrafico(data);

        renderStatsCards(dadosGrafico);
        renderProducts(data);
        renderChart(dadosGrafico);
    } else if (data.success && Array.isArray(data.data)) {
        // Outro formato possível (objeto com array em data)
        console.log('Usando formato alternativo (data array)');

        const dadosGrafico = processarDadosGrafico(data.data);

        renderStatsCards(dadosGrafico);
        renderProducts(data.data);
        renderChart(dadosGrafico);
    } else {
        console.error('Formato de dados desconhecido:', data);
        throw new Error('Formato de dados não reconhecido');
    }
}

/**
 * Processa os dados dos produtos para criar dados para o gráfico
 * @param {Array} produtos - Array de produtos
 * @returns {Object} Objeto com dados para o gráfico
 */
function processarDadosGrafico(produtos) {
    // Verifica se temos produtos
    if (!produtos || !produtos.length) {
        return {
            labels: [],
            precos: [],
            media: 0,
            minimo: 0,
            maximo: 0
        };
    }

    // Extrai os preços dos produtos
    const precos = produtos.map(p => {
        // Suporta diferentes formatos de preço
        const preco = p.preco || p.price || p.preço || 0;
        return typeof preco === 'string' ? parseFloat(preco.replace(/[^0-9.,]/g, '').replace(',', '.')) : preco;
    }).filter(p => !isNaN(p) && p > 0);

    // Calcula estatísticas
    const media = precos.length ? precos.reduce((a, b) => a + b, 0) / precos.length : 0;
    const minimo = precos.length ? Math.min(...precos) : 0;
    const maximo = precos.length ? Math.max(...precos) : 0;

    // Cria labels para o gráfico (até 10 produtos)
    const produtosParaGrafico = produtos.slice(0, 10);
    const labels = produtosParaGrafico.map(p => {
        const nome = p.titulo || p.name || p.nome || p.título || 'Produto';
        // Limita o tamanho do nome para o gráfico
        return nome.length > 20 ? nome.substring(0, 17) + '...' : nome;
    });

    // Extrai os preços para o gráfico
    const precosGrafico = produtosParaGrafico.map(p => {
        const preco = p.preco || p.price || p.preço || 0;
        return typeof preco === 'string' ? parseFloat(preco.replace(/[^0-9.,]/g, '').replace(',', '.')) : preco;
    });

    return {
        labels: labels,
        precos: precosGrafico,
        media: media,
        minimo: minimo,
        maximo: maximo
    };
}

/**
 * Mostra o conteúdo principal com animação
 * @param {number} progressInterval - ID do intervalo de progresso para limpar
 */
function showContent(progressInterval) {
    setTimeout(() => {
        loadingOverlay.style.opacity = '0';
        setTimeout(() => {
            loadingOverlay.style.display = 'none';
            mainContent.style.display = 'block';
            clearInterval(progressInterval);
        }, 500);
    }, 500);
}

/**
 * Alterna a visibilidade da barra lateral
 */
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');

    // Ajusta o botão do menu
    const menuToggle = document.querySelector('.menu-toggle');
    if (document.querySelector('.sidebar').classList.contains('active')) {
        menuToggle.innerHTML = '<i class="bi bi-x-lg" style="font-size: 1.5rem;"></i>';
    } else {
        menuToggle.innerHTML = '<i class="bi bi-list" style="font-size: 1.5rem;"></i>';
    }
}
