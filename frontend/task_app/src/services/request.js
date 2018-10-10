import axios from 'axios';
import { apiUrl, getAuthHeader } from '../utils/api-utils';

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
    localStorage.clear()
  }
  return Promise.reject(err);
});

export default {
  get(url) {
    return axios.get(url);
  },
  post(url, data) {
    return axios.post(url, data);
  },
  redirect(to) {
    return (window.location.href = to);
  }
};
