"""create db 6

Revision ID: b6780863208a
Revises: d80939900dee
Create Date: 2023-07-24 02:24:57.050765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6780863208a'
down_revision = 'd80939900dee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish', sa.Column('submenu_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'dish', 'menu', ['submenu_id'], ['id'])
    op.add_column('submenu', sa.Column('menu_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'submenu', 'menu', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenu', type_='foreignkey')
    op.drop_column('submenu', 'menu_id')
    op.drop_constraint(None, 'dish', type_='foreignkey')
    op.drop_column('dish', 'submenu_id')
    # ### end Alembic commands ###
