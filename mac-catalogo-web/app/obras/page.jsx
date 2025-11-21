"use client";

import { useEffect, useState, useRef } from "react";
import "./obras.css";

export default function ObrasPage() {
  const [artworks, setArtworks] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);

  const loaderRef = useRef(null);

  async function loadArtworks(p) {
    setLoading(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/artworks/?page=${p}&page_size=6`
      );
      const data = await res.json();

      const items = data.items ?? data.artworks ?? [];

      setArtworks((prev) => [...prev, ...items]);

      if (items.length < 6) {
        setHasMore(false);
      }
    } catch (err) {
      console.error("Error loading artworks:", err);
    }

    setLoading(false);
  }

  useEffect(() => {
    loadArtworks(page);
  }, [page]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          setPage((p) => p + 1);
        }
      },
      { threshold: 1 }
    );

    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [hasMore, loading]);

  return (
    <div className="obras-wrapper">
      <h1 className="obras-title">OBRAS</h1>

      <div className="obras-grid">
        {artworks.map((a) => (
          <div className="art-card" key={a.id}>
            <div className="art-img-wrapper">
              <img
                src={a.image_url || "/placeholder.png"}
                alt={a.title}
                className="art-img"
                onError={(e) => (e.target.src = "/placeholder.png")}
              />
            </div>

            <h3 className="art-title">{a.title || "Sin título"}</h3>

            <p className="art-meta">
              {a.artist_name} {a.artist_surname} — {a.year || "Año desconocido"}
            </p>
          </div>
        ))}
      </div>

      {loading && (
        <div className="loader">
          <span className="dot d1"></span>
          <span className="dot d2"></span>
          <span className="dot d3"></span>
        </div>
      )}

      <div ref={loaderRef} />
    </div>
  );
}
