"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import "./artista.css";

export default function ArtistaDetallePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id;

  const [artist, setArtist] = useState(null);
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);

        const artistRes = await fetch(`http://127.0.0.1:8000/artists/${id}`);
        const artworksRes = await fetch(
          `http://127.0.0.1:8000/artworks/artist/${id}`
        );

        const artistData = await artistRes.json();
        const artworksData = await artworksRes.json();

        setArtist(artistData);
        setArtworks(artworksData || []);
      } finally {
        setLoading(false);
      }
    }
    if (id) load();
  }, [id]);

  if (loading) return <div className="loading">Cargando...</div>;
  if (!artist) return <div className="loading">Artista no encontrado</div>;

  const name = `${artist.name} ${artist.surname}`;

  return (
    <div className="artist-page">

      {/* --------- BOTÓN REGRESAR --------- */}
      <button onClick={() => router.push("/artistas")} className="back-button">
        ← REGRESAR A CATÁLOGO
      </button>

      {/* --------- PERFIL DEL ARTISTA --------- */}
      <section className="artist-header">
        <div className="artist-photo">
          {artist.image_url ? (
            <img src={artist.image_url} alt={name} />
          ) : (
            <div className="no-photo">Sin foto</div>
          )}
        </div>

        <div className="artist-info">
          <h1 className="artist-name">{name}</h1>
          <p className="artist-bio">
            {artist.biography ??
              "La biografía de este artista aún no ha sido registrada en el sistema."}
          </p>
        </div>
      </section>

      {/* --------- OBRAS DEL ARTISTA --------- */}
      <section className="artist-works-section">
        <h2 className="works-title">Obras del Artista en MAC</h2>

        {artworks.length === 0 && (
          <p className="no-works">Aún no hay obras registradas.</p>
        )}

        {artworks.length > 0 && (
          <div className="works-grid">
            {artworks.map((a) => (
              <a key={a.id} href={`/obras/${a.id}`} className="work-card">
                <img
                  src={a.image_url}
                  alt={a.title}
                  className="work-img"
                />
                <div className="work-info">
                  <p className="work-title">{a.title}</p>
                  <p className="work-meta">
                    {artist.name} {artist.surname} — {a.year ?? "Año desconocido"}
                  </p>
                </div>
              </a>
            ))}
          </div>
        )}
      </section>

      {/* --------- COMENTARIOS --------- */}
      <section className="comments-section">
        <h3 className="comments-title">¿Algún comentario?</h3>

        <input
          className="comment-input"
          placeholder="Comparte tu opinión..."
        />

        <div className="comments-list">
          <div className="comment-item">
            <span className="comment-icon">💬</span>
            <p>Interesante pintura! Realmente marcó la historia.</p>
          </div>

          <hr />

          <div className="comment-item">
            <span className="comment-icon">💬</span>
            <p>
              No entendí muy bien la pintura, pero la información adjunta me
              ayudó mucho!
            </p>
          </div>
        </div>

        <button className="see-more">Ver más</button>
      </section>

      {/* --------- FOOTER --------- */}
      <footer className="footer">
        <p>MAC Lima © 2019 | All Rights Reserved</p>
      </footer>
    </div>
  );
}
