/**
 * FeedbackButton Component
 * Allows users to report inappropriate content for continuous improvement
 * 
 * Responsible AI: Essential for collecting feedback and improving safety systems
 */

import React, { useState } from 'react';
import axios from 'axios';
import './FeedbackButton.css';

const FeedbackButton = ({ meme, onFeedbackSubmitted }) => {
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [selectedReason, setSelectedReason] = useState('');
  const [userComment, setUserComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const feedbackReasons = [
    { value: 'inappropriate', label: '❌ Inappropriate content' },
    { value: 'offensive', label: '⚠️ Offensive or harmful' },
    { value: 'inaccurate', label: '📝 Inaccurate or misleading' },
    { value: 'low_quality', label: '📉 Low quality output' },
    { value: 'other', label: '🔧 Other issue' }
  ];

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedReason) {
      alert('Please select a reason for your feedback');
      return;
    }

    setIsSubmitting(true);

    try {
      await axios.post('/api/feedback', {
        meme_text: meme.meme_text,
        reason: selectedReason,
        user_comment: userComment.trim() || undefined
      });

      setHasSubmitted(true);
      onFeedbackSubmitted();
      
      // Reset form after a delay
      setTimeout(() => {
        setShowFeedbackForm(false);
        setSelectedReason('');
        setUserComment('');
        setHasSubmitted(false);
      }, 2000);

    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (hasSubmitted) {
    return (
      <div className="feedback-container submitted">
        <div className="feedback-success">
          <span className="success-icon">✓</span>
          <p>Thank you for your feedback!</p>
          <small>Your report helps improve our AI safety systems.</small>
        </div>
      </div>
    );
  }

  return (
    <div className="feedback-container">
      {!showFeedbackForm ? (
        <button
          onClick={() => setShowFeedbackForm(true)}
          className="btn btn-secondary feedback-trigger"
        >
          🚩 Flag this meme
        </button>
      ) : (
        <div className="feedback-form-container">
          <h4>Report this content</h4>
          <p className="feedback-explanation">
            Help us improve by reporting content that shouldn't have passed our safety checks.
            Your feedback is valuable for training better AI safety systems.
          </p>
          
          <form onSubmit={handleFeedbackSubmit} className="feedback-form">
            <div className="form-group">
              <label>What's wrong with this meme?</label>
              <div className="reason-options">
                {feedbackReasons.map((reason) => (
                  <label key={reason.value} className="reason-option">
                    <input
                      type="radio"
                      name="reason"
                      value={reason.value}
                      checked={selectedReason === reason.value}
                      onChange={(e) => setSelectedReason(e.target.value)}
                      disabled={isSubmitting}
                    />
                    <span className="reason-label">{reason.label}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="comment">
                Additional comments (optional):
              </label>
              <textarea
                id="comment"
                value={userComment}
                onChange={(e) => setUserComment(e.target.value)}
                placeholder="Describe the issue in more detail..."
                rows="3"
                maxLength="500"
                disabled={isSubmitting}
                className="comment-textarea"
              />
              <small className="char-count">
                {userComment.length}/500 characters
              </small>
            </div>

            <div className="feedback-actions">
              <button
                type="button"
                onClick={() => setShowFeedbackForm(false)}
                disabled={isSubmitting}
                className="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!selectedReason || isSubmitting}
                className="btn btn-primary"
              >
                {isSubmitting ? (
                  <>
                    <span className="loading"></span>
                    Submitting...
                  </>
                ) : (
                  'Submit Report'
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default FeedbackButton;