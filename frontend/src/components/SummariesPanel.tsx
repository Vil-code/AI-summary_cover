interface Props {
    summary?: string | null;
    summarizing?: boolean;
  }
  
  export default function SummariesPanel({ summary, summarizing }: Props) {
    return (
      <section className="summary">
        <h2>Summary</h2>
        {summarizing && <p>Summarizing…</p>}
        {!summarizing && summary && <pre>{summary}</pre>}
        {!summarizing && !summary && <p>Select a book to summarize.</p>}
      </section>
    );
  }
  