export async function getServerSideProps() {
  const res = await fetch(process.env.API_URL + "/articles");
  const data = await res.json();

  return { props: { articles: data } };
}

export default function Home({ articles }) {
  return (
    <div style={{ padding: 30 }}>
      <h1>MTV News</h1>

      {articles.map(a => (
        <div key={a.id} style={{ marginBottom: 40 }}>
          <h2>{a.title}</h2>
          <p>{a.date} {a.time} – {a.category}</p>

          {a.is_video ? (
            <video width="100%" controls poster={a.video_poster} src={a.video_url} />
          ) : (
            <img width="100%" src={a.image} />
          )}

          <p>{a.text.substring(0, 200)}...</p>
        </div>
      ))}
    </div>
  );
}
