import streamlit as st

from extractors.pdf_extractor import extract_text_from_pdf
from extractors.docx_extractor import extract_text_from_docx
from extractors.txt_extractor import extract_text_from_txt

from pipeline.cleaner import clean_text
from pipeline.chunker import chunk_text
from pipeline.metrics import compare_metrics

from prompt.language_detector import detect_language
from prompt.prompt_builder import build_all_prompts


st.set_page_config(
    page_title="Normalização de Texto com Pipeline e SLMs",
    layout="wide"
)

st.title("Normalização de Texto com Pipeline de Pré-Processamento e SLMs")
st.write("Etapa 01 — Extração, Limpeza e Preparação do Prompt")

uploaded_file = st.file_uploader(
    "Carrega um ficheiro PDF, DOCX ou TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    file_name = uploaded_file.name
    file_extension = file_name.split(".")[-1].lower()

    st.subheader("1. Informação do ficheiro")
    st.write(f"**Nome:** {file_name}")
    st.write(f"**Formato:** {file_extension.upper()}")

    if file_extension == "pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        raw_text = extract_text_from_docx(uploaded_file)
    elif file_extension == "txt":
        raw_text = extract_text_from_txt(uploaded_file)
    else:
        st.error("Formato não suportado.")
        st.stop()

    st.subheader("2. Texto bruto extraído")
    st.text_area(
        "Texto original antes da limpeza",
        raw_text,
        height=300
    )

    st.subheader("3. Configuração da pipeline de limpeza")

    col1, col2, col3 = st.columns(3)

    with col1:
        remove_artifacts = st.checkbox("Remover artefactos", value=True)
        rebuild_paragraphs = st.checkbox("Reconstruir parágrafos", value=True)

    with col2:
        normalize_spacing = st.checkbox("Normalizar espaços", value=True)
        normalize_punct = st.checkbox("Normalizar pontuação", value=True)

    with col3:
        remove_headers = st.checkbox("Remover cabeçalhos/rodapés repetidos", value=True)
        max_chars = st.number_input("Tamanho máximo por chunk", min_value=300, max_value=3000, value=1200)

    cleaned_text, steps_applied = clean_text(
        raw_text,
        remove_artifacts=remove_artifacts,
        rebuild_paragraphs=rebuild_paragraphs,
        normalize_spacing=normalize_spacing,
        normalize_punct=normalize_punct,
        remove_headers=remove_headers
    )

    st.subheader("4. Texto limpo")
    st.text_area(
        "Texto depois da pipeline de limpeza",
        cleaned_text,
        height=300
    )

    st.subheader("5. Etapas aplicadas")
    for step in steps_applied:
        st.success(step)

    st.subheader("6. Métricas antes/depois")

    metrics = compare_metrics(raw_text, cleaned_text)

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    metric_col1.metric(
        "Caracteres antes",
        metrics["raw"]["characters"]
    )

    metric_col2.metric(
        "Caracteres depois",
        metrics["cleaned"]["characters"]
    )

    metric_col3.metric(
        "Linhas vazias removidas",
        metrics["empty_lines_removed"]
    )

    metric_col4.metric(
        "Caracteres removidos",
        metrics["characters_removed"]
    )

    st.subheader("7. Deteção de idioma")
    language = detect_language(cleaned_text)
    st.info(f"Idioma detetado: {language}")

    st.subheader("8. Segmentação em chunks")
    chunks = chunk_text(cleaned_text, max_chars=max_chars)
    st.write(f"Foram criados **{len(chunks)} chunks**.")

    for index, chunk in enumerate(chunks, start=1):
        with st.expander(f"Chunk {index}"):
            st.text(chunk)

    st.subheader("9. Prompts gerados automaticamente")

    prompts = build_all_prompts(chunks, language)

    for index, prompt in enumerate(prompts, start=1):
        with st.expander(f"Prompt {index}"):
            st.text(prompt)

    st.subheader("10. Pré-visualização do body para futura API SLM")

    if prompts:
        api_body = {
            "model": "llama-3.2-1b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": prompts[0]
                }
            ]
        }

        st.json(api_body)

    st.download_button(
        label="Descarregar texto limpo",
        data=cleaned_text,
        file_name="texto_limpo.txt",
        mime="text/plain"
    )