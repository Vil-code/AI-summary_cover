import axios from "axios";

const API_BASE = "https://ai-summary-cover.onrender.com";

export async function fetchItems(q?: string, source = "books") {
  try {
    const res = await axios.get(`${API_BASE}/items`, {
      params: { q, source },
    });
    return res.data as {
      title: string;
      url: string;
      source: string;
      description?: string;
    }[];
  } catch (err) {
    console.error("fetchItems failed", err);
    return [];
  }
}

export async function summarizeItem(payload: { url?: string; text?: string }) {
  const res = await axios.post(`${API_BASE}/summarize`, payload);
  return res.data as { summary: string };
}

export async function generateCover(description: string, title?: string) {
  const res = await axios.post(`${API_BASE}/cover`, {
    description,
    title,
  });
  return res.data as { image_base64?: string; error?: string };
}
