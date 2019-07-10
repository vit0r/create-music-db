# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship, backref
from database import Base


class Musica(Base):
    __tablename__ = 'Musica'
    Id = Column(String, primary_key=True)
    Nome = Column(String, nullable=False)
    ArtistaId = Column(String, ForeignKey('Artista.Id'))
    artista_rel = relationship('Artista', foreign_keys='Musica.ArtistaId')

    def __init__(self, musica):
        self.Id = musica.get('Id')
        self.Nome = musica.get('Nome')
        self.ArtistaId = musica.get('ArtistaId')

    def __repr__(self):
        return '<Musica %r>' % self.Id


class Artista(Base):
    __tablename__ = 'Artista'
    Id = Column(String, primary_key=True)
    Nome = Column(String, nullable=False)

    def __init__(self, artista):
        self.Id = artista.get('Id')
        self.Nome = artista.get('Nome')

    def __repr__(self):
        return '<Artista %r>' % self.Id
