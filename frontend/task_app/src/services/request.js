import axios from 'axios';
import router from '../router/index';
import { apiUrl, getAuthHeader } from '../utils/api-utils';
import AuthService from './auth-service';

require('promise.prototype.finally').shim();

axios.defaults.baseURL = apiUrl();

axios.interceptors.request.use(config => {
  config.headers['Authorization'] = getAuthHeader();
  return config;
});

axios.interceptors.response.use(response => response, err => {
  const error = err.response;
  if (error.status === 401 && error.config && !error.config.__isRetryRequest) {
    // request for a new token
    AuthService.logout();
    router.push('/logout');
  } else {
    return Promise.reject(err); // stop next action/ return error
  }
});

export default {
  get(url) {
    return axios.get(url);
  },
  post(url, data) {
    return axios.post(url, data);
  },
  put (url, data) {
    return axios.put(url, data);
  },
  patch (url, data) {
    return axios.patch(url, data);
  },
  redirect(to) {
    return router.push(to)
  }
};
