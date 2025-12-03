'use client';

import { useEffect, useState, useRef } from "react";
import "./artistas.css";
import SearchBar from "../../components/SearchBar";
import FiltersSideBar from "../../components/FiltersArtistas";

export default function ArtistasPage() {
  const [artists, setArtists] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState({});

  const loaderRef = useRef(null);

  function cleanFilters(obj) {
    const out = {};
    for (const key in obj) {
      const val = obj[key];
      if (val !== undefined && val !== "" && val !== null) {
        out[key] = val;
      }
    }
    return out;
  }

  async function loadArtists(p, currentFilters = {}) {
    const cleaned = cleanFilters(currentFilters);
    setLoading(true);

    const queryParams = new URLSearchParams({
      page: p,
      page_size: 6,
    });

    if (cleaned.query) queryParams.append("q", cleaned.query);
    if (cleaned.order) queryParams.append("order", cleaned.order);

    if (cleaned.gender) queryParams.append("gender", cleaned.gender);
    if (cleaned.birth_decade) queryParams.append("birth_decade", cleaned.birth_decade);
    if (cleaned.active_only !== undefined) {
      queryParams.append("active_only", cleaned.active_only);
    }

    try {
      const res = await fetch(`https://mac-digital-catalog.onrender.com/artists/?${queryParams}`);
      const data = await res.json();

      const items = data.artists || [];

      setArtists((prev) => {
        if (p === 1) return items;

        const combined = [...prev, ...items];
        return Array.from(new Map(combined.map((a) => [a.id, a])).values());
      });

      if (items.length < 6) setHasMore(false);

    } catch (err) {
      console.error("Error loading artists:", err);
    }

    setLoading(false);
  }

  useEffect(() => {
    loadArtists(page, filters);
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

  function handleSearch(value) {
    setSearch(value);
    const updated = { ...filters, query: value };
    setFilters(updated);
    setPage(1);
    setArtists([]);
    loadArtists(1, updated);
  }

  function handleFilters(updatedFilters) {
    setFilters(updatedFilters);
    setPage(1);
    setArtists([]);
    loadArtists(1, updatedFilters);
  }

  const [filterOptions, setFilterOptions] = useState({
    genders: [],
    birth_decades: []
  });

  useEffect(() => {
    async function loadFilterOptions() {
      const res = await fetch("https://mac-digital-catalog.onrender.com/artists/filter-options");
      const data = await res.json();
      setFilterOptions(data);
    }
    loadFilterOptions();
  }, []);

  function removeFilter(key, value = null) {
    const updated = { ...filters };
    
    if (value && Array.isArray(updated[key])) {
      updated[key] = updated[key].filter(v => v !== value);
      if (updated[key].length === 0) delete updated[key];
    } else {
      delete updated[key];
    }
    
    handleFilters(updated);
  }

  return (
    <div className="page-layout">

      <aside className="filters-column desktop-only">
        <FiltersSideBar
          filters={filters}
          onChange={handleFilters}
          onClear={() => handleFilters({})}
          options={filterOptions}
          type="artists"
        />

        <div className="active-filters">
          {Object.keys(filters).map((key) => {
            if (key === 'query') return null;

            const value = filters[key];
            if (Array.isArray(value)) {
              return value.map((val) => (
                <span className="filter-tag" key={key + val}>
                  {val} <button onClick={() => removeFilter(key, val)}>×</button>
                </span>
              ));
            }

            return (
              <span className="filter-tag" key={key}>
                {value}
                <button onClick={() => removeFilter(key)}>×</button>
              </span>
            );
          })}
        </div>
      </aside>

      <div className="content-column">
        <h1 className="artistas-title">ARTISTAS</h1>

        <SearchBar
          value={search}
          onChange={handleSearch}
          placeholder="Buscar artista..."
        />

        <div className="filters-mobile-wrapper">
          <FiltersSideBar
            filters={filters}
            onChange={handleFilters}
            onClear={() => handleFilters({})}
            options={filterOptions}
            type="artists"
          />

          <div className="active-filters">
            {Object.keys(filters).map((key) =>
              key !== "query" &&
              (Array.isArray(filters[key])
                ? filters[key].map((val) => (
                    <span className="filter-tag" key={key + val}>
                      {val} <button onClick={() => removeFilter(key, val)}>×</button>
                    </span>
                  ))
                : filters[key] && (
                    <span className="filter-tag" key={key}>
                      {filters[key]}
                      <button onClick={() => removeFilter(key)}>×</button>
                    </span>
                  ))
            )}
          </div>
        </div>

        <div className="artistas-grid">
          {artists.map((artist) => (
            <div className="artist-card" key={artist.id}>
              <a href={`/artistas/${artist.id}`} className="artist-img-wrapper">
                <img
                  src={artist.image_url || "/default-artist.jpg"}
                  alt={`${artist.name} ${artist.surname}`}
                  className="artist-img"
                  onError={(e) => (e.target.src = "/default-artist.jpg")}
                />
              </a>

              <a href={`/artistas/${artist.id}`} className="artist-name hover-text">
                {artist.name} {artist.surname}
              </a>
            </div>
          ))}
        </div>

        {loading && (
          <div className="loader loader-center">
            <span className="dot d1"></span>
            <span className="dot d2"></span>
            <span className="dot d3"></span>
          </div>
        )}

        <div ref={loaderRef} />
      </div>
    </div>
  );
}
