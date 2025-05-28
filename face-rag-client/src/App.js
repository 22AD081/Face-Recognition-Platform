import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [image, setImage] = useState(null);
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [responseMsg, setResponseMsg] = useState('');

  const handleImageUpload = async () => {
    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('http://localhost:5001/register', formData);
      setResponseMsg(response.data.message);
    } catch (error) {
      setResponseMsg('Face registration failed.');
    }
  };

  const handleQuerySubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5002/ask', { query });
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer('Failed to get answer from RAG engine.');
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>📷 Face Registration</h2>
      <input type="file" accept="image/*" onChange={e => setImage(e.target.files[0])} />
      <button onClick={handleImageUpload}>Register Face</button>
      <p>{responseMsg}</p>

      <h2>🤖 Ask AI About Registered Faces</h2>
      <input
        type="text"
        placeholder="Ask a question"
        value={query}
        onChange={e => setQuery(e.target.value)}
        style={{ width: 300, marginRight: 10 }}
      />
      <button onClick={handleQuerySubmit}>Ask</button>
      <p><strong>Answer:</strong> {answer}</p>
    </div>
  );
}

export default App;
