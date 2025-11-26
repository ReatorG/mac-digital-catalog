'use client';

import { usePathname } from 'next/navigation';
import Navbar from './Navbar';

export default function NavbarController() {
  const pathname = usePathname();

  // Ocultar en páginas individuales
  const hideNavbar =
    pathname.startsWith('/obras/') ||
    pathname.startsWith('/artistas/');

  if (hideNavbar) return null;

  return <Navbar />;
}
