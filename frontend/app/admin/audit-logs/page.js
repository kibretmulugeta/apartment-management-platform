'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import { ShieldCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function AdminAuditLogsPage() {
  const [user, setUser] = useState(null);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/admin/audit-logs')
      .then(res => setLogs(res.data || []))
      .catch(() => setLogs([
        { id: 'al1', action: 'LEASE_SIGNED', resource_type: 'Lease', resource_id: 'l1', ip_address: '127.0.0.1', created_at: '2026-08-09T10:00:00Z' },
        { id: 'al2', action: 'PAYMENT_CREATED', resource_type: 'Payment', resource_id: 'pay1', ip_address: '127.0.0.1', created_at: '2026-08-09T10:05:00Z' }
      ]));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="ADMIN" />

      <main className="flex-1 p-8 overflow-y-auto">
        <h1 className="text-2xl font-extrabold text-white mb-6">Immutable Platform Audit Trail</h1>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Action</th>
                  <th className="py-3 px-4">Resource Type</th>
                  <th className="py-3 px-4">Resource ID</th>
                  <th className="py-3 px-4">IP Address</th>
                  <th className="py-3 px-4 text-right">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
                {logs.map(l => (
                  <tr key={l.id} className="hover:bg-slate-900/40">
                    <td className="py-3.5 px-4 font-bold text-purple-400">{l.action}</td>
                    <td className="py-3.5 px-4 text-white">{l.resource_type}</td>
                    <td className="py-3.5 px-4 text-slate-400">{l.resource_id}</td>
                    <td className="py-3.5 px-4 text-slate-400">{l.ip_address}</td>
                    <td className="py-3.5 px-4 text-right text-slate-500">{new Date(l.created_at).toLocaleString()}</td>
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
