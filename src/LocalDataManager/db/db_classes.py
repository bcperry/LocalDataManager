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
    file_metadata: Mapped[List["Metadata"]] = relationship(back_populates="file")

    def __repr__(self) -> str:
        return f"File(hash={self.hash!r}, name={self.name!r}, location={self.location!r}, metadata={self.file_metadata!r})"
    

class Metadata(Base):
    __tablename__ = "file_metadata"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hash: Mapped[str] = mapped_column(ForeignKey("files.hash"))
    file: Mapped["File"] = relationship(back_populates="file_metadata")
    metadata_key: Mapped[Optional[str]] 
    metadata_value: Mapped[Optional[str]]


    def __repr__(self) -> str:
        return f"Metadata(hash={self.hash!r}, key={self.metadata_key!r}, value={self.metadata_value!r})"