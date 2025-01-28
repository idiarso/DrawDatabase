import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AuthService from '../services/AuthService';

interface Invitation {
  id: number;
  diagram_id: number;
  invited_email: string;
  permission_level: 'view' | 'edit' | 'admin';
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
}

const Invitations: React.FC = () => {
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchInvitations();
  }, []);

  const fetchInvitations = async () => {
    try {
      const response = await axios.get('/api/invitations', {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });
      setInvitations(response.data);
    } catch (err) {
      setError('Failed to fetch invitations');
    }
  };

  const acceptInvitation = async (invitationId: number) => {
    try {
      await axios.post(`/api/invitations/${invitationId}/accept`, {}, {
        headers: { 'Authorization': `Bearer ${AuthService.getToken()}` }
      });
      
      // Remove the accepted invitation from the list
      setInvitations(invitations.filter(inv => inv.id !== invitationId));
      
      // Optionally redirect to the diagram or show a success message
      window.location.href = `/diagram/${invitationId}`;
    } catch (err) {
      setError('Failed to accept invitation');
    }
  };

  return (
    <div className="invitations-container">
      <h2>Diagram Invitations</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      {invitations.length === 0 ? (
        <p>No pending invitations</p>
      ) : (
        <div className="invitations-list">
          {invitations.map((invitation) => (
            <div key={invitation.id} className="invitation-item">
              <div className="invitation-details">
                <p>Invited to diagram</p>
                <p>Permission Level: {invitation.permission_level}</p>
                <p>Invited on: {new Date(invitation.created_at).toLocaleDateString()}</p>
              </div>
              <div className="invitation-actions">
                <button 
                  onClick={() => acceptInvitation(invitation.id)}
                  className="accept-button"
                >
                  Accept
                </button>
                <button 
                  onClick={() => {/* Implement reject logic */}}
                  className="reject-button"
                >
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Invitations;
