//frontend/src/App.js (React with functional components)
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async () => {
    setError(null);
    try {
      const jsonData = JSON.parse(inputText);
      const res = await axios.post('/api/process', jsonData);
      setResponse(res.data);
      setShowDropdown(true);
    } catch (err) {
      setError('Invalid JSON or API error: ' + err.message);
      setResponse(null);
      setShowDropdown(false);
    }
  };

  const handleDropdownChange = (e) => {
    const selected = Array.from(e.target.selectedOptions, option => option.value);
    setSelectedOptions(selected);
  };

  const renderFilteredResponse = () => {
    if (!response || selectedOptions.length === 0) return null;

    let filteredData = response.data;

    if (selectedOptions.includes('Alphabets') && !selectedOptions.includes('Highest alphabet')) {
      filteredData = filteredData.filter(item => typeof item === 'string' && item.match(/[a-zA-Z]/));
    }
    if (selectedOptions.includes('Numbers')) {
      filteredData = filteredData.filter(item => typeof item === 'number');
    }
    if (selectedOptions.includes('Highest alphabet')) {
      const alphabets = response.data.filter(item => typeof item === 'string' && item.match(/[a-zA-Z]/));
      if (alphabets.length > 0) {
        const highest = alphabets.reduce((max, current) => (current > max ? current : max), alphabets[0]);
        if(selectedOptions.includes('Numbers')){
            filteredData = response.data.filter(item => typeof item === 'number');
            filteredData.push(highest);
        } else {
          filteredData = [highest];
        }

      } else {
        filteredData = [];
      }
    } else if(selectedOptions.includes('Alphabets') && selectedOptions.includes('Numbers')){
        filteredData = response.data.filter(item => typeof item === 'string' && item.match(/[a-zA-Z]/) || typeof item === 'number');
    } else if (selectedOptions.length === 0){
        filteredData = response.data;
    }

    return (
      <div>
        <h3>Filtered Response:</h3>
        <pre>{JSON.stringify(filteredData, null, 2)}</pre>
      </div>
    );
  };

  return (
    <div>
      <h1>Roll Number Website</h1>
      <textarea
        value={inputText}
        onChange={handleInputChange}
        placeholder="Enter JSON data (e.g., {&quot;data&quot;: [&quot;A&quot;,&quot;C&quot;,&quot;z&quot;, 1, 2]})"
      />
      <button onClick={handleSubmit}>Submit</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {showDropdown && (
        <div>
          <select multiple onChange={handleDropdownChange}>
            <option value="Alphabets">Alphabets</option>
            <option value="Numbers">Numbers</option>
            <option value="Highest alphabet">Highest alphabet</option>
          </select>
          {renderFilteredResponse()}
        </div>
      )}

      {response && !showDropdown && (
        <div>
          <h3>Raw Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
