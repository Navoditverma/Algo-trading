import Navbar from './components/Navbar';
import './globals.css';

export const metadata = {
  title: 'AlgoTradeX',
  description: 'Algorithmic Trading Platform Prototype',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-white text-black">
        <Navbar />
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}
