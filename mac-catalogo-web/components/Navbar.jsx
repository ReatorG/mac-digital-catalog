'use client';
import Link from 'next/link';
import './navbar.css';

export default function Navbar() {
  return (
    <header className="navbar-container">

      <div className="nav-top">
        <div className="nav-top-left">
          <Link href="https://maclima.pe/">REGRESAR A MUSEO</Link>
        </div>

        <div className="nav-top-right">
          <Link href="https://www.facebook.com/museomaclima/"><i className="fab fa-facebook-f" /></Link>
          <Link href="https://www.instagram.com/museo_maclima/"><i className="fab fa-instagram" /></Link>
          <Link href="https://www.tiktok.com/@museo.mac.lima"><i className="fab fa-tiktok" /></Link>
          <Link href="https://www.linkedin.com/company/mac-lima/"><i className="fab fa-linkedin-in" /></Link>
        </div>
      </div>

      <div className="nav-middle">

        <div className="nav-logo-container">
          <img src="/assets/mac.png" alt="MAC Lima" className="nav-logo" />
        </div>

        <nav className="nav-menu">
          <Link href="/obras">OBRAS</Link>
          <Link href="/artistas">ARTISTAS</Link>
        </nav>

      </div>

    </header>
  );
}
