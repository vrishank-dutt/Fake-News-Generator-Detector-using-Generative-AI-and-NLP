async function generateHeadline() {
  const topic = document.getElementById("seedText").value.trim();
  const output = document.getElementById("generatedHeadline");

  if (!topic) {
    output.textContent = "⚠️ Please enter a topic first.";
    return;
  }

  output.textContent = "⏳ Generating...";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });

    const data = await response.json();
    output.textContent = `📰 ${data.headline}`;
  } catch (error) {
    console.error("Generation error:", error);
    output.textContent = "❌ Error generating headline.";
  }
}

async function classifyHeadline() {
  const headline = document.getElementById("headlineText").value.trim();
  const output = document.getElementById("classificationResult");

  if (!headline) {
    output.textContent = "⚠️ Please enter a headline first.";
    return;
  }

  output.textContent = "⏳ Classifying...";

  try {
    const response = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline }),
    });

    const data = await response.json();
    output.textContent = `✅ Result: ${data.prediction}`;
  } catch (error) {
    console.error("Classification error:", error);
    output.textContent = "❌ Error classifying headline.";
  }
}

async function fetchNews() {
  const query = document.getElementById("newsQuery").value.trim() || "technology";
  const container = document.getElementById("newsResults");
  container.innerHTML = "⏳ Fetching news...";

  try {
    const response = await fetch(`/fetch_news?q=${encodeURIComponent(query)}`);
    const data = await response.json();

    if (data.articles && data.articles.length > 0) {
      container.innerHTML = "";
      data.articles.forEach((article) => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
          <h3>${article.title}</h3>
          <p>${article.content || "No content available."}</p>
          <small>📅 ${new Date(article.publishedAt).toLocaleString()} | 🏷️ ${article.source}</small>
          <small><a href="${article.url}" target="_blank">🔗 Read more</a></small>
        `;

        container.appendChild(card);
      });
    } else {
      container.innerHTML = "No articles found for this query.";
    }
  } catch (error) {
    console.error("News fetch error:", error);
    container.innerHTML = "❌ Failed to fetch news.";
  }
}
