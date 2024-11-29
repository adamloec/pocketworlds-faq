import FormattedMessage from "./FormattedMessage.jsx";

const ChatMessage = ({ message, onTextUpdate }) => {
    const { sender, text, isNew, supportingUrls } = message;
  
    return (
      <div
        className={`flex ${
          sender === "user" ? "justify-end" : "justify-start"
        } items-end space-x-2`}
      >
        {sender === "bot" && (
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white text-sm font-bold">
            H
          </div>
        )}
        <div
          className={`max-w-[70%] px-6 py-4 rounded-2xl ${
            sender === "user"
              ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white"
              : "bg-[#374151] text-gray-100"
          } shadow-lg`}
        >
          <FormattedMessage 
            text={text}
            isNew={isNew}
            onTextUpdate={onTextUpdate}
          />
          {supportingUrls && supportingUrls.length > 0 && (
            <div className="mt-3 space-y-1 text-sm">
              <p className="text-gray-400">For more information visit:</p>
              {supportingUrls.map((url, index) => (
                <a
                  key={index}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-purple-400 hover:text-purple-300 transition-colors"
                >
                  {url}
                </a>
              ))}
            </div>
          )}
        </div>
        {sender === "user" && (
          <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-white text-sm">
            U
          </div>
        )}
      </div>
    );
  };
  
  export default ChatMessage;