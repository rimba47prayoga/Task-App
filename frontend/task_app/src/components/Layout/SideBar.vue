<template>
  <v-navigation-drawer
    :clipped="$vuetify.breakpoint.lgAndUp"
    :value="sidebar"
    fixed
    app
    :mini-variant="mini_variant"
    stateless
    width="260"
  >
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
