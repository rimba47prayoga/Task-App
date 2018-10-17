<template>
  <v-toolbar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      color="blue darken-3"
      dark
      app
      fixed
    >
      <v-toolbar-title style="width: 264px" class="ml-0">
        <v-toolbar-side-icon @click.stop="setSidebar()"></v-toolbar-side-icon>
        <img src="@/assets/task_icon.png" class="task_icon" />
        <span class="hidden-sm-and-down ml-3">Task App</span>
      </v-toolbar-title>

      <v-autocomplete
        v-model="select"
        :loading="loading_search"
        :items="items"
        :search-input.sync="search"
        item-text="title"
        item-value="id"
        clearable
        flat
        hide-no-data
        label="Search"
        prepend-inner-icon="search"
        solo-inverted
        :menu-props="{zIndex:'10000000'}"
        id="search_autocomplete"
      >
      </v-autocomplete>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>notifications</v-icon>
      </v-btn>
      <v-btn icon large>
        <v-avatar size="32px" tile>
          <img
            src="https://cdn.vuetifyjs.com/images/logos/logo.svg"
            alt="Vuetify"
          >
        </v-avatar>
      </v-btn>
    </v-toolbar>
</template>

<script>
import request from "../../services/request.js";

export default {
  data(){
    return {
      loading_search: false,
      items: [],
      recent_search: [],
      cache_result: [],
      select: null,
      search: null
    }
  },
  methods: {
    setSidebar(){
      this.$store.commit('setSidebar', !this.$store.getters.sidebar)
    }
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
      request.get(`task/search/autocomplete?q=${val}`)
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
  },
  mounted(){
    let search = document.getElementById('search_autocomplete');
    search.addEventListener('keydown', (event) => {
      if (event.keyCode == 13){
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        console.log(event);
        return false;
      }
    })
  }
}
</script>

<style>
.v-list__tile__title {
  font-weight: bold;
}
.v-list__tile__title > .v-list__tile__mask {
  font-weight: normal;
  background: none !important;
  color: unset !important;
}
.task_icon {
  width: 40px;
  vertical-align: middle;
}
nav .v-autocomplete .v-input__slot {
  margin: 0;
}
</style>
