import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(false);
    setResults(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error("Search failed:", err.message);
      setError(true);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>🧠 AI Reimbursement Agent</h1>

      <input
        type="text"
        placeholder="Enter diagnosis or procedure..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        style={{ padding: "10px", width: "300px" }}
      />
      <button onClick={handleSearch} style={{ marginLeft: "10px", padding: "10px" }}>
        Search
      </button>

      {loading && <p>🔄 Searching...</p>}
      {error && <p style={{ color: "red" }}>❌ Something went wrong. Try again.</p>}

      {results &&
        Object.entries(results).map(([category, matches]) => (
          <div key={category} style={{ marginTop: "2rem" }}>
            <h3>{category}</h3>
            {matches.length === 0 ? (
              <p>No results found.</p>
            ) : (
              <ul>
                {matches.map((item, index) => (
                  <li key={index}>
                    <strong>Score:</strong> {item.score} <br />
                    <pre>{item.text}</pre>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
    </div>
  );
}

export default App;
