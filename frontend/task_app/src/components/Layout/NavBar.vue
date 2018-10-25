<template>
  <v-toolbar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      color="blue darken-3"
      dark
      app
      fixed
      class="task-navbar"
    >
      <v-toolbar-title style="width: 260px" class="ml-1 pl-2 mr-4">
        <v-toolbar-side-icon @click.stop="setSidebar()"></v-toolbar-side-icon>
          <img src="@/assets/task_icon.png" class="task_icon" />
        <span class="hidden-sm-and-down ml-1">Task App</span>
      </v-toolbar-title>

      <v-autocomplete
        v-model="select"
        :loading="loading_search"
        :items="items"
        :search-input.sync="search"
        :autofocus="true"
        item-text="title"
        item-value="id"
        clearable
        flat
        no-filter
        hide-no-data
        label="Search"
        prepend-inner-icon="search"
        solo-inverted
        :menu-props="{
          zIndex:'10000000',
          overflowY: true,
          overflowX: true,
          offsetOverflow: false
        }"
        ref="search_autocomplete"
        @change="change"
        return-object
      >
        <template
          slot="item"
          slot-scope="{ parent, item, tile }"
        >
          <v-list-tile-avatar v-if="item.assignee != null">
            <v-img v-if="item.avatar != null" :src="item.avatar"></v-img>
            <v-icon v-else class="primary--text">
              account_circle
            </v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <!--Highlight output item.name-->
            <!-- <v-list-tile-title v-html="`${parent.genFilteredText(item.title)}`">
            </v-list-tile-title> -->
            <v-list-tile-title class="font-weight-bold" v-html="item.title_highlighted"></v-list-tile-title>
            <v-list-tile-sub-title v-text="item.assignee"></v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <div class="text-xs-center">
              <v-chip>
                <v-avatar class="teal">{{ item.branch.split('-')[0] }}</v-avatar>
                {{ item.branch.split('-')[1] }}
              </v-chip>
            </div>
          </v-list-tile-action>
       </template>

      </v-autocomplete>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <v-btn icon @click="FullScreen()" slot="activator">
          <v-icon>fullscreen</v-icon>
        </v-btn>
        <span>Set FullScreen</span>
      </v-tooltip>

      <v-tooltip bottom>
        <v-btn icon slot="activator">
          <v-icon>apps</v-icon>
        </v-btn>
        <span>Apps</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn icon slot="activator">
          <v-icon>notifications</v-icon>
        </v-btn>
        <span>Notifications</span>
      </v-tooltip>
      <div class="text-xs-center">
        <v-menu
          v-model="menu"
          :close-on-content-click="false"
          :nudge-width="200"
          offset-y
        >
          <v-btn icon large class="mr-4" slot="activator">
            <v-avatar size="32px" tile>
              <img v-if="user && user.profile && user.profile.picture"
                src="https://cdn.vuetifyjs.com/images/logos/logo.svg"
                alt="Vuetify"
              >
              <v-icon v-else size="32px">
                account_circle
              </v-icon>
            </v-avatar>
          </v-btn>

          <v-card>
            <v-list>
              <v-list-tile avatar>
                <v-list-tile-avatar>
                  <img v-if="user && user.profile && user.profile.picture"
                    src="https://cdn.vuetifyjs.com/images/logos/logo.svg"
                    alt="Vuetify"
                  >
                  <v-icon v-else size="32px">
                    account_circle
                  </v-icon>
                </v-list-tile-avatar>

                <v-list-tile-content>
                  <v-list-tile-title>{{ user.first_name }} {{ user.last_name }}</v-list-tile-title>
                  <v-list-tile-sub-title>Full Stack developer</v-list-tile-sub-title>
                </v-list-tile-content>

                <v-list-tile-action>
                  <v-btn
                    class="red--text"
                    icon
                  >
                    <v-icon>favorite</v-icon>
                  </v-btn>
                </v-list-tile-action>
              </v-list-tile>
            </v-list>

            <v-divider></v-divider>

            <v-list>
              <v-list-tile>
                <v-list-tile-action>
                  <v-icon>
                    account_circle
                  </v-icon>
                </v-list-tile-action>
                <v-list-tile-title>Profile</v-list-tile-title>
              </v-list-tile>

              <v-list-tile>
                <v-list-tile-action>
                  <v-icon>
                    settings
                  </v-icon>
                </v-list-tile-action>
                <v-list-tile-title>Settings</v-list-tile-title>
              </v-list-tile>
            </v-list>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn color="primary" ripple flat @click="$router.push('/logout')">Log out</v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </div>
    </v-toolbar>
</template>

<script>
import { EventBus } from '../../event-bus.js';
import request from "../../services/request.js";
import { toggleFullScreen } from '../../utils/common.js';

export default {
  data(){
    return {
      loading_search: false,
      items: [],
      recent_search: [],
      cache_result: [],
      select: null,
      search: null,
      user: this.$store.getters.user,
      menu: false,
      search_width: null
    }
  },
  methods: {
    setSidebar(){
      EventBus.$emit('toggleSidebar');
    },
    change(val){
      this.$store.commit('setSearch', this.select);
      if (typeof val == "undefined") {
        this.$router.push({
          query: {}
        });
        return;
      }
      var q = window.encodeURIComponent(val.title);
      this.$router.push({
        query: {
          q: q
        }
      });
    },
    FullScreen(){
      toggleFullScreen();
    }
  },
  computed: {
    selected_project(){
      var selected = this.$store.getters.selected_project ||
      localStorage.getItem('selected_project');
      if (selected == null) return false;
      if (typeof selected == "string"){
        selected = JSON.parse(selected);
      }
      return selected.id;
    }
  },
  mounted(){
    let search_width = this.$refs.search_autocomplete.$el.offsetWidth;
    this.search_width = search_width;
  },
  watch: {
    search(val){

      if(this.recent_search.indexOf(val) > -1){
        let recent_word = this.cache_result.filter((item, index) => {
          return item.key == val;
        });
        this.items = recent_word[0].result;
        return;
      };
      if (val == null || !val || val == ''){
        this.items = [];
        return;
      }
      this.loading_search = true;
      let selected_project = this.selected_project;
      if (!selected_project){
        this.$router.push({
          name: 'dashboard'
        });
        return false;
      }
      request.get(`task/search/autocomplete?q=${val}&project=${selected_project}`)
      .then(response => {
        this.items = response.data.result;
        this.recent_search.push(val);
        this.cache_result.push({
          key: val,
          result: response.data.result
        });
      }).finally(() => {
        this.loading_search = false;
      })
    }
  }
}
</script>

<style>
/* .v-list__tile__title {
  font-weight: bold;
}
.v-list__tile__title > .v-list__tile__mask {
  font-weight: normal;
  background: none !important;
  color: unset !important;
} */
span.highlighted {
  font-weight: lighter !important;
}
.task_icon {
  width: 34px;
  vertical-align: middle;
}
nav .v-autocomplete .v-input__slot {
  margin: 0;
}
nav.task-navbar .v-toolbar__content {
  padding: 0;
}
</style>
