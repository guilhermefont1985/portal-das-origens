import streamlit as st
from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

client = OpenAI()

st.set_page_config(
    page_title="Portal das Origens",
    page_icon="🌎",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7efe0;
    }
    .titulo {
        text-align: center;
        color: #3b2a1a;
        font-family: Georgia, serif;
    }
    .subtitulo {
        text-align: center;
        color: #5c452b;
        font-size: 20px;
    }
    .caixa {
        background-color: #fff8e7;
        padding: 25px;
        border-radius: 18px;
        border: 2px solid #8B6F47;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    .folha {
        background-color: #fff8e7;
        padding: 25px;
        border-radius: 18px;
        border: 4px double #8B6F47;
        font-family: Georgia, serif;
        color: #2b2118;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='titulo'>🌎 Portal das Origens</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitulo'>Uma viagem histórica personalizada com Inteligência Artificial</p>",
    unsafe_allow_html=True
)

st.markdown("---")

col_form, col_info = st.columns([1, 1])

with col_form:
    st.markdown("<div class='caixa'>", unsafe_allow_html=True)

    st.markdown("### 📝 Dados da experiência")

    nome_completo = st.text_input("Digite seu nome completo")

    periodo = st.selectbox(
        "Escolha sua viagem no tempo",
        [
            "Egito Antigo",
            "Grécia Antiga",
            "Roma Antiga",
            "Idade Média",
            "Grandes Navegações",
            "Brasil Colonial",
            "Império do Brasil",
            "Primeira República",
            "Cabedelo e a Fortaleza de Santa Catarina",
            "História da Paraíba"
        ]
    )

    st.markdown("### 📸 Uso da imagem")

    st.info(
        "A foto será usada exclusivamente para gerar uma representação histórica nesta atividade educativa. "
        "A foto não será armazenada pelo projeto nem utilizada para outros fins."
    )

    aceite1 = st.checkbox(
        "Autorizo o uso da minha imagem exclusivamente para esta atividade da feira de ciências."
    )

    aceite2 = st.checkbox(
        "Declaro estar ciente de que a imagem não será usada para outros fins."
    )

    foto = st.camera_input("Tire sua foto")

    gerar = st.button("📜 Gerar meu Passaporte das Origens")

    st.markdown("</div>", unsafe_allow_html=True)

with col_info:
    st.markdown("<div class='caixa'>", unsafe_allow_html=True)
    st.markdown("### 📜 Como funciona?")
    st.write(
        "1. Digite seu nome completo.\n\n"
        "2. Escolha um período histórico.\n\n"
        "3. Autorize o uso da imagem para a atividade.\n\n"
        "4. Tire uma foto.\n\n"
        "5. A IA cria uma folha histórica com texto e retrato."
    )

    st.markdown("### 🌎 Tema: Origens")
    st.write(
        "O objetivo é mostrar que nomes, lugares, culturas e sociedades possuem histórias. "
        "A IA não descobre a ancestralidade real da pessoa, mas ajuda a explorar possíveis origens "
        "do nome e conexões com períodos históricos."
    )
    st.markdown("</div>", unsafe_allow_html=True)


def criar_pdf(nome, periodo, texto, imagem_bytes):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4

    # Fundo pergaminho
    c.setFillColorRGB(1, 0.97, 0.88)
    c.rect(0, 0, largura, altura, fill=1)

    # Moldura histórica
    c.setStrokeColorRGB(0.42, 0.28, 0.12)
    c.setLineWidth(4)
    c.rect(1 * cm, 1 * cm, largura - 2 * cm, altura - 2 * cm)

    c.setLineWidth(1.5)
    c.rect(1.3 * cm, 1.3 * cm, largura - 2.6 * cm, altura - 2.6 * cm)

    # Títulos
    c.setFillColorRGB(0.18, 0.12, 0.07)
    c.setFont("Times-Bold", 24)
    c.drawCentredString(largura / 2, altura - 2.2 * cm, "PORTAL DAS ORIGENS")

    c.setFont("Times-Bold", 17)
    c.drawCentredString(largura / 2, altura - 3.0 * cm, "Passaporte Histórico do Visitante")

    # Dados principais
    c.setFont("Times-Bold", 12)
    c.drawString(2 * cm, altura - 4.2 * cm, f"Nome: {nome}")
    c.drawString(2 * cm, altura - 4.9 * cm, f"Destino histórico: {periodo}")

    # Imagem
    img_reader = ImageReader(BytesIO(imagem_bytes))
    c.drawImage(
        img_reader,
        2 * cm,
        8.2 * cm,
        width=8 * cm,
        height=8 * cm,
        preserveAspectRatio=True,
        anchor="c"
    )

    # Título do texto
    c.setFont("Times-Bold", 14)
    c.drawString(10.7 * cm, altura - 6.0 * cm, "Registro Histórico")

    # Texto
    c.setFont("Times-Roman", 10)
    x = 10.7 * cm
    y = altura - 6.8 * cm
    max_chars = 47

    linhas = []
    for paragrafo in texto.split("\n"):
        palavras = paragrafo.split()
        linha = ""
        for palavra in palavras:
            if len((linha + " " + palavra).strip()) <= max_chars:
                linha = (linha + " " + palavra).strip()
            else:
                linhas.append(linha)
                linha = palavra
        if linha:
            linhas.append(linha)
        linhas.append("")

    for linha in linhas[:42]:
        c.drawString(x, y, linha)
        y -= 0.43 * cm

    # Missão
    c.setFont("Times-Bold", 12)
    c.drawString(2 * cm, 6.3 * cm, "Missão do Historiador:")
    c.setFont("Times-Roman", 10)
    c.drawString(2 * cm, 5.8 * cm, "Observe sua viagem no tempo e descubra:")
    c.drawString(2 * cm, 5.3 * cm, "• Como as pessoas viviam nesse período?")
    c.drawString(2 * cm, 4.8 * cm, "• Que costumes permanecem até hoje?")
    c.drawString(2 * cm, 4.3 * cm, "• O que essa história revela sobre nossas origens?")

    # Rodapé
    c.setFont("Times-Italic", 10)
    c.drawCentredString(
        largura / 2,
        1.7 * cm,
        "Projeto de História | Feira de Ciências | Portal das Origens"
    )

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


