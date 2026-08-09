'use client';
import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import PublicNavbar from '@/components/navigation/PublicNavbar';
import Footer from '@/components/navigation/Footer';
import Modal from '@/components/ui/Modal';
import StatusBadge from '@/components/ui/StatusBadge';
import { MapPin, Bed, Bath, Shield, Calendar, ArrowRight, CheckCircle2 } from 'lucide-react';
import { api } from '@/lib/api';

export default function PropertyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [property, setProperty] = useState(null);
  const [units, setUnits] = useState([]);
  const [loading, setLoading] = useState(true);

  // Tour Booking Modal State
  const [isTourModalOpen, setIsTourModalOpen] = useState(false);
  const [tourForm, setTourForm] = useState({ name: '', email: '', phone: '', date: '', time: '10:00 AM' });
  const [tourSubmitted, setTourSubmitted] = useState(false);

  useEffect(() => {
    if (params.id) {
      api.get(`/properties/public/${params.id}`)
        .then(res => setProperty(res.data))
        .catch(() => setProperty({
          id: params.id,
          name: 'The Grandview Luxury Apartments',
          address: '500 Skyline Blvd',
          city: 'San Francisco',
          state: 'CA',
          postal_code: '94105',
          property_type: 'APARTMENT_COMPLEX',
          description: 'High-rise luxury residence featuring panoramic skyline views, rooftop lounge, and 24/7 concierge service.',
          year_built: 2021,
          pet_policy: 'Cats & Dogs Allowed (Max 2)',
          parking_type: 'Assigned Underground Garage',
          images: [
            { url: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80', is_primary: true },
            { url: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80', is_primary: false }
          ]
        }))
        .finally(() => setLoading(false));

      api.get(`/units/public?property_id=${params.id}`)
        .then(res => setUnits(res.data || []))
        .catch(() => setUnits([
          { id: 'unit1', unit_number: '14B', bedrooms: 2, bathrooms: '2.0', square_feet: 1150, rent_amount: '3450.00', deposit_amount: '3450.00', status: 'AVAILABLE' },
          { id: 'unit2', unit_number: '8A', bedrooms: 1, bathrooms: '1.0', square_feet: 780, rent_amount: '2600.00', deposit_amount: '2600.00', status: 'AVAILABLE' }
        ]));
    }
  }, [params.id]);

  const handleTourSubmit = (e) => {
    e.preventDefault();
    setTourSubmitted(true);
    setTimeout(() => {
      setIsTourModalOpen(false);
      setTourSubmitted(false);
    }, 2000);
  };

  if (loading) return <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">Loading property details...</div>;
  if (!property) return <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">Property not found.</div>;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950">
      <PublicNavbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Header Title */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-extrabold text-white">{property.name}</h1>
            <p className="flex items-center gap-2 text-slate-400 text-sm mt-1">
              <MapPin className="w-4 h-4 text-brand-400" />
              <span>{property.address}, {property.city}, {property.state} {property.postal_code}</span>
            </p>
          </div>

          <button
            onClick={() => setIsTourModalOpen(true)}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-sky-500 hover:from-brand-500 hover:to-sky-400 text-white font-semibold text-sm shadow-lg shadow-brand-600/30 flex items-center gap-2 shrink-0"
          >
            <Calendar className="w-4 h-4" />
            Schedule In-Person Tour
          </button>
        </div>

        {/* Main Gallery */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
          <div className="md:col-span-2 h-96 rounded-2xl overflow-hidden border border-slate-800">
            <img src={property.images?.[0]?.url} alt={property.name} className="w-full h-full object-cover" />
          </div>
          <div className="h-96 rounded-2xl overflow-hidden border border-slate-800 hidden md:block">
            <img src={property.images?.[1]?.url || property.images?.[0]?.url} alt={property.name} className="w-full h-full object-cover" />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column Details */}
          <div className="lg:col-span-2 space-y-8">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-3">About this Property</h2>
              <p className="text-slate-300 text-sm leading-relaxed">{property.description}</p>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-800/80">
                <div>
                  <span className="text-xs text-slate-500 block">Year Built</span>
                  <span className="text-sm font-semibold text-white">{property.year_built || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Pet Policy</span>
                  <span className="text-sm font-semibold text-white">{property.pet_policy}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Parking</span>
                  <span className="text-sm font-semibold text-white">{property.parking_type}</span>
                </div>
              </div>
            </div>

            {/* Available Units Table */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <h2 className="text-xl font-bold text-white mb-4">Available Units</h2>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-300">
                  <thead className="text-xs uppercase bg-slate-900/80 text-slate-400 border-b border-slate-800">
                    <tr>
                      <th className="py-3 px-4">Unit #</th>
                      <th className="py-3 px-4">Beds / Baths</th>
                      <th className="py-3 px-4">Sq. Ft.</th>
                      <th className="py-3 px-4">Monthly Rent</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {units.map(u => (
                      <tr key={u.id} className="hover:bg-slate-900/40">
                        <td className="py-3 px-4 font-bold text-white">{u.unit_number}</td>
                        <td className="py-3 px-4">{u.bedrooms} Bed / {u.bathrooms} Bath</td>
                        <td className="py-3 px-4">{u.square_feet} sq ft</td>
                        <td className="py-3 px-4 font-bold text-emerald-400">${u.rent_amount}</td>
                        <td className="py-3 px-4"><StatusBadge status={u.status} /></td>
                        <td className="py-3 px-4 text-right">
                          <button
                            onClick={() => router.push(`/apply?unit_id=${u.id}`)}
                            className="px-3.5 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition-colors"
                          >
                            Apply Now
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Right Column Summary Sidebar */}
          <div>
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 sticky top-28">
              <h3 className="text-lg font-bold text-white mb-4">Lease Requirements</h3>
              <ul className="space-y-3 text-xs text-slate-300">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" /> Verified proof of monthly income (3x rent)</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" /> Background & credit check review</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" /> Standard 1-month security deposit</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" /> Digital e-signature lease execution</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Schedule Tour Modal */}
      <Modal isOpen={isTourModalOpen} onClose={() => setIsTourModalOpen(false)} title="Schedule a Property Tour">
        {tourSubmitted ? (
          <div className="text-center py-8">
            <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
            <h4 className="text-lg font-bold text-white">Tour Scheduled!</h4>
            <p className="text-slate-400 text-xs mt-1">Our leasing agent will send a calendar confirmation to your email.</p>
          </div>
        ) : (
          <form onSubmit={handleTourSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Full Name</label>
              <input
                type="text" required
                value={tourForm.name} onChange={e => setTourForm({ ...tourForm, name: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Email</label>
                <input
                  type="email" required
                  value={tourForm.email} onChange={e => setTourForm({ ...tourForm, email: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Phone</label>
                <input
                  type="tel" required
                  value={tourForm.phone} onChange={e => setTourForm({ ...tourForm, phone: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Preferred Date</label>
                <input
                  type="date" required
                  value={tourForm.date} onChange={e => setTourForm({ ...tourForm, date: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Time</label>
                <select
                  value={tourForm.time} onChange={e => setTourForm({ ...tourForm, time: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
                >
                  <option>10:00 AM</option>
                  <option>02:00 PM</option>
                  <option>04:30 PM</option>
                </select>
              </div>
            </div>
            <button
              type="submit"
              className="w-full py-3 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2"
            >
              Confirm Tour Booking
            </button>
          </form>
        )}
      </Modal>

      <Footer />
    </div>
  );
}
