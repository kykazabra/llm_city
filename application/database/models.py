from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

"""
Модуль для физического взаимодействия с БД
"""

Base = declarative_base()

class AgentProfile(Base):
    __tablename__ = 'agent_profile'

    id = sa.Column(sa.Integer, primary_key=True)
    nickname = sa.Column(sa.String(128), nullable=False)
    full_name = sa.Column(sa.String(256))
    bio = sa.Column(sa.String(512))
    avatar = sa.Column(sa.String(256))

    def __repr__(self):
        return f"AgentProfile(id={self.id}, nickname='{self.nickname}', full_name='{self.full_name}', bio='{self.bio}', avatar='{self.avatar}')"