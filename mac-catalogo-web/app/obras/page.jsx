// app/obras/page.jsx
'use client';

import { useEffect, useState, useMemo } from 'react';
import { fetchArtworks } from '../lib/api';
import ArtworkCard from '../components/ArtworkCard';
import SearchBar from '../components/SearchBar';
import ArtworkFilterPanel from '../components/ArtworkFilterPanel';

export default function ObrasPage() {
  const [artworks, setArtworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    onDisplayOnly: false,
    technique: null,
    materials: null,
    location: null,
  });

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await fetchArtworks({ page: 1, page_size: 200 });
        setArtworks(data.artworks || []);
        setError(null);
      } catch (e) {
        console.error(e);
        setError('No se pudieron cargar las obras.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = useMemo(() => {
    return artworks.filter((a) => {
      // search por título o artista
      const term = search.toLowerCase();
      if (term) {
        const artistName = `${a.artist_name || ''} ${a.artist_surname || ''}`;
        const matchTitle = a.title?.toLowerCase().includes(term);
        const matchArtist = artistName.toLowerCase().includes(term);
        if (!matchTitle && !matchArtist) return false;
      }

      if (filters.onDisplayOnly && !a.on_display) return false;
      if (filters.technique && a.technique !== filters.technique) return false;
      if (filters.materials && a.materials !== filters.materials) return false;
      if (filters.location && a.location !== filters.location) return false;

      return true;
    });
  }, [artworks, search, filters]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif tracking-[0.25em] mb-8">
        OBRAS
      </h1>

      {/* Buscador + filtros */}
      <div className="mb-6">
        <SearchBar
          value={search}
          onChange={setSearch}
          placeholder="Buscar obra o artista..."
        />
      </div>

      <ArtworkFilterPanel
        artworks={artworks}
        filters={filters}
        onChangeFilters={setFilters}
      />

      {loading && <p>Cargando obras...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && (
        <div className="mt-4 grid gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 justify-items-center">
          {filtered.map((artwork) => (
            <ArtworkCard key={artwork.id} artwork={artwork} />
          ))}
        </div>
      )}
    </div>
  );
}
