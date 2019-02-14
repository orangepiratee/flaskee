# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TMessage(Base):
    __tablename__ = 't_message'

    message_id = Column(INTEGER(11), primary_key=True)
    message_content = Column(Text, nullable=False)
    message_datetime = Column(DateTime, nullable=False)
    message_delete = Column(INTEGER(11), server_default=text("'0'"))


class TRole(Base):
    __tablename__ = 't_role'

    role_id = Column(INTEGER(11), primary_key=True)
    role_name = Column(String(45))
    role_default = Column(TINYINT(4), server_default=text("'0'"))
    role_permission = Column(INTEGER(11))


class TUser(Base):
    __tablename__ = 't_user'

    user_id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_password = Column(String(128), nullable=False)
    user_available = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    user_department = Column(INTEGER(11), nullable=False)
    user_role = Column(INTEGER(11), nullable=False)
    user_regtime = Column(DateTime)
    user_lastlogtime = Column(DateTime)


class TItem(Base):
    __tablename__ = 't_item'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_category = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_author = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    item_read = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_accept = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_delete = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_attachment = Column(String(255))

    t_user = relationship('TUser')


class TMessageUser(Base):
    __tablename__ = 't_message_user'

    m_u_id = Column(INTEGER(11), primary_key=True)
    m_u_mid = Column(ForeignKey('t_message.message_id'), nullable=False, index=True)
    m_u_uid = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    m_u_read = Column(INTEGER(11), nullable=False)
    m_u_readtime = Column(DateTime, nullable=False)
    m_u_delete = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    t_message = relationship('TMessage')
    t_user = relationship('TUser')


class TComment(Base):
    __tablename__ = 't_comment'

    comment_id = Column(INTEGER(11), primary_key=True)
    comment_content = Column(Text, nullable=False)
    comment_author = Column(String(255), nullable=False, index=True)
    comment_author_name = Column(String(45), nullable=False)
    comment_target = Column(ForeignKey('t_item.item_id'), nullable=False, index=True)
    comment_datetime = Column(DateTime, nullable=False)

    t_item = relationship('TItem')
