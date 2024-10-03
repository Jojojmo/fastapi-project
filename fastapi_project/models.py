from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, func
from sqlalchemy.orm import registry, Mapped, mapped_column, relationship
from typing import Optional, List

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int]  = mapped_column(init=False, primary_key=True )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now())
    #children: Mapped[List["Model"]] = relationship()


# Tabela de associação para Collection e Document (opcional)
collection_document_association = Table(
    "collection_document_association",
    table_registry.metadata,
    Column("collection_id", ForeignKey("collections.id"), primary_key=True),
    Column("document_id", ForeignKey("documents.id"), primary_key=True)
)

@table_registry.mapped_as_dataclass
class Document:
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    topic: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relação Many-to-Many com Collection, opcional
    collections: Mapped[Optional[List["Collection"]]] = relationship(
        secondary=collection_document_association,
        back_populates="documents",
        default_factory=list
    )


@table_registry.mapped_as_dataclass
class Collection:
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relação Many-to-Many com Document, opcional
    documents: Mapped[Optional[List["Document"]]] = relationship(
        secondary=collection_document_association,
        back_populates="collections",
        default_factory=list
    )