'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import Modal from '@/components/ui/Modal';
import { Wrench, UserPlus, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordMaintenancePage() {
  const [user, setUser] = useState(null);
  const [requests, setRequests] = useState([]);
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [selectedReq, setSelectedReq] = useState(null);

  useEffect(() => {
    setUser(getStoredUser());
    loadReqs();
  }, []);

  const loadReqs = () => {
    api.get('/maintenance/')
      .then(res => setRequests(res.data || []))
      .catch(() => setRequests([
        {
          id: 'm1',
          title: 'Kitchen Sink Minor Leak',
          description: 'Water slow drip coming from underneath main faucet pipe fixture.',
          category: 'PLUMBING',
          priority: 'MEDIUM',
          status: 'ASSIGNED',
          tenant_id: 'tenant1'
        }
      ]));
  };

  const handleAssignTech = () => {
    if (!selectedReq) return;
    api.post(`/maintenance/${selectedReq.id}/assign`, { staff_id: 'tech1', notes: 'Inspect seal gasket.' })
      .then(() => {
        setIsAssignModalOpen(false);
        loadReqs();
      })
      .catch(() => setIsAssignModalOpen(false));
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Maintenance Work Order Dispatch</h1>
            <p className="text-slate-400 text-xs mt-1">Receive resident work orders, assign technicians, track repair costs and completion.</p>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Ticket Title</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Tech Dispatch</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {requests.map(r => (
                  <tr key={r.id} className="hover:bg-slate-900/40">
                    <td className="py-4 px-4 font-bold text-white flex items-center gap-2">
                      <Wrench className="w-4 h-4 text-sky-400" />
                      {r.title}
                    </td>
                    <td className="py-4 px-4 text-xs text-slate-400">{r.category}</td>
                    <td className="py-4 px-4 font-semibold text-amber-400 text-xs">{r.priority}</td>
                    <td className="py-4 px-4"><StatusBadge status={r.status} /></td>
                    <td className="py-4 px-4 text-right">
                      <button
                        onClick={() => { setSelectedReq(r); setIsAssignModalOpen(true); }}
                        className="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold inline-flex items-center gap-1 transition-colors"
                      >
                        <UserPlus className="w-3.5 h-3.5" /> Assign Tech
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Assign Tech Modal */}
      <Modal isOpen={isAssignModalOpen} onClose={() => setIsAssignModalOpen(false)} title="Dispatch Maintenance Technician">
        <div className="space-y-4">
          <p className="text-slate-300 text-xs">Assign qualified technician for: <strong className="text-white">{selectedReq?.title}</strong></p>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Select Technician</label>
            <select className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none">
              <option value="tech1">Marcus Vance (Plumbing & HVAC Specialist)</option>
            </select>
          </div>
          <button onClick={handleAssignTech} className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Confirm Dispatch
          </button>
        </div>
      </Modal>
    </div>
  );
}
