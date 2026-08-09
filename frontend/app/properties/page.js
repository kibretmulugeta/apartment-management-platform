'use client';
import { useState, useEffect } from 'react';
import PublicNavbar from '@/components/navigation/PublicNavbar';
import Footer from '@/components/navigation/Footer';
import PropertyCard from '@/components/properties/PropertyCard';
import { Search, Filter, SlidersHorizontal } from 'lucide-react';
import { api } from '@/lib/api';

export default function PropertiesCatalogPage() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cityFilter, setCityFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = () => {
    setLoading(true);
    let query = '/properties/public';
    const params = [];
    if (cityFilter) params.push(`city=${encodeURIComponent(cityFilter)}`);
    if (typeFilter) params.push(`property_type=${encodeURIComponent(typeFilter)}`);
    if (params.length) query += `?${params.join('&')}`;

    api.get(query)
      .then(res => setProperties(res.data || []))
      .catch(() => setProperties([
        {
          id: 'prop1',
          name: 'The Grandview Luxury Apartments',
          address: '500 Skyline Blvd',
          city: 'San Francisco',
          state: 'CA',
          property_type: 'APARTMENT_COMPLEX',
          description: 'High-rise luxury residence featuring panoramic skyline views, rooftop lounge, and 24/7 concierge.',
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
      ]))
      .finally(() => setLoading(false));
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <PublicNavbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Browse Available Residences</h1>
            <p className="text-slate-400 text-sm mt-1">Discover luxury apartments and condos ready for immediate lease.</p>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="glass-panel p-4 rounded-2xl border border-slate-800 mb-8 flex flex-col md:flex-row items-center gap-4">
          <div className="flex-1 flex items-center gap-2 px-3 py-2 bg-slate-900/80 rounded-xl border border-slate-800 w-full">
            <Search className="w-4 h-4 text-brand-400" />
            <input
              type="text"
              placeholder="Search by city name..."
              value={cityFilter}
              onChange={(e) => setCityFilter(e.target.value)}
              className="bg-transparent border-none text-white focus:outline-none text-sm w-full placeholder:text-slate-500"
            />
          </div>

          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-4 py-2.5 bg-slate-900/80 rounded-xl border border-slate-800 text-white text-sm focus:outline-none w-full md:w-48"
          >
            <option value="">All Property Types</option>
            <option value="APARTMENT_COMPLEX">Apartment Complex</option>
            <option value="CONDO">Condo</option>
            <option value="SINGLE_FAMILY">Single Family</option>
          </select>

          <button
            onClick={fetchProperties}
            className="w-full md:w-auto px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-sm font-semibold transition-all shadow-md shadow-brand-600/30 shrink-0"
          >
            Apply Filters
          </button>
        </div>

        {/* Property Grid */}
        {loading ? (
          <div className="text-center py-20 text-slate-400">Loading catalog...</div>
        ) : properties.length === 0 ? (
          <div className="text-center py-20 glass-panel rounded-2xl border border-slate-800">
            <p className="text-slate-400">No properties matched your search parameters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {properties.map(p => (
              <PropertyCard key={p.id} property={p} />
            ))}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
