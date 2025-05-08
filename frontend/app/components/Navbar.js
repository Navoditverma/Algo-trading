// components/Navbar.js
'use client'

import Link from 'next/link'

const navItems = [
  { name: 'Dashboard', href: '/dashboard' },
  { name: 'Strategies', href: '/strategies' },
  { name: 'Backtest', href: '/backtest' },
  { name: 'Live Trading', href: '/live-trading' },
  { name: 'History', href: '/history' },
  { name: 'Logs', href: '/logs' },
]

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white p-4 flex gap-6">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="hover:text-blue-400 transition"
        >
          {item.name}
        </Link>
      ))}
    </nav>
  )
}
