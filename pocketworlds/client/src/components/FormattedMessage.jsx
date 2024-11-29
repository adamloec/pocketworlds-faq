import React from "react";
import TypewriterText from "./TypewriterText.jsx";
import TypewriterList from "./TypewriterList.jsx";
import { formatListItems } from "../utils/formatListItems.js";

const FormattedMessage = ({ text, isNew, onTextUpdate }) => {
  const processedText = formatListItems(text);
  
  if (typeof processedText === 'object') {
    return isNew ? (
      <TypewriterList processedText={processedText} onTextUpdate={onTextUpdate} />
    ) : (
      <div className="space-y-4">
        {processedText.intro && <p>{processedText.intro}</p>}
        <ul className={`${processedText.isNumberedList ? 'list-decimal' : 'list-disc'} space-y-2 pl-6`}>
          {processedText.items.map((item, idx) => (
            <li key={idx} className="ml-2">{item}</li>
          ))}
        </ul>
        {processedText.outro && <p className="mt-4">{processedText.outro}</p>}
      </div>
    );
  }

  return isNew ? (
    <TypewriterText text={text} onTextUpdate={onTextUpdate} />
  ) : (
    <span>{text}</span>
  );
};

export default FormattedMessage;