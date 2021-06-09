import uuid

from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy import String, Text, Boolean, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from setting import settings

engine = create_engine(settings.MYSQL_SQLALCHEMY_DB_URI,
                       echo=False,
                       pool_size=50,
                       pool_recycle=7200,
                       max_overflow=10)
Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()


def gen_uuid() -> str:
    # 生成uuid
    # https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy?rq=1
    return uuid.uuid4().hex


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户表'}
    id = Column(Integer, autoincrement=True, nullable=False, unique=True, primary_key=True)
    uuid = Column(VARCHAR(32), default=gen_uuid, comment="用户uuid", primary_key=False)
    name = Column(String(128), nullable=True, comment="姓名")
    phone = Column(String(128), nullable=True, comment="手机号")
    avatar = Column(String(1024), nullable=True, comment="头像")
    gender = Column("gender", ENUM("male", "female"), comment="性别")
    salt = Column(String(128), nullable=True, comment="加密使用的salt")
    hashed_password = Column(Text, nullable=True, comment="加密之后的密码")
    email = Column(String(128), nullable=True, comment="邮箱")
    email_check = Column(Boolean, nullable=False, server_default="0", comment="邮箱认证")
    access_token = Column(Text, nullable=True, comment="access_token")

    last_login = Column(Integer, nullable=True, comment="上次登录")
    register_timestamp = Column(Integer, nullable=True, comment="注册时间")

    following = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers',
        lazy="dynamic",
    )

    follower = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.following_id,
        secondaryjoin=lambda: User.id == user_following.c.user_id,
        backref='followings',
        lazy="dynamic",
    )

    def __repr__(self):
        return '<id %r>' % self.uuid

    def format_dict(self):
        return dict(uuid=self.uuid,
                    name=self.name,
                    phone=self.phone,
                    email=self.email,
                    avatar=self.avatar,
                    )


user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
)


def init_db():
    Base.metadata.create_all(bind=engine)
