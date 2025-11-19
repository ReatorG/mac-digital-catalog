// app/components/Navbar.jsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { label: 'CONTEMPORÁNEO', href: '#' }, // placeholder
  { label: 'OBRAS', href: '/obras' },
  { label: 'ARTISTAS', href: '/artistas' },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="w-full border-b border-neutral-200 bg-neutral-900 text-white">
      {/* Barra superior pequeña */}
      <div className="text-xs text-center tracking-wide bg-neutral-800 py-1">
        REGRESAR A MUSEO
      </div>

      {/* Barra principal */}
      <div className="flex items-center justify-between px-4 sm:px-10 py-3">
        {/* Logo */}
        <div className="flex items-center gap-3">
          {/* Pon tu svg en /public/assets/mac.svg */}
          <img
            src="/assets/mac.svg"
            alt="MAC Lima"
            className="h-10 w-auto"
          />
          <span className="hidden sm:inline text-xs uppercase tracking-[0.2em]">
            Museo de Arte Contemporáneo
          </span>
        </div>

        {/* Navegación */}
        <nav className="flex items-center gap-6 text-xs sm:text-sm uppercase tracking-[0.25em]">
          {navItems.map((item) => {
            const isActive =
              item.href !== '#' && pathname.startsWith(item.href);
            return (
              <Link
                key={item.label}
                href={item.href === '#' ? '/obras' : item.href}
                className={`pb-1 border-b-2 ${
                  isActive ? 'border-white' : 'border-transparent'
                } hover:border-white/80 transition-colors`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Redes placeholder */}
        <div className="hidden md:flex gap-3 text-xs">
          <span>f</span>
          <span>i</span>
          <span>t</span>
          <span>▶</span>
        </div>
      </div>
    </header>
  );
}
