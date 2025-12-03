"use client";

import { useState, useRef, useEffect } from "react";
import "./searchbar.css";

export default function SearchBar({ value, onChange, filters, onFiltersChange }) {
  const panelRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="searchbar-wrapper">

      {/* Input */}
      <div className="searchbar-input-wrapper">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Buscar..."
          className="searchbar-input"
        />
        <div className="searchbar-icon" />
      </div>

    </div>
  );
}
