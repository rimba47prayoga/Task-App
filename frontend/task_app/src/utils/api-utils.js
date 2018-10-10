import { store } from '../store/store';
import AuthService from '../services/auth-service';

function apiUrl() {
  return process.env.API_HOST;
}

function getAuthHeader() {
  const isLoggedIn = store.getters.isLoggedIn;
  if (isLoggedIn) {
    let prefix = btoa('TaskApp El Psy Congroo');
    let token = AuthService.getToken();
    return `${prefix} ${token}`;
  }
  return '';
}

export { apiUrl, getAuthHeader };
