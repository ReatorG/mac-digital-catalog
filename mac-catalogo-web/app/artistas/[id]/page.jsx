// app/artistas/[id]/page.jsx
'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
  fetchArtistById,
  fetchArtworksByArtist,
} from '../../lib/api';
import ArtworkCard from '../../components/ArtworkCard';
import CommentsSection from '../../components/CommentsSection';

export default function ArtistaDetallePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id;

  const [artist, setArtist] = useState(null);
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [artistData, artworksData] = await Promise.all([
          fetchArtistById(id),
          fetchArtworksByArtist(id),
        ]);
        setArtist(artistData);
        setArtworks(artworksData || []);
        setError(null);
      } catch (e) {
        console.error(e);
        setError('No se pudo cargar el artista.');
      } finally {
        setLoading(false);
      }
    };
    if (id) load();
  }, [id]);

  if (loading) return <div className="p-10">Cargando...</div>;
  if (error) return <div className="p-10 text-red-600">{error}</div>;
  if (!artist) return <div className="p-10">No encontrado.</div>;

  const fullName = `${artist.name} ${artist.surname}`;

  return (
    <div className="w-full">
      {/* Sección superior con foto redonda y biografía */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
        <button
          onClick={() => router.push('/artistas')}
          className="mb-6 text-xs uppercase tracking-[0.2em]"
        >
          ← REGRESAR A CATÁLOGO
        </button>

        <div className="grid gap-10 md:grid-cols-[1fr,1.2fr] items-center">
          <div className="flex justify-center">
            <div className="w-40 h-40 sm:w-56 sm:h-56 rounded-full overflow-hidden bg-neutral-200 shadow-sm">
              {artist.image_url ? (
                <img
                  src={artist.image_url}
                  alt={fullName}
                  className="h-full w-full object-cover"
                />
              ) : (
                <div className="h-full w-full flex items-center justify-center text-xs text-neutral-400">
                  Sin foto
                </div>
              )}
            </div>
          </div>

          <div>
            <h1 className="text-3xl sm:text-4xl font-serif mb-4">
              {fullName}
            </h1>
            <p className="text-sm sm:text-base leading-relaxed text-neutral-700">
              {artist.biography ||
                'La biografía de este artista aún no ha sido registrada en el sistema.'}
            </p>
          </div>
        </div>
      </section>

      {/* Obras del artista */}
      <section className="bg-white border-t border-neutral-200 py-10 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-xl sm:text-2xl font-serif mb-6">
            Obras del Artista en MAC
          </h2>

          {artworks.length === 0 && (
            <p className="text-sm text-neutral-600">
              Aún no hay obras registradas para este artista.
            </p>
          )}

          {artworks.length > 0 && (
            <div className="grid gap-y-10 gap-x-6 sm:grid-cols-3 justify-items-center">
              {artworks.map((aw) => (
                <ArtworkCard key={aw.id} artwork={aw} />
              ))}
            </div>
          )}

          <CommentsSection
            initialComments={[
              {
                id: 1,
                text: 'Interesante trayectoria artística, realmente influyente.',
              },
              {
                id: 2,
                text:
                  'No conocía mucho al artista, pero la información adjunta me ayudó bastante.',
              },
            ]}
          />
        </div>
      </section>
    </div>
  );
}
