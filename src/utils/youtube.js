/** Strict, provider-specific YouTube URL matching. Never extract an ID from a
 * URL with a deceptive hostname/scheme. Existing bare IDs still preview.
 */
const ID = /^[A-Za-z0-9_-]{11}$/;
const MAIN = new Set(['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtube-nocookie.com', 'www.youtube-nocookie.com']);
const SHORT = new Set(['youtu.be', 'www.youtu.be']);

export const extractYouTubeVideoId = (value) => {
  if (typeof value !== 'string' || !value || value !== value.trim()) return null;
  if (ID.test(value)) return value; // Existing legacy lesson records.
  if (/[\u0000-\u0020\u007f\\]/.test(value) || value.length > 2048) return null;
  try {
    const url = new URL(value);
    const rawAuthority = value.match(/^https:\/\/([^/?#]+)/)?.[1]?.toLowerCase();
    if (url.protocol !== 'https:' || url.username || url.password || url.port || url.hash ||
        !rawAuthority || rawAuthority !== url.hostname ||
        (!MAIN.has(url.hostname) && !SHORT.has(url.hostname))) return null;
    let videoId = null;
    if (SHORT.has(url.hostname)) {
      videoId = url.pathname.startsWith('/') ? url.pathname.slice(1) : null;
    } else if (url.pathname === '/watch') {
      const ids = url.searchParams.getAll('v');
      videoId = ids.length === 1 ? ids[0] : null;
    } else {
      videoId = url.pathname.match(/^\/(?:embed|shorts|live|v)\/([A-Za-z0-9_-]{11})$/)?.[1];
    }
    return ID.test(videoId || '') ? videoId : null;
  } catch {
    return null;
  }
};

export const isValidYouTubeUrl = value => value === '' ||
  (typeof value === 'string' && value.startsWith('https://') &&
   !!extractYouTubeVideoId(value) && !ID.test(value));

export const getYouTubeEmbedUrl = value => {
  const id = extractYouTubeVideoId(value);
  return id ? `https://www.youtube-nocookie.com/embed/${id}?rel=0&modestbranding=1&enablejsapi=1` : null;
};
