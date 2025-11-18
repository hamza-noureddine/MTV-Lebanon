from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, unique=True, index=True)   # <── Add this
    title = Column(Text)
    url = Column(Text)
    date = Column(String)
    time = Column(String)
    text = Column(Text)
    category = Column(String)
    image = Column(Text)
    is_video = Column(Boolean, default=False)
    video_poster = Column(Text)
    video_url = Column(Text)
