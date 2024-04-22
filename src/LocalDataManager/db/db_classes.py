from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = "files"
    hash: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    location: Mapped[Optional[str]]
    # metadata: Mapped[List["Metadata"]] = relationship(
    #     back_populates="file", cascade="all, delete-orphan"
    # )
    def __repr__(self) -> str:
        return f"File(hash={self.hash!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Metadata(Base):
#     __tablename__ = "metadata"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     file: Mapped["File"] = relationship(back_populates="metadata")
#     def __repr__(self) -> str:
#         return f"Metadata(id={self.id!r}, email_address={self.email_address!r})"