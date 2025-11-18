from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String, unique=True)
    date = Column(String)
    time = Column(String)
    text = Column(Text)
    category = Column(String)
    image = Column(String)
    is_video = Column(Boolean, default=False)
    video_poster = Column(String)
    video_url = Column(String)