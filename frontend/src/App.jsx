import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null); // Reset error state
    const userMessage = { role: 'user', content: input };
    
    setChatLog((prevLog) => [...prevLog, userMessage]);
    setInput('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', {
        message: input,
      });

      // Create the bot message
      const botMessage = { role: 'bot', content: response.data.response };
      
      // Add bot message to the chat log
      setChatLog((prevLog) => [...prevLog, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while fetching the response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className='flex items-center justify-center h-screen'>
    <div className="w-3/5 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold mb-4 text-center text-black">Chat with University AI</h1>
      <div className="chat-log border border-gray-300 p-4 rounded-lg h-80 overflow-y-auto mb-4 bg-gray-50 flex flex-col">
        {chatLog.map((message, index) => (
          <div key={index} className={`message ${message.role} mb-2 flex ${message.role}`}>
            <strong className={message.role === 'user' ? 'text-blue-600' : 'text-green-600'}>
              {message.role === 'user' ? 'You' : 'AI'}:
            </strong>
            <span className="ml-2 text-black">{message.content}</span>
          </div>
        ))}
        {isLoading && <div className="message mb-2 text-green-600"><strong>AI:</strong> ...</div>}
        {error && <div className="text-red-600 mt-2">{error}</div>} {/* Display error message */}
      </div>
      <div className="chat-input flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown} // Add key down listener
          placeholder="Type your message..."
          className="flex-grow border border-gray-300 rounded-lg p-2 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button onClick={handleSend} disabled={isLoading} className="bg-blue-600 text-white rounded-lg p-2">
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
    </div>
  );
};

export default App;