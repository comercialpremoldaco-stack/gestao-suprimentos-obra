import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos - Obra", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos e Obras")
st.markdown("---")

# Inicializando o banco de dados temporário na memória
if 'requisicoes' not in st.session_state:
    st.session_state.requisicoes = []

# Menu lateral de navegação expandido
menu = st.sidebar.selectbox("Menu Principal", [
    "1. Nova Solicitação (Obra)", 
    "2. Cotações (Suprimentos)", 
    "3. Ordens de Compra (OC)",
    "4. Recebimento e Conferência (Obra)"
])

# ----------------------------------------------------
# ETAPA 1: SOLICITAÇÃO DE MATERIAIS E SERVIÇOS
# ----------------------------------------------------
if menu == "1. Nova Solicitação (Obra)":
    st.header("📝 Solicitação de Materiais e Serviços")
    st.write("Preencha os dados da obra e edite a tabela de itens:")
    
    col1, col2 = st.columns(2)
    with col1:
        obra_nome = st.text_input("Nome da Obra", value="ACPA Extrusão de Alumínio Ltda")
        etapa = st.text_input("Etapa de Serviço", placeholder="Ex: Fundações, Estrutura")
    with col2:
        solicitante = st.text_input("Responsável pela Solicitação", placeholder="Seu nome")
        data_solicitacao = st.date_input("Data", datetime.date.today())
        
    df_modelo_inicial = pd.DataFrame([
        {"Item": 1, "Quant.": 10.0, "Unid.": "barra", "Descrição Material / Serviço": "Aço CA 60 Ø 12,5mm", "Observações": "Entregar barra reta"}
    ])
    
    df_editado = st.data_editor(df_modelo_inicial, num_rows="dynamic", use_container_width=True, key="tab_obra")
    
    if st.button("Gerar Solicitação e Enviar para Suprimentos", type="primary"):
        if df_editado.empty:
            st.error("A tabela não pode estar vazia.")
        else:
            proximo_num = len(st.session_state.requisicoes) + 1
            num_sequencial = f"{proximo_num:02d}-26"
            
            nova_req = {
                "ID": num_sequencial,
                "Obra": obra_nome,
                "Etapa": etapa,
                "Solicitante": solicitante,
                "Data": str(data_solicitacao),
                "Itens": df_editado.to_dict('records'),
                "Status": "Aguardando Cotação",
                "Fornecedores": {},
                "Vencedor": None,
                "Recebimento": {}
            }
            st.session_state.requisicoes.append(nova_req)
            st.success(f"✅ Solicitação registrada com sucesso! Número: **{num_sequencial}**")

# ----------------------------------------------------
# ETAPA 2: COTAÇÃO (SUPRIMENTOS)
# ----------------------------------------------------
elif menu == "2. Cotações (Suprimentos)":
    st.header("📊 Painel de Cotações (3 Fornecedores)")
    
    if not st.session_state.requisicoes:
        st.warning("⚠️ Nenhuma solicitação cadastrada.")
    else:
        ids_disp = [req["ID"] for req in st.session_state.requisicoes]
        req_sel = st.selectbox("Selecione a Requisição", ids_disp)
        req_atual = next(r for r in st.session_state.requisicoes if r["ID"] == req_sel)
        
        st.info(f"**Obra:** {req_atual['Obra']} | **Status:** {req_atual['Status']}")
        st.dataframe(pd.DataFrame(req_atual['Itens']), use_container_width=True)
        
        with st.form("form_cot"):
            col1, col2, col3 = st.columns(3)
            with col1:
                f1_nome = st.text_input("Fornecedor 1", value="Tião")
                f1_total = st.number_input("Total F1 (R$)", value=340.00)
                f1_pgto = st.text_input("Pgto F1", value="Boleto 30d")
            with col2:
                f2_nome = st.text_input("Fornecedor 2", value="Comercial Ferro")
                f2_total = st.number_input("Total F2 (R$)", value=355.00)
                f2_pgto = st.text_input("Pgto F2", value="Boleto 15d")
            with col3:
                f3_nome = st.text_input("Fornecedor 3", value="Aço Forte")
                f3_total = st.number_input("Total F3 (R$)", value=330.00)
                f3_pgto = st.text_input("Pgto F3", value="Pix")
            
            if st.form_submit_button("Salvar Cotações"):
                req_atual["Status"] = "Aguardando Aprovação Cliente"
                req_atual["Fornecedores"] = {
                    "F1": {"nome": f1_nome, "total": f1_total, "pgto": f1_pgto},
                    "F2": {"nome": f2_nome, "total": f2_total, "pgto": f2_pgto},
                    "F3": {"nome": f3_nome, "total": f3_total, "pgto": f3_pgto},
                }
                st.success("✅ Cotações salvas com sucesso!")

