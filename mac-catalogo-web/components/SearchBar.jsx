'use client';

export default function SearchBar({ value, onChange, placeholder }) {
  return (
    <div className="flex items-center gap-3 w-full max-w-3xl">
      <button
        type="button"
        className="flex items-center justify-center w-10 h-10 rounded-md border border-neutral-300 bg-white shadow-sm"
      >
        <div className="w-4 h-4 flex flex-col justify-between">
          <span className="block h-[2px] bg-neutral-700 w-full" />
          <span className="block h-[2px] bg-neutral-700 w-3/4 self-end" />
          <span className="block h-[2px] bg-neutral-700 w-1/2" />
        </div>
      </button>

      <div className="flex-1 relative">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full rounded-md border border-neutral-300 bg-white py-2.5 pl-4 pr-10 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-neutral-500"
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2">
          <span className="inline-block w-4 h-4 border border-neutral-500 rounded-full relative">
            <span className="block w-2 h-[2px] bg-neutral-500 rotate-45 origin-left absolute right-[-4px] bottom-[-1px]" />
          </span>
        </div>
      </div>
    </div>
  );
}
