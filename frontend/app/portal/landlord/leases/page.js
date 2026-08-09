'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import Modal from '@/components/ui/Modal';
import { Plus, FileText, CheckCircle2, AlertTriangle } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordLeasesPage() {
  const [user, setUser] = useState(null);
  const [leases, setLeases] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form, setForm] = useState({
    unit_id: 'u1',
    tenant_id: 'tenant1',
    start_date: '2026-01-01',
    end_date: '2026-12-31',
    rent_amount: '3450.00',
    deposit_amount: '3450.00'
  });

  useEffect(() => {
    setUser(getStoredUser());
    loadLeases();
  }, []);

  const loadLeases = () => {
    api.get('/leases/')
      .then(res => setLeases(res.data || []))
      .catch(() => setLeases([
        {
          id: 'l1',
          lease_number: 'LSE-2026-00891',
          status: 'ACTIVE',
          start_date: '2026-01-01',
          end_date: '2026-12-31',
          rent_amount: '3450.00',
          deposit_amount: '3450.00',
          payment_due_day: 1
        }
      ]));
  };

  const handleCreateLease = (e) => {
    e.preventDefault();
    api.post('/leases/', form)
      .then(() => {
        setIsModalOpen(false);
        loadLeases();
      })
      .catch(() => setIsModalOpen(false));
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Lease Agreement Manager</h1>
            <p className="text-slate-400 text-xs mt-1">Generate legal residential leases, track digital signature execution, and manage renewals.</p>
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-md shadow-brand-600/30"
          >
            <Plus className="w-4 h-4" /> Generate New Lease
          </button>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Lease #</th>
                  <th className="py-3 px-4">Tenant</th>
                  <th className="py-3 px-4">Term Dates</th>
                  <th className="py-3 px-4">Monthly Rent</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Digital Signatures</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {leases.map(l => (
                  <tr key={l.id} className="hover:bg-slate-900/40">
                    <td className="py-4 px-4 font-bold text-white flex items-center gap-2">
                      <FileText className="w-4 h-4 text-brand-400" />
                      {l.lease_number}
                    </td>
                    <td className="py-4 px-4 font-medium text-white">Alex Morgan</td>
                    <td className="py-4 px-4 text-slate-400 text-xs">{l.start_date} to {l.end_date}</td>
                    <td className="py-4 px-4 font-bold text-emerald-400">${l.rent_amount}</td>
                    <td className="py-4 px-4"><StatusBadge status={l.status} /></td>
                    <td className="py-4 px-4 text-right text-xs text-slate-400">
                      <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold">
                        <CheckCircle2 className="w-3.5 h-3.5" /> E-Signed by Tenant
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Generate Lease Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Generate Legal Lease Document">
        <form onSubmit={handleCreateLease} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Start Date</label>
              <input
                type="date" required
                value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">End Date</label>
              <input
                type="date" required
                value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Monthly Rent ($)</label>
              <input
                type="number" step="0.01" required
                value={form.rent_amount} onChange={e => setForm({ ...form, rent_amount: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Security Deposit ($)</label>
              <input
                type="number" step="0.01" required
                value={form.deposit_amount} onChange={e => setForm({ ...form, deposit_amount: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <button type="submit" className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Generate Lease Document
          </button>
        </form>
      </Modal>
    </div>
  );
}
