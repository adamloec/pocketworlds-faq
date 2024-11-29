import React, { useState, useEffect } from "react";

const TypewriterList = ({ processedText, onTextUpdate }) => {
  const [displayState, setDisplayState] = useState({
    intro: "",
    items: [],
    outro: "",
    completed: false
  });
  const [stage, setStage] = useState("intro");
  const [currentChar, setCurrentChar] = useState(0);
  const [currentItem, setCurrentItem] = useState(0);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (stage === "intro" && processedText.intro) {
        if (currentChar < processedText.intro.length) {
          setDisplayState(prev => ({
            ...prev,
            intro: processedText.intro.slice(0, currentChar + 1)
          }));
          setCurrentChar(prev => prev + 1);
        } else {
          setStage("items");
          setCurrentChar(0);
        }
      } else if (stage === "items") {
        if (currentItem < processedText.items.length) {
          const currentItemText = processedText.items[currentItem];
          if (currentChar < currentItemText.length) {
            setDisplayState(prev => ({
              ...prev,
              items: [
                ...prev.items.slice(0, currentItem),
                currentItemText.slice(0, currentChar + 1)
              ]
            }));
            setCurrentChar(prev => prev + 1);
          } else {
            setCurrentItem(prev => prev + 1);
            setCurrentChar(0);
          }
        } else {
          setStage("outro");
          setCurrentChar(0);
        }
      } else if (stage === "outro" && processedText.outro) {
        if (currentChar < processedText.outro.length) {
          setDisplayState(prev => ({
            ...prev,
            outro: processedText.outro.slice(0, currentChar + 1)
          }));
          setCurrentChar(prev => prev + 1);
        } else {
          setDisplayState(prev => ({ ...prev, completed: true }));
        }
      } else {
        setDisplayState(prev => ({ ...prev, completed: true }));
      }
      onTextUpdate();
    }, 5);

    return () => clearTimeout(timeout);
  }, [stage, currentChar, currentItem, processedText, onTextUpdate]);

  return (
    <div className="space-y-4">
      {displayState.intro && <p>{displayState.intro}</p>}
      {displayState.items.length > 0 && (
        <ul className={`${processedText.isNumberedList ? 'list-decimal' : 'list-disc'} space-y-2 pl-6`}>
          {displayState.items.map((item, idx) => (
            <li key={idx} className="ml-2">{item}</li>
          ))}
        </ul>
      )}
      {displayState.outro && <p className="mt-4">{displayState.outro}</p>}
    </div>
  );
};

export default TypewriterList;