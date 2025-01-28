import React, { useState } from 'react';
import { fabric } from 'fabric';
import axios from 'axios';

interface Table {
  name: string;
  columns: Column[];
}

interface Column {
  name: string;
  type: string;
  constraints?: string[];
}

const SchemaDesigner: React.FC = () => {
  const [canvas, setCanvas] = useState<fabric.Canvas | null>(null);
  const [tables, setTables] = useState<Table[]>([]);

  React.useEffect(() => {
    const newCanvas = new fabric.Canvas('schema-canvas', {
      width: window.innerWidth,
      height: window.innerHeight,
      backgroundColor: '#f0f0f0'
    });
    setCanvas(newCanvas);
  }, []);

  const addTable = () => {
    const newTable: Table = {
      name: `Table_${tables.length + 1}`,
      columns: [{ name: 'id', type: 'INTEGER', constraints: ['PRIMARY KEY'] }]
    };
    setTables([...tables, newTable]);
  };

  const saveSchema = async () => {
    try {
      await axios.post('/schemas', { 
        name: 'My Schema', 
        tables 
      });
      alert('Schema saved successfully!');
    } catch (error) {
      console.error('Failed to save schema', error);
    }
  };

  return (
    <div>
      <div>
        <button onClick={addTable}>Add Table</button>
        <button onClick={saveSchema}>Save Schema</button>
      </div>
      <canvas id="schema-canvas" />
    </div>
  );
};

export default SchemaDesigner;