if gerar:

    if nome_completo.strip() == "":
        st.warning("Digite seu nome completo.")
    elif not aceite1 or not aceite2:
        st.warning("É necessário marcar os dois aceites para continuar.")
    elif foto is None:
        st.warning("Tire uma foto para gerar o retrato histórico.")
    else:
        with st.spinner("Gerando texto histórico..."):

            prompt_texto = f"""
            Você é um professor de História do Ensino Fundamental.

            Crie um texto curto para um Passaporte das Origens em uma feira escolar.

            Dados:
            Nome completo: {nome_completo}
            Período histórico: {periodo}

            Use este formato:

            Origem do Nome:
            máximo 2 frases.

            Origem Possível do Sobrenome:
            máximo 2 frases.

            Contexto Histórico:
            máximo 3 frases.

            Curiosidade Histórica:
            máximo 2 frases.

            Conexão com as Origens:
            máximo 2 frases.

            Regras:
            - Não invente ancestralidade real.
            - Use "possivelmente", "pode estar associado" e "em muitos casos".
            - Linguagem simples e educativa.
            - Texto curto, claro e adequado para qualquer visitante da feira.
            """

            resposta = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt_texto
            )

            texto_historico = resposta.output_text

        with st.spinner("Transformando sua foto em retrato histórico..."):

            foto_bytes = foto.getvalue()
            arquivo_foto = BytesIO(foto_bytes)
            arquivo_foto.name = "foto_visitante.png"

            prompt_imagem = f"""
            Transforme a pessoa da foto em um retrato histórico educativo.

            Contexto histórico: {periodo}

            Manter o rosto reconhecível de forma respeitosa.
            Adaptar roupas, cenário e elementos visuais ao período histórico escolhido.
            Estilo: ilustração histórica colorida, livro didático, adequada para estudantes.
            Não incluir violência, símbolos ofensivos, caricaturas ou estereótipos.
            """

            imagem = client.images.edit(
                model="gpt-image-1",
                image=arquivo_foto,
                prompt=prompt_imagem,
                size="1024x1024"
            )

            image_bytes = base64.b64decode(imagem.data[0].b64_json)
            img = Image.open(BytesIO(image_bytes))

        st.markdown("---")
        st.success("Passaporte das Origens criado!")

        col_img, col_txt = st.columns([1, 1.2])

        with col_img:
            st.image(
                img,
                caption=f"{nome_completo} em {periodo}",
                use_container_width=True
            )

        with col_txt:
            st.markdown(
                f"""
                <div class='folha'>
                <h2 style="text-align:center;">📜 Passaporte das Origens</h2>
                <p><strong>Nome:</strong> {nome_completo}</p>
                <p><strong>Destino histórico:</strong> {periodo}</p>
                <hr>
                <div style="font-size:15px;">
                {texto_historico.replace(chr(10), "<br>")}
                </div>
                <hr>
                <p style="font-size:13px; text-align:center;">
                Projeto de História | Feira de Ciências | Portal das Origens
                </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        pdf_bytes = criar_pdf(
            nome_completo,
            periodo,
            texto_historico,
            image_bytes
        )

        st.download_button(
            label="⬇️ Baixar Passaporte das Origens em PDF",
            data=pdf_bytes,
            file_name="passaporte_das_origens.pdf",
            mime="application/pdf"
        )

        st.download_button(
            label="⬇️ Baixar apenas o retrato histórico",
            data=image_bytes,
            file_name="retrato_historico.png",
            mime="image/png"
        )
       