<template>
  <div id="app">
    <v-app id="inspire" v-if="$store.getters.isLoggedIn">
      <side-bar></side-bar>
      <nav-bar></nav-bar>
      <v-content>
        <v-layout align-content-space-between justify-start pa-3 ml-3>
        <div style="font-size: 25px;line-height: -moz-block-height;" class="mr-2">{{ lastPath() }}</div>
        <v-breadcrumbs :large="true" divider="-" class="pr-4 pl-4 ma-2">

          <v-breadcrumbs-item
            v-for="(item, index) in breadcrumbs"
            :key="index"
            :disabled="true"
          >
            <v-icon v-if="item.icon">{{ item.icon }}</v-icon>
            {{ item.name }}
          </v-breadcrumbs-item>
        </v-breadcrumbs>
        </v-layout>
        <router-view></router-view>
      </v-content>
    </v-app>
    <router-view v-else></router-view>
  </div>
</template>

<script>
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
    lastPath(){
      return capitalize(this.$route.name)
    }
  },
  computed: {
    breadcrumbs(){
      let route_name = this.$route.name;
      if (route_name == null){
        route_name = this.$router.currentRoute.name;
      }
      return [
        {
          icon: 'home',
          name: ''
        },
        {
          icon: null,
          name: capitalize(route_name)
        }
      ]
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
</style>
