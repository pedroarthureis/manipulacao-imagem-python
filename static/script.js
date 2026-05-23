document.addEventListener('DOMContentLoaded', () => {
    const modBtns = document.querySelectorAll('.mod-btn');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const runBtn = document.getElementById('run-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const resultsArea = document.getElementById('results-area');
    const resultsGrid = document.getElementById('results-grid');
    const paramsArea = document.getElementById('params-area');
    const paramsContent = document.getElementById('params-content');

    let currentModule = '1';
    let selectedFile = null;

    const moduleParams = {
        '1': `
            <label style="color:var(--text-muted)">Escala (%)
                <input type="number" id="param_scale" value="0.5" step="0.1" style="width:100%; padding:0.5rem; margin-top:0.5rem; background:rgba(0,0,0,0.2); border:1px solid var(--glass-border); color:white; border-radius:4px;">
            </label>
            <label style="color:var(--text-muted)">Thumb Size (px)
                <input type="number" id="param_thumb_size" value="128" step="1" style="width:100%; padding:0.5rem; margin-top:0.5rem; background:rgba(0,0,0,0.2); border:1px solid var(--glass-border); color:white; border-radius:4px;">
            </label>
        `,
        '2': `
            <label style="color:var(--text-muted)">Ângulo de Rotação (Graus)
                <input type="number" id="param_angle" value="45" step="1" style="width:100%; padding:0.5rem; margin-top:0.5rem; background:rgba(0,0,0,0.2); border:1px solid var(--glass-border); color:white; border-radius:4px;">
            </label>
        `,
        '3': `
            <label style="color:var(--text-muted)">Contraste (Ex: 1.3)
                <input type="number" id="param_contrast" value="1.3" step="0.1" style="width:100%; padding:0.5rem; margin-top:0.5rem; background:rgba(0,0,0,0.2); border:1px solid var(--glass-border); color:white; border-radius:4px;">
            </label>
            <label style="color:var(--text-muted)">Temperatura (Graus RGB)
                <input type="number" id="param_temperature" value="30" step="1" style="width:100%; padding:0.5rem; margin-top:0.5rem; background:rgba(0,0,0,0.2); border:1px solid var(--glass-border); color:white; border-radius:4px;">
            </label>
        `
    };

    function renderParams(modId) {
        if (moduleParams[modId]) {
            paramsContent.innerHTML = moduleParams[modId];
            paramsArea.classList.remove('hidden');
        } else {
            paramsContent.innerHTML = '';
            paramsArea.classList.add('hidden');
        }
    }

    // Inicialização
    renderParams(currentModule);

    // Seleção de Módulos
    modBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentModule = btn.dataset.mod;
            renderParams(currentModule);
        });
    });

    // Eventos de Drag & Drop
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        selectedFile = file;
        fileNameDisplay.textContent = `Arquivo selecionado: ${file.name}`;
        fileNameDisplay.classList.add('highlight');
    }

    // Executar Módulo
    runBtn.addEventListener('click', async () => {
        // UI Loading State
        btnText.textContent = 'Processando...';
        loader.classList.remove('hidden');
        runBtn.disabled = true;
        resultsArea.classList.add('hidden');
        resultsGrid.innerHTML = '';

        const formData = new FormData();
        if (selectedFile) {
            formData.append('file', selectedFile);
        }

        // Coletar Parâmetros Dinâmicos
        const inputs = paramsContent.querySelectorAll('input, select');
        inputs.forEach(input => {
            const key = input.id.replace('param_', '');
            formData.append(key, input.value);
        });

        try {
            const response = await fetch(`/api/run/${currentModule}`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                renderResults(data);
            } else {
                alert(data.error || 'Erro desconhecido ao processar.');
            }
        } catch (error) {
            console.error(error);
            alert('Erro de conexão com o servidor.');
        } finally {
            // Restore UI
            btnText.textContent = 'Executar Módulo';
            loader.classList.add('hidden');
            runBtn.disabled = false;
        }
    });

    function renderResults(data) {
        resultsArea.classList.remove('hidden');
        
        const results = data.results;
        for (const [title, path] of Object.entries(results)) {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            // To avoid cache issues on images with same name, add timestamp
            const timestamp = new Date().getTime();
            const fileName = path.split('/').pop();
            card.innerHTML = `
                <img src="/${path}?t=${timestamp}" alt="${title}">
                <h4>${title}</h4>
                <a href="/${path}" download="${fileName}" style="display:inline-block; margin-top:0.8rem; background:var(--primary); color:white; text-decoration:none; padding:0.5rem 1rem; border-radius:4px; font-size:0.9rem; font-weight:bold; transition:all 0.3s ease;">⬇ Baixar Imagem</a>
            `;
            resultsGrid.appendChild(card);
        }

        // Caso especial para módulo 4 e 5 (mostrar badge de contagem ou ângulo)
        if (data.count !== undefined) {
            const infoCard = document.createElement('div');
            infoCard.className = 'result-card';
            infoCard.style.display = 'flex';
            infoCard.style.alignItems = 'center';
            infoCard.style.justifyContent = 'center';
            infoCard.style.padding = '2rem';
            infoCard.innerHTML = `<h3 style="color: var(--accent); font-size: 2rem;">Contagem: ${data.count}</h3>`;
            resultsGrid.prepend(infoCard);
        }

        if (data.angle !== undefined) {
            const infoCard = document.createElement('div');
            infoCard.className = 'result-card';
            infoCard.style.display = 'flex';
            infoCard.style.alignItems = 'center';
            infoCard.style.justifyContent = 'center';
            infoCard.style.padding = '2rem';
            infoCard.innerHTML = `<h3 style="color: var(--primary); font-size: 1.5rem;">Inclinação: ${data.angle}°</h3>`;
            resultsGrid.prepend(infoCard);
        }
        
        // Scroll to results
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    }
});
