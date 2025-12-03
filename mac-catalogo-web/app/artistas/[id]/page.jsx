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

        const artistRes = await fetch(`https://mac-digital-catalog.onrender.com/artists/${id}`);
        const artworksRes = await fetch(
          `https://mac-digital-catalog.onrender.com/artworks/artist/${id}`
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

  if (loading)
    return (
      <div className="loader-center">
        <span className="dot d1"></span>
        <span className="dot d2"></span>
        <span className="dot d3"></span>
      </div>
    );

  if (!artist) return <div className="loading">Artista no encontrado</div>;

  const name = `${artist.name} ${artist.surname}`;

  return (
    <div className="artist-page">

      <button onClick={() => router.push("/artistas")} className="back-button">
        ← REGRESAR A CATÁLOGO
      </button>

      <section className="artist-header">
        <div className="artist-photo">
          {artist.image_url ? (
            <img src={artist.image_url} alt={name} />
          ) : (
            <div className="no-photo">Sin foto</div>
          )}
        </div>

        <div className="artist-text">
          <h1 className="artist-name">{name}</h1>

          <p className="artist-bio">
            {artist.biography ??
              "La biografía de este artista aún no ha sido registrada en el sistema."}
          </p>
        </div>
      </section>


      <section className="artist-works-section">
        <h2 className="works-title">Obras del Artista en MAC</h2>

        {artworks.length === 0 && (
          <p className="no-works">Aún no hay obras registradas.</p>
        )}

        {artworks.length > 0 && (
          <div className="works-grid mobile-two-cols">
            {artworks.map((a) => (
              <a key={a.id} href={`/obras/${a.id}`} className="work-card">
                <img src={a.image_url} alt={a.title} className="work-img" />
                <div className="work-info">
                  <p className="work-title">{a.title}</p>
                  <p className="work-meta">
                    {artist.name} {artist.surname} —{" "}
                    {a.year ?? "Año desconocido"}
                  </p>
                </div>
              </a>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
