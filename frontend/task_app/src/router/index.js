import Vue from 'vue';
import Router from 'vue-router';
import { store } from '../store/store';
import Login from '@/components/User/Login';
import AuthService from '../services/auth-service';

Vue.use(Router);

// async components :D

function lazyLoad(component) {
  return () => import(`@/components/${component}`);
}

let router = new Router({
  routes: [
    {
      path: '',
      name: 'HelloWorld',
      component: lazyLoad('HelloWorld')
    },
    {
      path: '/task',
      name: 'TaskList',
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

router.beforeEach((to, _from, next) => {
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

export default router;
