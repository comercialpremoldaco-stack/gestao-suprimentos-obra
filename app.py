import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos - Obra")
st.markdown("---")

st.sidebar.header("Painel de Controle")
opcao = st.sidebar.radio("Navegação", ["Nova Solicitação (Upload)", "Status das Solicitações"])

if opcao == "Nova Solicitação (Upload)":
    st.header("Upload de Planilha de Cotação")
    st.write("Faça o upload da planilha preenchida para gerar uma nova requisição.")
    
    arquivo = st.file_uploader("Selecione o arquivo (.xls, .xlsx)", type=["xlsx", "xls"])
    
    if arquivo is not None:
        try:
            # Lendo a planilha (ignorando cabeçalhos muito complexos por enquanto)
            df = pd.read_excel(arquivo, header=None)
            
            st.success("Arquivo carregado com sucesso!")
            
            # Mostrando a planilha crua para o usuário conferir
            st.subheader("Pré-visualização dos Dados")
            st.dataframe(df.head(15))
            
            # Simulando a geração do ID
            if st.button("Aprovar e Gerar Requisição"):
                ano = datetime.datetime.now().year
                id_requisicao = f"REQ-{ano}-001" # No futuro, será sequencial do banco
                
                st.success(f"✅ Solicitação registrada com sucesso! ID: **{id_requisicao}**")
                st.info("A requisição foi enviada para a fila do departamento de suprimentos.")
                
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

elif opcao == "Status das Solicitações":
    st.header("📊 Painel de Status")
    st.write("Aqui você acompanhará o andamento de cada pedido até a entrega da Nota Fiscal.")
    
    # Criando dados fictícios por enquanto (Nosso futuro banco de dados)
    dados_falsos = {
        "ID": ["REQ-2026-001", "REQ-2026-002"],
        "Data": ["10/08/2026", "11/08/2026"],
        "Descrição Resumida": ["Aço CA 60 e 50", "Terraplanagem - Furo estaca"],
        "Status": ["Aguardando Cotação", "Aguardando Aprovação Cliente"],
        "Fornecedor Vencedor": ["-", "Land Fort"]
    }
    
    df_status = pd.DataFrame(dados_falsos)
    
    # Adicionando cores aos status (Dica visual)
    def colorir_status(val):
        color = 'orange' if val == 'Aguardando Cotação' else 'blue' if val == 'Aguardando Aprovação Cliente' else 'black'
        return f'color: {color}; font-weight: bold'

    st.dataframe(df_status.style.map(colorir_status, subset=['Status']), use_container_width=True)
