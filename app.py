import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos - Obra", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos")
st.markdown("---")

# Inicializando o "banco de dados" temporário na memória do app
if 'requisicoes' not in st.session_state:
    st.session_state.requisicoes = []

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
            etapa = st.text_input("Etapa de Serviço", placeholder="Ex: Fundações, Estrutura")
        with col2:
            solicitante = st.text_input("Responsável pela Solicitação", placeholder="Seu nome")
            data_solicitacao = st.date_input("Data", datetime.date.today())
            
        st.markdown("### Item Solicitado")
        quantidade = st.number_input("Quantidade", min_value=0.0, value=10.0)
        unidade = st.text_input("Unidade (ex: barra, m², furo, vb)", value="barra")
        descricao = st.text_input("Descrição do Material ou Serviço", placeholder="Ex: Aço CA 60 Ø 12,5mm")
        observacao = st.text_input("Observações / Especificação", placeholder="Ex: Entregar barra reta")
        
        enviar = st.form_submit_button("Gerar Solicitação e Planilha de Cotação")
        
        if enviar:
            # Gerando número sequencial automático (ex: 01-26, 02-26)
            proximo_num = len(st.session_state.requisicoes) + 1
            num_sequencial = f"{proximo_num:02d}-26"
            
            nova_req = {
                "ID": num_sequencial,
                "Obra": obra_nome,
                "Etapa": etapa,
                "Solicitante": solicitante,
                "Data": str(data_solicitacao),
                "Quantidade": quantidade,
                "Unidade": unidade,
                "Descricao": descricao,
                "Observacao": observacao,
                "Status": "Aguardando Cotação",
                "Fornecedores": {}
            }
            
            st.session_state.requisicoes.append(nova_req)
            st.success(f"✅ Solicitação registrada com sucesso! Número de Controle: **{num_sequencial}**")
            st.info("A requisição foi enviada de forma integrada para o painel do Departamento de Suprimentos.")

