"""empty message

Revision ID: 1545d5be1ba0
Revises: 2de044152663
Create Date: 2024-06-23 09:45:02.253158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1545d5be1ba0'
down_revision = '2de044152663'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('cat_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('cat_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###