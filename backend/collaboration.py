from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
import models
import schemas
import auth
from email_service import EmailService
import os

def invite_user_to_diagram(
    db: Session, 
    diagram_id: int, 
    inviter_user_id: int, 
    invited_email: str, 
    permission_level: str = 'view'
):
    """
    Invite a user to collaborate on a diagram
    Permission levels: 'view', 'edit', 'admin'
    """
    # Ambil informasi diagram dan pengguna yang mengundang
    diagram = db.query(models.Diagram).filter(models.Diagram.id == diagram_id).first()
    inviter = db.query(models.User).filter(models.User.id == inviter_user_id).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram tidak ditemukan")
    
    # Cek apakah pengguna sudah terdaftar
    invited_user = db.query(models.User).filter(models.User.email == invited_email).first()
    
    if not invited_user:
        # Buat undangan
        invitation = models.DiagramInvitation(
            diagram_id=diagram_id,
            inviter_id=inviter_user_id,
            invited_email=invited_email,
            permission_level=permission_level,
            status='pending'
        )
        
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        
        # Kirim email undangan
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        invitation_link = f"{frontend_url}/invitations/{invitation.id}"
        
        EmailService.send_invitation_email(
            to_email=invited_email, 
            diagram_name=diagram.name, 
            inviter_name=inviter.username,
            invitation_link=invitation_link
        )
        
        return {
            "message": "Undangan terkirim", 
            "invitation_id": invitation.id
        }
    
    # Create collaboration entry
    collaboration = models.DiagramCollaboration(
        diagram_id=diagram_id,
        user_id=invited_user.id,
        permission_level=permission_level
    )
    
    db.add(collaboration)
    db.commit()
    db.refresh(collaboration)
    
    return {"message": "User added to diagram"}

def get_diagram_collaborators(
    db: Session, 
    diagram_id: int, 
    current_user_id: int
):
    """
    Get all collaborators for a specific diagram
    """
    # Check if user has access to the diagram
    diagram = db.query(models.Diagram).filter(
        models.Diagram.id == diagram_id,
        (models.Diagram.owner_id == current_user_id)
    ).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")
    
    # Fetch collaborators
    collaborators = db.query(models.DiagramCollaboration, models.User).join(
        models.User, models.DiagramCollaboration.user_id == models.User.id
    ).filter(
        models.DiagramCollaboration.diagram_id == diagram_id
    ).all()
    
    return [
        {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "permission_level": collab.permission_level
        } for collab, user in collaborators
    ]

def remove_collaborator(
    db: Session, 
    diagram_id: int, 
    current_user_id: int, 
    collaborator_id: int
):
    """
    Remove a collaborator from a diagram
    """
    # Check if current user is the diagram owner
    diagram = db.query(models.Diagram).filter(
        models.Diagram.id == diagram_id, 
        models.Diagram.owner_id == current_user_id
    ).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")
    
    # Remove collaboration entry
    collaboration = db.query(models.DiagramCollaboration).filter(
        models.DiagramCollaboration.diagram_id == diagram_id,
        models.DiagramCollaboration.user_id == collaborator_id
    ).first()
    
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    db.delete(collaboration)
    db.commit()
    
    return {"message": "Collaborator removed successfully"}

def update_collaborator_permission(
    db: Session, 
    diagram_id: int, 
    current_user_id: int, 
    collaborator_id: int, 
    new_permission_level: str
):
    """
    Update a collaborator's permission level
    """
    # Check if current user is the diagram owner
    diagram = db.query(models.Diagram).filter(
        models.Diagram.id == diagram_id, 
        models.Diagram.owner_id == current_user_id
    ).first()
    
    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")
    
    # Update collaboration entry
    collaboration = db.query(models.DiagramCollaboration).filter(
        models.DiagramCollaboration.diagram_id == diagram_id,
        models.DiagramCollaboration.user_id == collaborator_id
    ).first()
    
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    collaboration.permission_level = new_permission_level
    db.commit()
    
    return {
        "message": "Collaborator permission updated",
        "new_permission": new_permission_level
    }
