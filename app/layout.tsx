import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'CloudCurio.cc - Curate, Compute, Create',
  description: 'Cloud-based platform for script distribution, code reviews, AI chat, and more.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}