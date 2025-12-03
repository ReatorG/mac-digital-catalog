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
    <section className="obra-comments-section">

      <h3 className="obra-comments-title">¿Algún comentario?</h3>

      <div className="obra-comments-input-wrapper">
        <input
          type="text"
          placeholder="Comparte tu opinión..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="obra-comment-input"
        />
        <button onClick={handleAdd} className="obra-comment-button">
          Enviar
        </button>
      </div>

      <div className="obra-comments-list">
        {comments.map((c) => (
          <div key={c.id} className="obra-comment-item">
            <span className="obra-comment-icon">💬</span>
            <p>{c.text}</p>
          </div>
        ))}

        {comments.length === 0 && (
          <p className="obra-no-comments">¡Sé el primero en comentar!</p>
        )}
      </div>

    </section>
  );
}