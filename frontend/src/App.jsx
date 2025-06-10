import { useState } from "react";
import { searchQuery } from "./api";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({});

  const handleSearch = async () => {
    const res = await searchQuery(query);
    setResults(res);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>AI Reimbursement Agent</h1>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
        style={{ width: "300px", padding: "8px" }}
      />
      <button onClick={handleSearch} style={{ marginLeft: "1rem" }}>Search</button>

      {Object.entries(results).map(([name, items]) => (
        <div key={name} style={{ marginTop: "2rem" }}>
          <h2>{name}</h2>
          {items.length === 0 && <p>No matches found.</p>}
          {items.map((item, i) => (
            <div key={i}>
              <strong>Score:</strong> {item.score}
              <pre>{item.text}</pre>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default App;
