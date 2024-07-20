from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

meme_platform_table = Table('meme_platform', Base.metadata,
    Column('meme_id', Integer, ForeignKey('meme.id')),
    Column('platform_id', Integer, ForeignKey('social_media_platform.id'))
)

creator_follower_table = Table('creator_follower', Base.metadata,
    Column('creator_id', Integer, ForeignKey('meme_creator.id')),
    Column('follower_id', Integer, ForeignKey('follower.id'))
)

class MemeCreator(Base):
    __tablename__ = 'meme_creator'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    memes = relationship('Meme', back_populates='creator')
    followers = relationship('Follower', secondary=creator_follower_table, back_populates='creators')

class Meme(Base):
    __tablename__ = 'meme'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('meme_creator.id'))
    creator = relationship('MemeCreator', back_populates='memes')
    platforms = relationship('SocialMediaPlatform', secondary=meme_platform_table, back_populates='memes')

class SocialMediaPlatform(Base):
    __tablename__ = 'social_media_platform'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    memes = relationship('Meme', secondary=meme_platform_table, back_populates='platforms')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creators = relationship('MemeCreator', secondary=creator_follower_table, back_populates='followers')

engine = create_engine('sqlite:///gen_z_fun.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

creator1 = MemeCreator(name="DankMaster")
creator2 = MemeCreator(name="LOLQueen")

meme1 = Meme(title="When you code all night", creator=creator1)
meme2 = Meme(title="React vs. Angular", creator=creator2)
meme3 = Meme(title="Python is love", creator=creator1)

platform1 = SocialMediaPlatform(name="Instagram")
platform2 = SocialMediaPlatform(name="TikTok")

follower1 = Follower(name="John Doe")
follower2 = Follower(name="Jane Smith")

meme1.platforms.extend([platform1, platform2])
meme2.platforms.append(platform1)
meme3.platforms.append(platform2)

creator1.followers.extend([follower1, follower2])
creator2.followers.append(follower1)

session.add_all([creator1, creator2, meme1, meme2, meme3, platform1, platform2, follower1, follower2])
session.commit()

for creator in session.query(MemeCreator).all():
    print(f"Meme Creator: {creator.name}")
    for meme in creator.memes:
        print(f" - Meme: {meme.title}")
    for follower in creator.followers:
        print(f" - Follower: {follower.name}")

for platform in session.query(SocialMediaPlatform).all():
    print(f"Platform: {platform.name}")
    for meme in platform.memes:
        print(f" - Meme: {meme.title}")

for follower in session.query(Follower).all():
    print(f"Follower: {follower.name}")
    for creator in follower.creators:
        print(f" - Follows: {creator.name}")
