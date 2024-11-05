from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '407eec0194b8'
down_revision = 'aa67dc8a19b9'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # URLs a insertar en los primeros 4 registros
    urls = [
        "https://www.lanacion.com.ar/resizer/v2/la-casa-austral-gano-un-premio-internacional-como-RF74XA7U2BAW3MANZMC3WXVOYU.JPG?auth=908de4664be6f87d9a4910b8a8b6e7e5451087edec90c7dfbeef3e3e6772ce79&width=880&height=586&quality=70&smart=true",
        "https://www.portaldearquitectos.com/uploads/prop_properties/estudio-de-arquitectura-leone-loray-arquitectos-casa-austral-C-171-018-05.jpg",
        "https://media.istockphoto.com/id/1198218812/es/foto/moderna-casa-de-dos-pisos-y-patio-delantero-en-buenos-aires.jpg?s=2048x2048&w=is&k=20&c=KRpOx2uw6zHohBy_DTOM6RSkSV2q3tLkCkxZFuVe8-k=",
        "https://media.istockphoto.com/id/2157153934/es/foto/vista-frontal-de-la-casa-moderna-con-piscina-y-jard%C3%ADn-delantero.jpg?s=2048x2048&w=is&k=20&c=oAAs15nPrFkJnu3u_BMf7nf2nACZRbh-3Cp2F4P8yF0="
    ]

    for i, url in enumerate(urls, start=1):
        connection.execute(
            sa.text(f"UPDATE image SET url = :url WHERE id = :id"),
            {"url": url, "id": i}
        )


def downgrade():
    connection = op.get_bind()

    for i in range(1, 5):
        connection.execute(
            sa.text(f"UPDATE image SET url = '' WHERE id = :id"),
            {"id": i}
        )
