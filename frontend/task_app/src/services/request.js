import axios from "axios";

axios.interceptors.request.use(config => {
  return config
})

export default {
  get (url) {
    return axios.get(url)
  },
  post (url, data) {
    axios.post()
  },
  redirect (to) {
    return window.location.href = to;
  }
};
