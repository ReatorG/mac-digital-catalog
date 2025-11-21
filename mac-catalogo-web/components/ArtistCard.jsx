import Link from 'next/link';

export default function ArtistCard({ artist }) {
  const fullName = `${artist.name} ${artist.surname}`;

  return (
    <Link
      href={`/artistas/${artist.id}`}
      className="group flex flex-col items-center text-center cursor-pointer"
    >
      <div className="w-32 h-32 sm:w-40 sm:h-40 rounded-full overflow-hidden bg-neutral-200 shadow-sm">
        {artist.image_url ? (
          <img
            src={artist.image_url}
            alt={fullName}
            className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-xs text-neutral-400">
            Sin foto
          </div>
        )}
      </div>
      <h3 className="mt-3 text-sm sm:text-base font-serif">{fullName}</h3>
    </Link>
  );
}
