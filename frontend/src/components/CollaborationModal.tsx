import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AuthService from '../services/AuthService';

interface Collaborator {
  user_id: number;
  username: string;
  email: string;
  permission_level: 'view' | 'edit' | 'admin';
}

interface CollaborationModalProps {
  diagramId: number;
  onClose: () => void;
}

const CollaborationModal: React.FC<CollaborationModalProps> = ({ diagramId, onClose }) => {
  const [collaborators, setCollaborators] = useState<Collaborator[]>([]);
  const [inviteEmail, setInviteEmail] = useState('');
  const [permissionLevel, setPermissionLevel] = useState<'view' | 'edit' | 'admin'>('view');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCollaborators();
  }, [diagramId]);

  const fetchCollaborators = async () => {
    try {
      const response = await axios.get(`/api/diagrams/${diagramId}/collaborators`, {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });
      setCollaborators(response.data);
    } catch (err) {
      setError('Failed to fetch collaborators');
    }
  };

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await axios.post(`/api/diagrams/${diagramId}/invite`, {
        invited_email: inviteEmail,
        permission_level: permissionLevel
      }, {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });

      setInviteEmail('');
      fetchCollaborators();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to invite collaborator');
    }
  };

  const removeCollaborator = async (collaboratorId: number) => {
    try {
      await axios.delete(`/api/diagrams/${diagramId}/collaborators/${collaboratorId}`, {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });
      fetchCollaborators();
    } catch (err) {
      setError('Failed to remove collaborator');
    }
  };

  const updatePermission = async (collaboratorId: number, newPermission: 'view' | 'edit' | 'admin') => {
    try {
      await axios.put(`/api/diagrams/${diagramId}/collaborators/${collaboratorId}/permission`, 
        { new_permission: newPermission },
        {
          headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
        }
      );
      fetchCollaborators();
    } catch (err) {
      setError('Failed to update permission');
    }
  };

  return (
    <div className="collaboration-modal">
      <div className="modal-content">
        <h2>Diagram Collaboration</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleInvite} className="invite-form">
          <input 
            type="email" 
            placeholder="Enter email to invite" 
            value={inviteEmail}
            onChange={(e) => setInviteEmail(e.target.value)}
            required
          />
          <select 
            value={permissionLevel}
            onChange={(e) => setPermissionLevel(e.target.value as 'view' | 'edit' | 'admin')}
          >
            <option value="view">View</option>
            <option value="edit">Edit</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit">Invite</button>
        </form>

        <div className="collaborators-list">
          <h3>Current Collaborators</h3>
          {collaborators.map((collaborator) => (
            <div key={collaborator.user_id} className="collaborator-item">
              <span>{collaborator.username} ({collaborator.email})</span>
              <select 
                value={collaborator.permission_level}
                onChange={(e) => updatePermission(
                  collaborator.user_id, 
                  e.target.value as 'view' | 'edit' | 'admin'
                )}
              >
                <option value="view">View</option>
                <option value="edit">Edit</option>
                <option value="admin">Admin</option>
              </select>
              <button onClick={() => removeCollaborator(collaborator.user_id)}>
                Remove
              </button>
            </div>
          ))}
        </div>

        <button onClick={onClose} className="close-button">Close</button>
      </div>
    </div>
  );
};

export default CollaborationModal;
