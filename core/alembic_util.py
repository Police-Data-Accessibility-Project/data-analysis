import sqlalchemy as sa


def get_created_at_column_ddl(name: str = "created_at") -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(),
        nullable=False,
        default=sa.func.current_timestamp()
    )

def get_id_column_ddl() -> sa.Column:
    return sa.Column(
        'id',
        sa.Integer(),
        primary_key=True,
        index=True
    )

def get_url_id_column_ddl() -> sa.Column:
    return sa.Column(
        'url_id',
        sa.Integer(),
        sa.ForeignKey('urls.id'),
        nullable=False
    )

def get_enum_column_ddl(column_name: str, enum_name: str, values: list[str]) -> sa.Column:
    return sa.Column(
        column_name,
        sa.Enum(*values, name=enum_name),
        nullable=False
    )