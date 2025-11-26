import './globals.css';
import NavbarController from '../components/NavbarController';
import Footer from '../components/Footer';

export const metadata = {
  title: 'Catálogo MAC',
  description: 'Catálogo digital de obras y artistas del MAC',
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Heebo:wght@100;200;300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />

        <link
          rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
        />
      </head>

      <body className="min-h-screen bg-white text-neutral-900 flex flex-col m-0 p-0">
        <NavbarController />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
