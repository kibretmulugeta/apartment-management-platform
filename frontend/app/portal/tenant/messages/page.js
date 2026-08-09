'use client';
import { useState, useEffect } from 'react';
import PortalSidebar from '@/components/navigation/PortalSidebar';
import { Send } from 'lucide-react';
import { getStoredUser } from '@/lib/auth';

export default function TenantMessagesPage() {
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([
    { id: 1, sender: 'Alex Morgan', content: 'Hi, I submitted a plumbing maintenance ticket regarding the kitchen sink.', time: '10:14 AM', isMe: true },
    { id: 2, sender: 'Sarah Jenkins (Property Manager)', content: 'Thanks Alex! I assigned technician Marcus Vance to inspect the faucet seal.', time: '10:20 AM', isMe: false }
  ]);
  const [text, setText] = useState('');

  useEffect(() => {
    setUser(getStoredUser());
  }, []);

  const handleSend = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setMessages([...messages, { id: Date.now(), sender: 'You', content: text, time: 'Just now', isMe: true }]);
    setText('');
  };

  return (
    <div className="flex min-h-screen bg-slate-950">
      <PortalSidebar user={user} role="TENANT" />

      <main className="flex-1 p-8 flex flex-col h-screen">
        <h1 className="text-2xl font-extrabold text-white mb-6">Property Manager Direct Messaging</h1>

        <div className="flex-1 glass-panel rounded-2xl border border-slate-800 flex flex-col overflow-hidden">
          <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-brand-500/20 text-brand-400 flex items-center justify-center font-bold text-xs">SJ</div>
            <div>
              <h4 className="text-sm font-bold text-white">Sarah Jenkins</h4>
              <span className="text-xs text-slate-400">Property Manager (Apex PM)</span>
            </div>
          </div>

          <div className="flex-1 p-6 space-y-4 overflow-y-auto">
            {messages.map(m => (
              <div key={m.id} className={`flex flex-col ${m.isMe ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-md p-3.5 rounded-2xl text-sm ${m.isMe ? 'bg-brand-600 text-white rounded-br-none' : 'bg-slate-900 text-slate-200 border border-slate-800 rounded-bl-none'}`}>
                  {m.content}
                </div>
                <span className="text-[10px] text-slate-500 mt-1">{m.time}</span>
              </div>
            ))}
          </div>

          <form onSubmit={handleSend} className="p-4 bg-slate-900/80 border-t border-slate-800 flex items-center gap-3">
            <input
              type="text"
              placeholder="Type message to property manager..."
              value={text} onChange={e => setText(e.target.value)}
              className="flex-1 px-4 py-2.5 bg-slate-950 rounded-xl border border-slate-800 text-white text-sm focus:outline-none placeholder:text-slate-500"
            />
            <button type="submit" className="p-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white transition-colors">
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
