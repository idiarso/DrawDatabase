import axios from 'axios';

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterCredentials extends LoginCredentials {
  email: string;
}

interface User {
  id: number;
  username: string;
  email: string;
}

class AuthService {
  private static BASE_URL = '/api/auth';

  static async login(credentials: LoginCredentials): Promise<string> {
    try {
      const response = await axios.post(`${this.BASE_URL}/token`, {
        username: credentials.username,
        password: credentials.password
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      return access_token;
    } catch (error) {
      console.error('Login failed', error);
      throw error;
    }
  }

  static async register(credentials: RegisterCredentials): Promise<User> {
    try {
      const response = await axios.post(`${this.BASE_URL}/users/`, credentials);
      return response.data;
    } catch (error) {
      console.error('Registration failed', error);
      throw error;
    }
  }

  static logout(): void {
    localStorage.removeItem('token');
  }

  static isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }

  static getToken(): string | null {
    return localStorage.getItem('token');
  }

  static async getCurrentUser(): Promise<User> {
    try {
      const response = await axios.get(`${this.BASE_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${this.getToken()}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch current user', error);
      throw error;
    }
  }
}

export default AuthService;
