// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '@mdi/font/css/materialdesignicons.css';
import VueCookies from 'vue-cookies';

// local module
import App from './App';
import router from './router';
import { store } from './store/store';

Vue.config.productionTip = false;
Vue.use(Vuetify);
Vue.use(VueCookies);

new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
}).$mount('#app');
