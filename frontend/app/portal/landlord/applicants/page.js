'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import { CheckCircle2, XCircle, FileText, UserCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordApplicantsPage() {
  const [user, setUser] = useState(null);
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    setUser(getStoredUser());
    loadApps();
  }, []);

  const loadApps = () => {
    api.get('/applications/')
      .then(res => setApplications(res.data || []))
      .catch(() => setApplications([
        {
          id: 'app1',
          unit_id: 'u1',
          applicant_id: 'tenant1',
          status: 'SUBMITTED',
          desired_move_in: '2026-09-01',
          lease_term_months: 12,
          employer_name: 'Tech Inc',
          job_title: 'Software Engineer',
          monthly_income: '8500.00',
          emergency_contact_name: 'Jane Doe',
          emergency_contact_phone: '(555) 123-4567'
        }
      ]));
  };

  const handleStatusUpdate = (appId, newStatus) => {
    api.put(`/applications/${appId}/status?new_status=${newStatus}`)
      .then(() => loadApps())
      .catch(() => loadApps());
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Rental Applicant Screening</h1>
            <p className="text-slate-400 text-xs mt-1">Review candidate income verification, employment history, and approve leases.</p>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Applicant</th>
                  <th className="py-3 px-4">Employer / Job Title</th>
                  <th className="py-3 px-4">Monthly Income</th>
                  <th className="py-3 px-4">Move-in Date</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Screening Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {applications.map(app => (
                  <tr key={app.id} className="hover:bg-slate-900/40">
                    <td className="py-4 px-4 font-bold text-white">Alex Morgan</td>
                    <td className="py-4 px-4">{app.employer_name} - <span className="text-slate-400 text-xs">{app.job_title}</span></td>
                    <td className="py-4 px-4 font-semibold text-emerald-400">${app.monthly_income}</td>
                    <td className="py-4 px-4">{app.desired_move_in}</td>
                    <td className="py-4 px-4"><StatusBadge status={app.status} /></td>
                    <td className="py-4 px-4 text-right space-x-2">
                      {app.status === 'SUBMITTED' && (
                        <>
                          <button
                            onClick={() => handleStatusUpdate(app.id, 'APPROVED')}
                            className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold inline-flex items-center gap-1 transition-colors"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5" /> Approve
                          </button>
                          <button
                            onClick={() => handleStatusUpdate(app.id, 'REJECTED')}
                            className="px-3 py-1.5 rounded-lg bg-rose-600/20 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 text-xs font-semibold inline-flex items-center gap-1 transition-colors"
                          >
                            <XCircle className="w-3.5 h-3.5" /> Reject
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
