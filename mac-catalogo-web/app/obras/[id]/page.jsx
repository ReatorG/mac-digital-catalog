'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { fetchArtworkById } from '../../../lib/api';
import CommentsSection from '../../../components/CommentsSection';
import './obra.css';

export default function ObraDetallePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id;

  const [artwork, setArtwork] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    function onScroll() {
        const scrollY = window.scrollY;
        const vh = window.innerHeight;

        const hero = document.querySelector('.obra-hero-text');
        const desc = document.querySelector('.obra-description-content');

        if (!hero || !desc) return;

        const heroFade = Math.min(1, scrollY / (vh * 0.5));
        hero.style.opacity = `${1 - heroFade}`;

        const heroOverlay = document.querySelector('.obra-hero-overlay');
        if (heroOverlay) {
          heroOverlay.style.opacity = `${1 - heroFade}`;
        }
        const descStart = vh * 0.9;
        const descEnd   = vh * 2.3;

        let descOpacity = 0;

        if (scrollY < descStart) {
          descOpacity = 0;
        } else if (scrollY > descEnd) {
          descOpacity = 0;
        } else {
          const full = descEnd - descStart;

          const fadeIn = full * 0.25;

          if (scrollY - descStart < fadeIn) {
            descOpacity = (scrollY - descStart) / fadeIn;
          }
          else if (scrollY - descStart < full * 0.7) {
            descOpacity = 1;
          }
          else {
            const fadeOut = full * 0.3;
            descOpacity = 1 - ((scrollY - descStart - full * 0.7) / fadeOut);
          }
        }



        const descOverlay = document.querySelector('.obra-description-overlay');
        if (descOverlay) {
          descOverlay.style.opacity = descOpacity;
        }

        descOpacity = Math.max(0, Math.min(1, descOpacity));

        if (descOverlay) {
          descOverlay.style.opacity = descOpacity;
        }

        desc.style.opacity = descOpacity;
      }
    

    window.addEventListener('scroll', onScroll);
    onScroll();

    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await fetchArtworkById(id);
        setArtwork(data);
        setError(null);
      } catch (e) {
        console.error(e);
        setError('No se pudo cargar la obra.');
      } finally {
        setLoading(false);
      }
    }
    if (id) load();
  }, [id]);

  if (loading) {
    return (
      <div className="obra-loader-wrapper">
        <div className="loader">
          <span className="dot d1"></span>
          <span className="dot d2"></span>
          <span className="dot d3"></span>
        </div>
      </div>
    );
  }

  if (error) return <div className="obra-error">{error}</div>;
  if (!artwork) return <div className="obra-error">Obra no encontrada.</div>;

  const artistName =
    artwork.artist_name && artwork.artist_surname
      ? `${artwork.artist_name} ${artwork.artist_surname}`
      : '';

  const year = artwork.year || '';
  const technique = artwork.technique || '';
  const bgImage = artwork.image_url || '/cat.jpg';

  return (
    <div className="obra-page">
      <div
        className="obra-fixed-bg"
        style={{ backgroundImage: `url(${bgImage})` }}
      />

      <section className="obra-hero">
        <div className="obra-hero-overlay" />

        <button
          onClick={() => router.push('/obras')}
          className="obra-back-btn"
        >
          ← REGRESAR A CATÁLOGO
        </button>

        <div className="obra-hero-text">
          <h1 className="obra-title">{artwork.title}</h1>

          <p className="obra-subtitle">
            {artistName && <span>{artistName}</span>}
            {technique && <span> • {technique}</span>}
            {year && <span> • {year}</span>}
          </p>

        </div>
      </section>

      <section className="obra-gap"></section>

      <section className="obra-description-section">
        <div className="obra-description-overlay" />
        <div className="obra-description-content">
          <p>
            {artwork.description ||
              'La descripción de esta obra aún no ha sido registrada.'}
          </p>
        </div>
      </section>

      <div className="obra-description-bottom-gap"></div>

      <section className="obra-details-section">
        <div className="obra-details-inner">
          <div className="obra-tech">
            <h2 className="obra-tech-title">Datos Técnicos</h2>

            <div className="obra-tech-box">
              <p>
                <span className="obra-tech-label">Título:</span> {artwork.title}
              </p>
              {artistName && (
                <p>
                  <span className="obra-tech-label">Autor:</span>{" "}
                  <a
                    href={`/artistas/${artwork.artist_id}`}
                    className="obra-tech-artist-link"
                  >
                    {artistName}
                  </a>
                </p>
              )}
              {year && (
                <p>
                  <span className="obra-tech-label">Año:</span> {year}
                </p>
              )}
              {technique && (
                <p>
                  <span className="obra-tech-label">Técnica:</span> {technique}
                </p>
              )}
              {artwork.materials && (
                <p>
                  <span className="obra-tech-label">Materiales:</span>{' '}
                  {artwork.materials}
                </p>
              )}
              {artwork.location && (
                <p>
                  <span className="obra-tech-label">Ubicación:</span>{' '}
                  {artwork.location}
                </p>
              )}
            </div>
          </div>

          <div className="obra-tech-image">
            <img src={bgImage} alt={artwork.title} />
          </div>
        </div>

        <div className="obra-comments-wrapper">
          <CommentsSection
            artworkId={artwork.id}
            initialComments={[
              { id: 1, text: 'El cielo parece estar vivo, impresionante.' },
              { id: 2, text: 'Una obra que transmite mucha emoción.' },
            ]}
          />
        </div>
      </section>
    </div>
  );
}


