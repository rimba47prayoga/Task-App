import Vue from 'vue';
import Router from 'vue-router';
import NProgress from 'nprogress';
import { store } from '../store/store';
import Login from '@/components/User/Login';
import AuthService from '../services/auth-service';
import 'nprogress/nprogress.css';
import request from '../services/request';

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
      component: lazyLoad('Dashboard'),
      meta: {
        breadcrumbs: ['dashboard']
      }
    },
    {
      path: '/task/list',
      name: 'task',
      component: lazyLoad('Task/TaskList'),
      meta: {
        requireAuth: true,
        breadcrumbs: ['task', 'list']
      }
    },
    {
      path: '/project/create-project',
      name: 'Create Project',
      component: lazyLoad('Project/CreateProject'),
      meta: {
        breadcrumbs: ['project', 'create project']
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
  speed: 1000
});

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
      // if (localStorage.getItem('projects') == null) {
      //   next({
      //     name: 'dashboard'
      //   });
      // }
      next();
    }
  } else if (to.name == 'logout') {
    AuthService.logout();
    next({
      path: '/login'
    });
    NProgress.done();
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  store.dispatch('setRoute', to);
  NProgress.done();
  // if (localStorage.getItem('projects') == null) {
  //   let blocked_url = ['task']
  //   if (blocked_url.indexOf(to.name) > -1) {
  //     request.get('project/').then(response => {
  //       if (!response.data.length) {
  //         router.push('/');
  //       }
  //     });
  //   }
  // }
});

export default router;
