import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    const refresh = searchParams.get('refresh');

    if (token && refresh) {
      login(token, refresh);
      navigate('/', { replace: true });
    } else {
      navigate('/login', { replace: true });
    }
  }, [searchParams, navigate, login]);

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <div className="hero-bg" />
      <div className="glow-beam" />
      <div className="text-center relative z-10">
        <div className="w-8 h-8 border-2 border-white/20 border-t-blue-400 rounded-full animate-spin mx-auto mb-4" />
        <p className="text-slate-400 text-sm">Authenticating...</p>
      </div>
    </div>
  );
}
