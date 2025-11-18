export async function getServerSideProps() {
  const apiUrl = process.env.API_URL;

  try {
    const res = await fetch(`${apiUrl}/articles/`);
    const data = await res.json();

    return { props: { articles: data } };
  } catch (error) {
    console.error("Error fetching articles:", error);
    return { props: { articles: [] } };
  }
}

export default function Home({ articles }) {
  return (
    <div style={{ padding: 30 }}>
      <h1>MTV News Feed</h1>

      {articles.length === 0 && <p>No articles found.</p>}

      {articles.map((a) => (
        <div key={a.id} style={{ marginBottom: 40 }}>
          <h2>{a.title}</h2>
          <p>
            {a.date} {a.time} — <strong>{a.category}</strong>
          </p>

          {a.is_video ? (
            <video
              width="100%"
              controls
              poster={a.video_poster}
              src={a.video_url}
            />
          ) : (
            a.image && <img width="100%" src={a.image} />
          )}

          <p>{a.text.substring(0, 180)}...</p>

          <a
            href={`/article/${a.id}`}
            style={{ color: "blue", textDecoration: "underline" }}
          >
            Read Full Article
          </a>
        </div>
      ))}
    </div>
  );
}
