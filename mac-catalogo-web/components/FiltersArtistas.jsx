"use client";

import "./filters.css";

export default function FiltersArtistas({ filters, onChange, onClear, options }) {

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
          <option value="title_asc">Nombre A-Z</option>
          <option value="title_desc">Nombre Z-A</option>
          <option value="year_asc">Año de nacimiento ↑</option>
          <option value="year_desc">Año de nacimiento ↓</option>
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
