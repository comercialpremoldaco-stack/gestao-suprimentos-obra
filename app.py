import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos - Obra", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos")
st.markdown("---")

# Inicializando o banco de dados temporário na memória
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
    st.write("Preencha os dados da obra e edite a tabela abaixo como se estivesse no Excel:")
    
    col1, col2 = st.columns(2)
    with col1:
        obra_nome = st.text_input("Nome da Obra", value="ACPA Extrusão de Alumínio Ltda")
        etapa = st.text_input("Etapa de Serviço", placeholder="Ex: Fundações, Estrutura, Instalações")
    with col2:
        solicitante = st.text_input("Responsável pela Solicitação", placeholder="Seu nome")
        data_solicitacao = st.date_input("Data", datetime.date.today())
        
    st.markdown("### 📋 Tabela de Itens (Edição Direta)")
    st.info("💡 Dica: Você pode alterar valores, adicionar novas linhas clicando no botão abaixo da tabela ou apagar linhas facilmente.")
    
    # Criando um modelo inicial de tabela para o usuário editar
    df_modelo_inicial = pd.DataFrame([
        {"Item": 1, "Quant.": 10.0, "Unid.": "barra", "Descrição Material / Serviço": "Aço CA 60 Ø 12,5mm", "Observações": "Entregar barra reta"}
    ])
    
    # Tabela interativa estilo Excel
    df_editado = st.data_editor(
        df_modelo_inicial,
        num_rows="dynamic",
        use_container_width=True,
        key="tabela_edicao_obra"
    )
    
    if st.button("Gerar Solicitação e Enviar para Suprimentos", type="primary"):
        if df_editado.empty:
            st.error("A tabela não pode estar vazia.")
        else:
            # Gerando número sequencial automático (ex: 01-26)
            proximo_num = len(st.session_state.requisicoes) + 1
            num_sequencial = f"{proximo_num:02d}-26"
            
            itens_lista = df_editado.to_dict('records')
            
            nova_req = {
                "ID": num_sequencial,
                "Obra": obra_nome,
                "Etapa": etapa,
                "Solicitante": solicitante,
                "Data": str(data_solicitacao),
                "Itens": itens_lista,
                "Status": "Aguardando Cotação",
                "Fornecedores": {}
            }
            
            st.session_state.requisicoes.append(nova_req)
            st.success(f"✅ Solicitação registrada com sucesso! Número de Controle gerado: **{num_sequencial}**")
            st.info("A planilha foi enviada automaticamente para o painel do Departamento de Suprimentos.")

