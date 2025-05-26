from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
import os
from dotenv import load_dotenv

load_dotenv()

# Database Setup
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

def main():
    today_date = datetime.now().strftime("%B %d, %Y")

    stories_query = session.query(Story).all()

    stories = [
        {
            "title": s.title,
            "url": s.url,
            "image": s.image,
            "source": s.source,
            "snippet": s.snippet
        } for s in stories_query
    ]

    #Jinja2 environment to load templates from current folder
    env = Environment(loader=FileSystemLoader('.'))
    
    template = env.get_template('template.html')

    rendered_html = template.render(date=today_date, stories=stories)

    with open('index1.html', 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print("index1.html generated successfully!")

if __name__ == "__main__":
    main()
