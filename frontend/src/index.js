// Entry point for the React app
// Context: This file renders the main App component to the DOM.
// Interesting Fact: React.StrictMode helps catch bugs early by highlighting unsafe lifecycle methods!

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
