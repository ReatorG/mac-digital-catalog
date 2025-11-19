// app/components/CommentsSection.jsx
'use client';

import { useState, useEffect } from 'react';
import { fetchCommentsByArtwork, createComment } from '../lib/api';

export default function CommentsSection({ artworkId }) {
  const [comments, setComments] = useState([]);
  const [text, setText] = useState('');

  const load = async () => {
    try {
      const data = await fetchCommentsByArtwork(artworkId);
      setComments(data);
    } catch (e) {
      console.error('Error cargando comentarios');
    }
  };

  useEffect(() => {
    load();
  }, [artworkId]);

  const handleAdd = async () => {
    if (!text.trim()) return;

    await createComment({
      artwork_id: artworkId,
      text: text.trim(),
    });

    setText('');
    await load();
  };

  return (
    <section className="mt-10 border-t border-neutral-200 pt-8">
      <h2 className="text-xl font-serif mb-6">Comentarios</h2>

      <div className="mb-6">
        <p className="text-center text-lg font-serif mb-3">
          ¿Algún comentario?
        </p>
        <div className="max-w-xl mx-auto flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            placeholder="Comparte tu opinión..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="flex-1 border border-neutral-300 rounded-md py-2 px-3 shadow-sm"
          />
          <button
            onClick={handleAdd}
            className="px-4 py-2 rounded-md bg-neutral-900 text-white text-sm uppercase tracking-[0.15em]"
          >
            Enviar
          </button>
        </div>
      </div>

      <div className="space-y-4 text-sm">
        {comments.map((c) => (
          <div key={c.id} className="flex gap-3 items-start">
            <div className="mt-1">
              <div className="w-7 h-7 border border-neutral-400 rounded-full flex items-center justify-center">
                💬
              </div>
            </div>
            <p className="border-b border-neutral-200 pb-2 flex-1">{c.text}</p>
          </div>
        ))}
        {comments.length === 0 && (
          <p className="text-neutral-500 text-sm">Aún no hay comentarios.</p>
        )}
      </div>
    </section>
  );
}
