import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResults([]);

    try {
      const response = await fetch(
        `https://psychic-space-telegram-v6g5vpjg6g6xhpwv-8000.app.github.dev/search?q=${query}`
      );

      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search error:", error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h2>🔍 Company Search</h2>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter company name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p>Searching...</p>}

      <div className="results">
        {results.length === 0 && !loading ? (
          <p>No results found.</p>
        ) : (
          results.map((item, index) => (
            <div key={index} className="card">
              <h3>{item.name}</h3>
              <p>{item.description}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
