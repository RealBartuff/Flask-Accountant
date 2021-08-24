"""wplata

Revision ID: bbca573c3eff
Revises: 6fdedd9e82a4
Create Date: 2021-08-24 17:50:14.874926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = 'bbca573c3eff'
down_revision = '6fdedd9e82a4'
branch_labels = ()
depends_on = None


Base = declarative_base()


class History(Base):
    __tablename__ = "history"

    id = sa.Column(sa.Integer, primary_key=True)
    what_action = sa.Column(sa.String(12), unique=False)
    first_action = sa.Column(sa.Integer, unique=False)
    second_action = sa.Column(sa.String(120), unique=False)
    third_action = sa.Column(sa.Integer, unique=False)


class Account(Base):
    __tablename__ = "account"

    id = sa.Column(sa.Integer, primary_key=True)
    account = sa.Column(sa.Integer, unique=False, nullable=False)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    history = History(
            what_action="saldo",
            first_action=1000000,
            second_action="wplata wlasna",
            third_action=None
        )
    session.add(history)
    account = Account(account=1000000)
    session.add(account)
    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
