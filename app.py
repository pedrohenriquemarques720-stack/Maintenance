import streamlit as st
import streamlit.components.v1 as components
import pyodbc
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="Painel HolisTech Mirror")

# --- CONFIGURAÇÃO DE CONEXÃO (Ajuste com os dados da sua planta) ---
def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=IP_DO_SERVIDOR;' # Ex: 192.168.0.100
            'DATABASE=NOME_BANCO_HOLISTECH;'
            'UID=USUARIO_DB;'
            'PWD=SENHA_DB'
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar no banco do HolisTech: {e}")
        return None

# --- BUSCA DE DADOS ---
def buscar_dados_holistech():
    conn = get_connection()
    if conn:
        # Exemplo de Query: busca OS abertas, máquina e descrição da falha
        query = """
        SELECT 
            ID_OS, 
            NOME_MAQUINA, 
            DESCRICAO_FALHA, 
            NOME_MANUTENTOR,
            STATUS
        FROM TABELA_ORDENS_SERVICO 
        WHERE STATUS = 'Aberta' OR STATUS = 'Em Andamento'
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict(orient='records')
    return []

def main():
    st.title("Gestão de Manutenção - Espelhamento HolisTech")
    
    # Busca os dados reais do banco
    dados_reais = buscar_dados_holistech()
    
    # Converte os dados do Python para JSON para o Javascript do HTML entender
    json_dados = json.dumps(dados_reais)

    # O seu HTML com um pequeno ajuste para receber os dados do banco
    html_code = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <style>
            /* (Mantenha o CSS que te enviei anteriormente aqui) */
            body {{ font-family: sans-serif; background: #f4f7f6; color: #2c3e50; }}
            .container {{ padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #2c3e50; color: white; }}
            .status-badge {{ background: #f1c40f; padding: 5px; border-radius: 4px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h3>Máquinas em Atendimento (Sincronizado com HolisTech)</h3>
            <table id="tabela-sincronizada">
                <thead>
                    <tr>
                        <th>Máquina</th>
                        <th>Falha</th>
                        <th>Manutentor</th>
                        <th>Status HolisTech</th>
                    </tr>
                </thead>
                <tbody id="corpo-tabela"></tbody>
            </table>
        </div>

        <script>
            // Recebe os dados vindo do Python/Banco de Dados
            const dadosDoBanco = {json_dados};
            
            const tbody = document.getElementById('corpo-tabela');
            
            if(dadosDoBanco.length === 0) {{
                tbody.innerHTML = "<tr><td colspan='4'>Nenhuma OS aberta encontrada no banco.</td></tr>";
            }} else {{
                tbody.innerHTML = dadosDoBanco.map(item => `
                    <tr>
                        <td>${{item.NOME_MAQUINA}}</td>
                        <td>${{item.DESCRICAO_FALHA}}</td>
                        <td><b>${{item.NOME_MANUTENTOR || 'Aguardando'}}</b></td>
                        <td><span class="status-badge">${{item.STATUS}}</span></td>
                    </tr>
                `).join('');
            }}
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=600, scrolling=True)
    
    if st.button("🔄 Atualizar Dados agora"):
        st.rerun()

if __name__ == "__main__":
    main()
