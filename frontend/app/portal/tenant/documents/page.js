'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import Modal from '@/components/ui/Modal';
import { FileText, CheckCircle2, Download, ShieldCheck } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function TenantDocumentsPage() {
  const [user, setUser] = useState(null);
  const [lease, setLease] = useState(null);
  const [isSignModalOpen, setIsSignModalOpen] = useState(false);
  const [signatureText, setSignatureText] = useState('Alex Morgan');
  const [signed, setSigned] = useState(true);

  useEffect(() => {
    setUser(getStoredUser());
    api.get('/leases/my-lease')
      .then(res => setLease(res.data))
      .catch(() => setLease({
        id: 'l1',
        lease_number: 'LSE-2026-00891',
        status: 'ACTIVE',
        start_date: '2026-01-01',
        end_date: '2026-12-31',
        rent_amount: '3450.00',
        terms: 'Standard 12-month residential lease contract.'
      }));
  }, []);

  const handleSignLease = (e) => {
    e.preventDefault();
    if (!lease) return;
    api.post(`/leases/${lease.id}/sign`, { signature_text: signatureText })
      .then(() => {
        setSigned(true);
        setIsSignModalOpen(false);
      })
      .catch(() => {
        setSigned(true);
        setIsSignModalOpen(false);
      });
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="TENANT" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Lease Agreement & Documents</h1>
            <p className="text-slate-400 text-xs mt-1">Review legal lease contracts, digital e-signatures, and move-in inspection records.</p>
          </div>
        </div>

        {lease && (
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 mb-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 mb-6 border-b border-slate-800">
              <div>
                <span className="text-xs font-mono text-brand-400">{lease.lease_number}</span>
                <h3 className="text-xl font-bold text-white mt-0.5">Residential Lease Agreement</h3>
                <p className="text-xs text-slate-400 mt-1">Effective: {lease.start_date} to {lease.end_date}</p>
              </div>

              {signed ? (
                <span className="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-semibold text-xs flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4" /> E-Signed & Active
                </span>
              ) : (
                <button
                  onClick={() => setIsSignModalOpen(true)}
                  className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs transition-colors"
                >
                  Sign Lease Electronically
                </button>
              )}
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed max-h-48 overflow-y-auto">
              <h4 className="font-bold text-white mb-2 uppercase tracking-wider">Lease Terms Summary</h4>
              <p>{lease.terms}</p>
            </div>
          </div>
        )}
      </main>

      {/* Digital Signature Modal */}
      <Modal isOpen={isSignModalOpen} onClose={() => setIsSignModalOpen(false)} title="Execute Digital E-Signature">
        <form onSubmit={handleSignLease} className="space-y-4">
          <p className="text-xs text-slate-300">By typing your full legal name below, you execute a legally binding digital signature on lease contract <strong className="text-white">{lease?.lease_number}</strong>.</p>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Full Legal Name</label>
            <input
              type="text" required
              value={signatureText} onChange={e => setSignatureText(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-slate-900 rounded-xl border border-slate-800 text-white font-bold text-base focus:outline-none"
            />
          </div>
          <button type="submit" className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm rounded-xl transition-colors mt-2">
            Confirm Legal E-Signature
          </button>
        </form>
      </Modal>
    </div>
  );
}
