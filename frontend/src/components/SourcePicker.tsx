import { useState } from "react";

interface Props {
  onSearch: (query: string, source: string) => void;
}

export default function SourcePicker({ onSearch }: Props) {
  const [query, setQuery] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSearch(query, "books"); 
  }

  return (
    <form onSubmit={handleSubmit} className="search">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search books (e.g. Tolkien, Murakami, mystery...)"
      />
      <button type="submit">Search</button>
    </form>
  );
}
