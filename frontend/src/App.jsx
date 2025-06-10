import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data);
    } catch (err) {
      alert("Error searching. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>AI Reimbursement Agent</h1>
      <input
        type="text"
        placeholder="Enter diagnosis or treatment..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={handleSearch} style={{ marginLeft: "10px", padding: "10px" }}>
        Search
      </button>

      {loading && <p>Loading...</p>}
      {results &&
        Object.entries(results).map(([name, matches]) => (
          <div key={name} style={{ marginTop: "20px" }}>
            <h3>{name}</h3>
            <ul>
              {matches.map((m, i) => (
                <li key={i}>{m.text} (score: {m.score})</li>
              ))}
            </ul>
          </div>
        ))}
    </div>
  );
}

export default App;
