const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    cache: "no-store",
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    console.error("API error:", res.status, path);
    throw new Error(`Error al llamar a ${path}: ${res.status}`);
  }

  return res.json();
}

export async function fetchArtworks({ page = 1, page_size = 200 } = {}) {
  return apiFetch(`/artworks/?page=${page}&page_size=${page_size}`);
}

export async function fetchArtworkById(id) {
  return apiFetch(`/artworks/${id}`);
}

export async function fetchArtworksByArtist(artistId) {
  return apiFetch(`/artworks/artist/${artistId}`);
}

export async function fetchArtists({ page = 1, page_size = 200 } = {}) {
  return apiFetch(`/artists/?page=${page}&page_size=${page_size}`);
}

export async function fetchArtistById(id) {
  return apiFetch(`/artists/${id}`);
}

export async function fetchCommentsByArtwork(id) {
  return apiFetch(`/comments/artwork/${id}`);
}

export async function createComment({ artwork_id, text }) {
  return apiFetch(`/comments/`, {
    method: "POST",
    body: JSON.stringify({ artwork_id, text }),
  });
}

export async function searchArtworks(query, page = 1, page_size = 200) {
  return apiFetch(
    `/search/artworks?query=${encodeURIComponent(query)}&page=${page}&page_size=${page_size}`
  );
}

export async function searchArtists(query, page = 1, page_size = 200) {
  return apiFetch(
    `/search/artists?query=${encodeURIComponent(query)}&page=${page}&page_size=${page_size}`
  );
}

