import axios from "axios";

require('promise.prototype.finally').shim();

axios.interceptors.request.use(config => {
  return config
})

export default {
  get (url) {
    return axios.get(url)
  },
  post (url, data) {
    return axios.post(url, data)
  },
  redirect (to) {
    return window.location.href = to;
  }
};
