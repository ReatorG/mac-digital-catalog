// app/components/ArtworkCard.jsx
import Link from 'next/link';

export default function ArtworkCard({ artwork }) {
  const artistName = artwork.artist_name && artwork.artist_surname
    ? `${artwork.artist_name} ${artwork.artist_surname}`
    : '';

  return (
    <Link
      href={`/obras/${artwork.id}`}
      className="group flex flex-col items-center text-center cursor-pointer"
    >
      <div className="w-full max-w-xs aspect-[4/3] overflow-hidden bg-neutral-100 shadow-sm">
        {artwork.image_url ? (
          <img
            src={artwork.image_url}
            alt={artwork.title}
            className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-xs text-neutral-400">
            Sin imagen
          </div>
        )}
      </div>

      <h3 className="mt-4 text-lg font-serif">{artwork.title}</h3>
      <p className="mt-1 text-xs text-neutral-600">
        {artistName}
        {artwork.year && `  -  ${artwork.year}`}
      </p>
    </Link>
  );
}
