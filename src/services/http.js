import axios from 'axios';

// Session JWT is HttpOnly cookie. The CSRF nonce is deliberately memory-only.
export const http = axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api', withCredentials: true, timeout: 15000 });
let csrf = '';
export function setCsrf(value) { csrf = value || ''; }
http.interceptors.request.use(config => {
  if (!['get', 'head', 'options'].includes((config.method || 'get').toLowerCase()) && csrf) config.headers['X-CSRF-Token'] = csrf;
  return config;
});
http.interceptors.response.use(response => response.data, error => {
  const detail = error.response?.data?.detail;
  const message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map(x => x.msg).join('; ') : error.message || 'Request failed';
  return Promise.reject(new Error(message));
});
