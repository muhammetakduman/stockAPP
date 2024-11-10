"""remov private id

Revision ID: ce81fade7327
Revises: 3e7fefd00e11
Create Date: 2024-11-10 14:07:09.496962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce81fade7327'
down_revision = '3e7fefd00e11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('private_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('private_id', sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###