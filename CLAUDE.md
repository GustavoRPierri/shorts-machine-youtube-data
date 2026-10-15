# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

YouTube channel scraper com duas fontes de dados:

- **YouTube Data API v3** (`ApiService`) — informações gerais de canal e vídeo: metadados, estatísticas e comentários via REST, usando `YOUTUBE_API_KEY` do `.env`.
- **yt-dlp** (`ScraperService`) — transcrições (legendas json3, manual > automática) e comentários completos com respostas aninhadas.

Salva um JSON por vídeo mais um `index.json` por canal. Code, comments, CLI flags, env vars and model field names are in **Portuguese** — keep new code consistent with that.

## Setup & running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # yt-dlp, python-dotenv, pydantic (v2)

# New layered code (src/) — modules import each other as top-level packages
# (`from service import ...`), so src/ must be on PYTHONPATH (VS Code sets this):
PYTHONPATH=src python src/controller/scrape_controller.py
```

Recent yt-dlp versions need a JS runtime (`deno`, `node` or `bun`) on PATH to solve YouTube challenges.

There are no tests, linter, or build configuration.

## Architecture

O projeto segue a arquitetura MVC, com camadas independentes em `src/`:

- **Models (`src/model/`)** — classes DTO, compostas apenas por atributos (getters/setters ou records). Hoje são models Pydantic v2 frozen.
- **Repository (`src/repository/`)** — classes DAO, responsáveis por persistir os DTOs no banco SQLite. A pasta ainda não existe.
- **Services (`src/service/`)** — dois papéis: classes que fazem as transações com as APIs e retornam JSON, e classes que convertem esse JSON para preencher os DTOs.
- **Controller (`src/controller/`)** — integra todas as outras camadas e orquestra o fluxo: primeiro as services que obtêm os dados, depois as services que convertem os dados em DTOs e, por fim, os DAOs que persistem.

Cada camada é independente e não chama nenhuma outra internamente. Só a Controller une as camadas.

### Estado atual

O código está no meio do refactor do script único para essas camadas, e ainda não segue a separação:

- **`src/service/`** — só existem services de obtenção; nenhuma service de conversão:
  - `ApiService` (YouTube Data API v3, `requests`): `get_canal`, `get_videos`, `get_comentarios`. Já mapeia a resposta para dicts com chaves em português, misturando obtenção e conversão — esse mapeamento deve migrar para uma service de conversão.
  - `ScraperService` (yt-dlp): `get_channel_playlist` (fixo nos 5 primeiros itens), `get_transcricao` (json3, manual > automática), `get_comentarios` (lista plana no formato yt-dlp).
  - `CrawlerService`: monta as URLs das abas `/videos` e `/shorts` a partir do handle.
- **`src/model/`** — models Pydantic v2 frozen (`ChannelModel`, `VideoModel`, `CommentModel`). Campos em português com **aliases nas chaves cruas do yt-dlp**, então dicts do yt-dlp entram direto em `Model.model_validate(info)`; `validate_by_name=True` aceita também os dicts em português do `ApiService`. `VideoModel` tem validator `before` que cai de `timestamp` para `upload_date`. As duas fontes de comentários retornam lista plana; o aninhamento em `respostas` ainda não existe em `src/` (referência: `aninhar_comentarios` em `main.py`).
- **`src/repository/`** — pasta criada, vazia. Nenhum DAO nem schema SQLite ainda.
- **`src/controller/scrape_controller.py`** — script solto (sem classe nem função) que liga crawler → scraper → `ChannelModel.model_validate` para um canal fixo. Faz a conversão direto, o que pela arquitetura alvo cabe a uma service de conversão.
- **Outros:** `src/config/youtube_api_schemas.py` tem constantes `PARAMETROS_*`/`CAMPOS_*` que **ninguém importa** (o `ApiService` repete os dicts inline, como pede `.claude/rules/coding-style.md`). `src/config/settings_config.py`, `src/util/logger_utils.py`, `src/views/` e `src/log/` estão vazios.

## Gotchas

- **Imports:** `src/__init__.py` usa imports relativos (`from .service import ...`), enquanto o resto de `src/` usa imports absolutos que dependem de `PYTHONPATH=src`. Não misture os dois estilos em código novo.
- **`.gitignore`:** ignora `__init__.py`, `.claude/` e `CLAUDE.md`. Os re-exports em `src/model/__init__.py` e `src/service/__init__.py` (e qualquer `__init__.py` novo, como o de `src/repository/`) não vão para o git enquanto essa regra existir.
- **Independência das camadas:** os `__init__.py` de pacote só re-exportam a própria camada. Nenhuma service, model ou DAO deve importar outra camada; só a controller importa tudo.
- **Efeitos no import:** `ApiService`, `ScraperService` e `CrawlerService` chamam `logging.basicConfig` ao serem importadas, e `ApiService`/`ScraperService` chamam `load_dotenv()` relativo ao diretório de trabalho (no `main.py`, relativo à pasta do script).
- **`ApiService`:** o construtor levanta `ValueError` se `YOUTUBE_API_KEY` não estiver no `.env`. `get_videos` usa `search.list`, que custa 100 unidades da cota diária (10.000); `get_videos` e `get_comentarios` buscam só 1 página (marcadas com `shortcut:`).
- **Comentários raiz:** as duas fontes marcam o comentário raiz com `pai`/`parent` = `"root"`, então o aninhamento pode tratar as duas da mesma forma.
