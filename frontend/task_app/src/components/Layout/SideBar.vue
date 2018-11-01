<template>
  <v-navigation-drawer
    :clipped="$vuetify.breakpoint.lgAndUp"
    v-model="drawer"
    fixed
    app
    :mini-variant="mini_variant"
    width="260"
    class="white-grey-blue"
  >
    <side-bar-item
      v-bind:mini_variant="mini_variant"
      v-on:set-mini-variant="setMiniVariant()"
    ></side-bar-item>
  </v-navigation-drawer>
</template>

<script>
import { EventBus } from '../../event-bus.js';
import SideBarItem from "./SideBarItem";

import { mapState } from 'vuex';

export default {
  components: {
    SideBarItem
  },
  data: () => ({
    drawer: true,
    mini_variant: localStorage.getItem('mini_variant') == null
                    ? true
                    : localStorage.getItem('mini_variant') == 'true',
  }),
  methods: {
    setMiniVariant(){
      this.mini_variant = !this.mini_variant;
      localStorage.setItem('mini_variant', this.mini_variant)
    }
  },
  computed: {
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
  },
  mounted(){
    EventBus.$on('toggleSidebar', () => {
      this.drawer = !this.drawer;
    })
  }
}
</script>

<style>
.white-grey-blue {
  background: #F4F5F7 !important;
}
</style>
