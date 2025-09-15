from storage import read_json, write_json
from models import Jogadora, Documento, Time, Torneio, Inscricao, new_id
from notifications import notify_email
from typing import List, Optional
from pathlib import Path
import mimetypes
import datetime

# -----------------------
# Caminhos dos arquivos JSON usados como "banco de dados"
# -----------------------
DB_DIR = Path("data")  # diretório base dos arquivos
PLAYERS_FILE = str(DB_DIR / "jogadoras.json")  # dados de jogadoras
DOCS_FILE = str(DB_DIR / "documentos.json")  # documentos enviados
TEAMS_FILE = str(DB_DIR / "times.json")  # times cadastrados
TOURNAMENTS_FILE = str(DB_DIR / "torneios.json")  # torneios
INSCR_FILE = str(DB_DIR / "inscricoes.json")  # inscrições de times
OCR_CACHE_FILE = str(DB_DIR / "ocr_cache.json")  # cache de OCR simulado


# =======================
# Funções de Jogadoras
# =======================

def listar_jogadoras() -> List[dict]:
    """
    Retorna todas as jogadoras cadastradas no sistema.
    """
    return read_json(PLAYERS_FILE)


def criar_jogadora(nome: str, idade: int, contato: str) -> dict:
    """
    Cria uma nova jogadora com nome, idade e contato.
    Salva no arquivo JSON e retorna o dicionário da jogadora criada.
    """
    if not nome.strip() or not contato.strip():
        raise ValueError("Nome e contato são obrigatórios")

    jogadores = listar_jogadoras()
    j = Jogadora(id=new_id(), nome=nome.strip(), idade=idade, contato=contato.strip())
    jogadores.append(j.to_dict())
    write_json(PLAYERS_FILE, jogadores)
    return j.to_dict()


def atualizar_jogadora(jog_id: str, nome: Optional[str], idade: Optional[int], contato: Optional[str]) -> dict:
    """
    Atualiza dados de uma jogadora existente.
    Permite alterar nome, idade e contato.
    """
    jogadores = listar_jogadoras()
    for i, j in enumerate(jogadores):
        if j["id"] == jog_id:
            if nome and nome.strip():
                j["nome"] = nome.strip()
            if idade is not None:
                j["idade"] = int(idade)
            if contato and contato.strip():
                j["contato"] = contato.strip()
            jogadores[i] = j
            write_json(PLAYERS_FILE, jogadores)
            return j
    raise KeyError("Jogadora não encontrada")


def remover_jogadora(jog_id: str) -> None:
    """
    Remove uma jogadora do sistema pelo seu ID.
    """
    jogadores = listar_jogadoras()
    novos = [j for j in jogadores if j["id"] != jog_id]
    if len(novos) == len(jogadores):
        raise KeyError("Jogadora não encontrada")
    write_json(PLAYERS_FILE, novos)


# =======================
# Funções de Documentos
# =======================

ALLOWED = {".pdf", ".jpg", ".jpeg", ".png"}  # extensões permitidas para upload


def listar_documentos():
    """
    Retorna todos os documentos cadastrados.
    """
    return read_json(DOCS_FILE)


def subir_documento(jogadora_id: str, filepath: str) -> dict:
    """
    Registra um documento enviado por uma jogadora.
    Verifica existência do arquivo e tipo permitido.
    Salva no JSON e envia notificação por email.
    """
    jogadores = listar_jogadoras()
    if not any(j["id"] == jogadora_id for j in jogadores):
        raise KeyError("Jogadora não encontrada")

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError("Arquivo não encontrado")

    ext = path.suffix.lower()
    if ext not in ALLOWED:
        raise ValueError("Tipo de arquivo não permitido")

    docs = listar_documentos()
    mtype = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    doc = Documento(
        id=new_id(),
        jogadora_id=jogadora_id,
        filename=path.name,
        filetype=mtype,
        status="pending",
        history=[],
    )
    docs.append(doc.to_dict())
    write_json(DOCS_FILE, docs)

    # Notificação para organizadores
    notify_email(
        "organizers@copapab.local",
        "Novo documento enviado",
        f"Jogadora {jogadora_id} enviou {path.name}"
    )
    return doc.to_dict()


def atualizar_documento(doc_id: str, new_filepath: str) -> dict:
    """
    Atualiza um documento existente com novo arquivo.
    Registra histórico da ação e envia notificação.
    """
    docs = listar_documentos()
    for i, d in enumerate(docs):
        if d["id"] == doc_id:
            path = Path(new_filepath)
            if not path.exists():
                raise FileNotFoundError("Arquivo não encontrado")
            ext = path.suffix.lower()
            if ext not in ALLOWED:
                raise ValueError("Tipo de arquivo não permitido")

            d["filename"] = path.name
            d["filetype"] = mimetypes.guess_type(new_filepath)[0] or d["filetype"]
            d["status"] = "pending"
            if "history" not in d or d["history"] is None:
                d["history"] = []
            d["history"].append({"action": "updated", "at": datetime.datetime.utcnow().isoformat()})
            docs[i] = d
            write_json(DOCS_FILE, docs)
            notify_email("organizers@copapab.local", "Documento atualizado", f"Documento {doc_id} atualizado")
            return d
    raise KeyError("Documento não encontrado")


