def build_prompt(text_chunk, language):
    return f"""
És um assistente especializado em normalização textual.

Tarefa:
Normaliza o texto abaixo mantendo o significado original.

Regras:
- Mantém o idioma original: {language}
- Corrige erros de formatação, espaçamento e pontuação
- Reconstrói frases ou parágrafos quando necessário
- Remove ruído textual evidente
- Não inventes informação nova
- Não resumas o conteúdo
- Mantém o texto em plain text
- Preserva nomes próprios, datas, números e entidades importantes

Texto a normalizar:
{text_chunk}
""".strip()


def build_all_prompts(chunks, language):
    return [build_prompt(chunk, language) for chunk in chunks]