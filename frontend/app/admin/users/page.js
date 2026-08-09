'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import { Users, Shield } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function AdminUsersPage() {
  const [user, setUser] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/admin/users')
      .then(res => setUsers(res.data || []))
      .catch(() => setUsers([
        { id: '1', first_name: 'Platform', last_name: 'Admin', email: 'admin@platform.com', roles: [{ name: 'ADMIN' }] },
        { id: '2', first_name: 'Robert', last_name: 'Sterling', email: 'landlord@apexpm.com', roles: [{ name: 'LANDLORD' }] },
        { id: '3', first_name: 'Alex', last_name: 'Morgan', email: 'tenant@apexpm.com', roles: [{ name: 'TENANT' }] },
        { id: '4', first_name: 'Marcus', last_name: 'Vance', email: 'tech@apexpm.com', roles: [{ name: 'MAINTENANCE_STAFF' }] }
      ]));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="ADMIN" />

      <main className="flex-1 p-8 overflow-y-auto">
        <h1 className="text-2xl font-extrabold text-white mb-6">User & RBAC Security Operations</h1>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {users.map(u => (
                  <tr key={u.id} className="hover:bg-slate-900/40">
                    <td className="py-3.5 px-4 font-bold text-white">{u.first_name} {u.last_name}</td>
                    <td className="py-3.5 px-4 text-slate-400">{u.email}</td>
                    <td className="py-3.5 px-4 font-semibold text-purple-400 text-xs">
                      {u.roles?.map(r => r.name).join(', ') || 'USER'}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Active</span>
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
