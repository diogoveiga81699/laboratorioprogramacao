# Normalização de Texto com Pipeline de Pré-Processamento e SLMs

## Objetivo

Este projeto foi desenvolvido no âmbito da unidade curricular de Laboratório de Programação.

A aplicação permite extrair texto de documentos PDF, DOCX e TXT, aplicar uma pipeline de limpeza e preparar o texto para futura normalização por um modelo de linguagem de pequena dimensão.

## Funcionalidades implementadas

- Upload de ficheiros PDF, DOCX e TXT
- Extração de texto bruto
- Visualização do texto antes da limpeza
- Pipeline de limpeza configurável
- Remoção de artefactos textuais
- Reconstrução de parágrafos
- Normalização de espaços e pontuação
- Remoção de cabeçalhos e rodapés repetidos
- Visualização do texto depois da limpeza
- Deteção automática de idioma
- Segmentação do texto em chunks
- Geração automática de prompts
- Pré-visualização do body JSON para futura ligação à API do SLM

## Tecnologias utilizadas

- Python
- Streamlit
- pdfplumber
- python-docx
- langdetect

## Como executar

Instalar dependências:

```bash
pip install -r requirements.txt