import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    sidebar: true,
    isCreatingTask: false
  },
  mutations: {
    setSidebar (state, sidebar) {
      state.sidebar = sidebar;
    },
    showDialogCreateTask (state, isCreating) {
      state.isCreatingTask = isCreating;
    }
  },
  actions: {
    setSidebar ({ commit }, sidebar) {
      commit('setSidebar', sidebar);
    },
    showDialogCreateTask ({ commit }, isCreating) {
      commit('showDialogCreateTask', isCreating);
    }
  },
  getters: {
    sidebar: state => {
      return state.sidebar;
    },
    isCreatingTask: ({ isCreatingTask }) => {
      return isCreatingTask
    }
  }
});
