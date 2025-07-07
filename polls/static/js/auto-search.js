document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const suggestionsBox = document.getElementById('suggestions');

    // Lista de títulos (isso será preenchido pelo template)
    const livrosLista = JSON.parse(document.getElementById('livros-data').textContent);

    searchInput.addEventListener('input', function () {
        const input = this.value.toLowerCase();
        suggestionsBox.innerHTML = ''; // Limpa as sugestões

        if (input === '') {
            suggestionsBox.style.display = 'none';
            return;
        }

        const suggestions = livrosLista.filter(livro =>
            livro.toLowerCase().includes(input)
        );

        if (suggestions.length > 0) {
            const ul = document.createElement('ul');
            suggestions.forEach(sugestao => {
                const li = document.createElement('li');
                li.textContent = sugestao;
                li.addEventListener('click', () => {
                    searchInput.value = sugestao;
                    suggestionsBox.innerHTML = '';
                    suggestionsBox.style.display = 'none';
                });
                ul.appendChild(li);
            });
            suggestionsBox.appendChild(ul);
            suggestionsBox.style.display = 'block';
        } else {
            suggestionsBox.style.display = 'none';
        }
    });

    // Ocultar sugestões ao clicar fora
    document.addEventListener('click', (e) => {
        if (!suggestionsBox.contains(e.target) && e.target !== searchInput) {
            suggestionsBox.style.display = 'none';
        }
    });
});