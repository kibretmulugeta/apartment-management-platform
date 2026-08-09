'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import Modal from '@/components/ui/Modal';
import { Plus, Wrench, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function TenantMaintenancePage() {
  const [user, setUser] = useState(null);
  const [requests, setRequests] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form, setForm] = useState({
    property_id: 'prop1',
    unit_id: 'u1',
    title: '',
    description: '',
    category: 'PLUMBING',
    priority: 'MEDIUM'
  });

  useEffect(() => {
    setUser(getStoredUser());
    loadReqs();
  }, []);

  const loadReqs = () => {
    api.get('/maintenance/my-requests')
      .then(res => setRequests(res.data || []))
      .catch(() => setRequests([
        {
          id: 'm1',
          title: 'Kitchen Sink Minor Leak',
          description: 'Water slow drip coming from underneath main faucet pipe fixture.',
          category: 'PLUMBING',
          priority: 'MEDIUM',
          status: 'ASSIGNED',
          created_at: '2026-08-05T09:00:00Z'
        }
      ]));
  };

  const handleCreateTicket = (e) => {
    e.preventDefault();
    api.post('/maintenance/', form)
      .then(() => {
        setIsModalOpen(false);
        setForm({ ...form, title: '', description: '' });
        loadReqs();
      })
      .catch(() => setIsModalOpen(false));
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="TENANT" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Maintenance Work Orders</h1>
            <p className="text-slate-400 text-xs mt-1">Submit repair tickets directly to property managers and track technician arrival status.</p>
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-md shadow-brand-600/30"
          >
            <Plus className="w-4 h-4" /> Submit Repair Request
          </button>
        </div>

        {/* Ticket List */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Title & Description</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Submitted</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {requests.map(r => (
                  <tr key={r.id} className="hover:bg-slate-900/40">
                    <td className="py-4 px-4 font-bold text-white">
                      <div className="flex items-center gap-2">
                        <Wrench className="w-4 h-4 text-sky-400" />
                        {r.title}
                      </div>
                      <p className="text-xs text-slate-400 font-normal mt-0.5">{r.description}</p>
                    </td>
                    <td className="py-4 px-4 text-xs text-slate-400">{r.category}</td>
                    <td className="py-4 px-4 font-semibold text-amber-400 text-xs">{r.priority}</td>
                    <td className="py-4 px-4"><StatusBadge status={r.status} /></td>
                    <td className="py-4 px-4 text-right text-xs text-slate-500">{new Date(r.created_at || Date.now()).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* New Ticket Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="New Maintenance Repair Request">
        <form onSubmit={handleCreateTicket} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Issue Title</label>
            <input
              type="text" required placeholder="e.g. Kitchen sink leak"
              value={form.title} onChange={e => setForm({ ...form, title: e.target.value })}
              className="w-full px-3.5 py-2.5 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Category</label>
              <select
                value={form.category} onChange={e => setForm({ ...form, category: e.target.value })}
                className="w-full px-3.5 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
              >
                <option value="PLUMBING">Plumbing</option>
                <option value="ELECTRICAL">Electrical</option>
                <option value="HVAC">Heating & Air (HVAC)</option>
                <option value="APPLIANCE">Appliance</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Urgency Priority</label>
              <select
                value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value })}
                className="w-full px-3.5 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
              >
                <option value="LOW">Low Priority</option>
                <option value="MEDIUM">Medium Priority</option>
                <option value="HIGH">High Priority</option>
                <option value="URGENT">Urgent (Emergency)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Detailed Problem Description</label>
            <textarea
              rows="3" required placeholder="Describe the issue and location within unit..."
              value={form.description} onChange={e => setForm({ ...form, description: e.target.value })}
              className="w-full px-3.5 py-2 bg-slate-900 rounded-xl border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>

          <button type="submit" className="w-full py-3 bg-brand-600 hover:bg-brand-500 text-white font-bold text-sm rounded-xl transition-colors mt-2">
            Submit Repair Ticket
          </button>
        </form>
      </Modal>
    </div>
  );
}
