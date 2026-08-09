'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import Modal from '@/components/ui/Modal';
import { Wrench, CheckCircle2, Clock, Camera, FileText } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function MaintenanceStaffPage() {
  const [user, setUser] = useState(null);
  const [assignedJobs, setAssignedJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [isUpdateModalOpen, setIsUpdateModalOpen] = useState(false);
  const [updateForm, setUpdateForm] = useState({ status: 'IN_PROGRESS', actual_cost: '45.00', comment: 'Replaced rubber gasket and sealed joint fittings.' });

  useEffect(() => {
    setUser(getStoredUser());
    loadJobs();
  }, []);

  const loadJobs = () => {
    api.get('/maintenance/assigned-tech')
      .then(res => setAssignedJobs(res.data || []))
      .catch(() => setAssignedJobs([
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

  const handleUpdateStatus = (e) => {
    e.preventDefault();
    if (!selectedJob) return;
    api.put(`/maintenance/${selectedJob.id}/status`, updateForm)
      .then(() => {
        setIsUpdateModalOpen(false);
        loadJobs();
      })
      .catch(() => {
        setIsUpdateModalOpen(false);
        loadJobs();
      });
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="MAINTENANCE_STAFF" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Technician Work Order Queue</h1>
            <p className="text-slate-400 text-xs mt-1">Assigned maintenance jobs, status updates, photo evidence, and material cost logs.</p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 border border-amber-500/30 text-amber-400">
            Technician: Marcus Vance
          </span>
        </div>

        {/* Assigned Jobs List */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {assignedJobs.map(job => (
            <div key={job.id} className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 border border-amber-500/30 text-amber-400">
                    {job.priority} PRIORITY
                  </span>
                  <StatusBadge status={job.status} />
                </div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <Wrench className="w-5 h-5 text-sky-400" />
                  {job.title}
                </h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{job.description}</p>
                <div className="mt-4 pt-4 border-t border-slate-800/60 text-xs text-slate-400 space-y-1">
                  <p><strong className="text-slate-300">Location:</strong> Unit 14B — The Grandview</p>
                  <p><strong className="text-slate-300">Category:</strong> {job.category}</p>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
                <button
                  onClick={() => { setSelectedJob(job); setIsUpdateModalOpen(true); }}
                  className="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs transition-colors"
                >
                  Update Status & Work Notes
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Update Job Status Modal */}
      <Modal isOpen={isUpdateModalOpen} onClose={() => setIsUpdateModalOpen(false)} title="Update Work Order Progress">
        <form onSubmit={handleUpdateStatus} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Work Status</label>
            <select
              value={updateForm.status} onChange={e => setUpdateForm({ ...updateForm, status: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            >
              <option value="IN_PROGRESS">In Progress (On-site)</option>
              <option value="WAITING_FOR_PARTS">Waiting for Parts</option>
              <option value="COMPLETED">Completed (Job Finished)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Actual Materials & Labor Cost ($)</label>
            <input
              type="number" step="0.01" required
              value={updateForm.actual_cost} onChange={e => setUpdateForm({ ...updateForm, actual_cost: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Repair Execution Notes & Summary</label>
            <textarea
              rows="3" required
              value={updateForm.comment} onChange={e => setUpdateForm({ ...updateForm, comment: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>

          <button type="submit" className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Submit Status Update
          </button>
        </form>
      </Modal>
    </div>
  );
}
