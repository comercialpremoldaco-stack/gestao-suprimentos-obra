import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Gestão de Suprimentos - Obra", layout="wide")

st.title("🏗️ Sistema de Gestão de Suprimentos e Obras")
st.markdown("---")

# Inicializando o banco de dados temporário na memória
if 'requisicoes' not in st.session_state:
    st.session_state.requisicoes = []

# Menu lateral de navegação com o novo Portal do Cliente
menu = st.sidebar.selectbox("Menu Principal", [
    "1. Nova Solicitação (Obra)", 
    "2. Cotações (Suprimentos)", 
    "3. Aprovação do Cliente",
    "4. Emissão de Ordem de Compra (OC)",
    "5. Recebimento e Conferência (Obra)",
    "6. Departamento Fiscal e Controle"
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
                "Cliente_Aprovacao": {},
                "Recebimento": {},
                "Fiscal": {}
            }
            st.session_state.requisicoes.append(nova_req)
            st.success(f"✅ Solicitação registrada com sucesso! Número: **{num_sequencial}**")

# ----------------------------------------------------
# ETAPA 2: COTAÇÃO (SUPRIMENTOS)
# ----------------------------------------------------
elif menu == "2. Cotações (Suprimentos)":
    st.header("📊 Painel de Cotações (3 Fornecedores Obrigatórios)")
    
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
            
            if st.form_submit_button("Salvar Cotações e Enviar para o Cliente"):
                req_atual["Status"] = "Aguardando Aprovação do Cliente"
                req_atual["Fornecedores"] = {
                    "F1": {"nome": f1_nome, "total": f1_total, "pgto": f1_pgto},
                    "F2": {"nome": f2_nome, "total": f2_total, "pgto": f2_pgto},
                    "F3": {"nome": f3_nome, "total": f3_total, "pgto": f3_pgto},
                }
                st.success("✅ Cotações salvas! Encaminhado para o Portal de Aprovação do Cliente.")

# ----------------------------------------------------
# ETAPA 3: APROVAÇÃO DO CLIENTE (PORTAL DO CLIENTE)
# ----------------------------------------------------
elif menu == "3. Aprovação do Cliente":
    st.header("👑 Portal de Aprovação do Cliente")
    st.write("Área exclusiva onde o cliente revisa as propostas e autoriza a aquisição.")
    
    reqs_cliente = [r for r in st.session_state.requisicoes if r["Status"] == "Aguardando Aprovação do Cliente"]
    
    if not reqs_cliente:
        st.warning("⚠️ Nenhuma requisição pendente de aprovação do cliente no momento.")
    else:
        id_cli = st.selectbox("Selecione a Requisição para Análise", [r["ID"] for r in reqs_cliente])
        req_c = next(r for r in st.session_state.requisicoes if r["ID"] == id_cli)
        
        st.info(f"**Obra:** {req_c['Obra']} | **Solicitante:** {req_c['Solicitante']}")
        st.dataframe(pd.DataFrame(req_c['Itens']), use_container_width=True)
        
        if req_c["Fornecedores"]:
            f_dados = req_c["Fornecedores"]
            df_comparativo = pd.DataFrame([
                {"Fornecedor": f_dados['F1']['nome'], "Valor Total (R$)": f_dados['F1']['total'], "Condição de Pagamento": f_dados['F1']['pgto']},
                {"Fornecedor": f_dados['F2']['nome'], "Valor Total (R$)": f_dados['F2']['total'], "Condição de Pagamento": f_dados['F2']['pgto']},
                {"Fornecedor": f_dados['F3']['nome'], "Valor Total (R$)": f_dados['F3']['total'], "Condição de Pagamento": f_dados['F3']['pgto']},
            ])
            st.markdown("### 📊 Mapa Comparativo de Propostas")
            st.dataframe(df_comparativo, use_container_width=True)
            
            with st.form("form_aprovacao_cliente"):
                fornecedor_escolhido = st.selectbox("Indique o Fornecedor Aprovado:", [f_dados['F1']['nome'], f_dados['F2']['nome'], f_dados['F3']['nome']])
                comentario_cliente = st.text_area("Observações / Diretrizes do Cliente", placeholder="Ex: Aprovado conforme menor preço.")
                
                autorizar = st.form_submit_button("✅ Aprovar e Liberar para Emissão de OC", type="primary")
                
                if autorizar:
                    req_c["Status"] = "Aprovado pelo Cliente - Aguardando OC"
                    req_c["Cliente_Aprovacao"] = {
                        "Fornecedor_Indicado": fornecedor_escolhido,
                        "Comentario": comentario_cliente,
                        "Data": str(datetime.date.today())
                    }
                    st.success(f"🎉 Compra aprovada com sucesso para **{fornecedor_escolhido}**! O departamento de suprimentos já pode emitir a Ordem de Compra.")
        else:
            st.info("As cotações para esta requisição ainda não foram finalizadas pelo suprimentos.")

# ----------------------------------------------------
# ETAPA 4: EMISSÃO DE ORDEM DE COMPRA (OC)
# ----------------------------------------------------
elif menu == "4. Emissão de Ordem de Compra (OC)":
    st.header("🛒 Emissão de Ordem de Compra (OC)")
    st.write("Fechamento da aquisição e emissão da OC baseada na indicação do cliente.")
    
    reqs_oc = [r for r in st.session_state.requisicoes if r["Status"] == "Aprovado pelo Cliente - Aguardando OC"]
    
    if not reqs_oc:
        st.warning("⚠️ Nenhuma requisição aprovada pelo cliente aguardando emissão de OC.")
    else:
        oc_escolhida = st.selectbox("Selecione a Requisição Aprovada", [r["ID"] for r in reqs_oc])
        req_oc = next(r for r in st.session_state.requisicoes if r["ID"] == oc_escolhida)
        
        indicacao = req_oc["Cliente_Aprovacao"].get("Fornecedor_Indicado")
        st.info(f"**Fornecedor Indicado pelo Cliente:** {indicacao}")
        
        if st.button("Emitir Ordem de Compra Oficial (OC)", type="primary"):
            req_oc["Status"] = "OC Emitida - Aguardando Entrega"
            req_oc["Vencedor"] = indicacao
            st.success(f"🎉 Ordem de Compra oficial gerada e enviada para o fornecedor **{indicacao}**, solicitante e controle!")

# ----------------------------------------------------
# ETAPA 5: RECEBIMENTO E CONFERÊNCIA EM OBRA
# ----------------------------------------------------
elif menu == "5. Recebimento e Conferência (Obra)":
    st.header("🚚 Recebimento e Conferência Física em Obra")
    
    reqs_rec = [r for r in st.session_state.requisicoes if "OC Emitida" in r["Status"]]
    
    if not reqs_rec:
        st.warning("⚠️ Nenhuma OC emitida aguardando recebimento na obra.")
    else:
        id_rec = st.selectbox("Selecione a OC para Conferência", [r["ID"] for r in reqs_rec])
        req_rec = next(r for r in st.session_state.requisicoes if r["ID"] == id_rec)
        
        st.info(f"**Fornecedor Vencedor:** {req_rec['Vencedor']} | **Obra:** {req_rec['Obra']}")
        
        with st.form("form_recebimento"):
            nf_numero = st.text_input("Número da Nota Fiscal (NF)")
            nf_valor = st.number_input("Valor Total da NF (R$)", min_value=0.0)
            
            st.markdown("**Checklist de Verificação Obrigatória:**")
            check_qtde = st.checkbox(" Quantidades conferidas fisicamente batem com a OC?")
            check_especif = st.checkbox(" Especificações e unidades corretas?")
            check_preco = st.checkbox(" Preço unitário e total idêntico ao negociado na OC?")
            
            upload_nf = st.file_uploader("Upload da Nota Fiscal Digitalizada", type=["pdf", "png", "jpg", "jpeg"])
            
            if st.form_submit_button("Aprovar Recebimento e Enviar ao Controle"):
                if not check_qtde or not check_especif or not check_preco:
                    st.error("❌ ERRO: Divergência com a OC! Nenhum produto/serviço pode ser recebido.")
                elif not nf_numero:
                    st.error("Informe o número da Nota Fiscal.")
                else:
                    req_rec["Status"] = "Concluído - NF Enviada ao Controle"
                    req_rec["Recebimento"] = {"NF": nf_numero, "Valor": nf_valor}
                    st.success("✅ Recebimento aprovado! Encaminhado ao Departamento Fiscal.")

# ----------------------------------------------------
# ETAPA 6: DEPARTAMENTO FISCAL E CONTROLE
# ----------------------------------------------------
elif menu == "6. Departamento Fiscal e Controle":
    st.header("⚖️ Departamento Fiscal, Compliance e Liberação")
    
    reqs_fiscal = [r for r in st.session_state.requisicoes if r["Status"] == "Concluído - NF Enviada ao Controle"]
    
    if not reqs_fiscal:
        st.warning("⚠️ Nenhuma Nota Fiscal aguardando validação fiscal.")
    else:
        id_fisc = st.selectbox("Selecione a Requisição para Análise Fiscal", [r["ID"] for r in reqs_fiscal])
        req_f = next(r for r in st.session_state.requisicoes if r["ID"] == id_fisc)
        
        st.info(f"**Requisição:** {req_f['ID']} | **Fornecedor:** {req_f['Vencedor']} | **NF:** {req_f['Recebimento'].get('NF')}")
        
        with st.form("form_fiscal"):
            chk_sefaz = st.checkbox(" Nota Fiscal válida e autorizada na Sefaz")
            chk_cnd = st.checkbox(" CNDs do Fornecedor regulares")
            chk_impostos = st.checkbox(" Retenções de impostos conferidas")
            
            if st.form_submit_button("Aprovar e Liberar para Pagamento"):
                if not chk_sefaz or not chk_cnd or not chk_impostos:
                    st.error("❌ ERRO: Validações fiscais obrigatórias pendentes!")
                else:
                    req_f["Status"] = "Finalizado - Pago / Contabilizado"
                    st.success("🎉 Processo concluído com sucesso! Nota Fiscal validada e integrada.")
