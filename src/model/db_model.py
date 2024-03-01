from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, mapped_column

Base = declarative_base()


class Role(Base):
    __tablename__ = "letco_role"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    users = relationship('User', back_populates='role', lazy=True)

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

    def __repr__(self):
        return "<User(id='%s', name='%s', pseudo='%s', email='%s', password='%s', bluetooth='%s', role='%s')>" % (
            self.id,
            self.name,
            self.pseudo,
            self.email,
            self.password,
            self.bluetooth,
            self.role
        )


class Competence(Base):
    __tablename__ = "letco_competence"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return "<User(id='%s', type='%s', description='%s')>" % (
            self.id,
            self.type,
            self.description
        )


class UserCompetence(Base):
    __tablename__ = "user_competence"

    id = Column(Integer, primary_key=True)
    iduser = mapped_column(ForeignKey('letco_user.id'))
    user = relationship('User', back_populates='competences')

    # def __repr__(self):
    #     return "<User(id='%s', type='%s', description='%s')>" % (
    #         self.id,
    #         self.type,
    #         self.description
    #     )


class UserSearch(Base):
    __tablename__ = "user_search"

    id = Column(Integer, primary_key=True)
    iduser = mapped_column(ForeignKey('letco_user.id'))
    user = relationship('User', back_populates='competences')

    # def __repr__(self):
    #     return "<User(id='%s', type='%s', description='%s')>" % (
    #         self.id,
    #         self.type,
    #         self.description
    #     )

