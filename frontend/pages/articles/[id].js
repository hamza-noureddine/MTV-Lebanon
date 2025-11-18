export async function getServerSideProps({ params }) {
  const { id } = params;
  const apiUrl = process.env.API_URL;

  try {
    const res = await fetch(`${apiUrl}/articles/${id}`);
    const data = await res.json();

    return { props: { article: data } };
  } catch (error) {
    console.error(error);
    return { props: { article: null } };
  }
}

export default function ArticlePage({ article }) {
  if (!article) return <p>Article not found.</p>;

  return (
    <div style={{ padding: 30 }}>
      <h1>{article.title}</h1>
      <p>
        {article.date} {article.time} — {article.category}
      </p>

      {article.is_video ? (
        <video
          width="100%"
          controls
          poster={article.video_poster}
          src={article.video_url}
        />
      ) : (
        article.image && <img width="100%" src={article.image} />
      )}

      <p style={{ marginTop: 20, whiteSpace: "pre-line" }}>{article.text}</p>
    </div>
  );
}
