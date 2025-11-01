import { useEffect, useState } from "react";
import { fetchItems, summarizeItem, generateCover } from "./api";
import SourcePicker from "./components/SourcePicker";
import ArticleList, { Article } from "./components/ArticleList";
import SummariesPanel from "./components/SummariesPanel";

export default function App() {
  const [items, setItems] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState<Article | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [cover, setCover] = useState<string | null>(null);
  const [coverError, setCoverError] = useState<string | null>(null);
  const [coverLoading, setCoverLoading] = useState(false);

  useEffect(() => {
    loadItems();
  }, []);

  async function loadItems(query?: string, source = "books") {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchItems(query, source);
      const capped = data.slice(0, 6);
      setItems(capped);
      if (capped.length === 0) {
        setError("No books found.");
      }
    } catch {
      setError("Could not load books from backend.");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleSummarize(item: Article) {
    setSelected(item);
    setSummarizing(true);
    setSummary(null);
    setCover(null);
    setCoverError(null);
    try {
      const data = await summarizeItem({
        url: item.url,
        text: item.description,
      });
      setSummary(data.summary);
    } catch {
      setSummary("Could not summarize this item.");
    } finally {
      setSummarizing(false);
    }
  }

  async function handleGenerateCover(item: Article) {
    setSelected(item);
    setCover(null);
    setCoverError(null);
    setCoverLoading(true);
    try {
      const data = await generateCover(item.description || item.title, item.title);
      if (data.image_base64) {
        setCover(`data:image/png;base64,${data.image_base64}`);
      } else if (data.error) {
        setCoverError(data.error);
      } else {
        setCoverError("No image returned from backend.");
      }
    } catch {
      setCoverError("Generating image failed.");
    } finally {
      setCoverLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>📚 AI Book Assistant</h1>
        <SourcePicker onSearch={loadItems} />
      </header>

      <main className="layout">
        <div>
          {loading && <p>Loading…</p>}
          {error && !loading && <p>{error}</p>}
          {!loading && !error && (
            <ArticleList
              articles={items}
              onSummarize={handleSummarize}
              onGenerateCover={handleGenerateCover}
              selectedUrl={selected?.url}
            />
          )}
        </div>

        <div className="right-panel">
          <SummariesPanel summary={summary} summarizing={summarizing} />

          <div className="cover-area">
    <h2>Generated Cover</h2>
    {coverLoading && <p>Generating cover…</p>}
    {coverError && <p style={{ color: "salmon" }}>{coverError}</p>}

    {!cover && !coverLoading && !coverError && (
      <p>Select a book to generate a cover.</p>
    )}

    {cover && !coverError && (
      <img
        src={cover}
        alt="Generated cover"
        className="generated-cover-image"
      />
    )}
          </div>
        </div>
      </main>
    </div>
  );
}
