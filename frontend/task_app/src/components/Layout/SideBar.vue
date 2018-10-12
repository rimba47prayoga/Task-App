<template>
  <v-navigation-drawer
    :clipped="$vuetify.breakpoint.lgAndUp"
    :value="sidebar"
    fixed
    app
    :mini-variant="mini_variant"
    stateless
  >
    <v-list class="pt-2 mb-1">
      <v-list-tile avatar>
        <v-list-tile-avatar>
          <img
          v-if="user.picture != null"
          :src="user.picture"
          >
          <v-icon v-else>account_circle</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
          <v-list-tile-title>{{ user.username }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
    <v-divider class="mb-3"></v-divider>
    <side-bar-item
      v-bind:mini_variant="mini_variant"
      v-on:set-mini-variant="mini_variant = true"
      v-on:unset-mini-variant="mini_variant = false"
    ></side-bar-item>
  </v-navigation-drawer>
</template>

<script>
import SideBarItem from "./SideBarItem";

import {mapState} from 'vuex';

export default {
  components: {
    SideBarItem
  },
  data: () => ({
    mini_variant: true,
  }),
  computed: {
    ...mapState([
      'sidebar'
    ]),
    user(){
      let user = this.$store.getters.user;
      var picture;
      if (user.profile == null){
        picture = null;
      } else {
        if(user.profile.picture != 'undefined') {
          picture = user.profile.picture;
        } else {
          picture = null;
        }
      }
      user.picture = picture;
      return user;
    }
  }
}
</script>

<style>

</style>
