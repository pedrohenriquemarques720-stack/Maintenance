import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para ocupar a tela toda (melhor para gestão de fábrica)
st.set_page_config(layout="wide", page_title="Gestão de Manutenção")

def main():
    st.title("Painel de Controle de Manutentores")
    st.write("Interface de gestão rápida para o chão de fábrica.")

    # O código HTML completo que te enviei anteriormente
    # Dica: Você pode salvar o HTML em um arquivo separado e ler aqui, 
    # mas para ser "simples" como pediu, inseri a variável abaixo:
    
    html_code = """
    <!DOCTYPE html>
    ... (copie e cole o conteúdo do HTML anterior aqui) ...
    """

    # Renderiza o HTML dentro do Streamlit
    # Ajustamos a altura (height) para garantir que a tabela apareça bem
    components.html(html_code, height=800, scrolling=True)

if __name__ == "__main__":
    main()
