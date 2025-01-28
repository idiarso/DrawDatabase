import axios from 'axios';
import AuthService from './AuthService';

interface Column {
  name: string;
  data_type: string;
  is_primary_key?: boolean;
  is_nullable?: boolean;
}

interface Table {
  name: string;
  x_position?: number;
  y_position?: number;
  columns: Column[];
}

interface Diagram {
  id?: number;
  name: string;
  description?: string;
  is_public?: boolean;
  tables?: Table[];
}

class DiagramService {
  private static BASE_URL = '/api/diagrams';

  static async createDiagram(diagram: Diagram): Promise<Diagram> {
    try {
      const response = await axios.post(this.BASE_URL, diagram, {
        headers: {
          'Authorization': `Bearer ${AuthService.getToken()}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to create diagram', error);
      throw error;
    }
  }

  static async getDiagrams(skip = 0, limit = 100): Promise<Diagram[]> {
    try {
      const response = await axios.get(`${this.BASE_URL}/?skip=${skip}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${AuthService.getToken()}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch diagrams', error);
      throw error;
    }
  }

  static async addTableToDiagram(diagramId: number, table: Table): Promise<Table> {
    try {
      const response = await axios.post(`${this.BASE_URL}/${diagramId}/tables/`, table, {
        headers: {
          'Authorization': `Bearer ${AuthService.getToken()}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to add table to diagram', error);
      throw error;
    }
  }

  static async exportDiagram(diagramId: number) {
    try {
      const response = await axios.get(`${this.BASE_URL}/${diagramId}/export`, {
        headers: {
          'Authorization': `Bearer ${AuthService.getToken()}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to export diagram', error);
      throw error;
    }
  }
}

export default DiagramService;
export { Diagram, Table, Column };
