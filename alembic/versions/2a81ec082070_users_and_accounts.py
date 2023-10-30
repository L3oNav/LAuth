"""Users and accounts

Revision ID: 2a81ec082070
Revises: 95359d944c5b
Create Date: 2023-10-28 01:24:33.690914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a81ec082070'
down_revision = '95359d944c5b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('accounts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('issuer', sa.String(length=32), nullable=False),
    sa.Column('subject', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
