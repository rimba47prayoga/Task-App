import VueCookies from 'vue-cookies';

import request from './request';
import CryptoService from './crypto-service';

export default {
  login(username, password) {
    return request.post('auth/login', {
      username: username,
      password: password
    });
  },
  setToken(token_ori) {
    let salt = token_ori.substring(0, 10);
    let token = token_ori.substring(10, token_ori.length - 10);
    // __ft_sa -- first token salt 10 substring
    // __lt10 -- last token 10 substring
    // __ta -- token app
    let __lt10 = token_ori.substring(token_ori.length - 10, token_ori.length);
    VueCookies.set('__ft_sa', CryptoService.encrypt(salt));
    VueCookies.set('__ta', btoa(token)); // base64 encode
    VueCookies.set('__lt10', CryptoService.encrypt(__lt10));

    let random = CryptoService.randomString(30); // token ori has minus 30, cause i choose it
    let fake_token = `${btoa(token.substring(0, token.length - 10))}.${random}`;
    localStorage.setItem('token', fake_token);
    VueCookies.set('__isLn', 1); // set data if user isLoggedIn -- __isLn = isLoggedIn
  },
  getToken() {
    let salt = CryptoService.decrypt(VueCookies.get('__ft_sa'));
    let token = atob(VueCookies.get('__ta'));
    let __lt10 = CryptoService.decrypt(VueCookies.get('__lt10'));
    const __token = `${salt}${token}${__lt10}`;
    return __token;
  }
};
