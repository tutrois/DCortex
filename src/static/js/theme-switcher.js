/**
 * DCortex Amazon Dashboard - Theme Switcher
 * Script para gerenciar a alternância de temas
 */

// Verifica o tema salvo no localStorage ou usa o tema padrão (light)
const savedTheme = localStorage.getItem('theme') || 'light';

// Aplica o tema imediatamente para evitar flash de tema incorreto
document.documentElement.setAttribute('data-bs-theme', savedTheme);
document.body.setAttribute('data-bs-theme', savedTheme);

// Adiciona ou remove a classe dark-theme do body
if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
} else {
    document.body.classList.remove('dark-theme');
}

// Função para atualizar o ícone do botão de tema
function updateThemeIconOnLoad() {
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (savedTheme === 'dark') {
            themeIcon.classList.remove('bi-sun-fill');
            themeIcon.classList.add('bi-moon-fill');
        } else {
            themeIcon.classList.remove('bi-moon-fill');
            themeIcon.classList.add('bi-sun-fill');
        }
    }
}

// Executa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', updateThemeIconOnLoad);
