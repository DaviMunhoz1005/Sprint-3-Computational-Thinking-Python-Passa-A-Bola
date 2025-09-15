# 📖 Plataforma Copa PAB – CLI

Este projeto implementa uma plataforma de gerenciamento da Copa PAB em Python, com suporte a jogadoras, times, torneios e inscrições.
Todos os dados são armazenados em arquivos **JSON** dentro da pasta `data/`.

## 🔧 Instalação

Clone o repositório ou copie os arquivos, e certifique-se de ter **Python 3.9+** instalado.
No terminal, rode:

```bash
  python main.py -h
```

Isso mostrará o menu principal.

## 📂 Estrutura de Comandos
### 1. 👩 Jogadoras

Gerenciar jogadoras (CRUD básico).

**Listar todas**

```bash
  python main.py jogadora listar
```

**Criar nova jogadora**

```bash
python main.py jogadora criar "Maria Silva" 22 "maria@gmail.com"
```

`nome` → Nome completo

`idade` → Idade (int)

`contato` → Email ou telefone

**Exemplo de saída (JSON):**

```json
{
  "id": "jog-123",
  "nome": "Maria Silva",
  "idade": 22,
  "contato": "maria@gmail.com"
}
```

### 2. 🏆 Times

Times são compostos por jogadoras já cadastradas.

**Listar todos os times**

```bash
    python main.py time listar
```

**Criar novo time**

```bash
  python main.py time criar "As Panteras" jog-123 jog-456
```

`nome` → Nome do time

`integrantes` → IDs das jogadoras (obtidos com `jogadora listar`)

### 3. ⚽ Torneios

Gerenciar torneios disponíveis.

**Listar torneios**

```bash
    python main.py torneio listar
```

**Criar torneio**

```bash
  python main.py torneio criar "Copa Feminina 2025" 4
```

`nome` → Nome do torneio

`vagas` → Número de vagas (times)

### 4. 📝 Inscrições

Permite inscrever times em torneios.

**Inscrever time em torneio**

```
python main.py inscrever <torneio_id> <time_id>
```


`torneio_id` → ID de um torneio (veja com torneio listar)

`time_id` → ID de um time (veja com time listar)

Se houver vaga disponível, status será **confirmed**.

Se não houver, status será **waiting** (lista de espera).

## 🚀 Fluxo de Exemplo Completo
### 1. Criar duas jogadoras

```bash
  python main.py jogadora criar "Maria Silva" 22 "maria@gmail.com"
  python main.py jogadora criar "Ana Costa" 24 "ana@gmail.com"
```

### 2. Listar jogadoras e anotar IDs

```bash
  python main.py jogadora listar
```

### 3. Criar um time com essas jogadoras

```bash
  python main.py time criar "As Panteras" jog-001 jog-002
```

### 4. Criar torneio

```bash
    python main.py torneio criar "Copa Feminina 2025" 4
```

### 5. Listar torneios e pegar ID

```bash
    python main.py torneio listar
```

### 6. Inscrever o time no torneio

```bash
    python main.py inscrever tor-001 time-001
```

## 📂 Estrutura de Dados (JSON)

Os dados ficam na pasta `data/`:

`jogadoras.json` → Jogadoras

`times.json` → Times

`torneios.json` → Torneios

`inscricoes.json` → Inscrições

## 📌 Observações

IDs (`jog-001`, `time-001`, `tor-001`) são gerados automaticamente.

Contato pode ser **telefone** ou **email**.

Se um torneio lotar, novas inscrições ficam na **lista de espera**.

Todos os comandos retornam saída em JSON.