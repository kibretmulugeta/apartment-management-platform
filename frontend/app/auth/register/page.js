'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Building2 } from 'lucide-react';
import { api } from '@/lib/api';
import { setAuthTokens } from '@/lib/auth';

export default function RegisterPage() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role_name: 'TENANT'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleRegister = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    api.post('/auth/register', form)
      .then(() => {
        setSuccess(true);
      })
      .catch(err => setError(err.message || 'Registration failed'))
      .finally(() => setLoading(false));
  };

  const handleOAuthRegister = (provider) => {
    setLoading(true);
    api.get(`/auth/oauth/${provider}/callback?code=mock_${provider}_code&role=${form.role_name}`)
      .then(res => {
        const { access_token, refresh_token, user } = res.data;
        setAuthTokens(access_token, refresh_token, user);
        window.location.href = form.role_name === 'LANDLORD' ? '/portal/landlord' : '/portal/tenant';
      })
      .catch(err => setError(err.message || 'OAuth registration failed'))
      .finally(() => setLoading(false));
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
          <h2 className="text-xl font-bold text-white mt-4">Create Account</h2>
          <p className="text-slate-400 text-xs mt-1">Join with email or single sign-on enterprise providers.</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 shadow-2xl">
          {error && <div className="p-3 mb-4 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">{error}</div>}
          
          {success ? (
            <div className="text-center py-6">
              <h3 className="text-lg font-bold text-white mb-2">Account Created!</h3>
              <p className="text-slate-400 text-xs mb-4">You can now log in to access your portal.</p>
              <Link href="/auth/login" className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs rounded-xl inline-block">
                Go to Sign In
              </Link>
            </div>
          ) : (
            <>
              {/* OAuth Provisioning Buttons */}
              <div className="grid grid-cols-2 gap-2 mb-6">
                <button
                  onClick={() => handleOAuthRegister('google')}
                  className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"/><path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/><path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 12.4 0 15.3c0 2.9.7 5.6 1.9 8l3.7-2.9z"/><path fill="#34A853" d="M12 23.5c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 16.5C3.7 20.2 7.5 23.5 12 23.5z"/></svg>
                  Google
                </button>
                <button
                  onClick={() => handleOAuthRegister('microsoft')}
                  className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
                >
                  <svg className="w-4 h-4" viewBox="0 0 23 23"><path fill="#f35325" d="M1 1h10v10H1z"/><path fill="#81bc06" d="M12 1h10v10H12z"/><path fill="#05a6f0" d="M1 12h10v10H1z"/><path fill="#ffba08" d="M12 12h10v10H12z"/></svg>
                  Microsoft
                </button>
                <button
                  onClick={() => handleOAuthRegister('facebook')}
                  className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
                >
                  <svg className="w-4 h-4" fill="#1877F2" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                  Facebook
                </button>
                <button
                  onClick={() => handleOAuthRegister('linkedin')}
                  className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-white font-medium text-xs flex items-center justify-center gap-2 transition-colors"
                >
                  <svg className="w-4 h-4" fill="#0A66C2" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.25V10.9H6.46M7.86 6.7a1.64 1.64 0 1 0 0 3.28 1.64 1.64 0 0 0 0-3.28z"/></svg>
                  LinkedIn
                </button>
              </div>

              <div className="relative flex py-2 items-center mb-4">
                <div className="flex-grow border-t border-slate-800"></div>
                <span className="flex-shrink mx-4 text-[10px] text-slate-500 uppercase tracking-widest font-semibold">Or register with email</span>
                <div className="flex-grow border-t border-slate-800"></div>
              </div>

              <form onSubmit={handleRegister} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">First Name</label>
                    <input
                      type="text" required
                      value={form.first_name} onChange={e => setForm({ ...form, first_name: e.target.value })}
                      className="w-full px-3 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">Last Name</label>
                    <input
                      type="text" required
                      value={form.last_name} onChange={e => setForm({ ...form, last_name: e.target.value })}
                      className="w-full px-3 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Email Address</label>
                  <input
                    type="email" required
                    value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Password</label>
                  <input
                    type="password" required
                    value={form.password} onChange={e => setForm({ ...form, password: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Account Role</label>
                  <select
                    value={form.role_name} onChange={e => setForm({ ...form, role_name: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
                  >
                    <option value="TENANT">Tenant / Resident</option>
                    <option value="LANDLORD">Landlord / Owner</option>
                    <option value="MAINTENANCE_STAFF">Maintenance Tech</option>
                  </select>
                </div>

                <button
                  type="submit" disabled={loading}
                  className="w-full py-3 bg-brand-600 hover:bg-brand-500 text-white font-bold text-sm rounded-xl transition-all shadow-lg shadow-brand-600/30"
                >
                  {loading ? 'Creating Account...' : 'Register Account'}
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
