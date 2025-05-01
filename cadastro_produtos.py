import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cadastro Simples", layout="centered")
st.title("Cadastro de Produtos (Tela de Teste)")

# Inicializa variáveis de sessão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'produtos' not in st.session_state:
    st.session_state.produtos = []

# Login simples (sem validação)
if not st.session_state.logado:
    st.subheader("Login")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        st.session_state.logado = True
        st.rerun()
else:
    st.success("Login efetuado! Cadastre os produtos abaixo:")

    # Formulário de cadastro
    with st.form("form_cadastro"):
        codigo = st.text_input("Código")
        marca = st.text_input("Marca")
        tipo = st.text_input("Tipo")
        categoria = st.text_input("Categoria")
        preco_unitario = st.number_input("Preço Unitário", min_value=0.0, step=0.01)
        custo = st.number_input("Custo", min_value=0.0, step=0.01)
        obs = st.text_area("Observações")

        submitted = st.form_submit_button("Cadastrar Produto")
        if submitted:
            produto = {
                "Código": codigo,
                "Marca": marca,
                "Tipo": tipo,
                "Categoria": categoria,
                "Preço Unitário": preco_unitario,
                "Custo": custo,
                "Observações": obs
            }
            st.session_state.produtos.append(produto)
            st.success("Produto cadastrado com sucesso!")

    # Ações extras
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ver Produtos Cadastrados"):
            if st.session_state.produtos:
                st.subheader("Produtos Cadastrados")
                df = pd.DataFrame(st.session_state.produtos)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum produto cadastrado.")

    with col2:
        if st.button("Limpar Todos os Produtos"):
            st.session_state.produtos = []
            st.warning("Todos os produtos foram apagados.")

    # Botão de logout
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# Link ilustrativo
st.markdown("---")
st.markdown("[Link de teste: https://7zenilson.local](https://7zenilson.local) *(ilustrativo)*")
