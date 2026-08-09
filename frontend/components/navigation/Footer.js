import Link from 'next/link';
import { Building2 } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center">
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg text-white">Apparent</span>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            Enterprise-grade apartment rental & property management platform designed for multi-tenant organizations, landlords, and modern tenants.
          </p>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-3 uppercase tracking-wider">Public Marketplace</h4>
          <ul className="space-y-2 text-sm">
            <li><Link href="/properties" className="hover:text-white transition-colors">Search Apartments</Link></li>
            <li><Link href="/apply" className="hover:text-white transition-colors">Rental Application</Link></li>
            <li><Link href="/#pricing" className="hover:text-white transition-colors">Pricing Plans</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-3 uppercase tracking-wider">Portals</h4>
          <ul className="space-y-2 text-sm">
            <li><Link href="/portal/landlord" className="hover:text-white transition-colors">Landlord / Manager Portal</Link></li>
            <li><Link href="/portal/tenant" className="hover:text-white transition-colors">Tenant Portal</Link></li>
            <li><Link href="/portal/maintenance" className="hover:text-white transition-colors">Maintenance Portal</Link></li>
            <li><Link href="/admin" className="hover:text-white transition-colors">Administrator Portal</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-3 uppercase tracking-wider">Security & Legal</h4>
          <ul className="space-y-2 text-sm">
            <li><span className="text-slate-500">256-Bit Financial Ledger</span></li>
            <li><span className="text-slate-500">Double-Entry Accounting</span></li>
            <li><span className="text-slate-500">Multi-Tenant Isolation</span></li>
          </ul>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 mt-8 pt-6 border-t border-slate-900 text-xs text-center text-slate-600">
        &copy; {new Date().getFullYear()} Apparent Property Management Technologies. All rights reserved.
      </div>
    </footer>
  );
}
