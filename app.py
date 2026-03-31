import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração da página em modo Wide
st.set_page_config(layout="wide", page_title="Controle de Manutenção")

# 2. CSS para remover as margens padrão do Streamlit (as "abas" nos cantos)
st.markdown("""
    <style>
        /* Remove o espaço do topo e das laterais do Streamlit */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        /* Remove o header padrão do Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    # Seu HTML original com um ajuste no body para não ter margem
    html_puro = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <style>
            :root {
                --primary: #2c3e50;
                --secondary: #34495e;
                --accent: #3498db;
                --success: #27ae60;
                --warning: #f1c40f;
                --danger: #e74c3c;
                --light: #ecf0f1;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f6;
                margin: 0; /* Garante que o conteúdo cole na borda */
                padding: 0;
                color: var(--primary);
                width: 100vw;
                height: 100vh;
            }

            header {
                background-color: var(--primary);
                color: white;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }

            nav {
                display: flex;
                justify-content: center;
                background: var(--secondary);
                padding: 10px;
            }

            nav button {
                background: none;
                border: none;
                color: white;
                padding: 10px 20px;
                cursor: pointer;
                font-weight: bold;
            }

            nav button:hover {
                background: var(--accent);
                border-radius: 5px;
            }

            .container {
                max-width: 95%; /* Aumentado para ocupar mais espaço lateral */
                margin: 10px auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }

            .tab-content { display: none; }
            .active { display: block; }

            .form-group {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 10px;
                margin-bottom: 20px;
            }

            input, select, button.add-btn { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button.add-btn { background-color: var(--success); color: white; cursor: pointer; border: none; font-weight: bold; }

            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th, td { text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }
            th { background-color: var(--light); }

            .status-badge { padding: 4px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
            .pending { background: var(--warning); }
            .btn-finish { background: var(--accent); color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; }
        </style>
    </head>
    <body>

    <header>
        <h2 style="margin:0;">Controle de Manutenção de Fábrica</h2>
    </header>

    <nav>
        <button onclick="showTab('execucao')">Atendimento Atual</button>
        <button onclick="showTab('planejamento')">Máquinas a Planejar</button>
        <button onclick="showTab('historico')">Histórico Diário</button>
    </nav>

    <div class="container">
        <div id="execucao" class="tab-content active">
            <div class="form-group">
                <input type="text" id="exec-maquina" placeholder="Máquina">
                <input type="text" id="exec-falha" placeholder="Falha">
                <select id="exec-tecnico">
                    <option value="">Manutentor...</option>
                    <option>Lucas</option><option>Carlos Eduardo</option><option>Santana</option>
                    <option>Chico</option><option>Tadeu</option><option>Picolli</option>
                    <option>Kleber</option><option>Daniel</option><option>Cleber</option>
                    <option>Robson</option><option>Michael</option><option>Alisson</option>
                </select>
                <button class="add-btn" onclick="adicionarAtendimento()">Iniciar</button>
            </div>
            <table id="tabela-execucao">
                <thead><tr><th>Máquina</th><th>Falha</th><th>Técnico</th><th>Status</th><th>Ação</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>

        <div id="planejamento" class="tab-content">
            <div class="form-group">
                <input type="text" id="plan-maquina" placeholder="Máquina">
                <input type="text" id="plan-falha" placeholder="Obs">
                <button class="add-btn" onclick="adicionarPlanejamento()">Planejar</button>
            </div>
            <table id="tabela-planejamento">
                <thead><tr><th>Máquina</th><th>Obs</th><th>Ação</th></tr></thead>
                <tbody></tbody>
            </table>
        </div>

        <div id="historico" class="tab-content">
            <table id="tabela-historico">
                <thead><tr><th>Data/Hora</th><th>Máquina</th><th>Técnico</th><th>Falha</th></tr></thead>
                <tbody></tbody>
            </table>
            <button onclick="limparHistorico()" style="margin-top:20px; background:var(--danger); color:white; border:none; padding:8px; cursor:pointer; border-radius:4px;">Limpar Tudo</button>
        </div>
    </div>

    <script>
        let atendimentos = JSON.parse(localStorage.getItem('atendimentos')) || [];
        let planejamento = JSON.parse(localStorage.getItem('planejamento')) || [];
        let historico = JSON.parse(localStorage.getItem('historico')) || [];

        function showTab(id) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            renderizar();
        }

        function adicionarAtendimento() {
            const maq = document.getElementById('exec-maquina').value;
            const falha = document.getElementById('exec-falha').value;
            const tec = document.getElementById('exec-tecnico').value;
            if(!maq || !tec) return;
            atendimentos.push({ id: Date.now(), maq, falha, tec });
            document.getElementById('exec-maquina').value = ''; 
            document.getElementById('exec-falha').value = '';
            salvar();
        }

        function adicionarPlanejamento() {
            const maq = document.getElementById('plan-maquina').value;
            const falha = document.getElementById('plan-falha').value;
            if(!maq) return;
            planejamento.push({ id: Date.now(), maq, falha });
            document.getElementById('plan-maquina').value = '';
            document.getElementById('plan-falha').value = '';
            salvar();
        }

        function finalizar(id) {
            const index = atendimentos.findIndex(a => a.id === id);
            const item = atendimentos.splice(index, 1)[0];
            historico.unshift({ ...item, dataFim: new Date().toLocaleString('pt-BR') });
            salvar();
        }

        function removerPlan(id) {
            planejamento = planejamento.filter(p => p.id !== id);
            salvar();
        }

        function salvar() {
            localStorage.setItem('atendimentos', JSON.stringify(atendimentos));
            localStorage.setItem('planejamento', JSON.stringify(planejamento));
            localStorage.setItem('historico', JSON.stringify(historico));
            renderizar();
        }

        function limparHistorico() { if(confirm("Apagar tudo?")) { historico = []; atendimentos=[]; planejamento=[]; salvar(); } }

        function renderizar() {
            document.querySelector('#tabela-execucao tbody').innerHTML = atendimentos.map(a => `
                <tr><td>${a.maq}</td><td>${a.falha}</td><td><b>${a.tec}</b></td>
                <td><span class="status-badge pending">EM CURSO</span></td>
                <td><button class="btn-finish" onclick="finalizar(${a.id})">OK</button></td></tr>
            `).join('');

            document.querySelector('#tabela-planejamento tbody').innerHTML = planejamento.map(p => `
                <tr><td>${p.maq}</td><td>${p.falha}</td>
                <td><button onclick="removerPlan(${p.id})" style="color:red; background:none; border:none; cursor:pointer;">Remover</button></td></tr>
            `).join('');

            document.querySelector('#tabela-historico tbody').innerHTML = historico.map(h => `
                <tr style="color:gray; font-size:0.9em;"><td>${h.dataFim}</td><td>${h.maq}</td><td>${h.tec}</td><td>${h.falha}</td></tr>
            `).join('');
        }
        renderizar();
    </script>
    </body>
    </html>
    """

    # O segredo está aqui: height=1000 e usar o CSS acima para zerar o padding do Streamlit
    components.html(html_puro, height=1000, scrolling=True)

if __name__ == "__main__":
    main()
