<template>
  <v-navigation-drawer
    :clipped="$vuetify.breakpoint.lgAndUp"
    :value="sidebar"
    fixed
    app
    :mini-variant.sync="mini_variant"
    stateless
  >
    <v-list class="pt-2 mb-1">
      <v-list-tile avatar>
        <v-list-tile-avatar>
          <!-- <img
          v-if="$store.getters.user.picture != null"
          :src="$store.getters.user.picture"
          > -->
          <v-icon>account_circle</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
          <v-list-tile-title>Username</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
    <v-divider class="mb-3"></v-divider>
    <side-bar-item></side-bar-item>
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
    mini_variant: document.body.offsetWidth <= 1200
  }),
  computed: {
    ...mapState([
      'sidebar'
    ])
  }
}
</script>

<style>

</style>
