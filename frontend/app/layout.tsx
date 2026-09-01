import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Kasparro - Product AI Readiness Auditor',
  description: 'Check if your product descriptions are ready for AI shopping assistants.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-warm to-orange-50">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}
