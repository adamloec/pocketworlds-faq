import React, { useState, useEffect } from "react";

const TypewriterText = ({ text, onTextUpdate }) => {
  const [displayedText, setDisplayedText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(prev => prev + text[currentIndex]);
        setCurrentIndex(c => c + 1);
        onTextUpdate();
      }, 5);
      return () => clearTimeout(timeout);
    }
  }, [currentIndex, text, onTextUpdate]);

  return displayedText;
};

export default TypewriterText;
