/**
 * MemeGenerator Component
 * Handles user input and API calls for meme generation
 * 
 * Enterprise Feature: Input validation and user-friendly error handling
 */

import React, { useState } from 'react';
import axios from 'axios';
import './MemeGenerator.css';

const MemeGenerator = ({ onMemeGenerated, onError, isLoading, setIsLoading }) => {
  const [topic, setTopic] = useState('');
  const [mood, setMood] = useState('funny');

  const moodOptions = [
    { value: 'funny', label: '😄 Funny' },
    { value: 'sarcastic', label: '😏 Sarcastic' },
    { value: 'wholesome', label: '🥰 Wholesome' },
    { value: 'motivational', label: '💪 Motivational' },
    { value: 'relatable', label: '😅 Relatable' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      onError('Please enter a topic for your meme');
      return;
    }

    setIsLoading(true);
    
    try {
      const apiUrl = process.env.REACT_APP_API_URL || '/api';
      const response = await axios.post(`${apiUrl}/generate-visual-meme`, {
        topic: topic.trim(),
        mood: mood,
        include_image: true,
        include_text: true
      });

      if (response.data.success) {
        onMemeGenerated(response.data);
      } else {
        onError(response.data.message || 'Failed to generate meme');
      }
    } catch (error) {
      console.error('Error generating meme:', error);
      if (error.response?.data?.detail) {
        onError(error.response.data.detail);
      } else {
        onError('Failed to generate meme. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="meme-generator">
      <h2>Generate Your Meme</h2>
      <form onSubmit={handleSubmit} className="generator-form">
        <div className="form-group">
          <label htmlFor="topic">
            Topic or Subject:
          </label>
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., coding, meetings, coffee, deadlines..."
            maxLength={200}
            disabled={isLoading}
            className="topic-input"
          />
          <small className="help-text">
            Enter any workplace or general topic (max 200 characters)
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="mood">
            Mood/Tone:
          </label>
          <select
            id="mood"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            disabled={isLoading}
            className="mood-select"
          >
            {moodOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          disabled={isLoading || !topic.trim()}
          className="btn btn-primary generate-btn"
        >
          {isLoading ? (
            <>
              <span className="loading"></span>
              Generating...
            </>
          ) : (
            '🎭 Generate Meme'
          )}
        </button>
      </form>

      <div className="safety-notice">
        <h4>🛡️ Safety First</h4>
        <p>
          All generated content goes through Azure Content Safety checks 
          to ensure appropriate and professional memes for your team.
        </p>
      </div>
    </div>
  );
};

export default MemeGenerator;