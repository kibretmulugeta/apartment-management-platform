'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatCard from '@/components/ui/StatCard';
import StatusBadge from '@/components/ui/StatusBadge';
import { CreditCard, Home, Wrench, Calendar, ArrowRight, ShieldCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function TenantDashboard() {
  const [user, setUser] = useState(null);
  const [lease, setLease] = useState({
    lease_number: 'LSE-2026-00891',
    rent_amount: '3450.00',
    start_date: '2026-01-01',
    end_date: '2026-12-31',
    status: 'ACTIVE'
  });

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/leases/my-lease')
      .then(res => { if (res.data) setLease(res.data); })
      .catch(() => {});
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="TENANT" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Resident Portal Overview</h1>
            <p className="text-slate-400 text-xs mt-1">Welcome home! Manage your rent payments, lease terms, and maintenance tickets.</p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5" /> Lease Status: Active
          </span>
        </div>

        {/* Rent Due Alert Box */}
        <div className="glass-panel p-6 rounded-2xl border border-brand-500/30 bg-gradient-to-r from-brand-900/30 via-slate-900 to-slate-900 flex flex-col sm:flex-row items-center justify-between gap-6 mb-8 shadow-xl">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-brand-400 block mb-1">Upcoming Rent Payment</span>
            <h2 className="text-3xl font-extrabold text-white">${lease.rent_amount} <span className="text-xs font-normal text-slate-400">due on September 1, 2026</span></h2>
            <p className="text-xs text-slate-400 mt-1">Unit 14B — The Grandview Luxury Apartments</p>
          </div>
          <Link
            href="/portal/tenant/payments"
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 shrink-0"
          >
            <CreditCard className="w-4 h-4" /> Pay Rent via Stripe
          </Link>
        </div>

        {/* Tenant KPI Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          <StatCard title="Current Residence" value="Unit 14B" icon={Home} trend="2 Bed / 2 Bath Suite" color="brand" />
          <StatCard title="Lease Expiration" value="Dec 31, 2026" icon={Calendar} trend="142 Days Remaining" color="purple" />
          <StatCard title="Open Maintenance Tickets" value="1 Ticket" icon={Wrench} trend="Tech Assigned" color="amber" />
        </div>
      </main>
    </div>
  );
}
