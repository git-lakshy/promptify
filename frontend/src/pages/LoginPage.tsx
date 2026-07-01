import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import pIcon from '../assets/p-icon.png';
import { useAuth } from '../contexts/AuthContext';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user?: {
    id: number;
    email: string;
    name: string;
  };
}

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleGoogleLogin = () => {
    setIsLoading(true);
    window.location.href = `${API_URL}/auth/google/login`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    const endpoint = isSignup ? `${API_URL}/auth/signup` : `${API_URL}/auth/login`;
    const body = isSignup
      ? { email, password, name }
      : { email, password, remember_me: rememberMe };

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Authentication failed');
        setIsLoading(false);
        return;
      }

      const data: TokenResponse = await res.json();
      if (data.access_token && data.refresh_token) {
        login(data.access_token, data.refresh_token);
        navigate('/', { replace: true });
      }
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background Effects - matching main app */}
      <div className="hero-bg" />
      <div className="glow-beam" />

      {/* Top Logo / Brand */}
      <div className="fixed top-0 w-full z-50 px-12 py-6">
        <div className="max-w-7xl mx-auto flex items-center">
          <Link to="/" className="flex items-center gap-2 cursor-pointer group no-underline">
            <div className="w-10 h-10 flex items-center justify-center overflow-visible hover:scale-110 active:scale-90 transition-transform duration-150 ease-out">
              <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110" />
            </div>
            <span className="text-xl font-bold tracking-wide text-white drop-shadow-sm uppercase">
              PROMPTIFY
            </span>
          </Link>
        </div>
      </div>

      {/* Auth Card */}
      <main className="flex-grow flex items-center justify-center relative z-10 px-4">
        <div
          className="w-full max-w-md p-8 rounded-2xl backdrop-blur-xl border border-white/10"
          style={{
            background: 'rgba(15, 23, 42, 0.6)',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 0 40px rgba(59, 130, 246, 0.1)',
          }}
        >
          <div className="text-center mb-8">
            <h2 className="text-2xl font-light text-white tracking-wide mb-2">
              {isSignup ? 'Create Account' : 'Welcome Back'}
            </h2>
            <p className="text-sm text-slate-400">
              {isSignup ? 'Sign up to enhance your prompts' : 'Sign in to enhance your prompts'}
            </p>
          </div>

          {/* Email / Password Form */}
          <form onSubmit={handleSubmit} className="space-y-4 mb-6">
            {isSignup && (
              <div>
                <label className="block text-xs text-slate-400 mb-1 tracking-wide uppercase">Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-blue-400/50 transition-colors"
                  placeholder="Your name"
                />
              </div>
            )}

            <div>
              <label className="block text-xs text-slate-400 mb-1 tracking-wide uppercase">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-blue-400/50 transition-colors"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-xs text-slate-400 mb-1 tracking-wide uppercase">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-blue-400/50 transition-colors"
                placeholder="Your password"
                required
              />
            </div>

            {!isSignup && (
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="remember"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4 h-4 rounded border-white/20 bg-white/5 text-blue-400 focus:ring-blue-400"
                />
                <label htmlFor="remember" className="text-xs text-slate-400 cursor-pointer">
                  Remember me for 7 days
                </label>
              </div>
            )}

            {error && (
              <p className="text-sm text-red-400 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-xl bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/30 text-white text-sm font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Processing...' : isSignup ? 'Sign Up' : 'Sign In'}
            </button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-white/10"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="px-2 bg-[#0f172a] text-slate-500">or</span>
            </div>
          </div>

          {/* Google OAuth */}
          <button
            onClick={handleGoogleLogin}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.19 3.32 5.17 5.17 0 0 1-3.73 1.07 5.18 5.18 0 0 1-4.35-2.32 5.19 5.19 0 0 1-.17-5.28 5.18 5.18 0 0 1 4.52-2.63c1.31 0 2.5.48 3.43 1.26l2.63-2.63A8.87 8.87 0 0 0 12 2.5a8.5 8.5 0 0 0-8.5 8.5 8.5 8.5 0 0 0 8.5 8.5c2.45 0 4.63-1 6.24-2.63 1.3-1.3 2.09-3.14 2.09-5.12z" fill="#4285F4"/>
              <path d="M3.5 12.5a8.5 8.5 0 0 1 8.5-8.5c2.13 0 4.05.78 5.55 2.07l-2.62 2.63a5.18 5.18 0 0 0-3.43-1.26 5.18 5.18 0 0 0-4.52 2.63 5.19 5.19 0 0 0 .17 5.28 5.18 5.18 0 0 0 4.35 2.32c1.5 0 2.78-.52 3.68-1.4.67-.64 1.12-1.54 1.27-2.6H12v-3.5h8.14c.14.7.2 1.45.2 2.25 0 1.98-.79 3.82-2.09 5.12A8.87 8.87 0 0 1 12 21.5a8.5 8.5 0 0 1-8.5-8.5z" fill="#34A853"/>
            </svg>
            <span className="text-sm font-medium text-white tracking-wide">
              Continue with Google
            </span>
          </button>

          <div className="mt-6 text-center">
            <button
              onClick={() => { setIsSignup(!isSignup); setError(''); }}
              className="text-xs text-slate-400 hover:text-white transition-colors"
            >
              {isSignup ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
