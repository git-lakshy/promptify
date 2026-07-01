import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

interface User {
  id: number;
  email: string;
  name: string;
  avatar_url?: string;
  tier: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, refreshToken: string) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore auth state from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('promptify_token');
    const storedUser = localStorage.getItem('promptify_user');

    if (storedToken) {
      setToken(storedToken);
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch {
          // ignore parse errors
        }
      }
      // Refresh user data in the background
      refreshUser(storedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const refreshUser = async (authToken: string) => {
    try {
      const res = await fetch(`${API_URL}/me`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
        localStorage.setItem('promptify_user', JSON.stringify(data));
      } else if (res.status === 401) {
        // Token expired or invalid - clear auth state
        localStorage.removeItem('promptify_token');
        localStorage.removeItem('promptify_refresh_token');
        localStorage.removeItem('promptify_user');
        setUser(null);
        setToken(null);
      } else {
        // For other errors (e.g. 500), keep the cached user if available
        setUser((prev) => prev);
      }
    } catch {
      // Network error - don't clear tokens, keep cached user
      setUser((prev) => prev);
    } finally {
      setIsLoading(false);
    }
  };

  const login = (newToken: string, refreshToken: string) => {
    localStorage.setItem('promptify_token', newToken);
    localStorage.setItem('promptify_refresh_token', refreshToken);
    setToken(newToken);
    refreshUser(newToken);
  };

  const logout = () => {
    localStorage.removeItem('promptify_token');
    localStorage.removeItem('promptify_refresh_token');
    localStorage.removeItem('promptify_user');
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
}
