// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '../src/assets/css/material-font.css';
import VueCookies from 'vue-cookies';

// local module
import App from './App';
import router from './router';
import { store } from './store/store';
import request from './services/request';

Vue.config.productionTip = false;
Vue.use(Vuetify);
Vue.use(VueCookies);
window.onload = function () {
  request.get('project/')
    .then(response => {
      if (!response.data.length) return;
      localStorage.setItem('projects', JSON.stringify(response.data));
      var selected_project = localStorage.getItem('selected_project');
      if (selected_project == null || !selected_project) {
        return;
      }
      selected_project = JSON.parse(selected_project);
      let is_exist = response.data.filter((project, index) => {
        return project.id == selected_project.id;
      });
      if (!is_exist.length) {
        localStorage.removeItem('selected_project');
      };
  })
};
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
}).$mount('#app');