def validar_documento(doc_id: str, status: str, nota: str = "") -> dict:
    """
    Valida o documento, alterando seu status para 'approved', 'rejected' ou 'pending'.
    Salva histórico e notifica a jogadora via email.
    """
    if status not in ("approved", "rejected", "pending"):
        raise ValueError("Status inválido")

    docs = listar_documentos()
    for i, d in enumerate(docs):
        if d["id"] == doc_id:
            d["status"] = status
            if "history" not in d or d["history"] is None:
                d["history"] = []
            d["history"].append({
                "action": f"set_{status}",
                "note": nota,
                "at": datetime.datetime.utcnow().isoformat(),
            })
            docs[i] = d
            write_json(DOCS_FILE, docs)

            # Notifica jogadora
            jogadores = listar_jogadoras()
            jog = next((x for x in jogadores if x["id"] == d["jogadora_id"]), None)
            if jog:
                notify_email(jog["contato"], f"Documento {status}",
                             f"Seu documento {d['filename']} foi {status}. {nota}")
            return d
    raise KeyError("Documento não encontrado")


# =======================
# Funções de Times
# =======================

def listar_times():
    """
    Retorna todos os times cadastrados.
    """
    return read_json(TEAMS_FILE)


def criar_time(nome: str, integrantes: List[str]) -> dict:
    """
    Cria um time com nome e lista de jogadoras.
    """
    jogadores = listar_jogadoras()
    ids = {j["id"] for j in jogadores}
    for ig in integrantes:
        if ig not in ids:
            raise KeyError(f"Jogadora {ig} não encontrada")

    times = listar_times()
    t = Time(id=new_id(), nome=nome, integrantes=integrantes)
    times.append(t.to_dict())
    write_json(TEAMS_FILE, times)
    return t.to_dict()


def atualizar_time(time_id: str, nome: Optional[str], integrantes: Optional[List[str]]):
    """
    Atualiza nome ou integrantes de um time existente.
    """
    times = listar_times()
    for i, t in enumerate(times):
        if t["id"] == time_id:
            if nome and nome.strip():
                t["nome"] = nome.strip()
            if integrantes is not None:
                jogadores = listar_jogadoras()
                ids = {j["id"] for j in jogadores}
                for ig in integrantes:
                    if ig not in ids:
                        raise KeyError(f"Jogadora {ig} não encontrada")
                t["integrantes"] = integrantes
            times[i] = t
            write_json(TEAMS_FILE, times)
            return t
    raise KeyError("Time não encontrado")


def remover_time(time_id: str):
    """
    Remove um time pelo ID.
    """
    times = listar_times()
    novos = [t for t in times if t["id"] != time_id]
    if len(novos) == len(times):
        raise KeyError("Time não encontrado")
    write_json(TEAMS_FILE, novos)


# =======================
# Funções de Torneios e Inscrições
# =======================

def listar_torneios():
    """
    Retorna todos os torneios cadastrados.
    """
    return read_json(TOURNAMENTS_FILE)


def criar_torneio(nome: str, vagas: int) -> dict:
    """
    Cria um torneio com um número limitado de vagas.
    """
    tor = Torneio(id=new_id(), nome=nome, vagas=vagas, inscritos=[])
    ts = listar_torneios()
    ts.append(tor.to_dict())
    write_json(TOURNAMENTS_FILE, ts)
    return tor.to_dict()


def inscrever_time(torneio_id: str, time_id: str) -> dict:
    """
    Inscreve um time em um torneio.
    Se vagas estiverem preenchidas, status será 'waiting'.
    """
    torneios = listar_torneios()
    times = listar_times()
    inscricoes = read_json(INSCR_FILE)

    t = next((x for x in torneios if x["id"] == torneio_id), None)
    if not t:
        raise KeyError("Torneio não encontrado")
    if not any(x["id"] == time_id for x in times):
        raise KeyError("Time não encontrado")

    confirmed = [i for i in inscricoes if i["torneio_id"] == torneio_id and i["status"] == "confirmed"]
    status = "confirmed" if len(confirmed) < t["vagas"] else "waiting"

    ins = Inscricao(id=new_id(), torneio_id=torneio_id, time_id=time_id, status=status)
    inscricoes.append(ins.to_dict())
    write_json(INSCR_FILE, inscricoes)
    return ins.to_dict()


# =======================
# OCR Simulado
# =======================

def simular_ocr(doc_id: str, texto: str) -> dict:
    """
    Simula a leitura de um documento (OCR) armazenando texto extraído.
    """
    cache = read_json(OCR_CACHE_FILE)
    cache.append({"doc_id": doc_id, "texto": texto})
    write_json(OCR_CACHE_FILE, cache)
    return {"doc_id": doc_id, "texto": texto}
