'use client';

import { useEffect, useState, useMemo } from 'react';
import { fetchArtists } from '../../lib/api';
import ArtistCard from '../../components/ArtistCard';
import SearchBar from '../../components/SearchBar';
import { searchArtists } from "../../lib/api";


export default function ArtistasPage() {
  const [artists, setArtists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [activeOnly, setActiveOnly] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);

        if (search.trim() !== "") {
          const data = await searchArtists(search, 1, 10);
          setArtists(data.artists || []);
        } else {
          const data = await fetchArtists({ page: 1, page_size: 10 });
          setArtists(data.artists || []);
        }

        setError(null);
      } catch (e) {
        console.error(e);
        setError("Error buscando artistas.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [search]);



  const filtered = useMemo(() => {
    return artists.filter((a) => {
      if (activeOnly && !a.active_artworks) return false;

      const term = search.toLowerCase();
      if (term) {
        const fullName = `${a.name} ${a.surname}`.toLowerCase();
        if (!fullName.includes(term)) return false;
      }
      return true;
    });
  }, [artists, search, activeOnly]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-3xl sm:text-4xl font-serif tracking-[0.25em] mb-8">
        ARTISTAS
      </h1>

      <div className="mb-4">
        <SearchBar
          value={search}
          onChange={setSearch}
          placeholder="Buscar artista..."
        />
      </div>

      <div className="w-full max-w-3xl mb-4">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={activeOnly}
            onChange={(e) => setActiveOnly(e.target.checked)}
          />
          <span>Solo artistas con obras activas en el MAC</span>
        </label>
      </div>

      {loading && <p>Cargando artistas...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && (
        <div className="mt-4 grid gap-y-10 gap-x-6 sm:grid-cols-3 lg:grid-cols-3 justify-items-center">
          {filtered.map((artist) => (
            <ArtistCard key={artist.id} artist={artist} />
          ))}
        </div>
      )}
    </div>
  );
}
