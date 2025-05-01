import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cadastro Simples", layout="centered")
st.title("Cadastro de Produtos (Tela de Teste)")

# Inicializa variáveis de sessão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'produtos' not in st.session_state:
    st.session_state.produtos = []
if 'cadastro_id' not in st.session_state:
    st.session_state.cadastro_id = 0

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
        cid = st.session_state.cadastro_id  # id único por cadastro

        codigo = st.text_input("Código do Produto", key=f"codigo_{cid}", placeholder="Código do produto")
        marca = st.text_input("Marca do Produto", key=f"marca_{cid}", placeholder="Marca do Produto")
        tipo = st.text_input("Tipo do Produto", key=f"tipo_{cid}", placeholder="Tipo do Produto")
        categoria = st.text_input("Categoria do Produto", key=f"categoria_{cid}", placeholder="Categoria do Produto")
        preco_unitario = st.number_input("Preço Unitário", min_value=0.0, step=0.01, key=f"preco_{cid}")
        custo = st.number_input("Custo", min_value=0.0, step=0.01, key=f"custo_{cid}")
        obs = st.text_area("OBS", key=f"obs_{cid}", placeholder="Observações")

        col1, col2 = st.columns(2)
        with col1:
            cadastrar = st.form_submit_button("Enviar")
        with col2:
            limpar = st.form_submit_button("Limpar")

        if cadastrar:
            produto = {
                "Código": codigo,
                "Marca": marca,
                "Tipo": tipo,
                "Categoria": categoria,
                "Preço Un.": preco_unitario,
                "Custo": custo,
                "OBS": obs
            }
            st.session_state.produtos.append(produto)
            st.session_state.cadastro_id += 1  # atualiza o ID para gerar novos campos limpos
            st.success("✅ Produto cadastrado com sucesso!")
            st.rerun()

        elif limpar:
            st.session_state.produtos = []
            st.session_state.cadastro_id += 1  # força atualização dos campos
            st.warning("⚠️ Todos os produtos foram apagados.")
            st.rerun()

    if st.session_state.produtos:
        st.markdown("## Produtos Cadastrados")
        df = pd.DataFrame(st.session_state.produtos)
        st.dataframe(df, use_container_width=True)
