"""empty message

Revision ID: c552235f6967
Revises: ef3c58af741e
Create Date: 2022-03-21 14:53:58.715602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c552235f6967"
down_revision = "ef3c58af741e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sandbox", sa.Column("governance", sa.JSON(), nullable=True))
    op.add_column("sandbox", sa.Column("governance_cas", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sandbox", "governance")
    op.drop_column("sandbox", "governance_cas")
    # ### end Alembic commands ###
