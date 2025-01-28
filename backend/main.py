from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import auth
import collaboration
from database import engine, SessionLocal, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schema Designer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.post("/diagrams/", response_model=schemas.Diagram)
def create_diagram(
    diagram: schemas.DiagramCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_diagram = models.Diagram(**diagram.dict(), owner_id=current_user.id)
    db.add(db_diagram)
    db.commit()
    db.refresh(db_diagram)
    return db_diagram

@app.get("/diagrams/", response_model=List[schemas.Diagram])
def read_diagrams(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    diagrams = db.query(models.Diagram).filter(
        (models.Diagram.owner_id == current_user.id) | 
        (models.Diagram.is_public == True)
    ).offset(skip).limit(limit).all()
    return diagrams

@app.post("/diagrams/{diagram_id}/tables/", response_model=schemas.Table)
def create_table_for_diagram(
    diagram_id: int, 
    table: schemas.TableCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Check if diagram exists and belongs to current user
    diagram = db.query(models.Diagram).filter(
        models.Diagram.id == diagram_id, 
        models.Diagram.owner_id == current_user.id
    ).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")
    
    # Create table
    db_table = models.Table(
        name=table.name, 
        diagram_id=diagram_id,
        x_position=table.x_position,
        y_position=table.y_position
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    
    # Create columns
    for column_data in table.columns:
        db_column = models.Column(
            name=column_data.name,
            data_type=column_data.data_type,
            is_primary_key=column_data.is_primary_key,
            is_nullable=column_data.is_nullable,
            table_id=db_table.id
        )
        db.add(db_column)
    
    db.commit()
    db.refresh(db_table)
    
    return db_table

@app.get("/diagrams/{diagram_id}/export", response_model=schemas.DiagramExport)
def export_diagram(
    diagram_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Check if diagram exists and belongs to current user or is public
    diagram = db.query(models.Diagram).filter(
        models.Diagram.id == diagram_id,
        ((models.Diagram.owner_id == current_user.id) | (models.Diagram.is_public == True))
    ).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")
    
    # Generate SQL DDL
    sql_ddl = generate_sql_ddl(diagram)
    
    # Generate JSON schema
    json_schema = generate_json_schema(diagram)
    
    return {
        "sql_ddl": sql_ddl,
        "json_schema": json_schema
    }

@app.post("/diagrams/{diagram_id}/invite", response_model=dict)
def invite_collaborator(
    diagram_id: int,
    invitation: schemas.InvitationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Invite a user to collaborate on a diagram
    """
    try:
        result = collaboration.invite_user_to_diagram(
            db, 
            diagram_id, 
            current_user.id, 
            invitation.invited_email, 
            invitation.permission_level
        )
        return result
    except HTTPException as e:
        raise e

@app.get("/diagrams/{diagram_id}/collaborators", response_model=List[dict])
def get_diagram_collaborators(
    diagram_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get all collaborators for a specific diagram
    """
    try:
        collaborators = collaboration.get_diagram_collaborators(
            db, 
            diagram_id, 
            current_user.id
        )
        return collaborators
    except HTTPException as e:
        raise e

@app.delete("/diagrams/{diagram_id}/collaborators/{collaborator_id}")
def remove_collaborator(
    diagram_id: int,
    collaborator_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Remove a collaborator from a diagram
    """
    try:
        result = collaboration.remove_collaborator(
            db, 
            diagram_id, 
            current_user.id, 
            collaborator_id
        )
        return result
    except HTTPException as e:
        raise e

@app.put("/diagrams/{diagram_id}/collaborators/{collaborator_id}/permission")
def update_collaborator_permission(
    diagram_id: int,
    collaborator_id: int,
    new_permission: schemas.PermissionLevelEnum,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Update a collaborator's permission level
    """
    try:
        result = collaboration.update_collaborator_permission(
            db, 
            diagram_id, 
            current_user.id, 
            collaborator_id, 
            new_permission
        )
        return result
    except HTTPException as e:
        raise e

@app.get("/invitations", response_model=List[schemas.Invitation])
def get_user_invitations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get all pending invitations for the current user
    """
    invitations = db.query(models.DiagramInvitation).filter(
        models.DiagramInvitation.invited_email == current_user.email,
        models.DiagramInvitation.status == models.InvitationStatus.PENDING
    ).all()
    
    return invitations

@app.post("/invitations/{invitation_id}/accept")
def accept_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Accept a diagram collaboration invitation
    """
    invitation = db.query(models.DiagramInvitation).filter(
        models.DiagramInvitation.id == invitation_id,
        models.DiagramInvitation.invited_email == current_user.email,
        models.DiagramInvitation.status == models.InvitationStatus.PENDING
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Create collaboration entry
    collaboration_entry = models.DiagramCollaboration(
        diagram_id=invitation.diagram_id,
        user_id=current_user.id,
        permission_level=invitation.permission_level
    )
    
    # Update invitation status
    invitation.status = models.InvitationStatus.ACCEPTED
    
    db.add(collaboration_entry)
    db.commit()
    
    return {"message": "Invitation accepted"}

def generate_sql_ddl(diagram):
    """Generate SQL DDL for a diagram"""
    ddl = []
    for table in diagram.tables:
        table_ddl = f"CREATE TABLE {table.name} (\n"
        columns = []
        primary_keys = []
        
        for column in table.columns:
            column_def = f"    {column.name} {column.data_type}"
            
            if not column.is_nullable:
                column_def += " NOT NULL"
            
            if column.is_primary_key:
                primary_keys.append(column.name)
            
            columns.append(column_def)
        
        # Add columns to table definition
        table_ddl += ",\n".join(columns)
        
        # Add primary key constraint if exists
        if primary_keys:
            table_ddl += f",\n    PRIMARY KEY ({', '.join(primary_keys)})"
        
        table_ddl += "\n);"
        ddl.append(table_ddl)
    
    return "\n\n".join(ddl)

def generate_json_schema(diagram):
    """Generate JSON schema representation of a diagram"""
    schema = {
        "name": diagram.name,
        "tables": []
    }
    
    for table in diagram.tables:
        table_schema = {
            "name": table.name,
            "columns": []
        }
        
        for column in table.columns:
            column_schema = {
                "name": column.name,
                "type": column.data_type,
                "nullable": column.is_nullable,
                "primary_key": column.is_primary_key
            }
            table_schema["columns"].append(column_schema)
        
        schema["tables"].append(table_schema)
    
    return schema

@app.get("/")
def read_root():
    return {"message": "Welcome to Schema Designer API"}
