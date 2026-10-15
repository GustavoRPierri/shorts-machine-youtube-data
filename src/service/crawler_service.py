import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("crawler")

class CrawlerService:
    def __init__(self, canal: str):
        self.canal = canal.lstrip("@") # Remove o "@" do nome do canal

    def get_videos_url(self) -> str:
        url = f"https://www.youtube.com/@{self.canal}/videos"
        log.info(f"Videos URL: {url}")
        return url

    def get_shorts_url(self) -> str:
        url = f"https://www.youtube.com/@{self.canal}/shorts"
        log.info(f"Shorts URL: {url}")
        return url