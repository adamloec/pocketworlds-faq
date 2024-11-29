import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FeedbackButtons = ({ messageCount }) => {
  const [showFeedback, setShowFeedback] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [lastFeedbackCount, setLastFeedbackCount] = useState(1);

  useEffect(() => {
    let timeout;
    if (showFeedback) {
      timeout = setTimeout(() => {
        setShowFeedback(false);
        setLastFeedbackCount(messageCount);
      }, 2000);
    }
    return () => clearTimeout(timeout);
  }, [showFeedback, messageCount]);

  const shouldShowButtons = messageCount > 1 && 
                          messageCount > lastFeedbackCount && 
                          messageCount % 2 !== 0;

  if (!shouldShowButtons) return null;

  const handleFeedback = async (type) => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      await axios.post(`http://127.0.0.1:8000/feedback/${type}`);
      setShowFeedback(true);
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
    setIsLoading(false);
  };

  return (
    <div className="flex items-center justify-center space-x-4 p-4 border-t border-gray-700">
      {!showFeedback ? (
        <>
          <button
            onClick={() => handleFeedback('liked')}
            disabled={isLoading}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors hover:bg-gray-700"
          >
            <span>👍</span>
            <span>Helpful</span>
          </button>

          <button
            onClick={() => handleFeedback('disliked')}
            disabled={isLoading}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors hover:bg-gray-700"
          >
            <span>👎</span>
            <span>Not Helpful</span>
          </button>
        </>
      ) : (
        <span className="text-sm text-gray-400">
          Thank you for your feedback!
        </span>
      )}
    </div>
  );
};

export default FeedbackButtons;