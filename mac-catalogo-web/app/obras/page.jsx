"use client";

import { useEffect, useState, useRef } from "react";
import "./obras.css";
import SearchBar from "../../components/SearchBar";
import FiltersSideBar from "../../components/FiltersArtwork";

export default function ObrasPage() {
  const [artworks, setArtworks] = useState([]);
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

  function removeFilter(key, value = null) {
    const updated = { ...filters };

    if (value && Array.isArray(updated[key])) {
      updated[key] = updated[key].filter(v => v !== value);
      if (updated[key].length === 0) delete updated[key];
    } else {
      delete updated[key];
    }

    setFilters(updated);
    setPage(1);
    setArtworks([]);
    loadArtworks(1, updated);
  }

  async function loadArtworks(p, currentFilters = {}) {
    const cleaned = cleanFilters(currentFilters);
    setLoading(true);

    const queryParams = new URLSearchParams({
      page: p,
      page_size: 6,
    });

    if (cleaned.query) queryParams.append("q", cleaned.query);
    if (cleaned.order) queryParams.append("order", cleaned.order);

    if (cleaned.technique) queryParams.append("technique", cleaned.technique);
    if (cleaned.materials) queryParams.append("materials", cleaned.materials);
    if (cleaned.location) queryParams.append("location", cleaned.location);

    if (cleaned.on_display !== undefined) {
      queryParams.append("on_display", cleaned.on_display);
    }

    try {
      const res = await fetch(`https://mac-digital-catalog.onrender.com/artworks/?${queryParams}`);
      const data = await res.json();

      const items = data.artworks || [];

      setArtworks((prev) => {
        if (p === 1) return items;

        const combined = [...prev, ...items];
        return Array.from(new Map(combined.map((a) => [a.id, a])).values());
      });

      if (items.length < 6) setHasMore(false);

    } catch (err) {
      console.error("Error loading artworks:", err);
    }

    setLoading(false);
  }

  useEffect(() => {
    loadArtworks(page, filters);
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
    setArtworks([]);
    loadArtworks(1, updated);
  }

  function handleFilters(updatedFilters) {
    setFilters(updatedFilters);
    setPage(1);
    setArtworks([]);
    loadArtworks(1, updatedFilters);
  }
  const [filterOptions, setFilterOptions] = useState({
    locations: [],
    materials: [],
    techniques: []
  });

  useEffect(() => {
    async function loadFilterOptions() {
      const res = await fetch("https://mac-digital-catalog.onrender.com/artworks/filters");
      const data = await res.json();
      setFilterOptions(data);
    }
    loadFilterOptions();
  }, []);

  return (
  <div className="page-layout">

    <aside className="filters-column desktop-only">
      <FiltersSideBar
        filters={filters}
        onChange={handleFilters}
        onClear={() => handleFilters({})}
        options={filterOptions}
      />

      <div className="active-filters">
        {Object.keys(filters).map((key) =>
          Array.isArray(filters[key])
            ? filters[key].map((val) => (
                <span className="filter-tag" key={key + val}>
                  {val} <button onClick={() => removeFilter(key, val)}>×</button>
                </span>
              ))
            : filters[key] ? (
                <span className="filter-tag" key={key}>
                  {filters[key]} <button onClick={() => removeFilter(key)}>×</button>
                </span>
              ) : null
        )}
      </div>
    </aside>

    <div className="content-column">
      <h1 className="obras-title">OBRAS</h1>

      <SearchBar value={search} onChange={handleSearch} />

      <div className="filters-mobile-wrapper">
        <FiltersSideBar
          filters={filters}
          onChange={handleFilters}
          onClear={() => handleFilters({})}
          options={filterOptions}
        />

        <div className="active-filters">
          {Object.keys(filters).map((key) =>
            Array.isArray(filters[key])
              ? filters[key].map((val) => (
                  <span className="filter-tag" key={key + val}>
                    {val} <button onClick={() => removeFilter(key, val)}>×</button>
                  </span>
                ))
              : filters[key] ? (
                  <span className="filter-tag" key={key}>
                    {filters[key]} <button onClick={() => removeFilter(key)}>×</button>
                  </span>
                ) : null
          )}
        </div>
      </div>

      <div className="obras-grid">
        {artworks.map((a) => (
          <div className="art-card" key={a.id}>
            <a href={`/obras/${a.id}`} className="art-img-wrapper">
              <img
                src={a.image_url || "/cat.jpg"}
                alt={a.title}
                className="art-img"
              />
            </a>
            <a href={`/obras/${a.id}`} className="art-title hover-text">
              {a.title || "Sin título"}
            </a>
            <p className="art-meta">
              <a href={`/artistas/${a.artist_id}`} className="hover-text">
                {a.artist_name} {a.artist_surname}
              </a>{" "}
              — {a.year || "Año desconocido"}
            </p>
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
