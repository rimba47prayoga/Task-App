<template>
  <div id="app">
    <v-app id="inspire" v-if="$store.getters.isLoggedIn">
      <side-bar></side-bar>
      <nav-bar></nav-bar>
      <v-content>
        <v-layout align-content-space-between justify-start>
        <!-- <div style="font-size: 25px;line-height: -moz-block-height;" class="mr-2"></div> -->
        <v-breadcrumbs
          v-if="breadcrumbs.length"
          :large="true"
          divider="-"
          class="pr-4 pl-4 ma-2"
        >
          <v-breadcrumbs-item style="font-size: 25px">
            {{ basePath() }}
          </v-breadcrumbs-item>
          <v-breadcrumbs-item
            v-for="(item, index) in breadcrumbs"
            :key="index"
            :disabled="index == breadcrumbs.length - 1"
          >
            <v-icon v-if="item == 'home'">home</v-icon>
            {{ item != 'home' ? item: '' }}
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
      </v-content>
    </v-app>
    <router-view v-else></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex';

import NavBar from './components/Layout/NavBar';
import SideBar from './components/Layout/SideBar';

import { capitalize } from './utils/common.js';

export default {
  name: "app",
  components: {
    NavBar,
    SideBar
  },
  methods: {
    basePath(){
      if (this.breadcrumbs){
        return capitalize(this.breadcrumbs[1])
      }
      return []
    }
  },
  computed: {
    ...mapState([
      'search'
    ]),
    breadcrumbs(){
      var currentRoute = this.$route;
      if (typeof currentRoute.meta.breadcrumbs != "undefined"){
        return ['home', ...currentRoute.meta.breadcrumbs];
      }
      return false;
    }
  },
  watch: {
    search(obj){
      if (typeof obj == "undefined" || !obj || obj == null || obj == {}){
        return;
      }
      if (obj.table == 'task'){
        this.$router.push({
          name: 'task',
          query: {
            q: window.encodeURIComponent(obj.title)
          }
        })
      }
    }
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
  height: 3px;
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
</style>
