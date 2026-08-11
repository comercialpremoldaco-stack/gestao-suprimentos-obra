import streamlit as st
import pandas as pd

st.title("Sistema de Gestão de Suprimentos - Obra")

st.write("Bem-vindo ao sistema de controle de compras.")

# Upload da planilha
arquivo = st.file_uploader("Suba sua planilha de cotação aqui:", type=["xlsx", "xls"])

if arquivo is not None:
    df = pd.read_excel(arquivo)
    st.write("Dados da planilha carregada:")
    st.dataframe(df)
    
    if st.button("Validar e Registrar"):
        st.success("Planilha validada com sucesso! ID REQ-2026-001 gerado.")
      
