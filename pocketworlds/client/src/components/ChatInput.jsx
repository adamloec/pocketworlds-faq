import React from "react";

const ChatInput = ({ input, setInput, handleSendMessage, loading }) => {
  return (
    <div className="p-6 border-t border-gray-700 bg-[#1F2937] rounded-b-2xl">
      <div className="flex space-x-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter") handleSendMessage();
          }}
          placeholder="Type your message..."
          className="flex-1 bg-[#374151] text-gray-100 rounded-xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-purple-500 border border-gray-600 placeholder-gray-400"
        />
        <button
          onClick={handleSendMessage}
          disabled={loading}
          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-xl font-medium transition-all hover:opacity-90 disabled:opacity-50 shadow-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInput;