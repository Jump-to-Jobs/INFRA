function App() {
  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Hi, this is JJobs</h1>

      <video
        controls
        style={styles.video}
        src="https://upcdn.io/kW2K8Pz/raw/Woori%20Bae%20momentum%20video.mp4"
      />

      <p style={styles.text}>Please test our App:</p>
      <a href="https://dev.getjjobs.nz" style={styles.link}>
        https://dev.getjjobs.nz
      </a>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    padding: '2rem',
    textAlign: 'center',
    backgroundColor: '#f9f9f9',
    fontFamily: 'sans-serif',
  },
  header: {
    fontSize: '2.5rem',
    marginBottom: '2rem',
  },
  video: {
    maxWidth: '100%',
    width: '720px',
    marginBottom: '1.5rem',
  },
  text: {
    fontSize: '1.2rem',
    marginBottom: '0.5rem',
  },
  link: {
    fontSize: '1.2rem',
    color: '#0070f3',
    textDecoration: 'underline',
  },
};

export default App;
