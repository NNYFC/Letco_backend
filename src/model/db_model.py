from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, mapped_column

Base = declarative_base()


class Role(Base):
    __tablename__ = "letco_role"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    users = relationship('User', back_populates='role')

    def __repr__(self):
        return "<Role(id='%s', type='%s')>" % (
            self.id,
            self.type
        )


class User(Base):
    __tablename__ = "letco_user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pseudo = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    bluetooth = Column(String, nullable=False, unique=True)
    idrole = mapped_column(ForeignKey('letco_role.id'))
    role = relationship('Role', back_populates='users')
    competences = relationship('UserCompetence', back_populates='user', lazy=True)
    searches = relationship('UserSearch', back_populates='user', lazy=True)

    # def __repr__(self):
    #     return "<User(id='%s', name='%s', pseudo='%s', email='%s', password='%s', bluetooth='%s')>" % (
    #         self.id,
    #         self.name,
    #         self.pseudo,
    #         self.email,
    #         self.password,
    #         self.bluetooth
    #     )


class Competence(Base):
    __tablename__ = "letco_competence"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    user_competence = relationship('UserCompetence', back_populates='competence', lazy=True)
    user_search = relationship('UserSearch', back_populates='competence', lazy=True)

    def __repr__(self):
        return "<Competence'%s', type='%s', description='%s')>" % (
            self.id,
            self.type,
            self.description
        )


class UserCompetence(Base):
    __tablename__ = "user_competence"

    id = Column(Integer, primary_key=True)
    iduser = mapped_column(ForeignKey('letco_user.id'))
    user = relationship('User', back_populates='competences')
    idcompetence = mapped_column(ForeignKey('letco_competence.id'))
    competence = relationship('Competence', back_populates='user_competence')


class UserSearch(Base):
    __tablename__ = "user_search"

    id = Column(Integer, primary_key=True)
    iduser = mapped_column(ForeignKey('letco_user.id'))
    user = relationship('User', back_populates='searches')
    idcompetence = mapped_column(ForeignKey('letco_competence.id'))
    competence = relationship('Competence', back_populates='user_search')

