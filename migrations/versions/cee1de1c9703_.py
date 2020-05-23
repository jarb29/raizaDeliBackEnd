"""empty message

Revision ID: cee1de1c9703
Revises: 
Create Date: 2020-05-22 21:20:33.712025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cee1de1c9703'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('modelo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_programa', sa.String(length=100), nullable=False),
    sa.Column('numero_ot', sa.Integer(), nullable=True),
    sa.Column('cantiadUnidadesFabricarEnLaOt', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('nestic_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('modeloProduccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('modelo_produccion', sa.String(length=100), nullable=False),
    sa.Column('ot_produccion', sa.Integer(), nullable=True),
    sa.Column('cantidad_producir', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nestic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('programa_nestic', sa.String(length=100), nullable=False),
    sa.Column('numero_piezas_criticas', sa.Integer(), nullable=True),
    sa.Column('tiempo_corte', sa.Integer(), nullable=True),
    sa.Column('espesor', sa.Integer(), nullable=True),
    sa.Column('longitud_nestic', sa.Integer(), nullable=True),
    sa.Column('modelo_elegido', sa.String(length=100), nullable=True),
    sa.Column('pieza_id', sa.String(length=100), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nesticProduccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planchas_cortadas', sa.Integer(), nullable=True),
    sa.Column('ot_cortada', sa.Integer(), nullable=True),
    sa.Column('operador', sa.String(length=100), nullable=False),
    sa.Column('nestic_cortado', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('piezas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_pieza', sa.String(length=100), nullable=False),
    sa.Column('cantidadPiezasPorPlancha', sa.Integer(), nullable=True),
    sa.Column('crearLongitudCortePieza', sa.Integer(), nullable=True),
    sa.Column('nesticElegido', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('piezasIntegranProductoTerminado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ot_seleccionada', sa.Integer(), nullable=True),
    sa.Column('sub_producto_seleccionado', sa.String(length=100), nullable=False),
    sa.Column('producto_terminado_utilizado_estufa', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('piezasIntegranSubProducto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subProductoSeleccionado', sa.String(length=100), nullable=False),
    sa.Column('piezaSeleccionaIntegraSubproducto', sa.String(length=100), nullable=False),
    sa.Column('subProducto_ot_seleccionado', sa.Integer(), nullable=True),
    sa.Column('cantidad_utilizada_por_subproducto', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pintura',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pintura_ot_seleccionado', sa.Integer(), nullable=True),
    sa.Column('pinturaPiezaSeleccionada', sa.String(length=100), nullable=False),
    sa.Column('pinturaCantidadPiezas', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planProduccionMensual',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ot_en_produccion', sa.Integer(), nullable=True),
    sa.Column('estufas_plan_producc', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plegado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plegado_ot_seleccionado', sa.Integer(), nullable=True),
    sa.Column('plegadoPiezaSeleccionada', sa.String(length=100), nullable=False),
    sa.Column('plegadoMaquinaSeleccionada', sa.String(length=100), nullable=False),
    sa.Column('plegadoOperadorSeleccionado', sa.String(length=100), nullable=False),
    sa.Column('plegadoCantidadPiezas', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ot_seleccionada', sa.Integer(), nullable=True),
    sa.Column('sub_producto_seleccionado', sa.String(length=100), nullable=False),
    sa.Column('produccion_Cantidad_fabricada', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produccionProductoTerminado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ot_seleccionada', sa.Integer(), nullable=True),
    sa.Column('sub_producto_seleccionado', sa.String(length=100), nullable=False),
    sa.Column('producto_terminado_utilizado_estufa', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subproducto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Linea1NombreSubproducto', sa.String(length=100), nullable=False),
    sa.Column('subProducto_ot_seleccionado', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subproducto')
    op.drop_table('produccionProductoTerminado')
    op.drop_table('produccion')
    op.drop_table('plegado')
    op.drop_table('planProduccionMensual')
    op.drop_table('pintura')
    op.drop_table('piezasIntegranSubProducto')
    op.drop_table('piezasIntegranProductoTerminado')
    op.drop_table('piezas')
    op.drop_table('nesticProduccion')
    op.drop_table('nestic')
    op.drop_table('modeloProduccion')
    op.drop_table('modelo')
    # ### end Alembic commands ###