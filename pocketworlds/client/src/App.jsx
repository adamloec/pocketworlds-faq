import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { API_BASE_URL } from './config.js';
import Header from "./components/Header.jsx";
import ChatMessage from "./components/ChatMessage.jsx";
import ChatInput from "./components/ChatInput.jsx";
import FeedbackButtons from "./components/FeedbackButtons.jsx";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    let mounted = true;
    
    const initializeChatbot = async () => {
      if (mounted) {
        try {
          await axios.post(`${API_BASE_URL}/initialize`);
          setMessages([
            {
              sender: "bot",
              text: "Hi! I'm your Highrise support assistant. How can I help you today?",
            },
          ]);
        } catch (error) {
          console.error("Error initializing chatbot:", error);
          setMessages([
            { sender: "bot", text: "Sorry, this service is unavailable right now! Please try refereshing the page or try again later." },
          ]);
        }
      }
    };

    initializeChatbot();
    
    return () => {
      mounted = false;
    };
  }, []);

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        user_message: input,
      });

      setMessages([
        ...newMessages,
        {
          sender: "bot",
          text: response.data.system_response,
          supportingUrls: response.data.supporting_urls || [],
          isNew: true,
        },
      ]);
    } catch (error) {
      console.error("Error details:", error.response || error);
      setMessages([
        ...newMessages,
        { sender: "bot", text: "Sorry, this service is unavailable right now! Please try refereshing the page or try again later." },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  return (
    <div className="min-h-screen h-screen bg-[#111827] text-gray-100 flex flex-col overflow-hidden">
      <div className="flex-1 max-w-5xl w-full mx-auto p-6 flex flex-col h-full">
        <Header />

        <div className="flex-1 bg-[#1F2937] rounded-2xl shadow-2xl border border-gray-700 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg, index) => (
              <ChatMessage 
                key={index} 
                message={msg} 
                onTextUpdate={scrollToBottom}
              />
            ))}
            {loading && (
              <div className="flex justify-start items-end space-x-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white text-sm font-bold">
                  H
                </div>
                <div className="bg-[#374151] rounded-2xl px-6 py-4 shadow-lg">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <FeedbackButtons messageCount={messages.length} />
          <ChatInput 
            input={input}
            setInput={setInput}
            handleSendMessage={handleSendMessage}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
}

export default App;