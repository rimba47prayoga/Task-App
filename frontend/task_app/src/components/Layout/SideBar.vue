<template>
  <v-navigation-drawer
    :clipped="$vuetify.breakpoint.lgAndUp"
    :value="sidebar"
    fixed
    app
    :mini-variant="mini_variant"
    stateless
    hide-overlay
    width="260"
    class="white-grey-blue"
  >
    <side-bar-item
      v-bind:mini_variant="mini_variant"
      v-on:set-mini-variant="mini_variant = !mini_variant"
    ></side-bar-item>
  </v-navigation-drawer>
</template>

<script>
import SideBarItem from "./SideBarItem";

import { mapState } from 'vuex';

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
.white-grey-blue {
  background: #F4F5F7 !important;
}
</style>
