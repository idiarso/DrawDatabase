from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class PermissionLevel(enum.Enum):
    VIEW = "view"
    EDIT = "edit"
    ADMIN = "admin"

class InvitationStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    diagrams = relationship("Diagram", back_populates="owner")
    collaborations = relationship("DiagramCollaboration", back_populates="user")

class Diagram(Base):
    __tablename__ = "diagrams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="diagrams")
    tables = relationship("Table", back_populates="diagram")
    collaborations = relationship("DiagramCollaboration", back_populates="diagram")

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    diagram_id = Column(Integer, ForeignKey("diagrams.id"))
    x_position = Column(Integer)
    y_position = Column(Integer)

    diagram = relationship("Diagram", back_populates="tables")
    columns = relationship("Column", back_populates="table")

class Column(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    data_type = Column(String)
    is_primary_key = Column(Boolean, default=False)
    is_nullable = Column(Boolean, default=True)
    table_id = Column(Integer, ForeignKey("tables.id"))

    table = relationship("Table", back_populates="columns")

class DiagramCollaboration(Base):
    __tablename__ = "diagram_collaborations"

    id = Column(Integer, primary_key=True, index=True)
    diagram_id = Column(Integer, ForeignKey("diagrams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_level = Column(Enum(PermissionLevel), default=PermissionLevel.VIEW)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    diagram = relationship("Diagram", back_populates="collaborations")
    user = relationship("User", back_populates="collaborations")

class DiagramInvitation(Base):
    __tablename__ = "diagram_invitations"

    id = Column(Integer, primary_key=True, index=True)
    diagram_id = Column(Integer, ForeignKey("diagrams.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invited_email = Column(String, nullable=False)
    permission_level = Column(Enum(PermissionLevel), default=PermissionLevel.VIEW)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    diagram = relationship("Diagram")
    inviter = relationship("User", foreign_keys=[inviter_id])
