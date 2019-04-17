from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class VideoObject(Base):

    __tablename__ = 'video_objects'

    id = Column(Integer, primary_key=True)
    video_name = Column(String)
    frame_id = Column(Integer)
    obj_1 = Column(String)
    obj_2 = Column(String)
    obj_3 = Column(String)
    obj_4 = Column(String)
    obj_5 = Column(String)
    obj_6 = Column(String)
    obj_7 = Column(String)
    obj_8 = Column(String)
    obj_9 = Column(String)
    obj_10 = Column(String)

    def __repr__(self):
        return f'<VideoObject(video={self.video_name}, frame_id={self.frame_id}, ' \
               f'top10=[{self.obj_1}, {self.obj_2}, {self.obj_3}, {self.obj_4}, {self.obj_5}, ' \
               f'{self.obj_6}, {self.obj_7}, {self.obj_8}, {self.obj_9}, {self.obj_10}])>'


class Conn:

    def __init__(self, db_path='sqlite:///db.sqlite'):
        self.engine = create_engine(db_path)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, vo):
        self.session.add(vo)
        self.session.commit()

    def close(self):
        self.session.close()
