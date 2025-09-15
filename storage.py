import json
from pathlib import Path
from typing import Any

def read_json(path: str):
    """
    Lê os dados de um arquivo JSON e retorna como objeto Python (lista ou dicionário).

    Parâmetros:
        path (str): Caminho do arquivo JSON.

    Retorno:
        list | dict: Dados do arquivo JSON.
        Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia [].
    """
    path_json = Path(path)
    if not path_json.exists():
        return []
    try:
        # Lê o conteúdo do arquivo e converte de JSON para objeto Python
        return json.loads(path_json.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        # Se houver erro de leitura (arquivo corrompido ou vazio), retorna lista vazia
        return []


def write_json(path: str, data: Any):
    """
    Salva dados em um arquivo JSON no caminho especificado.

    Parâmetros:
        path (str): Caminho do arquivo JSON.
        data (Any): Dados em formato Python (lista ou dicionário) a serem gravados.

    Observações:
        - Cria automaticamente a pasta do arquivo, caso não exista.
        - Formata o JSON com indentação para facilitar leitura.
    """
    path_json = Path(path)

    # Cria pastas necessárias automaticamente (ex: 'data/')
    path_json.parent.mkdir(parents=True, exist_ok=True)

    # Converte os dados em JSON formatado e escreve no arquivo
    path_json.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding='utf-8'
    )
