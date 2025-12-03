import "./footer.css";
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="mac-footer">
      <div className="footer-inner">

        {/* LOGO */}
        <div className="footer-col logo-col">
          <img src="/assets/mac2.png" alt="MAC Lima" className="footer-logo" />
        </div>

        {/* MÁS SOBRE */}
        <div className="footer-col">
          <h3 className="footer-title">Más sobre el MAC Lima</h3>
          <ul>
            <li>Publicaciones</li>
            <li>Archivo MAC Lima</li>
            <li>Centro de documentación</li>
            <li>Oportunidades laborales</li>
            <li>Eventos privados</li>
            <li>Prensa</li>
            <li>Cumplearte</li>
            <li>Cafetería</li>
            <li>Auspicios</li>
            <li>Políticas de uso de los jardines</li>
            <li>Políticas de privacidad</li>
          </ul>
        </div>

        {/* HORARIO */}
        <div className="footer-col">
          <h3 className="footer-title">Horario</h3>
          <p>Abierto: Martes a domingo de 10 a 7 p.m.</p>
          <p>Cerrado: Lunes</p>
          <p className="footer-note">
            *Sujeto a cambios sin previo aviso, según las disposiciones del Gobierno.
          </p>
          <img
            src="/assets/book-claim-icon.png"
            alt="Libro de reclamaciones"
            className="libro-img"
          />
        </div>

        {/* CONTACTO */}
        <div className="footer-col">
          <h3 className="footer-title">Contacto</h3>
          <p>Museo de Arte Contemporáneo de Lima (MAC Lima)</p>
          <p>Av. Grau 1511, Barranco (Lima – Perú)</p>
          <p>Lima 15063</p>
          <p>(01) 513-9000</p>

          <p>contacto@maclima.pe</p>

          <div className="social-row">
            <Link href="https://www.facebook.com/museomaclima/"><i className="fab fa-facebook-f" /></Link>
          <Link href="https://www.instagram.com/museo_maclima/"><i className="fab fa-instagram" /></Link>
          <Link href="https://www.tiktok.com/@museo.mac.lima"><i className="fab fa-tiktok" /></Link>
          <Link href="https://www.linkedin.com/company/mac-lima/"><i className="fab fa-linkedin-in" /></Link>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        Políticas de privacidad | MAC Lima © 2019 | All Rights Reserved
      </div>
    </footer>
  );
}
