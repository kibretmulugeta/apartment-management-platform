'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Building2, ArrowRight } from 'lucide-react';
import { api } from '@/lib/api';
import { setAuthTokens } from '@/lib/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('landlord@apexpm.com');
  const [password, setPassword] = useState('LandlordPass123!');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    api.post('/auth/login', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
      .then(res => {
        const { access_token, refresh_token, user } = res.data;
        setAuthTokens(access_token, refresh_token, user);
        
        const roles = user.roles?.map(r => r.name) || [];
        if (roles.includes('ADMIN')) window.location.href = '/admin';
        else if (roles.includes('LANDLORD') || roles.includes('PROPERTY_MANAGER')) window.location.href = '/portal/landlord';
        else if (roles.includes('MAINTENANCE_STAFF')) window.location.href = '/portal/maintenance';
        else window.location.href = '/portal/tenant';
      })
      .catch(err => {
        setError(err.message || 'Invalid credentials');
      })
      .finally(() => setLoading(false));
  };

  const handleOAuthLogin = (provider) => {
    setLoading(true);
    api.get(`/auth/oauth/${provider}/url`)
      .then(res => {
        if (res.data?.authorization_url && !res.data.authorization_url.includes('mock_client_id')) {
          window.location.href = res.data.authorization_url;
        } else {
          // Development fallback with mock code if GOOGLE_CLIENT_ID is not configured yet
          return api.get(`/auth/oauth/${provider}/callback?code=mock_${provider}_code`).then(cbRes => {
            const { access_token, refresh_token, user } = cbRes.data;
            setAuthTokens(access_token, refresh_token, user);
            const roles = user.roles?.map(r => r.name) || [];
            if (roles.includes('ADMIN')) window.location.href = '/admin';
            else if (roles.includes('LANDLORD') || roles.includes('PROPERTY_MANAGER')) window.location.href = '/portal/landlord';
            else if (roles.includes('MAINTENANCE_STAFF')) window.location.href = '/portal/maintenance';
            else window.location.href = '/portal/tenant';
          });
        }
      })
      .catch(err => setError(err.message || 'OAuth authentication failed'))
      .finally(() => setLoading(false));
  };

  const handleQuickDemo = (demoEmail, demoPw) => {
    setEmail(demoEmail);
    setPassword(demoPw);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-6">
          <Link href="/" className="inline-flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <Building2 className="w-6 h-6 text-white" />
            </div>
            <span className="font-bold text-2xl text-white">Apparent</span>
          </Link>
          <h2 className="text-xl font-bold text-white mt-4">Welcome Back</h2>
          <p className="text-slate-400 text-xs mt-1">Sign in with password or enterprise OAuth identity providers.</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 shadow-2xl">
          {error && <div className="p-3 mb-4 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">{error}</div>}

          {/* Social OAuth Buttons Grid */}
          <div className="grid grid-cols-2 gap-2 mb-6">
            <button
              onClick={() => handleOAuthLogin('google')}
              className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/><path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12.4 0 15.3c0 2.9.7 5.6 1.9 8l3.7-2.9z"/><path fill="#34A853" d="M12 23.5c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16.5C3.7 20.2 7.5 23.5 12 23.5z"/></svg>
              Google
            </button>
            <button
              onClick={() => handleOAuthLogin('microsoft')}
              className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
            >
              <svg className="w-4 h-4" viewBox="0 0 23 23"><path fill="#f35325" d="M1 1h10v10H1z"/><path fill="#81bc06" d="M12 1h10v10H12z"/><path fill="#05a6f0" d="M1 12h10v10H1z"/><path fill="#ffba08" d="M12 12h10v10H12z"/></svg>
              Microsoft
            </button>
            <button
              onClick={() => handleOAuthLogin('facebook')}
              className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
            >
              <svg className="w-4 h-4" fill="#1877F2" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              Facebook
            </button>
            <button
              onClick={() => handleOAuthLogin('linkedin')}
              className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
            >
              <svg className="w-4 h-4" fill="#0A66C2" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.25V10.9H6.46M7.86 6.7a1.64 1.64 0 1 0 0 3.28 1.64 1.64 0 0 0 0-3.28z"/></svg>
              LinkedIn
            </button>
          </div>

          <div className="relative flex py-2 items-center mb-4">
            <div className="flex-grow border-t border-slate-800"></div>
            <span className="flex-shrink mx-4 text-[10px] text-slate-500 uppercase tracking-widest font-semibold">Or sign in with email</span>
            <div className="flex-grow border-t border-slate-800"></div>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Email Address</label>
              <input
                type="email" required
                value={email} onChange={e => setEmail(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Password</label>
              <input
                type="password" required
                value={password} onChange={e => setPassword(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none focus:border-brand-500"
              />
            </div>

            <button
              type="submit" disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-brand-600 to-sky-500 hover:from-brand-500 hover:to-sky-400 text-white font-bold text-sm rounded-xl transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2"
            >
              {loading ? 'Authenticating...' : 'Sign In'} <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Credentials Assistant */}
          <div className="mt-6 pt-6 border-t border-slate-800/80">
            <p className="text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Quick Demo Login Selector:</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => handleQuickDemo('landlord@apexpm.com', 'LandlordPass123!')}
                className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-left border border-slate-800 text-brand-400 font-medium truncate"
              >
                Landlord / Owner
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemo('tenant@apexpm.com', 'TenantPass123!')}
                className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-left border border-slate-800 text-emerald-400 font-medium truncate"
              >
                Resident Tenant
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemo('tech@apexpm.com', 'TechPass123!')}
                className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-left border border-slate-800 text-amber-400 font-medium truncate"
              >
                Maintenance Tech
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemo('admin@platform.com', 'AdminPass123!')}
                className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-left border border-slate-800 text-purple-400 font-medium truncate"
              >
                Platform Admin
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
