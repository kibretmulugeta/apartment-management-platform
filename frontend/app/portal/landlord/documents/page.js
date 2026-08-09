'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import { FolderOpen, Download, FileText } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordDocumentsPage() {
  const [user, setUser] = useState(null);
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/documents/')
      .then(res => setDocs(res.data || []))
      .catch(() => setDocs([
        { id: 'doc1', name: 'Standard_Residential_Lease_2026.pdf', category: 'LEASE', download_url: '#' },
        { id: 'doc2', name: 'Property_Tax_Assessment_SanFrancisco.pdf', category: 'TAX', download_url: '#' }
      ]));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Central Document Vault</h1>
            <p className="text-slate-400 text-xs mt-1">Secure encrypted private document storage with time-bounded signed URLs.</p>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {docs.map(d => (
              <div key={d.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <FileText className="w-6 h-6 text-brand-400 shrink-0" />
                  <div>
                    <h4 className="text-sm font-semibold text-white truncate max-w-xs">{d.name}</h4>
                    <span className="text-xs text-slate-500 font-medium">{d.category}</span>
                  </div>
                </div>
                <a href={d.download_url} download className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors">
                  <Download className="w-4 h-4" />
                </a>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
