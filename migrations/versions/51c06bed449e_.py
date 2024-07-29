from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '51c06bed449e'
down_revision = 'c925014a5218'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Allow NULL values temporarily
    with op.batch_alter_table('stores') as batch_op:
        batch_op.alter_column('order', existing_type=sa.Integer(), nullable=True)

    # Step 2: Update existing NULL values to a default value (e.g., 0)
    op.execute("UPDATE stores SET \"order\" = 0 WHERE \"order\" IS NULL")

    # Step 3: Set the column to NOT NULL
    with op.batch_alter_table('stores') as batch_op:
        batch_op.alter_column('order', existing_type=sa.Integer(), nullable=False)

def downgrade():
    # Reverse the changes made in the upgrade
    with op.batch_alter_table('stores') as batch_op:
        batch_op.alter_column('order', existing_type=sa.Integer(), nullable=True)
    op.execute("UPDATE stores SET \"order\" = NULL WHERE \"order\" = 0")
    with op.batch_alter_table('stores') as batch_op:
        batch_op.alter_column('order', existing_type=sa.Integer(), nullable=True)
