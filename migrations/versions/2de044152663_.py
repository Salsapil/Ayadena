"""empty message

Revision ID: 2de044152663
Revises: b9be48a25bf8
Create Date: 2024-06-12 14:48:23.671372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2de044152663'
down_revision = 'b9be48a25bf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('course_category',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('product_category',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('cat_id')
    )
    op.create_table('subscription_plan',
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('plan_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('UserRole',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('role_id', 'user_id')
    )
    op.create_table('course',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.String(length=255), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cat_id'], ['course_category.cat_id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('learner_plan',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('learner_id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['learner_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['subscription_plan.plan_id'], ),
    sa.PrimaryKeyConstraint('pk_id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('block_no', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=False),
    sa.Column('city', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('postal_code', sa.Integer(), nullable=False),
    sa.Column('order_compelete', sa.Boolean(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('seller',
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('national_id', sa.String(length=255), nullable=False),
    sa.Column('bank_acc', sa.String(length=80), nullable=False),
    sa.Column('postal_code', sa.Integer(), nullable=False),
    sa.Column('brand_name', sa.String(length=80), nullable=False),
    sa.Column('units_sold', sa.String(length=80), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.Column('unpaid_balance', sa.Integer(), nullable=True),
    sa.Column('paid_balance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seller_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('seller_id')
    )
    op.create_table('user_event',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('pk_id')
    )
    op.create_table('learner_course',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('learner_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.ForeignKeyConstraint(['learner_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('pk_id')
    )
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('card_name', sa.String(length=255), nullable=False),
    sa.Column('card_number', sa.Integer(), nullable=False),
    sa.Column('exp_month', sa.String(length=255), nullable=False),
    sa.Column('exp_year', sa.Integer(), nullable=False),
    sa.Column('cvv', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(asdecimal=True), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cat_id'], ['product_category.cat_id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['seller.seller_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('video',
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('video', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.PrimaryKeyConstraint('video_id')
    )
    op.create_table('order_product',
    sa.Column('pk_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.PrimaryKeyConstraint('pk_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_product')
    op.drop_table('video')
    op.drop_table('product')
    op.drop_table('payment')
    op.drop_table('learner_course')
    op.drop_table('user_event')
    op.drop_table('seller')
    op.drop_table('order')
    op.drop_table('learner_plan')
    op.drop_table('course')
    op.drop_table('UserRole')
    op.drop_table('user')
    op.drop_table('subscription_plan')
    op.drop_table('product_category')
    op.drop_table('event')
    op.drop_table('course_category')
    op.drop_table('admin')
    # ### end Alembic commands ###
