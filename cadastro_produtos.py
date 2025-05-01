import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Cadastro Simples", layout="centered")
st.title("Cadastro de Produtos (Tela de Teste)")

# Inicializa variáveis de sessão
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'produtos' not in st.session_state:
    st.session_state.produtos = []
if 'cadastro_id' not in st.session_state:
    st.session_state.cadastro_id = 0
if 'pdf_buffer' not in st.session_state:
    st.session_state.pdf_buffer = None  # Armazenar o PDF gerado

# Função para gerar PDF
def gerar_pdf(lista_produtos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Produtos Cadastrados", styles["Title"]))
    elements.append(Paragraph(" ", styles["Normal"]))

    if lista_produtos:
        dados = [list(lista_produtos[0].keys())] + [list(prod.values()) for prod in lista_produtos]
        tabela = Table(dados)
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        elements.append(tabela)
    else:
        elements.append(Paragraph("Nenhum produto cadastrado.", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

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
        cid = st.session_state.cadastro_id

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
            st.session_state.cadastro_id += 1
            st.session_state.pdf_buffer = None  # Limpar PDF antigo
            st.success("✅ Produto cadastrado com sucesso!")
            st.rerun()

        elif limpar:
            st.session_state.produtos = []
            st.session_state.cadastro_id += 1
            st.session_state.pdf_buffer = None  # Limpar PDF ao limpar os produtos
            st.warning("⚠️ Todos os produtos foram apagados.")
            st.rerun()

    # Exibe tabela e botão de download após o formulário
    if st.session_state.produtos:
        st.markdown("## Produtos Cadastrados")
        df = pd.DataFrame(st.session_state.produtos)
        st.dataframe(df, use_container_width=True)

        # Gerar o PDF apenas uma vez e armazenar no estado
        if st.session_state.pdf_buffer is None:
            st.session_state.pdf_buffer = gerar_pdf(st.session_state.produtos)

        # Botão de download com PDF estável
        st.download_button(
            label="📄 Download PDF",
            data=st.session_state.pdf_buffer,
            file_name="produtos_cadastrados.pdf",
            mime="application/pdf",
            key="btn_pdf"
        )
