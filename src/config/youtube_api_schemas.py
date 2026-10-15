# Parâmetros e campos da YouTube Data API v3.
# Importe estas constantes em ApiService para evitar strings soltas.

# ── channels.list ────────────────────────────────────────────────────────────

PARAMETROS_CANAL = {
    "part": "snippet,statistics,brandingSettings",
    # Campos retornados (economiza cota ao filtrar na API)
    "fields": (
        "items(id,"
        "snippet(title,description,customUrl,publishedAt,country,thumbnails),"
        "statistics(subscriberCount,videoCount,viewCount),"
        "brandingSettings(channel(keywords)))"
    ),
}

# Campos presentes em cada item de channels.list
CAMPOS_CANAL = {
    "id": "str — ID do canal (UCxxxx)",
    "snippet.title": "str — nome do canal",
    "snippet.description": "str — descrição",
    "snippet.customUrl": "str — handle (@usuario)",
    "snippet.publishedAt": "str ISO 8601 — data de criação",
    "snippet.country": "str | None — código do país",
    "snippet.thumbnails": "dict — miniaturas (default, medium, high)",
    "statistics.subscriberCount": "str — inscritos (oculto se canal omite)",
    "statistics.videoCount": "str — total de vídeos públicos",
    "statistics.viewCount": "str — total de visualizações",
    "brandingSettings.channel.keywords": "str — tags separadas por espaço",
}

# ── videos.list ──────────────────────────────────────────────────────────────

PARAMETROS_VIDEO = {
    "part": "snippet,statistics,contentDetails",
    "fields": (
        "items(id,"
        "snippet(title,description,publishedAt,channelId,channelTitle,tags,thumbnails),"
        "statistics(viewCount,likeCount,commentCount),"
        "contentDetails(duration,caption))"
    ),
}

CAMPOS_VIDEO = {
    "id": "str — ID do vídeo",
    "snippet.title": "str — título",
    "snippet.description": "str — descrição",
    "snippet.publishedAt": "str ISO 8601 — data de publicação",
    "snippet.channelId": "str — ID do canal dono",
    "snippet.channelTitle": "str — nome do canal",
    "snippet.tags": "list[str] | None — tags",
    "snippet.thumbnails": "dict — miniaturas",
    "statistics.viewCount": "str — visualizações",
    "statistics.likeCount": "str | None — likes (oculto se desativado)",
    "statistics.commentCount": "str | None — comentários (oculto se desativado)",
    "contentDetails.duration": "str ISO 8601 duration — ex: PT1H2M3S",
    "contentDetails.caption": "str — 'true'/'false'",
}

# ── commentThreads.list ──────────────────────────────────────────────────────

PARAMETROS_COMENTARIOS = {
    "part": "snippet",
    # maxResults máximo permitido pela API é 100
    "maxResults": 100,
    "order": "relevance",  # ou "time"
    "fields": (
        "nextPageToken,"
        "items(id,"
        "snippet(topLevelComment(id,snippet(authorDisplayName,authorChannelId,"
        "textDisplay,likeCount,publishedAt,updatedAt)),totalReplyCount))"
    ),
}

CAMPOS_COMENTARIO = {
    "id": "str — ID do thread de comentário",
    "snippet.topLevelComment.id": "str — ID do comentário raiz",
    "snippet.topLevelComment.snippet.authorDisplayName": "str — nome do autor",
    "snippet.topLevelComment.snippet.authorChannelId.value": "str — ID do canal do autor",
    "snippet.topLevelComment.snippet.textDisplay": "str — texto (pode conter HTML)",
    "snippet.topLevelComment.snippet.likeCount": "int — likes no comentário",
    "snippet.topLevelComment.snippet.publishedAt": "str ISO 8601",
    "snippet.topLevelComment.snippet.updatedAt": "str ISO 8601",
    "snippet.totalReplyCount": "int — número de respostas",
    "nextPageToken": "str | None — token para próxima página",
}

# ── comments.list (respostas) ────────────────────────────────────────────────

PARAMETROS_RESPOSTAS = {
    "part": "snippet",
    "maxResults": 100,
    "fields": (
        "nextPageToken,"
        "items(id,"
        "snippet(authorDisplayName,authorChannelId,textDisplay,"
        "likeCount,publishedAt,updatedAt,parentId))"
    ),
}

CAMPOS_RESPOSTA = {
    "id": "str — ID da resposta",
    "snippet.authorDisplayName": "str",
    "snippet.authorChannelId.value": "str",
    "snippet.textDisplay": "str",
    "snippet.likeCount": "int",
    "snippet.publishedAt": "str ISO 8601",
    "snippet.updatedAt": "str ISO 8601",
    "snippet.parentId": "str — ID do comentário pai",
    "nextPageToken": "str | None",
}
