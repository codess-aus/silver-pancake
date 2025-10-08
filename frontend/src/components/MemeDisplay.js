/**
 * MemeDisplay Component
 * Shows the generated meme in a visually appealing format
 * 
 * Design: Modern visual meme display with Azure OpenAI image generation
 */

import React from 'react';
import './MemeDisplay.css';

const MemeDisplay = ({ meme }) => {
  if (!meme || !meme.meme_components) return null;
  const { visual, text } = meme.meme_components;

  return (
    <div className="meme-display">
      <h3>🎉 Your Meme is Ready!</h3>
      
      {/* Visual Meme Display */}
      <div className="meme-frame">
        <div className="meme-image-container">
          {visual?.image_url ? (
            <img 
              src={visual.image_url} 
              alt={`Meme about ${meme.topic}`}
              className="meme-image"
            />
          ) : (
            <div className="image-placeholder">
              <span className="placeholder-icon">🎨</span>
              <p>Generating your meme image...</p>
              <small>Using Azure OpenAI image generation</small>
            </div>
          )}
          
          {text && (
            <div className="meme-text-overlay">
              <div className="meme-text meme-text-top">
                {text.top_text}
              </div>
              <div className="meme-text meme-text-bottom">
                {text.bottom_text}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Text Component Display */}
      {text && (
        <div className="meme-text-format">
          <h4>Generated Meme Text:</h4>
          <div className="meme-content">
            {text.text}
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="meme-metadata">
        <div className="metadata-item">
          <strong>Topic:</strong> {meme.topic}
        </div>
        <div className="metadata-item">
          <strong>Mood:</strong> {meme.mood}
        </div>
        {visual && (
          <div className="metadata-item image-info">
            <strong>Image Status:</strong>
            {visual.image_url ? (
              <span className="status success">✓ Generated</span>
            ) : (
              <span className="status pending">⏳ Processing</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
export default MemeDisplay;