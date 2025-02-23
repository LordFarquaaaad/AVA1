"""Fix foreign key reference

Revision ID: 5d42bf561303
Revises: 
Create Date: 2025-02-12 12:08:24.295890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d42bf561303'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('enrollment_year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_submission',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('assignment_id', sa.String(), nullable=True),
    sa.Column('student_id', sa.String(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_submission')
    op.drop_table('grades')
    op.drop_table('students')
    op.drop_table('course')
    op.drop_table('assignment')
    # ### end Alembic commands ###
