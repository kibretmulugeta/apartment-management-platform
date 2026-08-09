import './globals.css';

export const metadata = {
  title: 'Apparent — Enterprise Apartment Rental & Property Management Platform',
  description: 'Production-ready SaaS platform for property owners, landlords, tenants, and maintenance teams.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  );
}
