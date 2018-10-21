import Vue from 'vue';
import Vuex from 'vuex';
import VueCookies from 'vue-cookies';

import router from '../router/index';
import AuthService from '../services/auth-service';
import ProjectType from '../constants/ProjectType';

Vue.use(Vuex);
export const store = new Vuex.Store({
  state: {
    sidebar: true,
    isCreatingTask: false,

    // user handler
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('__user')) || {},
    isLoggedIn: VueCookies.get('__isLn') == '1',
    currentRoute: {},
    selected_project: localStorage.getItem('selected_project')
  },
  mutations: {
    setSidebar(state, sidebar) {
      state.sidebar = sidebar;
    },
    showDialogCreateTask(state, isCreating) {
      state.isCreatingTask = isCreating;
    },

    // user handler
    auth_success(state, token, user) {
      state.token = token;
      state.user = user;
      state.isLoggedIn = true;
    },
    logout(state) {
      state.isLoggedIn = false;
    },
    setRoute(state, route) {
      state.currentRoute = route;
    },
    selectProject (state, project) {
      state.selected_project = project;
    }
  },
  actions: {
    setSidebar({ commit }, sidebar) {
      commit('setSidebar', sidebar);
    },
    showDialogCreateTask({ commit }, isCreating) {
      commit('showDialogCreateTask', isCreating);
    },

    // user handler
    login({ commit }, payload) {
      AuthService.login(payload.username, payload.password)
        .then(response => {
          response = response.data;
          localStorage.setItem('user', JSON.stringify(response.user));
          AuthService.setToken(response.token);
          commit('auth_success', response.token, response.user);
          router.push(localStorage.getItem('nextUrl'));
        })
        .catch(err => {
          console.log(err);
        });
    },

    logout({ commit }) {
      commit('logout');
    },
    setRoute({ commit }, route) {
      commit('setRoute', route);
    },
    selectProject ({ commit }, project) {
      commit('selectProject', project);
    }
  },
  getters: {
    sidebar: state => {
      return state.sidebar;
    },
    isCreatingTask: ({ isCreatingTask }) => {
      return isCreatingTask;
    },
    isLoggedIn: ({ isLoggedIn }) => isLoggedIn,
    user: ({ user }) => user,
    token: ({ token }) => token,
    currentRoute: ({ currentRoute }) => currentRoute,
    selected_project: ({ selected_project }) => {
      if (selected_project != null) {
        let project = selected_project;
        if (typeof project == "string") {
          project = JSON.parse(selected_project);
        }
        project.project_type = ProjectType.getProjectDisplay(project.project_type);
        return project;
      }
      return null;
    }
  }
});
