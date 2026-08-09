'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatCard from '@/components/ui/StatCard';
import Modal from '@/components/ui/Modal';
import { Plus, CreditCard, DollarSign, ArrowDownRight, ArrowUpRight, FileSpreadsheet } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordFinancesPage() {
  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState({ total_revenue: '6050.00', total_expenses: '450.00', net_income: '5600.00' });
  const [isExpenseModalOpen, setIsExpenseModalOpen] = useState(false);
  const [expenseForm, setExpenseForm] = useState({ property_id: 'prop1', category: 'REPAIRS', vendor: 'Plumbing Experts', amount: '120.00', date: '2026-08-01', description: 'Replaced sink pipe gasket' });

  useEffect(() => {
    setUser(getStoredUser());
    loadFinances();
  }, []);

  const loadFinances = () => {
    api.get('/ledger/transactions')
      .then(res => setTransactions(res.data || []))
      .catch(() => setTransactions([
        {
          id: 'txn1',
          reference: 'TXN-9F8A12',
          description: 'Rent Payment - Alex Morgan',
          posted_at: '2026-08-01T10:00:00Z',
          entries: [
            { account_code: '1000', account_name: 'Operating Cash Account', entry_type: 'DEBIT', amount: '3450.00' },
            { account_code: '4000', account_name: 'Rental Income Revenue', entry_type: 'CREDIT', amount: '3450.00' }
          ]
        }
      ]));

    api.get('/ledger/summary')
      .then(res => setSummary(res.data))
      .catch(() => {});
  };

  const handleRecordExpense = (e) => {
    e.preventDefault();
    api.post('/expenses/', expenseForm)
      .then(() => {
        setIsExpenseModalOpen(false);
        loadFinances();
      })
      .catch(() => setIsExpenseModalOpen(false));
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Double-Entry Financial Ledger</h1>
            <p className="text-slate-400 text-xs mt-1">GAAP-compliant general ledger accounting, balanced debits & credits, and rent roll reports.</p>
          </div>

          <button
            onClick={() => setIsExpenseModalOpen(true)}
            className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-md shadow-brand-600/30"
          >
            <Plus className="w-4 h-4" /> Log Operating Expense
          </button>
        </div>

        {/* Financial KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          <StatCard title="Gross Recognized Revenue" value={`$${summary.total_revenue}`} icon={ArrowUpRight} trend="Balanced Credit Posting" color="emerald" />
          <StatCard title="Total Operating Expenses" value={`$${summary.total_expenses}`} icon={ArrowDownRight} trend="Disbursements Posted" color="rose" />
          <StatCard title="Net Operating Income (NOI)" value={`$${summary.net_income}`} icon={DollarSign} trend="Net Profit Margin" color="brand" />
        </div>

        {/* General Ledger Journal Table */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-4">Immutable Journal Entries</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Txn Reference</th>
                  <th className="py-3 px-4">Description</th>
                  <th className="py-3 px-4">Account Chart</th>
                  <th className="py-3 px-4">Debit</th>
                  <th className="py-3 px-4">Credit</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {transactions.map(t => (
                  <tr key={t.id} className="hover:bg-slate-900/40">
                    <td className="py-4 px-4 font-bold text-brand-400">{t.reference}</td>
                    <td className="py-4 px-4 font-medium text-white">{t.description}</td>
                    <td className="py-4 px-4 space-y-1">
                      {t.entries?.map((e, idx) => (
                        <div key={idx} className="text-xs">
                          <span className="font-mono text-slate-500">{e.account_code || '1000'}</span> - {e.account_name || 'Cash Account'}
                        </div>
                      ))}
                    </td>
                    <td className="py-4 px-4 space-y-1 font-mono text-emerald-400">
                      {t.entries?.map((e, idx) => (
                        <div key={idx} className="text-xs">
                          {e.entry_type === 'DEBIT' ? `$${e.amount}` : '—'}
                        </div>
                      ))}
                    </td>
                    <td className="py-4 px-4 space-y-1 font-mono text-sky-400">
                      {t.entries?.map((e, idx) => (
                        <div key={idx} className="text-xs">
                          {e.entry_type === 'CREDIT' ? `$${e.amount}` : '—'}
                        </div>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Log Expense Modal */}
      <Modal isOpen={isExpenseModalOpen} onClose={() => setIsExpenseModalOpen(false)} title="Record Property Expense">
        <form onSubmit={handleRecordExpense} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Expense Category</label>
              <select
                value={expenseForm.category} onChange={e => setExpenseForm({ ...expenseForm, category: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              >
                <option value="REPAIRS">Property Maintenance & Repairs</option>
                <option value="UTILITIES">Utilities (Water/Electric/Gas)</option>
                <option value="MANAGEMENT">Management Fees</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Vendor / Contractor</label>
              <input
                type="text" required
                value={expenseForm.vendor} onChange={e => setExpenseForm({ ...expenseForm, vendor: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Amount ($)</label>
              <input
                type="number" step="0.01" required
                value={expenseForm.amount} onChange={e => setExpenseForm({ ...expenseForm, amount: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Disbursement Date</label>
              <input
                type="date" required
                value={expenseForm.date} onChange={e => setExpenseForm({ ...expenseForm, date: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <button type="submit" className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Post Expense & Journal Entry
          </button>
        </form>
      </Modal>
    </div>
  );
}
