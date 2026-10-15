---
name: discord-status
description: Posta status no canal do Discord mencionando o role do agente (techlead, writer ou qa). Use quando um agente precisar comunicar progresso no fluxo de mudança.
---

Args: `<agente> <mensagem>` — agente é `techlead`, `writer` ou `qa`.

```bash
set -a && source .env && set +a

case "$AGENTE" in
  techlead) ROLE_ID="$CLAUDE_DISCORD_ROLE_TECHLEAD" ;;
  writer)   ROLE_ID="$CLAUDE_DISCORD_ROLE_WRITER" ;;
  qa)       ROLE_ID="$CLAUDE_DISCORD_ROLE_QA" ;;
esac

curl -s -X POST "https://discord.com/api/v10/channels/${CLAUDE_DISCORD_CHANNEL_ID}/messages" \
  -H "Authorization: Bot ${CLAUDE_DISCORD_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"<@&${ROLE_ID}> ${MENSAGEM}\"}"
```
