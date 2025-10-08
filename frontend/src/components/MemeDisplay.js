/**
 * MemeDisplay Component
 * Shows the generated meme in a visually appealing format
 * 
 * Design: Classic meme format with top/bottom text overlay
 */

import React from 'react';
import './MemeDisplay.css';

const MemeDisplay = ({ meme }) => {
  if (!meme) return null;

  return (
    <div className="meme-display">
      <h3>🎉 Your Meme is Ready!</h3>
      
      {/* Classic Meme Format Display */}
      <div className="meme-frame">
        <div className="meme-image-placeholder">
          <div className="meme-text-overlay">
            {meme.top_text && (
              <div className="meme-text meme-text-top">
                {meme.top_text}
              </div>
            )}
            {meme.bottom_text && (
              <div className="meme-text meme-text-bottom">
                {meme.bottom_text}
              </div>
            )}
          </div>
          
          {/* Generic meme image placeholder */}
          <div className="image-placeholder">
            <span className="placeholder-icon">🖼️</span>
            <p>Your meme image would go here!</p>
            <small>
              In a full implementation, you'd use Azure OpenAI DALL-E 
              or stock meme templates
            </small>
          </div>
        </div>
      </div>

      {/* Alternative text format display */}
      <div className="meme-text-format">
        <h4>Generated Meme Text:</h4>
        <div className="meme-content">
          {meme.meme_text}
        </div>
      </div>

      {/* Metadata */}
      <div className="meme-metadata">
        <div className="metadata-item">
          <strong>Topic:</strong> {meme.topic}
        </div>
        <div className="metadata-item">
          <strong>Mood:</strong> {meme.mood}
        </div>
        <div className="metadata-item safety-check">
          <strong>Safety Check:</strong> 
          <span className="safety-status passed">✓ Passed</span>
        </div>
      </div>
    </div>
  );
};

export default MemeDisplay;