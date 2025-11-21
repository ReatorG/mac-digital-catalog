'use client';

import { useState } from 'react';

export default function ArtworkFilterPanel({
  artworks,
  filters,
  onChangeFilters,
}) {
  const [open, setOpen] = useState(false);

  const techniques = Array.from(
    new Set(artworks.map((a) => a.technique).filter(Boolean)),
  );
  const materials = Array.from(
    new Set(artworks.map((a) => a.materials).filter(Boolean)),
  );
  const locations = Array.from(
    new Set(artworks.map((a) => a.location).filter(Boolean)),
  );

  const update = (partial) => onChangeFilters({ ...filters, ...partial });

  return (
    <div className="w-full max-w-3xl mb-4">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="text-xs uppercase tracking-[0.25em] text-neutral-700 mb-2"
      >
        {open ? 'OCULTAR FILTROS' : 'MOSTRAR FILTROS'}
      </button>

      {open && (
        <div className="border border-neutral-200 rounded-md p-4 bg-white shadow-sm text-sm space-y-4">
          <div className="flex flex-wrap gap-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={filters.onDisplayOnly}
                onChange={(e) => update({ onDisplayOnly: e.target.checked })}
              />
              <span>Solo obras en exposición</span>
            </label>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <label className="block text-xs uppercase tracking-[0.2em] mb-1">
                Técnica
              </label>
              <select
                className="w-full border border-neutral-300 rounded-md py-1.5 px-2 text-sm"
                value={filters.technique || ''}
                onChange={(e) =>
                  update({ technique: e.target.value || null })
                }
              >
                <option value="">Todas</option>
                {techniques.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-[0.2em] mb-1">
                Material
              </label>
              <select
                className="w-full border border-neutral-300 rounded-md py-1.5 px-2 text-sm"
                value={filters.materials || ''}
                onChange={(e) =>
                  update({ materials: e.target.value || null })
                }
              >
                <option value="">Todos</option>
                {materials.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs uppercase tracking-[0.2em] mb-1">
                Ubicación
              </label>
              <select
                className="w-full border border-neutral-300 rounded-md py-1.5 px-2 text-sm"
                value={filters.location || ''}
                onChange={(e) =>
                  update({ location: e.target.value || null })
                }
              >
                <option value="">Todas</option>
                {locations.map((loc) => (
                  <option key={loc} value={loc}>
                    {loc}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
