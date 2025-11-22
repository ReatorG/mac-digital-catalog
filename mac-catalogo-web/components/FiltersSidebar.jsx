"use client";

import "./filters.css";

export default function FiltersSidebar({ filters, onChange, onClear, options }) {

  function update(key, value) {
    if (value === "Todos" || value === "Todas" || value === "") {
      value = "";
    }

    const updated = { ...filters, [key]: value };
    onChange(updated);
  }

  return (
    <div className="filter-box">
      <h2 className="filter-title">FILTROS</h2>

      {/* ORDEN */}
      <div className="filter-group">
        <label className="filter-label">Ordenar por</label>
        <select
          value={filters.order || ""}
          onChange={(e) => update("order", e.target.value)}
        >
          <option value="">Seleccionar</option>
          <option value="title_asc">Título A-Z</option>
          <option value="title_desc">Título Z-A</option>
          <option value="year_asc">Año ↑</option>
          <option value="year_desc">Año ↓</option>
        </select>
      </div>

      {/* UBICACIÓN */}
      <div className="filter-group">
        <label className="filter-label">Ubicación</label>
        <select
          value={filters.location || ""}
          onChange={(e) => update("location", e.target.value)}
        >
          <option value="">Todas</option>
          {(options.locations || []).map((loc) => (
            <option key={loc} value={loc}>{loc}</option>
          ))}
        </select>
      </div>

      {/* MATERIAL */}
      <div className="filter-group">
        <label className="filter-label">Material</label>
        <select
          value={filters.materials || ""}
          onChange={(e) => update("materials", e.target.value)}
        >
          <option value="">Todos</option>
          {(options.materials || []).map((mat) => (
            <option key={mat} value={mat}>{mat}</option>
          ))}
        </select>
      </div>

      {/* TECNICA */}
      <div className="filter-group">
        <label className="filter-label">Técnica</label>
        <select
          value={filters.technique || ""}
          onChange={(e) => update("technique", e.target.value)}
        >
          <option value="">Todas</option>
          {(options.techniques || []).map((tec) => (
            <option key={tec} value={tec}>{tec}</option>
          ))}
        </select>
      </div>

      {/* CHECKBOX DE EXHIBICIÓN */}
      <div className="filter-group">
        <label className="filter-label">En exhibición</label>
        <label className="checkbox-line">
          <input
            type="checkbox"
            checked={filters.on_display === true}
            onChange={(e) => update("on_display", e.target.checked ? true : undefined)}
          />
          <span>Mostrar solo obras activas</span>
        </label>
      </div>

      <button className="clear-button" onClick={onClear}>
        Limpiar filtros
      </button>
    </div>
  );
}
