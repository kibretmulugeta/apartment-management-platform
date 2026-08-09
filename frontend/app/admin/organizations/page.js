'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import { Building2 } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function AdminOrganizationsPage() {
  const [user, setUser] = useState(null);
  const [orgs, setOrgs] = useState([]);

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/admin/organizations')
      .then(res => setOrgs(res.data || []))
      .catch(() => setOrgs([
        { id: 'o1', name: 'Apex Property Management', slug: 'apex-pm', city: 'San Francisco', email: 'support@apexpm.com' }
      ]));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="ADMIN" />

      <main className="flex-1 p-8 overflow-y-auto">
        <h1 className="text-2xl font-extrabold text-white mb-6">Multi-Tenant Organizations</h1>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Organization Name</th>
                  <th className="py-3 px-4">Slug Identifier</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4 text-right">Contact Email</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {orgs.map(o => (
                  <tr key={o.id} className="hover:bg-slate-900/40">
                    <td className="py-3.5 px-4 font-bold text-white flex items-center gap-2">
                      <Building2 className="w-4 h-4 text-brand-400" />
                      {o.name}
                    </td>
                    <td className="py-3.5 px-4 text-xs font-mono text-brand-400">{o.slug}</td>
                    <td className="py-3.5 px-4 text-slate-400">{o.city}</td>
                    <td className="py-3.5 px-4 text-right text-slate-400">{o.email}</td>
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
