import functions
import requests
import data_classes

from .manganelo_base import ManganeloBase

from web_scrapper.download_base import DownloadBase

from bs4 import BeautifulSoup


class Search(ManganeloBase):
	def __init__(self, title):
		super().__init__("panel_story_list", "story_item")

		self.url = functions.create_manganelo_search_url(title)

	def _extract(self):
		for i, ele in enumerate(self.soup):
			story_name = ele.find(class_="story_name").find(href=True)
			story_chap = ele.find(class_="story_chapter").find(href=True)

			row = data_classes.SearchResult()

			row.title = story_name.text
			row.desc = story_chap["title"]
			row.url = story_name["href"]

			if not row.url.startswith("http"):
				row.url = "http" + story_name["href"]

			self.results.append(row)


class ChapterList(ManganeloBase):
	def __init__(self, url: str):
		super().__init__("chapter-list", "row")

		self.url = url

	def _extract(self):
		for i, ele in enumerate(reversed(self.soup)):
			chapter = data_classes.MangaChapter()

			chapter.url = ele.find("a")["href"]
			chapter.chapter_num = functions.remove_trailing_zeros_if_zero(chapter.url.split("chapter_")[-1])

			if not ele.find("a")["href"].startswith("http"):
				chapter.url = "http" + ele.find("a")["href"]

			self.results.append(chapter)


class ChapterDownload(DownloadBase):
	def __init__(self, src_url, dst_path):
		super().__init__(src_url, dst_path)

	def get_image_urls(self):
		page = functions.send_request(self.src_url)

		if page:
			try:
				soup = BeautifulSoup(page.content, "html.parser")

				image_soup = soup.findAll("img")

				self.image_urls = list(map(lambda i: i["src"], image_soup))

			except (AttributeError, requests.ConnectionError):
				pass