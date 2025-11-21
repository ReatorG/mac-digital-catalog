'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { fetchArtworkById } from '../../../lib/api';
import CommentsSection from '../../../components/CommentsSection';

export default function ObraDetallePage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id;

  const [artwork, setArtwork] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
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
    };
    if (id) load();
  }, [id]);

  if (loading) return <div className="p-10">Cargando...</div>;
  if (error) return <div className="p-10 text-red-600">{error}</div>;
  if (!artwork) return <div className="p-10">No encontrada.</div>;

  const artistName =
    artwork.artist_name && artwork.artist_surname
      ? `${artwork.artist_name} ${artwork.artist_surname}`
      : '';
  const year = artwork.year || '';
  const technique = artwork.technique || '';

  return (
    <div className="w-full">
      <section
        className="relative h-[70vh] sm:h-screen text-white overflow-hidden"
        style={{
          backgroundImage: `url(${artwork.image_url || ''})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed',
        }}
      >
        <div className="absolute inset-0 bg-black/40" />

        <div className="relative z-10 flex flex-col h-full">
          <button
            onClick={() => router.push('/obras')}
            className="mt-6 ml-4 text-xs uppercase tracking-[0.2em]"
          >
            ← REGRESAR A CATÁLOGO
          </button>

          <div className="flex-1 flex items-end justify-center pb-16 px-4">
            <div className="text-center max-w-2xl">
              <h1 className="text-3xl sm:text-4xl font-serif mb-2">
                {artwork.title}
              </h1>
              <p className="text-sm sm:text-base">
                {artistName}
                {technique && `  -  ${technique}`}
                {year && `  -  ${year}`}
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-cover bg-center bg-fixed text-white relative py-16 px-4 sm:px-6"
        style={{
          backgroundImage: `url(${artwork.image_url || ''})`,
        }}
      >
        <div className="absolute inset-0 bg-black/45" />
        <div className="relative max-w-3xl mx-auto text-center leading-relaxed text-sm sm:text-base">
          <p>
            {artwork.description ||
              'La descripción de esta obra aún no ha sido registrada en el sistema.'}
          </p>
        </div>
      </section>

      <section className="bg-white py-14 px-4 sm:px-6">
        <div className="max-w-5xl mx-auto grid gap-8 lg:grid-cols-[1.3fr,1fr]">
          <div>
            <h2 className="text-2xl font-serif mb-6">Datos Técnicos</h2>
            <div className="border border-neutral-300 p-5 text-sm leading-relaxed">
              <p>
                <span className="font-semibold">Título:</span> {artwork.title}
              </p>
              {artistName && (
                <p>
                  <span className="font-semibold">Autor:</span> {artistName}
                </p>
              )}
              {year && (
                <p>
                  <span className="font-semibold">Año:</span> {year}
                </p>
              )}
              {technique && (
                <p>
                  <span className="font-semibold">Técnica:</span> {technique}
                </p>
              )}
              {artwork.materials && (
                <p>
                  <span className="font-semibold">Materiales:</span>{' '}
                  {artwork.materials}
                </p>
              )}
              {artwork.location && (
                <p>
                  <span className="font-semibold">Ubicación actual:</span>{' '}
                  {artwork.location}
                </p>
              )}
            </div>
          </div>

          <div className="flex flex-col items-center gap-4">
            <div className="w-40 h-40 sm:w-52 sm:h-52 bg-neutral-100 overflow-hidden shadow-sm">
              {artwork.image_url && (
                <img
                  src={artwork.image_url}
                  alt={artwork.title}
                  className="h-full w-full object-cover"
                />
              )}
            </div>
            <div className="w-32 h-32 sm:w-40 sm:h-40 bg-neutral-100 overflow-hidden shadow-sm">
              {artwork.image_url && (
                <img
                  src={artwork.image_url}
                  alt={artwork.title}
                  className="h-full w-full object-cover"
                />
              )}
            </div>
          </div>
        </div>

        <CommentsSection artworkId={artwork.id} />

      </section>
    </div>
  );
}
