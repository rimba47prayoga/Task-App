import Vue from 'vue';
import Router from 'vue-router';
import NProgress from 'nprogress';
import { store } from '../store/store';
import Login from '@/components/User/Login';
import AuthService from '../services/auth-service';
import 'nprogress/nprogress.css';

Vue.use(Router);

// async components :D

function lazyLoad(component) {
  return () => import(`@/components/${component}`);
}

let router = new Router({
  routes: [
    {
      path: '',
      name: 'dashboard',
      component: lazyLoad('HelloWorld')
    },
    {
      path: '/task',
      name: 'task',
      component: lazyLoad('TaskList'),
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/logout',
      name: 'logout'
    }
  ],
  mode: 'history'
});

NProgress.configure({
  showSpinner: false,
  speed: 1000,
  easing: 'fade'
})

router.beforeEach((to, _from, next) => {
  NProgress.start();
  if (to.matched.some(record => record.meta.requireAuth)) {
    if (!store.getters.isLoggedIn) {
      localStorage.setItem('nextUrl', to.fullPath);
      next({
        path: '/login',
        query: {
          next: to.fullPath
        }
      });
    } else {
      next();
    }
  } else if (to.name == 'logout') {
    AuthService.logout();
    next({
      path: '/login'
    })
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  store.dispatch('setRoute', to);
  NProgress.done();
})

export default router;
