from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ColumnBase(BaseModel):
    name: str
    data_type: str
    is_primary_key: bool = False
    is_nullable: bool = True

class ColumnCreate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int
    table_id: int

    class Config:
        orm_mode = True

class TableBase(BaseModel):
    name: str
    x_position: int = 0
    y_position: int = 0

class TableCreate(TableBase):
    columns: List[ColumnCreate] = []

class Table(TableBase):
    id: int
    diagram_id: int
    columns: List[Column] = []

    class Config:
        orm_mode = True

class DiagramBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class DiagramCreate(DiagramBase):
    pass

class Diagram(DiagramBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    tables: List[Table] = []

    class Config:
        orm_mode = True

class DiagramExport(BaseModel):
    sql_ddl: str
    json_schema: dict
