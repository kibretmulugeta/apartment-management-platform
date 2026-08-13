'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';
import { setAuthTokens } from '@/lib/auth';
import { Loader2, AlertCircle } from 'lucide-react';

function CallbackContent() {
  const searchParams = useSearchParams();
  const [error, setError] = useState('');

  useEffect(() => {
    const state = searchParams.get('state');
    const provider = searchParams.get('provider') || (state ? state.split(':')[0] : 'google');
    const code = searchParams.get('code');

    if (!code) {
      setError('Authorization code missing from authentication provider.');
      return;
    }

    const stateParam = state ? `&state=${encodeURIComponent(state)}` : '';
    api.get(`/auth/oauth/${provider}/callback?code=${encodeURIComponent(code)}${stateParam}`)
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
        setError(err.message || 'Failed to verify OAuth response with server.');
      });
  }, [searchParams]);

  if (error) {
    return (
      <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center max-w-md w-full">
        <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
        <h2 className="text-xl font-bold text-white mb-2">Authentication Failed</h2>
        <p className="text-slate-400 text-sm mb-6">{error}</p>
        <a
          href="/auth/login"
          className="inline-block px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-medium transition-colors"
        >
          Return to Sign In
        </a>
      </div>
    );
  }

  return (
    <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center max-w-md w-full">
      <Loader2 className="w-10 h-10 text-brand-500 animate-spin mx-auto mb-4" />
      <h2 className="text-xl font-bold text-white mb-1">Verifying Credentials</h2>
      <p className="text-slate-400 text-sm">Logging you in securely with Google...</p>
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <Suspense fallback={
        <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center max-w-md w-full">
          <Loader2 className="w-10 h-10 text-brand-500 animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white">Loading...</h2>
        </div>
      }>
        <CallbackContent />
      </Suspense>
    </div>
  );
}
