// Main App component for Silver Pancake - AI Meme Generator
// Context: Enterprise-grade AI meme generator with responsible AI features
// Interesting Fact: This app demonstrates how to build user-friendly AI apps with safety guardrails!

import React, { useState } from 'react';
import MemeGenerator from './components/MemeGenerator';
import MemeDisplay from './components/MemeDisplay';
import FeedbackButton from './components/FeedbackButton';
import './App.css';

function App() {
  const [currentMeme, setCurrentMeme] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleMemeGenerated = (meme) => {
    setCurrentMeme(meme);
    setError(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setCurrentMeme(null);
  };

  const handleFeedbackSubmitted = () => {
    // Could add toast notification here
    console.log('Feedback submitted successfully');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🥞 Silver Pancake</h1>
        <p className="subtitle">AI Meme Generator for Team Morale</p>
        <div className="responsible-ai-badge">
          <span>✓ Content Safety Enabled</span>
        </div>
      </header>

      <main className="App-main">
        <MemeGenerator
          onMemeGenerated={handleMemeGenerated}
          onError={handleError}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />

        {error && (
          <div className="error-container">
            <h3>⚠️ Content Safety Notice</h3>
            <p>{error}</p>
            <small>
              Our AI safety systems help ensure appropriate content. 
              Please try a different topic or tone.
            </small>
          </div>
        )}

        {currentMeme && (
          <div className="meme-container">
            <MemeDisplay meme={currentMeme} />
            <FeedbackButton
              meme={currentMeme}
              onFeedbackSubmitted={handleFeedbackSubmitted}
            />
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>
          <strong>Responsible AI:</strong> All content is analyzed for safety and appropriateness.
        </p>
        <p>
          <small>
            Powered by Azure OpenAI • Content Safety by Azure AI • 
            Built with ❤️ for team morale
          </small>
        </p>
      </footer>
    </div>
  );
}

export default App;
