export const searchQuery = async (query) => {
  const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  return await res.json();
};
