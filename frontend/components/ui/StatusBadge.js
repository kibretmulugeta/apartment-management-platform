export default function StatusBadge({ status }) {
  const normalized = (status || '').toUpperCase();
  
  const styles = {
    // Unit / Property Statuses
    AVAILABLE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    OCCUPIED: 'bg-brand-500/10 text-brand-400 border-brand-500/30',
    RESERVED: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    APPLICATION_PENDING: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    MAINTENANCE: 'bg-rose-500/10 text-rose-400 border-rose-500/30',

    // Lease & Application Statuses
    ACTIVE: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    PENDING_SIGNATURE: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    APPROVED: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    REJECTED: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    SUBMITTED: 'bg-sky-500/10 text-sky-400 border-sky-500/30',

    // Payment Statuses
    SUCCEEDED: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    PENDING: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    FAILED: 'bg-rose-500/10 text-rose-400 border-rose-500/30',

    // Maintenance Request Statuses
    OPEN: 'bg-sky-500/10 text-sky-400 border-sky-500/30',
    ASSIGNED: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    IN_PROGRESS: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    COMPLETED: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
  };

  const badgeStyle = styles[normalized] || 'bg-slate-800 text-slate-300 border-slate-700';

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${badgeStyle}`}>
      {normalized.replace(/_/g, ' ')}
    </span>
  );
}
