'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import PublicNavbar from '@/components/navigation/PublicNavbar';
import Footer from '@/components/navigation/Footer';
import PropertyCard from '@/components/properties/PropertyCard';
import { Search, Building2, ShieldCheck, CreditCard, Wrench, ArrowRight, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function HomePage() {
  const [properties, setProperties] = useState([]);
  const [cityFilter, setCityFilter] = useState('');

  useEffect(() => {
    api.get('/properties/public')
      .then(res => setProperties(res.data || []))
      .catch(() => setProperties([
        {
          id: 'prop1',
          name: 'The Grandview Luxury Apartments',
          address: '500 Skyline Blvd',
          city: 'San Francisco',
          state: 'CA',
          property_type: 'APARTMENT_COMPLEX',
          description: 'High-rise luxury residence featuring panoramic skyline views, rooftop lounge, and concierge.',
          images: [{ url: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80', is_primary: true }]
        },
        {
          id: 'prop2',
          name: 'Bayview Urban Terraces',
          address: '220 Embarcadero Rd',
          city: 'San Francisco',
          state: 'CA',
          property_type: 'CONDO',
          description: 'Boutique townhouse complex near waterfront parks and tech transit hubs.',
          images: [{ url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80', is_primary: true }]
        }
      ]));
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <PublicNavbar />

      {/* Hero Section */}
      <section className="relative pt-20 pb-28 overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-brand-600/20 via-transparent to-transparent"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-400 text-xs font-semibold uppercase tracking-wider mb-6">
            Enterprise Property Management SaaS
          </div>
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
            Next-Generation Apartment Rentals & Property Operations
          </h1>
          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Unified multi-tenant ecosystem connecting landlords, property managers, tenants, and maintenance crews with double-entry financial ledger accounting.
          </p>

          {/* Search Box */}
          <div className="mt-10 max-w-3xl mx-auto glass-panel p-3 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-center gap-3 shadow-2xl">
            <div className="flex-1 flex items-center gap-3 px-4 py-2 text-left w-full">
              <Search className="w-5 h-5 text-brand-400" />
              <input
                type="text"
                placeholder="Search city, neighborhood, or address..."
                value={cityFilter}
                onChange={(e) => setCityFilter(e.target.value)}
                className="bg-transparent border-none text-white focus:outline-none w-full placeholder:text-slate-500 text-sm"
              />
            </div>
            <Link
              href={`/properties?city=${encodeURIComponent(cityFilter)}`}
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-sky-500 hover:from-brand-500 hover:to-sky-400 text-white font-semibold text-sm transition-all shadow-lg shadow-brand-600/30 flex items-center justify-center gap-2 shrink-0"
            >
              Search Apartments
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Properties Section */}
      <section className="py-20 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
            <div>
              <h2 className="text-3xl font-bold text-white">Featured Luxury Listings</h2>
              <p className="text-slate-400 text-sm mt-2">Explore available units across premier residential communities.</p>
            </div>
            <Link href="/properties" className="mt-4 md:mt-0 inline-flex items-center gap-2 text-brand-400 hover:text-brand-300 font-semibold text-sm">
              View All Properties <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {properties.map(p => (
              <PropertyCard key={p.id} property={p} />
            ))}
          </div>
        </div>
      </section>

      {/* Core Platform Solutions Section */}
      <section id="features" className="py-20 bg-slate-900/50 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-white">Complete Enterprise Ecosystem</h2>
            <p className="text-slate-400 text-sm mt-3">Tailored workflows designed for every role in real estate management.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <div className="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/30 flex items-center justify-center mb-4 text-brand-400">
                <Building2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Landlords & Owners</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Property CRUD, occupancy analytics, lease generation, and automated double-entry general ledger statements.
              </p>
            </div>

            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center mb-4 text-emerald-400">
                <CreditCard className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Tenants</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Tokenized Stripe rent payments, digital lease signing, maintenance request tracking, and direct chat.
              </p>
            </div>

            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mb-4 text-amber-400">
                <Wrench className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Maintenance Staff</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Priority work order dispatch, photo evidence uploads, work logs, and repair cost recording.
              </p>
            </div>

            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center mb-4 text-purple-400">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Platform Admins</h3>
              <p className="text-slate-400 text-xs leading-relaxed">
                Multi-tenant organization oversight, global user RBAC management, and immutable system audit logging.
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
