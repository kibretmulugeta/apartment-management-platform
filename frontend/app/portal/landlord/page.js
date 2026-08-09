'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatCard from '@/components/ui/StatCard';
import StatusBadge from '@/components/ui/StatusBadge';
import { Building2, Users, CreditCard, Wrench, ArrowUpRight, TrendingUp, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordDashboard() {
  const [user, setUser] = useState(null);
  const [analytics, setAnalytics] = useState({
    total_properties: 2,
    total_units: 4,
    occupied_units: 3,
    vacant_units: 1,
    occupancy_rate: 75.0,
    pending_applications: 1,
    open_maintenance: 1
  });

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/reports/dashboard-analytics')
      .then(res => setAnalytics(res.data))
      .catch(() => {});
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Landlord & Property Operations</h1>
            <p className="text-slate-400 text-xs mt-1">Multi-tenant portfolio performance and real-time operational overview.</p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-brand-500/10 border border-brand-500/30 text-brand-400">
            Organization: Apex Property Management
          </span>
        </div>

        {/* Analytics KPIs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title="Portfolio Occupancy" value={`${analytics.occupancy_rate}%`} icon={Building2} trend="3 of 4 Units Occupied" color="brand" />
          <StatCard title="Monthly Rental Revenue" value="$6,050.00" icon={CreditCard} trend="+12.4% vs last month" color="emerald" />
          <StatCard title="Pending Applications" value={analytics.pending_applications} icon={Users} trend="Requires Screening" color="purple" />
          <StatCard title="Open Maintenance" value={analytics.open_maintenance} icon={Wrench} trend="1 Tech Assigned" color="amber" />
        </div>

        {/* Financial Overview & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-slate-800">
            <h3 className="text-lg font-bold text-white mb-4">Cash Flow & Financial Ledger Performance</h3>
            <div className="h-64 flex items-end justify-between gap-4 px-4 pt-8 pb-2 bg-slate-900/60 rounded-xl border border-slate-800">
              {[
                { month: 'Jan', rev: 18500, exp: 4200 },
                { month: 'Feb', rev: 19200, exp: 3800 },
                { month: 'Mar', rev: 21000, exp: 5100 },
                { month: 'Apr', rev: 20500, exp: 4600 },
                { month: 'May', rev: 22400, exp: 3900 },
                { month: 'Jun', rev: 24800, exp: 4800 },
              ].map(bar => (
                <div key={bar.month} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                  <div className="w-full flex items-end justify-center gap-1.5 h-full">
                    <div className="w-1/2 bg-brand-500 rounded-t-md" style={{ height: `${(bar.rev / 30000) * 100}%` }} title={`Revenue: $${bar.rev}`} />
                    <div className="w-1/2 bg-rose-500/80 rounded-t-md" style={{ height: `${(bar.exp / 30000) * 100}%` }} title={`Expense: $${bar.exp}`} />
                  </div>
                  <span className="text-xs text-slate-400 font-medium">{bar.month}</span>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-6 justify-center mt-4 text-xs font-semibold">
              <span className="flex items-center gap-2 text-brand-400"><div className="w-3 h-3 bg-brand-500 rounded-sm" /> Gross Rental Income</span>
              <span className="flex items-center gap-2 text-rose-400"><div className="w-3 h-3 bg-rose-500/80 rounded-sm" /> Operating Expenses</span>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl border border-slate-800">
            <h3 className="text-lg font-bold text-white mb-4">Urgent Operations</h3>
            <div className="space-y-4">
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-white">Pending Application</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Alex Morgan submitted application for Unit 14B.</p>
                </div>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start gap-3">
                <Wrench className="w-5 h-5 text-sky-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-white">Work Order Assigned</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Kitchen Sink Minor Leak assigned to Tech Marcus Vance.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
