'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import StatusBadge from '@/components/ui/StatusBadge';
import Modal from '@/components/ui/Modal';
import { Plus, Building2, Home, MapPin, Edit3 } from 'lucide-react';
import { api } from '@/lib/api';
import { getStoredUser } from '@/lib/auth';

export default function LandlordPropertiesPage() {
  const [user, setUser] = useState(null);
  const [properties, setProperties] = useState([]);
  const [units, setUnits] = useState([]);
  const [isPropModalOpen, setIsPropModalOpen] = useState(false);
  const [isUnitModalOpen, setIsUnitModalOpen] = useState(false);

  const [newProp, setNewProp] = useState({ name: '', address: '', city: 'San Francisco', state: 'CA', postal_code: '94102', property_type: 'APARTMENT_COMPLEX' });
  const [newUnit, setNewUnit] = useState({ property_id: '', unit_number: '', bedrooms: 1, bathrooms: 1.0, rent_amount: '2500.00', deposit_amount: '2500.00', status: 'AVAILABLE' });

  useEffect(() => {
    setUser(getStoredUser());
    loadData();
  }, []);

  const loadData = () => {
    api.get('/properties/')
      .then(res => setProperties(res.data || []))
      .catch(() => setProperties([
        { id: 'prop1', name: 'The Grandview Luxury Apartments', address: '500 Skyline Blvd', city: 'San Francisco', state: 'CA', property_type: 'APARTMENT_COMPLEX' },
        { id: 'prop2', name: 'Bayview Urban Terraces', address: '220 Embarcadero Rd', city: 'San Francisco', state: 'CA', property_type: 'CONDO' }
      ]));

    api.get('/units/')
      .then(res => setUnits(res.data || []))
      .catch(() => setUnits([
        { id: 'u1', property_id: 'prop1', unit_number: '14B', bedrooms: 2, bathrooms: '2.0', rent_amount: '3450.00', status: 'OCCUPIED' },
        { id: 'u2', property_id: 'prop1', unit_number: '8A', bedrooms: 1, bathrooms: '1.0', rent_amount: '2600.00', status: 'AVAILABLE' }
      ]));
  };

  const handleCreateProperty = (e) => {
    e.preventDefault();
    api.post('/properties/', newProp)
      .then(() => {
        setIsPropModalOpen(false);
        loadData();
      })
      .catch(() => {
        setIsPropModalOpen(false);
      });
  };

  const handleCreateUnit = (e) => {
    e.preventDefault();
    api.post('/units/', newUnit)
      .then(() => {
        setIsUnitModalOpen(false);
        loadData();
      })
      .catch(() => {
        setIsUnitModalOpen(false);
      });
  };

  const handleStatusToggle = (unitId, currentStatus) => {
    const nextStatus = currentStatus === 'AVAILABLE' ? 'OCCUPIED' : 'AVAILABLE';
    api.put(`/units/${unitId}/status?status_str=${nextStatus}`)
      .then(() => loadData())
      .catch(() => {});
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="LANDLORD" />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-extrabold text-white">Properties & Units Manager</h1>
            <p className="text-slate-400 text-xs mt-1">Manage real estate inventory, unit availability, and pricing.</p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsPropModalOpen(true)}
              className="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-md shadow-brand-600/30"
            >
              <Plus className="w-4 h-4" /> Add Property
            </button>
            <button
              onClick={() => setIsUnitModalOpen(true)}
              className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center gap-2 border border-slate-700 transition-colors"
            >
              <Plus className="w-4 h-4" /> Add Unit
            </button>
          </div>
        </div>

        {/* Properties Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          {properties.map(p => (
            <div key={p.id} className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Building2 className="w-5 h-5 text-brand-400" />
                  <h3 className="text-lg font-bold text-white">{p.name}</h3>
                </div>
                <p className="flex items-center gap-1.5 text-xs text-slate-400">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" />
                  {p.address}, {p.city}, {p.state}
                </p>
                <span className="inline-block mt-3 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-900 border border-slate-800 text-slate-300">
                  {p.property_type?.replace(/_/g, ' ')}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Units Data Table */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-4">Unit Inventory ({units.length} total)</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs uppercase bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Unit #</th>
                  <th className="py-3 px-4">Beds / Baths</th>
                  <th className="py-3 px-4">Rent Amount</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Quick Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {units.map(u => (
                  <tr key={u.id} className="hover:bg-slate-900/40">
                    <td className="py-3 px-4 font-bold text-white">{u.unit_number}</td>
                    <td className="py-3 px-4">{u.bedrooms} Bed / {u.bathrooms} Bath</td>
                    <td className="py-3 px-4 font-bold text-emerald-400">${u.rent_amount}</td>
                    <td className="py-3 px-4"><StatusBadge status={u.status} /></td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleStatusToggle(u.id, u.status)}
                        className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 transition-colors"
                      >
                        Toggle Status
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Add Property Modal */}
      <Modal isOpen={isPropModalOpen} onClose={() => setIsPropModalOpen(false)} title="Add New Property">
        <form onSubmit={handleCreateProperty} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Property Name</label>
            <input
              type="text" required
              value={newProp.name} onChange={e => setNewProp({ ...newProp, name: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Address</label>
            <input
              type="text" required
              value={newProp.address} onChange={e => setNewProp({ ...newProp, address: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">City</label>
              <input
                type="text" required
                value={newProp.city} onChange={e => setNewProp({ ...newProp, city: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">State</label>
              <input
                type="text" required
                value={newProp.state} onChange={e => setNewProp({ ...newProp, state: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <button type="submit" className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Create Property
          </button>
        </form>
      </Modal>

      {/* Add Unit Modal */}
      <Modal isOpen={isUnitModalOpen} onClose={() => setIsUnitModalOpen(false)} title="Add Unit to Property">
        <form onSubmit={handleCreateUnit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Select Property</label>
            <select
              value={newUnit.property_id} onChange={e => setNewUnit({ ...newUnit, property_id: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
            >
              <option value="">Select Property</option>
              {properties.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Unit Number</label>
              <input
                type="text" required
                value={newUnit.unit_number} onChange={e => setNewUnit({ ...newUnit, unit_number: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Monthly Rent ($)</label>
              <input
                type="number" step="0.01" required
                value={newUnit.rent_amount} onChange={e => setNewUnit({ ...newUnit, rent_amount: e.target.value })}
                className="w-full px-3 py-2 bg-slate-900 rounded-lg border border-slate-800 text-white text-sm focus:outline-none"
              />
            </div>
          </div>
          <button type="submit" className="w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm rounded-xl transition-colors mt-2">
            Create Unit
          </button>
        </form>
      </Modal>
    </div>
  );
}
