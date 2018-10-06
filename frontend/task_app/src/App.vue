<template>
  <div id="app">
    <v-app id="inspire">
      <side-bar></side-bar>
      <nav-bar></nav-bar>
      <v-content>
        <router-view></router-view>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import NavBar from './components/Layout/NavBar';
import SideBar from './components/Layout/SideBar';
import Content from './components/Layout/Content';


export default {
  name: "app",
  components: {
    NavBar,
    SideBar,
    Content
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
</style>