# ----------------------------------------------------
# ETAPA 2: COTAÇÃO (DEPARTAMENTO DE SUPRIMENTOS)
# ----------------------------------------------------
elif menu == "2. Cotações em Andamento (Suprimentos)":
    st.header("📊 Painel de Cotações (Mínimo 3 Fornecedores)")
    st.write("O departamento de suprimentos gerencia e preenche as propostas eletrônicas.")
    
    if not st.session_state.requisicoes:
        st.warning("⚠️ Nenhuma solicitação cadastrada no momento. Vá para o menu '1. Nova Solicitação (Obra)' para criar a primeira.")
    else:
        # Selecionar qual requisição cotar
        ids_disponiveis = [req["ID"] for req in st.session_state.requisicoes]
        req_selecionada = st.selectbox("Selecione o Número da Requisição", ids_disponiveis)
        
        # Buscar dados da requisição escolhida
        req_atual = next(r for r in st.session_state.requisicoes if r["ID"] == req_selecionada)
        
        st.info(f"**Obra:** {req_atual['Obra']} | **Item:** {req_atual['Descricao']} | **Qtd:** {req_atual['Quantidade']} {req_atual['Unidade']} | **Status:** {req_atual['Status']}")
        
        st.markdown("### Preenchimento Eletrônico das Propostas (3 Fornecedores Obrigatórios)")
        
        with st.form("form_cotacao_sup"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Fornecedor 1")
                f1_nome = st.text_input("Nome F1", value="Tião")
                f1_unit = st.number_input("Valor Unitário F1", value=10.00, key="f1_u")
                f1_pgto = st.text_input("Condição Pgto F1", value="Boleto 30 dias", key="f1_p")
            
            with col2:
                st.subheader("Fornecedor 2")
                f2_nome = st.text_input("Nome F2", value="Comercial Ferro")
                f2_unit = st.number_input("Valor Unitário F2", value=10.50, key="f2_u")
                f2_pgto = st.text_input("Condição Pgto F2", value="Boleto 15 dias", key="f2_p")
            
            with col3:
                st.subheader("Fornecedor 3")
                f3_nome = st.text_input("Nome F3", value="Aço Forte")
                f3_unit = st.number_input("Valor Unitário F3", value=9.80, key="f3_u")
                f3_pgto = st.text_input("Condição Pgto F3", value="À vista Pix", key="f3_p")
            
            salvar_cot = st.form_submit_button("Salvar Cotações e Enviar para Análise")
            
            if salvar_cot:
                req_atual["Status"] = "Aguardando Aprovação do Cliente"
                req_atual["Fornecedores"] = {
                    "F1": {"nome": f1_nome, "unit": f1_unit, "total": f1_unit * req_atual['Quantidade'], "pgto": f1_pgto},
                    "F2": {"nome": f2_nome, "unit": f2_unit, "total": f2_unit * req_atual['Quantidade'], "pgto": f2_pgto},
                    "F3": {"nome": f3_nome, "unit": f3_unit, "total": f3_unit * req_atual['Quantidade'], "pgto": f3_pgto},
                }
                st.success("✅ Cotações salvas com sucesso! Status alterado para 'Aguardando Aprovação do Cliente'.")

# ----------------------------------------------------
# ETAPA 3: ORDEM DE COMPRA (OC)
# ----------------------------------------------------
elif menu == "3. Ordens de Compra (OC)":
    st.header("🛒 Emissão de Ordem de Compra (OC)")
    st.write("Gerada automaticamente após a escolha e aprovação do cliente.")
    
    reqs_prontas = [r for r in st.session_state.requisicoes if r["Status"] != "Aguardando Cotação"]
    
    if not reqs_prontas:
        st.warning("⚠️ Nenhuma requisição com cotação finalizada para emitir OC.")
    else:
        ids_oc = [r["ID"] for r in reqs_prontas]
        oc_escolhida = st.selectbox("Selecione a Requisição para Emitir a OC", ids_oc)
        
        req_oc = next(r for r in st.session_state.requisicoes if r["ID"] == oc_escolhida)
        
        st.write(f"**Detalhes da Compra - Requisição: {req_oc['ID']}**")
        st.write(f"Item: {req_oc['Descricao']} | Quantidade: {req_oc['Quantidade']} {req_oc['Unidade']}")
        
        if req_oc["Fornecedores"]:
            f_dados = req_oc["Fornecedores"]
            df_comp = pd.DataFrame([
                {"Fornecedor": f_dados['F1']['nome'], "Valor Unit.": f_dados['F1']['unit'], "Total": f_dados['F1']['total'], "Cond. Pgto": f_dados['F1']['pgto']},
                {"Fornecedor": f_dados['F2']['nome'], "Valor Unit.": f_dados['F2']['unit'], "Total": f_dados['F2']['total'], "Cond. Pgto": f_dados['F2']['pgto']},
                {"Fornecedor": f_dados['F3']['nome'], "Valor Unit.": f_dados['F3']['unit'], "Total": f_dados['F3']['total'], "Cond. Pgto": f_dados['F3']['pgto']},
            ])
            st.dataframe(df_comp, use_container_width=True)
            
            fornecedor_vencedor = st.selectbox("Fornecedor Aprovado pelo Cliente", [f_dados['F1']['nome'], f_dados['F2']['nome'], f_dados['F3']['nome']])
            
            if st.button("Emitir Ordem de Compra (OC Oficial)"):
                req_oc["Status"] = "OC Emitida"
                req_oc["Vencedor"] = fornecedor_vencedor
                st.success(f"🎉 Ordem de Compra emitida com sucesso para **{fornecedor_vencedor}**! Pronta para envio ao fornecedor e à obra.")
        else:
            st.info("As cotações para esta requisição ainda não foram preenchidas pelo departamento de suprimentos.")
