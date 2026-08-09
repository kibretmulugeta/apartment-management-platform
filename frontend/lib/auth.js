export function setAuthTokens(accessToken, refreshToken, user) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('apparent_access_token', accessToken);
    localStorage.setItem('apparent_refresh_token', refreshToken);
    localStorage.setItem('apparent_user', JSON.stringify(user));
  }
}

export function getStoredUser() {
  if (typeof window !== 'undefined') {
    const raw = localStorage.getItem('apparent_user');
    return raw ? JSON.parse(raw) : null;
  }
  return null;
}

export function clearAuth() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('apparent_access_token');
    localStorage.removeItem('apparent_refresh_token');
    localStorage.removeItem('apparent_user');
  }
}
