import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos - Obra", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos")
st.markdown("---")

# Menu lateral de navegação
menu = st.sidebar.selectbox("Menu Principal", [
    "1. Nova Solicitação (Obra)", 
    "2. Cotações em Andamento (Suprimentos)", 
    "3. Ordens de Compra (OC)"
])

# ----------------------------------------------------
# ETAPA 1: SOLICITAÇÃO DE MATERIAIS E SERVIÇOS
# ----------------------------------------------------
if menu == "1. Nova Solicitação (Obra)":
    st.header("📝 Solicitação de Materiais e Serviços")
    st.write("O responsável pela obra preenche a necessidade de insumos ou serviços.")
    
    with st.form("form_solicitacao"):
        col1, col2 = st.columns(2)
        with col1:
            obra_nome = st.text_input("Nome da Obra", value="ACPA Extrusão de Alumínio Ltda")
            etapa = st.text_input("Etapa de Serviço", placeholder="Ex: Fundações, Estrutura, Alvenaria")
        with col2:
            solicitante = st.text_input("Responsável pela Solicitação", placeholder="Seu nome")
            data_solicitacao = st.date_input("Data", datetime.date.today())
            
        st.markdown("### Itens Solicitados")
        st.write("Adicione os itens que precisam ser cotados:")
        
        # Simulando uma tabela interativa simples para os itens
        # No futuro, o usuário poderá colar direto da planilha dele
        quantidade = st.number_input("Quantidade", min_value=0.0, value=10.0)
        unidade = st.text_input("Unidade (ex: barra, m², furo, vb)", value="barra")
        observacao = st.text_input("Observações / Especificação", placeholder="Ex: Entregar barra reta")
        descricao = st.text_input("Descrição do Material ou Serviço", placeholder="Ex: Aço CA 60 Ø 12,5mm")
        
        enviar = st.form_submit_button("Gerar Solicitação e Planilha de Cotação")
        
        if enviar:
            # Gerando número sequencial único (ex: 01-26)
            num_sequencial = "01-26" 
            st.success(f"✅ Solicitação registrada com sucesso! Número de Controle: **{num_sequencial}**")
            st.info("O sistema gerou a Planilha de Cotação eletrônica e enviou para o Departamento de Suprimentos.")

# ----------------------------------------------------
# ETAPA 2: COTAÇÃO (DEPARTAMENTO DE SUPRIMENTOS)
# ----------------------------------------------------
elif menu == "2. Cotações em Andamento (Suprimentos)":
    st.header("📊 Painel de Cotações (Mínimo 3 Fornecedores)")
    st.write("O departamento de suprimentos insere as propostas eletrônicas obtidas.")
    
    st.info("Requisição ativa: **01-26** | Obra: ACPA Extrusão de Alumínio Ltda")
    
    # Tabela simulando o preenchimento dos 3 fornecedores exigidos por regra
    dados_cotacao = {
        "Item": [1, 2],
        "Quant.": [10, 10],
        "Unid.": ["barra", "barra"],
        "Descrição": ["Aço CA 60 Ø 12,5mm", "Aço CA 60 Ø 10,0mm"],
        "Fornecedor A (Unit.)": [10.00, 8.00],
        "Fornecedor B (Unit.)": [10.50, 8.20],
        "Fornecedor C (Unit.)": [9.80, 7.90]
    }
    df_cot = pd.DataFrame(dados_cotacao)
    st.dataframe(df_cot, use_container_width=True)
    
    if st.button("Enviar para Análise do Solicitante e Aprovação do Cliente"):
        st.success("📤 Cotação enviada para checagem do solicitante!")

# ----------------------------------------------------
# ETAPA 3: ORDEM DE COMPRA (OC)
# ----------------------------------------------------
elif menu == "3. Ordens de Compra (OC)":
    st.header("🛒 Emissão de Ordem de Compra (OC)")
    st.write("Gerada automaticamente após a aprovação do cliente.")
    st.warning("Nenhuma OC pendente de emissão no momento. Conclua a etapa 2 para liberar.")