# ----------------------------------------------------
# ETAPA 3: ORDENS DE COMPRA (OC)
# ----------------------------------------------------
elif menu == "3. Ordens de Compra (OC)":
    st.header("🛒 Emissão de Ordem de Compra (OC)")
    
    reqs_prontas = [r for r in st.session_state.requisicoes if r["Status"] != "Aguardando Cotação"]
    
    if not reqs_prontas:
        st.warning("⚠️ Nenhuma requisição pronta para OC.")
    else:
        oc_escolhida = st.selectbox("Selecione a Requisição", [r["ID"] for r in reqs_prontas])
        req_oc = next(r for r in st.session_state.requisicoes if r["ID"] == oc_escolhida)
        
        if req_oc["Fornecedores"]:
            f_dados = req_oc["Fornecedores"]
            df_comp = pd.DataFrame([
                {"Fornecedor": f_dados['F1']['nome'], "Total": f_dados['F1']['total'], "Pgto": f_dados['F1']['pgto']},
                {"Fornecedor": f_dados['F2']['nome'], "Total": f_dados['F2']['total'], "Pgto": f_dados['F2']['pgto']},
                {"Fornecedor": f_dados['F3']['nome'], "Total": f_dados['F3']['total'], "Pgto": f_dados['F3']['pgto']},
            ])
            st.dataframe(df_comp, use_container_width=True)
            
            vencedor = st.selectbox("Fornecedor Aprovado", [f_dados['F1']['nome'], f_dados['F2']['nome'], f_dados['F3']['nome']])
            
            if st.button("Emitir Ordem de Compra Oficial"):
                req_oc["Status"] = "OC Emitida - Aguardando Entrega"
                req_oc["Vencedor"] = vencedor
                st.success(f"🎉 OC emitida para **{vencedor}**! Liberada para entrega em obra.")
        else:
            st.info("Cotações pendentes.")

# ----------------------------------------------------
# ETAPA 4: RECEBIMENTO E CONFERÊNCIA EM OBRA
# ----------------------------------------------------
elif menu == "4. Recebimento e Conferência (Obra)":
    st.header("🚚 Recebimento e Conferência Física em Obra")
    st.write("Conferência cega entre a OC emitida e os dados da Nota Fiscal recebida no canteiro.")
    
    reqs_oc = [r for r in st.session_state.requisicoes if "OC Emitida" in r["Status"]]
    
    if not reqs_oc:
        st.warning("⚠️ Nenhuma OC emitida aguardando recebimento na obra.")
    else:
        id_rec = st.selectbox("Selecione a OC para Conferência", [r["ID"] for r in reqs_oc])
        req_rec = next(r for r in st.session_state.requisicoes if r["ID"] == id_rec)
        
        st.info(f"**Fornecedor Vencedor:** {req_rec['Vencedor']} | **Obra:** {req_rec['Obra']}")
        
        st.markdown("### Conferência Cega (Portaria / Almoxarifado)")
        with st.form("form_recebimento"):
            nf_numero = st.text_input("Número da Nota Fiscal (NF)")
            nf_valor = st.number_input("Valor Total da NF (R$)", min_value=0.0)
            
            st.markdown("**Checklist de Verificação Obrigatória:**")
            check_qtde = st.checkbox(" Quantidades conferidas fisicamente no canteiro batem com a OC?")
            check_especif = st.checkbox(" Especificações, unidades e diâmetros corretos?")
            check_preco = st.checkbox(" Preço unitário e total idêntico ao negociado na OC?")
            
            upload_nf = st.file_uploader("Upload da Nota Fiscal Digitalizada (PDF ou Imagem)", type=["pdf", "png", "jpg", "jpeg"])
            
            concluir_recebimento = st.form_submit_button("Aprovar Recebimento e Enviar ao Controle")
            
            if concluir_recebimento:
                if not check_qtde or not check_especif or not check_preco:
                    st.error("❌ ERRO DE COMPLIANCE: Nenhum produto/serviço pode ser aceito com divergência em relação à OC! Verifique os itens.")
                elif not nf_numero:
                    st.error("Informe o número da Nota Fiscal.")
                else:
                    req_rec["Status"] = "Concluído - NF Enviada ao Controle"
                    req_rec["Recebimento"] = {"NF": nf_numero, "Valor": nf_valor}
                    st.success("✅ Recebimento aprovado com sucesso! A Nota Fiscal digitalizada foi encaminhada ao Departamento de Controle.")