# ----------------------------------------------------
# ETAPA 2: COTAÇÃO (DEPARTAMENTO DE SUPRIMENTOS)
# ----------------------------------------------------
elif menu == "2. Cotações em Andamento (Suprimentos)":
    st.header("📊 Painel de Cotações (Mínimo 3 Fornecedores)")
    st.write("O departamento de suprimentos gerencia as propostas eletrônicas.")
    
    if not st.session_state.requisicoes:
        st.warning("⚠️ Nenhuma solicitação cadastrada no momento. Vá para o menu '1. Nova Solicitação (Obra)' para criar a primeira.")
    else:
        ids_disponiveis = [req["ID"] for req in st.session_state.requisicoes]
        req_selecionada = st.selectbox("Selecione o Número da Requisição", ids_disponiveis)
        
        req_atual = next(r for r in st.session_state.requisicoes if r["ID"] == req_selecionada)
        
        st.info(f"**Obra:** {req_atual['Obra']} | **Etapa:** {req_atual['Etapa']} | **Status:** {req_atual['Status']}")
        
        st.markdown("### Itens Solicitados pela Obra:")
        df_itens_obra = pd.DataFrame(req_atual['Itens'])
        st.dataframe(df_itens_obra, use_container_width=True)
        
        st.markdown("### 🏢 Preenchimento de Propostas (3 Fornecedores)")
        
        with st.form("form_cotacao_sup"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Fornecedor 1")
                f1_nome = st.text_input("Nome F1", value="Tião")
                f1_total = st.number_input("Valor Total F1 (R$)", value=340.00, key="f1_tot")
                f1_pgto = st.text_input("Condição Pgto F1", value="Boleto 30 dias", key="f1_p")
            
            with col2:
                st.subheader("Fornecedor 2")
                f2_nome = st.text_input("Nome F2", value="Comercial Ferro")
                f2_total = st.number_input("Valor Total F2 (R$)", value=355.00, key="f2_tot")
                f2_pgto = st.text_input("Condição Pgto F2", value="Boleto 15 dias", key="f2_p")
            
            with col3:
                st.subheader("Fornecedor 3")
                f3_nome = st.text_input("Nome F3", value="Aço Forte")
                f3_total = st.number_input("Valor Total F3 (R$)", value=330.00, key="f3_tot")
                f3_pgto = st.text_input("Condição Pgto F3", value="À vista Pix", key="f3_p")
            
            salvar_cot = st.form_submit_button("Salvar Cotações e Enviar para Análise")
            
            if salvar_cot:
                req_atual["Status"] = "Aguardando Aprovação do Cliente"
                req_atual["Fornecedores"] = {
                    "F1": {"nome": f1_nome, "total": f1_total, "pgto": f1_pgto},
                    "F2": {"nome": f2_nome, "total": f2_total, "pgto": f2_pgto},
                    "F3": {"nome": f3_nome, "total": f3_total, "pgto": f3_pgto},
                }
                st.success("✅ Cotações salvas! Status atualizado para 'Aguardando Aprovação do Cliente'.")

# ----------------------------------------------------
# ETAPA 3: ORDEM DE COMPRA (OC)
# ----------------------------------------------------
elif menu == "3. Ordens de Compra (OC)":
    st.header("🛒 Emissão de Ordem de Compra (OC)")
    st.write("Gerada após a escolha e aprovação do cliente.")
    
    reqs_prontas = [r for r in st.session_state.requisicoes if r["Status"] != "Aguardando Cotação"]
    
    if not reqs_prontas:
        st.warning("⚠️ Nenhuma requisição com cotação finalizada para emitir OC.")
    else:
        ids_oc = [r["ID"] for r in reqs_prontas]
        oc_escolhida = st.selectbox("Selecione a Requisição para a OC", ids_oc)
        
        req_oc = next(r for r in st.session_state.requisicoes if r["ID"]->oc_escolhida == oc_escolhida if False else r["ID"] == oc_escolhida)
        
        st.write(f"**Requisição Selecionada:** {req_oc['ID']} - {req_oc['Obra']}")
        
        if req_oc["Fornecedores"]:
            f_dados = req_oc["Fornecedores"]
            df_comp = pd.DataFrame([
                {"Fornecedor": f_dados['F1']['nome'], "Valor Total": f_dados['F1']['total'], "Cond. Pgto": f_dados['F1']['pgto']},
                {"Fornecedor": f_dados['F2']['nome'], "Valor Total": f_dados['F2']['total'], "Cond. Pgto": f_dados['F2']['pgto']},
                {"Fornecedor": f_dados['F3']['nome'], "Valor Total": f_dados['F3']['total'], "Cond. Pgto": f_dados['F3']['pgto']},
            ])
            st.dataframe(df_comp, use_container_width=True)
            
            fornecedor_vencedor = st.selectbox("Fornecedor Aprovado pelo Cliente", [f_dados['F1']['nome'], f_dados['F2']['nome'], f_dados['F3']['nome']])
            
            if st.button("Emitir Ordem de Compra Oficial"):
                req_oc["Status"] = "OC Emitida"
                req_oc["Vencedor"] = fornecedor_vencedor
                st.success(f"🎉 Ordem de Compra emitida com sucesso para **{fornecedor_vencedor}**!")
        else:
            st.info("As cotações ainda não foram preenchidas.")
