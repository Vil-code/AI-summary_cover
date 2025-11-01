export type Article = {
    title: string;
    url: string;
    source: string;
    description?: string;
  };
  
  interface Props {
    articles: Article[];
    onSummarize: (article: Article) => void;
    onGenerateCover: (article: Article) => void;
    selectedUrl?: string;
    loading?: boolean;
  }
  
  const pastelColors = [
    "#fef3c7", // light yellow
    "#e0f2fe", // light blue
    "#fce7f3", // light pink
    "#dcfce7", // light green
    "#ede9fe", // light purple
    "#fee2e2", // light red
  ];
  
  function colorFromString(str: string) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % pastelColors.length;
    return pastelColors[index];
  }
  
  export default function ArticleList({
    articles,
    onSummarize,
    onGenerateCover,
    selectedUrl,
    loading,
  }: Props) {
    if (loading) return <p>Loading…</p>;
    if (!articles || articles.length === 0) return <p>No items to show.</p>;
  
    return (
      <div className="articles">
        {articles.map((a, idx) => {
          const color = colorFromString(a.title || String(idx));
          return (
            <article
              key={a.url || a.title}
              className={`card ${selectedUrl === a.url ? "active" : ""}`}
              style={{ backgroundColor: color }}
            >
              <h3>{a.title}</h3>
              <p className="source">{a.source}</p>
              <p>{a.description || "No description available for this book."}</p>
              <div className="buttons">
                <button onClick={() => onSummarize(a)}>Summarize</button>
                <button onClick={() => onGenerateCover(a)}>Generate cover</button>
              </div>
            </article>
          );
        })}
      </div>
    );
  }
  