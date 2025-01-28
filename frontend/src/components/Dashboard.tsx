import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DiagramService, { Diagram } from '../services/DiagramService';
import AuthService from '../services/AuthService';

const Dashboard: React.FC = () => {
  const [diagrams, setDiagrams] = useState<Diagram[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch current user
        const user = await AuthService.getCurrentUser();
        setUsername(user.username);

        // Fetch user's diagrams
        const userDiagrams = await DiagramService.getDiagrams();
        setDiagrams(userDiagrams);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleCreateNewDiagram = async () => {
    try {
      const newDiagram: Diagram = {
        name: `Diagram ${diagrams.length + 1}`,
        description: 'New database schema',
        is_public: false
      };

      const createdDiagram = await DiagramService.createDiagram(newDiagram);
      window.location.href = `/diagram/${createdDiagram.id}`;
    } catch (err) {
      setError('Failed to create new diagram');
    }
  };

  const handleExportDiagram = async (diagramId: number) => {
    try {
      const exportData = await DiagramService.exportDiagram(diagramId);
      
      // Create a downloadable file
      const sqlBlob = new Blob([exportData.sql_ddl], { type: 'text/sql' });
      const jsonBlob = new Blob([JSON.stringify(exportData.json_schema, null, 2)], { type: 'application/json' });
      
      // SQL Export
      const sqlLink = document.createElement('a');
      sqlLink.href = URL.createObjectURL(sqlBlob);
      sqlLink.download = 'schema_export.sql';
      sqlLink.click();
      
      // JSON Export
      const jsonLink = document.createElement('a');
      jsonLink.href = URL.createObjectURL(jsonBlob);
      jsonLink.download = 'schema_export.json';
      jsonLink.click();
    } catch (err) {
      setError('Failed to export diagram');
    }
  };

  const handleLogout = () => {
    AuthService.logout();
    window.location.href = '/login';
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard-container">
      <header>
        <h1>Welcome, {username}!</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>

      <div className="dashboard-actions">
        <button 
          onClick={handleCreateNewDiagram} 
          className="create-diagram-button"
        >
          Create New Diagram
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="diagrams-list">
        <h2>Your Diagrams</h2>
        {diagrams.length === 0 ? (
          <p>No diagrams created yet. Start by creating a new diagram!</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {diagrams.map((diagram) => (
                <tr key={diagram.id}>
                  <td>{diagram.name}</td>
                  <td>{diagram.description || 'No description'}</td>
                  <td>{new Date(diagram.created_at || '').toLocaleDateString()}</td>
                  <td>
                    <Link 
                      to={`/diagram/${diagram.id}`} 
                      className="edit-diagram-link"
                    >
                      Edit
                    </Link>
                    <button 
                      onClick={() => diagram.id && handleExportDiagram(diagram.id)}
                      className="export-diagram-button"
                    >
                      Export
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
