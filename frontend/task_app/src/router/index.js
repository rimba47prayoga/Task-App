import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TaskList from '@/components/TaskList'
import Login from '@/components/User/Login'
import { store } from '../store/store';

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/task',
      name: 'TaskList',
      component: TaskList,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ],
  mode: "history"
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireAuth)) {
    if (!store.getters.isLoggedIn){
      next({
        path: '/login',
        query: {
          next: to.fullPath
        }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
