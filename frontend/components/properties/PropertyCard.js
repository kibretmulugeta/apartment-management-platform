import Link from 'next/link';
import { MapPin, Bed, Bath, ArrowUpRight } from 'lucide-react';
import StatusBadge from '@/components/ui/StatusBadge';

export default function PropertyCard({ property }) {
  const primaryImg = property.images?.find(i => i.is_primary)?.url ||
    property.images?.[0]?.url ||
    'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80';

  return (
    <div className="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between group">
      <div>
        <div className="relative h-48 w-full overflow-hidden bg-slate-900">
          <img
            src={primaryImg}
            alt={property.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div className="absolute top-3 right-3">
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-950/80 text-white border border-slate-700 backdrop-blur-md">
              {property.property_type?.replace(/_/g, ' ')}
            </span>
          </div>
        </div>

        <div className="p-5">
          <h3 className="text-lg font-bold text-white group-hover:text-brand-400 transition-colors line-clamp-1">
            {property.name}
          </h3>
          <p className="flex items-center gap-1.5 text-xs text-slate-400 mt-1 mb-3">
            <MapPin className="w-3.5 h-3.5 text-brand-400 shrink-0" />
            <span>{property.address}, {property.city}, {property.state}</span>
          </p>
          <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
            {property.description}
          </p>
        </div>
      </div>

      <div className="px-5 pb-5 pt-3 border-t border-slate-800/60 flex items-center justify-between">
        <div>
          <span className="text-xs text-slate-500 block">Starting at</span>
          <span className="text-xl font-bold text-white">$2,600 <span className="text-xs font-normal text-slate-400">/mo</span></span>
        </div>

        <Link
          href={`/properties/${property.id}`}
          className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-brand-600/20 hover:bg-brand-600 text-brand-400 hover:text-white border border-brand-500/30 text-xs font-semibold transition-all"
        >
          View Details
          <ArrowUpRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
