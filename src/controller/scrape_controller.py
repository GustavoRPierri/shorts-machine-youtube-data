from service import ApiService, ScraperService, ConversorService
from model import ChannelModel, VideoModel, CommentModel

api = ApiService()
scraper = ScraperService()
conversor = ConversorService()

canal_dados = api.get_canal("@renatocariani")
canal = conversor.obter_dados(canal_dados, ChannelModel)

print("Nome:", canal.nome)
print("Handle:", canal.handle)
print("ID:", canal.id)
print("Inscritos:", canal.inscritos)
print("Vídeos:", canal.qtd_videos)
print("Visualizações totais:", canal.qtd_visualizacoes)
print("Tags:", canal.tags)

videos_dados = api.get_videos(canal.id)
videos = conversor.obter_lista(videos_dados, VideoModel)

if videos:
    for v in videos:
        print(f"[{v.id}] {v.nome} | {v.duracao} | {v.views} views | {v.data_postagem.date()}")
        comentarios_dados = api.get_comentarios(v.id)
        comentarios = conversor.obter_lista(comentarios_dados, CommentModel)
        v.comentarios = comentarios        
        for c in v.comentarios:
            prefixo = "  ↳" if c.pai != "root" else "•"
            print(f"{prefixo} {c.autor}: {c.texto[:80]} ({c.likes} likes)")
