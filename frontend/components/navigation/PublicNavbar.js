'use client';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { Building2, User, LogOut, LayoutDashboard, Shield } from 'lucide-react';
import { getStoredUser, clearAuth } from '@/lib/auth';

export default function PublicNavbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const handleLogout = () => {
    clearAuth();
    setUser(null);
    window.location.href = '/';
  };

  const getPortalLink = () => {
    if (!user) return '/portal/landlord';
    const roles = user.roles?.map(r => r.name) || [];
    if (roles.includes('ADMIN')) return '/admin';
    if (roles.includes('LANDLORD') || roles.includes('PROPERTY_MANAGER')) return '/portal/landlord';
    if (roles.includes('MAINTENANCE_STAFF')) return '/portal/maintenance';
    return '/portal/tenant';
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center shadow-lg shadow-brand-500/20 group-hover:scale-105 transition-transform">
            <Building2 className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
              Apparent
            </span>
            <span className="text-xs text-brand-500 font-semibold block uppercase tracking-wider">Property SaaS</span>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-8 font-medium text-sm text-slate-300">
          <Link href="/properties" className="hover:text-brand-400 transition-colors">Properties</Link>
          <Link href="/#features" className="hover:text-brand-400 transition-colors">Platform Solutions</Link>
          <Link href="/#pricing" className="hover:text-brand-400 transition-colors">Pricing</Link>
          <Link href="/#about" className="hover:text-brand-400 transition-colors">About Us</Link>
        </nav>

        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3">
              <Link
                href={getPortalLink()}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm transition-all shadow-md shadow-brand-600/30"
              >
                <LayoutDashboard className="w-4 h-4" />
                Go to Portal
              </Link>
              <button
                onClick={handleLogout}
                className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link
                href="/auth/login"
                className="px-4 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-all"
              >
                Sign In
              </Link>
              <Link
                href="/auth/register"
                className="px-4 py-2 rounded-lg text-sm font-medium bg-gradient-to-r from-brand-600 to-sky-500 hover:from-brand-500 hover:to-sky-400 text-white transition-all shadow-md shadow-brand-600/30"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
