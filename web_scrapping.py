import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    url = Column(String(500), nullable=False)
    image = Column(String(500))
    source = Column(String(100), nullable=False)
    snippet = Column(Text)

Base.metadata.create_all(engine)

def fetch_space_com(top_n=2):
    url = "https://www.space.com/news"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("a.article-link")[:top_n]
    stories = []
    for card in cards:
        title = card.select_one("h3.article-name").get_text(strip=True)
        link = card["href"]
        snippet = card.select_one("p.synopsis").get_text(strip=True)
        img = card.select_one("div.image img")
        image_url = img["src"] if img else None

        stories.append({
            "title": title,
            "url": link,
            "snippet": snippet,
            "image": image_url,
            "source": "Space.com"
        })
    return stories

def fetch_phys_org(top_n=2):
    base_url = "https://phys.org"
    listing_url = f"{base_url}/space-news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(listing_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    link_tags = soup.select("h3.mb-1 a.news-link")[:top_n]
    stories = []
    for a in link_tags:
        href = a["href"]
        full_url = href if href.startswith("http") else f"{base_url}{href}"

        art_r = requests.get(full_url, headers=headers)
        art_r.raise_for_status()
        art_soup = BeautifulSoup(art_r.text, "html.parser")

        og_img = art_soup.select_one("meta[property='og:image']")
        image_url = og_img["content"] if og_img else None

        title = art_soup.select_one("meta[property='og:title']")["content"]
        snippet = art_soup.select_one("meta[name='description']")["content"]

        stories.append({
            "title": title,
            "url": full_url,
            "snippet": snippet,
            "image": image_url,
            "source": "Phys.org"
        })
    return stories


def save_to_db(story_list):
    for item in story_list:
        story = Story(
            title=item["title"],
            url=item["url"],
            image=item.get("image"),
            source=item["source"],
            snippet=item.get("snippet")
        )
        session.add(story)
    session.commit()


def main():
    # Clears old stories before adding new ones
    session.query(Story).delete()
    session.commit()
    print("Old stories deleted.")

    # Fetches new stories
    all_stories = fetch_space_com() + fetch_phys_org()

    # Saves new stories to database
    save_to_db(all_stories)
    print(f"{len(all_stories)} new stories processed and stored.")

if __name__ == "__main__":
    main()
