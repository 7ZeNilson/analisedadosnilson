import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cadastro Simples", layout="centered")
st.title("Cadastro de Produtos (Tela de Teste)")

# Inicializa variáveis de sessão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'produtos' not in st.session_state:
    st.session_state.produtos = []
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "codigo": "",
        "marca": "",
        "tipo": "",
        "categoria": "",
        "preco_unitario": 0.0,
        "custo": 0.0,
        "obs": ""
    }

# Tela de Login
if not st.session_state.logado:
    st.subheader("Login")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        st.session_state.logado = True
        st.rerun()

# Tela de Cadastro
else:
    st.success("Login efetuado com sucesso!")
    st.markdown("### Cadastro de Produto")

    with st.form("form_cadastro"):
        st.session_state.form_data["codigo"] = st.text_input(
            "Código do Produto", 
            value=st.session_state.form_data["codigo"], 
            placeholder="Código do produto"
        )
        st.session_state.form_data["marca"] = st.text_input(
            "Marca do Produto", 
            value=st.session_state.form_data["marca"], 
            placeholder="Marca do Produto"
        )
        st.session_state.form_data["tipo"] = st.text_input(
            "Tipo do Produto", 
            value=st.session_state.form_data["tipo"], 
            placeholder="Tipo do Produto"
        )
        st.session_state.form_data["categoria"] = st.text_input(
            "Categoria do Produto", 
            value=st.session_state.form_data["categoria"], 
            placeholder="Categoria do Produto"
        )
        st.session_state.form_data["preco_unitario"] = st.number_input(
            "Preço Unitário", 
            min_value=0.0, 
            step=0.01, 
            value=st.session_state.form_data["preco_unitario"]
        )
        st.session_state.form_data["custo"] = st.number_input(
            "Custo", 
            min_value=0.0, 
            step=0.01, 
            value=st.session_state.form_data["custo"]
        )
        st.session_state.form_data["obs"] = st.text_area(
            "OBS", 
            value=st.session_state.form_data["obs"], 
            placeholder="Observações"
        )

        col1, col2 = st.columns(2)
        with col1:
            cadastrar = st.form_submit_button("Enviar")
        with col2:
            limpar = st.form_submit_button("Limpar")

        if cadastrar:
            produto = {
                "Código": st.session_state.form_data["codigo"],
                "Marca": st.session_state.form_data["marca"],
                "Tipo": st.session_state.form_data["tipo"],
                "Categoria": st.session_state.form_data["categoria"],
                "Preço Un.": st.session_state.form_data["preco_unitario"],
                "Custo": st.session_state.form_data["custo"],
                "OBS": st.session_state.form_data["obs"]
            }
            st.session_state.produtos.append(produto)
            st.success("✅ Produto cadastrado com sucesso!")

            # Limpa os campos
            st.session_state.form_data = {
                "codigo": "",
                "marca": "",
                "tipo": "",
                "categoria": "",
                "preco_unitario": 0.0,
                "custo": 0.0,
                "obs": ""
            }
            st.rerun()

        elif limpar:
            st.session_state.produtos = []
            st.warning("⚠️ Todos os produtos foram apagados.")
            st.session_state.form_data = {
                "codigo": "",
                "marca": "",
                "tipo": "",
                "categoria": "",
                "preco_unitario": 0.0,
                "custo": 0.0,
                "obs": ""
            }
            st.rerun()

    if st.session_state.produtos:
        st.markdown("## Produtos Cadastrados")
        df = pd.DataFrame(st.session_state.produtos)
        st.dataframe(df, use_container_width=True)
