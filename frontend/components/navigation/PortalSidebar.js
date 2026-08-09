'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Building2, LayoutDashboard, Home, Users, FileText, CreditCard,
  Wrench, FolderOpen, MessageSquare, ShieldCheck, Settings, LogOut, ChevronRight
} from 'lucide-react';
import { clearAuth } from '@/lib/auth';

export default function PortalSidebar({ user, role = 'LANDLORD' }) {
  const pathname = usePathname();

  const landlordNav = [
    { label: 'Dashboard', href: '/portal/landlord', icon: LayoutDashboard },
    { label: 'Properties & Units', href: '/portal/landlord/properties', icon: Home },
    { label: 'Rental Applicants', href: '/portal/landlord/applicants', icon: Users },
    { label: 'Lease Manager', href: '/portal/landlord/leases', icon: FileText },
    { label: 'Financial Ledger', href: '/portal/landlord/finances', icon: CreditCard },
    { label: 'Maintenance Dispatch', href: '/portal/landlord/maintenance', icon: Wrench },
    { label: 'Document Vault', href: '/portal/landlord/documents', icon: FolderOpen },
    { label: 'Messages', href: '/portal/landlord/messages', icon: MessageSquare },
  ];

  const tenantNav = [
    { label: 'Overview', href: '/portal/tenant', icon: LayoutDashboard },
    { label: 'Rent & Payments', href: '/portal/tenant/payments', icon: CreditCard },
    { label: 'Maintenance Requests', href: '/portal/tenant/maintenance', icon: Wrench },
    { label: 'Lease & Documents', href: '/portal/tenant/documents', icon: FileText },
    { label: 'Direct Messages', href: '/portal/tenant/messages', icon: MessageSquare },
  ];

  const maintenanceNav = [
    { label: 'Assigned Jobs', href: '/portal/maintenance', icon: Wrench },
    { label: 'Messages', href: '/portal/maintenance/messages', icon: MessageSquare },
  ];

  const adminNav = [
    { label: 'System Overview', href: '/admin', icon: LayoutDashboard },
    { label: 'Users & Roles', href: '/admin/users', icon: Users },
    { label: 'Organizations', href: '/admin/organizations', icon: Building2 },
    { label: 'Audit Trail', href: '/admin/audit-logs', icon: ShieldCheck },
  ];

  let navItems = landlordNav;
  if (role === 'TENANT') navItems = tenantNav;
  if (role === 'MAINTENANCE_STAFF') navItems = maintenanceNav;
  if (role === 'ADMIN') navItems = adminNav;

  const handleLogout = () => {
    clearAuth();
    window.location.href = '/auth/login';
  };

  return (
    <aside className="w-64 glass-panel border-r border-slate-800 h-screen sticky top-0 flex flex-col justify-between p-4 z-40">
      <div>
        <Link href="/" className="flex items-center gap-3 p-2 mb-6">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
            <Building2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold text-lg text-white block leading-none">Apparent</span>
            <span className="text-xs text-brand-400 font-medium capitalize">{role.replace('_', ' ').toLowerCase()} Portal</span>
          </div>
        </Link>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-brand-600/20 text-brand-400 border border-brand-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-brand-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-4 h-4 text-brand-400" />}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="pt-4 border-t border-slate-800">
        <div className="flex items-center gap-3 p-2 mb-3">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-white font-semibold text-xs">
            {user?.first_name ? user.first_name[0] : 'U'}
          </div>
          <div className="truncate">
            <p className="text-sm font-medium text-white truncate">{user?.first_name || 'User'} {user?.last_name || ''}</p>
            <p className="text-xs text-slate-500 truncate">{user?.email || ''}</p>
          </div>
        </div>

        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-rose-400 hover:bg-rose-500/10 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
