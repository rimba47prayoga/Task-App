<template>
  <div id="app">
    <v-app id="inspire" v-if="$store.getters.isLoggedIn">
      <side-bar></side-bar>
      <nav-bar></nav-bar>
      <v-content>
        <v-layout align-content-space-between justify-start>
        <v-breadcrumbs
          v-if="breadcrumbs.length"
          :large="true"
          divider=" / "
          class="pr-4 pl-4 mt-1 ml-2 mr-2 mb-0"
        >
          <v-breadcrumbs-item
            v-for="(item, index) in breadcrumbs"
            :key="index"
            :disabled="index == breadcrumbs.length - 1"
          >
            {{ item }}
          </v-breadcrumbs-item>
        </v-breadcrumbs>
        </v-layout>
        <transition
          name="fade"
          mode="out-in"
          appear
        >
          <router-view></router-view>
        </transition>
        <v-snackbar
          :value="this.$store.getters.notifications.show"
          top
          right
          multi-line
          :timeout="60000"
          color="white"
          class="black--text"
        >
          <v-badge color="red" overlap class="mr-3">
              <span slot="badge">{{ this.$store.getters.notifications.count }}</span>
                <v-icon large>
                  notifications_active
                </v-icon>
            </v-badge>
          New notifications

          <v-btn
            color="blue"
            flat
            @click="closeNotifications()"
          >
            Close
          </v-btn>
        </v-snackbar>
        <create-task></create-task>
      </v-content>
    </v-app>
    <router-view v-else></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import NProgress from 'nprogress';

import NavBar from './components/Layout/NavBar';
import SideBar from './components/Layout/SideBar';
import CreateTask from "./components/Task/CreateTask";

import { capitalize as UtilCapitalize } from './utils/common.js';

export default {
  name: "app",
  components: {
    NavBar,
    SideBar,
    CreateTask
  },
  methods: {
    capitalize(value){
      return UtilCapitalize(value);
    },
    basePath(){
      if (this.breadcrumbs){
        return UtilCapitalize(this.breadcrumbs[1])
      }
      return []
    },
    closeNotifications(){
      this.$store.dispatch('setNotifications', {
        show: false,
        count: 0
      })
    }
  },
  computed: {
    ...mapState([
      'search'
    ]),
    breadcrumbs(){
      let selected_project = this.$store.getters.selected_project;
      if (selected_project){
        return [
          `${selected_project.name} - ${selected_project.project_type}`,
          `${selected_project.board_name} Board`
        ]
      }
      return [];
    }
  },
  watch: {
    search(obj){
      if (typeof obj == "undefined" || !obj || obj == null || obj == {}){
        return;
      }
      if (obj.table == 'task'){
        this.$router.push({
          name: 'task-list',
          params: {
            slug: this.$store.getters.selected_project.slug
          },
          query: {
            q: window.encodeURIComponent(obj.title)
          }
        })
      }
    }
  },
  beforeCreate(){
    NProgress.start();
  },
  mounted(){
    NProgress.done();
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.theme--light.application{
  background: #ffffff;
}
.fade-enter-active, .fade-leave-active {
  opacity: 0.3;
  background-color: #ffffff !important;
}
.fade-enter, .fade-leave-to {
  opacity: 0.3;
  background-color: #ffffff !important;
  transition: .5s
}

.router-change {
  background: #ffffff !important;
  opacity: .4;
}

#nprogress .bar {
  background: #42A5F5;
}
#nprogress {
  transition: none !important;
}
.theme--light.v-list .v-list__tile--link:hover {
  background: rgba(9, 30, 66, 0.04) !important;
}

aside .v-navigation-drawer__border {
  border-right: 1px solid rgba(0,0,0,.12);
  background: none !important;
  width: 10px;
}

aside .v-navigation-drawer__border:hover{
  transition: ease-in-out .3s;
  border-right: 2px solid #1565c0 !important;
  cursor: col-resize;
}

label.input-label {
  color: #5e6c84;
  font-weight: bold;
  margin-left: 1px;
}
span.required {
  color: #ff5252;
}
.v-tooltip__content {
  opacity: 1 !important;
  border-radius: 5px !important;
}

.sub-task, .theme--light.sub-task,
.task, .theme--light.task {
  color:#64B5F6;
}
.bug, .theme--light.bug {
  color: #E53935;
}

.priority-lowest, .theme--light.priority-lowest {
  color: #66BB6A;
}
.priority-low, .theme--light.priority-low {
  color: #2E7D32;
}
.priority-medium, .theme--light.priority-medium {
  color: #F57C00;
}
.priority-high, .theme--light.priority-high {
  color: #E53935;
}
.priority-highest, .theme--light.priority-highest {
  color: #B71C1C;
}
</style>
