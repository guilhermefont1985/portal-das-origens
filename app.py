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
    page_title="Máquina das Origens",
    page_icon="🌎",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f6eddc;
}
.hero {
    background: linear-gradient(135deg, #fff8e7, #ead7b7);
    border: 4px double #8B6F47;
    border-radius: 22px;
    padding: 35px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.18);
}
.hero h1 {
    font-family: Georgia, serif;
    color: #2b2118;
    font-size: 46px;
}
.hero p {
    font-size: 19px;
    color: #5c452b;
}
.resultado {
    background-color: #fff8e7;
    border: 4px double #8B6F47;
    border-radius: 20px;
    padding: 30px;
    font-family: Georgia, serif;
    color: #2b2118;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🌎 Máquina das Origens</h1>
    <p>Faça uma viagem no tempo e descubra histórias por trás do seu nome.</p>
    <p><strong>Projeto de História | Feira de Ciências</strong></p>
</div>
""", unsafe_allow_html=True)

col_form, col_info = st.columns([1, 1])

with col_form:
    st.markdown("## 📝 Dados da experiência")

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

    gerar_imagem = st.checkbox(
        "🎨 Quero gerar um retrato histórico com Inteligência Artificial"
    )

    foto = None
    aceite1 = True
    aceite2 = True

    if gerar_imagem:
        st.markdown("## 📸 Uso da imagem")

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

with col_info:
    st.markdown("## 📜 Como funciona?")
    st.markdown("""
    **1.** Digite seu nome completo.

    **2.** Escolha um período histórico.

    **3.** Se quiser, marque a opção para gerar retrato histórico.

    **4.** A Máquina das Origens cria seu passaporte histórico.

    **5.** Você pode baixar o resultado.
    """)

    st.markdown("## 🌎 Tema: Origens")
    st.write(
        "O objetivo é mostrar que nomes, culturas, povos e lugares possuem histórias. "
        "A inteligência artificial não descobre a ancestralidade real da pessoa, "
        "mas ajuda a explorar possíveis origens do nome e conexões com períodos históricos."
    )


def criar_pdf(nome, periodo, texto, imagem_bytes=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4

    c.setFillColorRGB(1, 0.97, 0.88)
    c.rect(0, 0, largura, altura, fill=1)

    c.setStrokeColorRGB(0.42, 0.28, 0.12)
    c.setLineWidth(4)
    c.rect(1 * cm, 1 * cm, largura - 2 * cm, altura - 2 * cm)

    c.setLineWidth(1.5)
    c.rect(1.3 * cm, 1.3 * cm, largura - 2.6 * cm, altura - 2.6 * cm)

    c.setFillColorRGB(0.18, 0.12, 0.07)
    c.setFont("Times-Bold", 24)
    c.drawCentredString(largura / 2, altura - 2.2 * cm, "MAQUINA DAS ORIGENS")

    c.setFont("Times-Bold", 17)
    c.drawCentredString(largura / 2, altura - 3.0 * cm, "Passaporte Historico do Visitante")

    c.setFont("Times-Bold", 12)
    c.drawString(2 * cm, altura - 4.2 * cm, f"Nome: {nome}")
    c.drawString(2 * cm, altura - 4.9 * cm, f"Destino historico: {periodo}")

    if imagem_bytes:
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
        x_texto = 10.7 * cm
        y_texto = altura - 6.0 * cm
        max_chars = 47
    else:
        x_texto = 2 * cm
        y_texto = altura - 6.2 * cm
        max_chars = 90

    c.setFont("Times-Bold", 14)
    c.drawString(x_texto, y_texto, "Registro Historico")

    c.setFont("Times-Roman", 10)
    x = x_texto
    y = y_texto - 0.8 * cm

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

    for linha in linhas[:48]:
        c.drawString(x, y, linha)
        y -= 0.43 * cm

    c.setFont("Times-Bold", 12)
    c.drawString(2 * cm, 4.3 * cm, "Missao do Historiador:")
    c.setFont("Times-Roman", 10)
    c.drawString(2 * cm, 3.8 * cm, "Observe sua viagem no tempo e descubra:")
    c.drawString(2 * cm, 3.3 * cm, "- Como as pessoas viviam nesse periodo?")
    c.drawString(2 * cm, 2.8 * cm, "- Que costumes permanecem ate hoje?")
    c.drawString(2 * cm, 2.3 * cm, "- O que essa historia revela sobre nossas origens?")

    c.setFont("Times-Italic", 10)
    c.drawCentredString(
        largura / 2,
        1.7 * cm,
        "Projeto de Historia | Feira de Ciencias | Maquina das Origens"
    )

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


if gerar:
    if nome_completo.strip() == "":
        st.warning("Digite seu nome completo.")
    elif gerar_imagem and (not aceite1 or not aceite2):
        st.warning("É necessário marcar os dois aceites para gerar o retrato histórico.")
    elif gerar_imagem and foto is None:
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

        img = None
        image_bytes = None

        if gerar_imagem:
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
            if gerar_imagem and img is not None:
                st.image(
                    img,
                    caption=f"{nome_completo} em {periodo}",
                    use_container_width=True
                )
            else:
                st.markdown("""
                ### 🌎 Viagem no Tempo

                Esta versão do passaporte foi gerada apenas com texto histórico.

                Para criar um retrato histórico personalizado, marque a opção:

                **🎨 Quero gerar um retrato histórico com Inteligência Artificial**
                """)

        with col_txt:
            st.markdown(
                f"""
                <div class="resultado">
                <h2 style="text-align:center;">📜 Passaporte das Origens</h2>
                <p><strong>Nome:</strong> {nome_completo}</p>
                <p><strong>Destino histórico:</strong> {periodo}</p>
                <hr>
                <div style="font-size:15px;">
                {texto_historico.replace(chr(10), "<br>")}
                </div>
                <hr>
                <p style="text-align:center; font-size:13px;">
                Projeto de História | Feira de Ciências | Máquina das Origens
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

        if gerar_imagem and image_bytes is not None:
            st.download_button(
                label="⬇️ Baixar apenas o retrato histórico",
                data=image_bytes,
                file_name="retrato_historico.png",
                mime="image/png"
            )
