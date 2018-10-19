<template>
  <v-list dense>

    <div class="mb-1 mt-1 project-sidebar-item">
      <v-menu
        v-model="menu"
        absolute
        :close-on-content-click="false"
        :nudge-width="300"
        offset-x
      >
        <v-list-tile class="mb-3 mt-3" slot="activator">
          <v-tooltip right z-index="1000000">
            <v-list-tile-action slot="activator">
              <img class="project_icon" src="@/assets/project_icon.png" />
            </v-list-tile-action>
            <span>Project Name</span>
          </v-tooltip>
          <v-list-tile-content>
            <v-list-tile-title style="font-size:17px;">
              Project Name
            </v-list-tile-title>
            <span style="font-size: 12px; color: #616161;">Software Project</span>
          </v-list-tile-content>
        </v-list-tile>

        <v-card>
          <v-list>
            <v-list-tile avatar>
              <v-list-tile-avatar>
                <img class="project_icon" src="@/assets/project_icon.png" />
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>Project Name</v-list-tile-title>
                <v-list-tile-sub-title>Software Project</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
          <v-divider></v-divider>
          <v-list>
            <v-list-tile avatar>
              <v-list-tile-avatar>
                <img class="project_icon" src="@/assets/project_icon.png" />
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>Project Name</v-list-tile-title>
                <v-list-tile-sub-title>Software Project</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn flat @click="menu = false">Cancel</v-btn>
            <v-btn color="primary" flat @click="menu = false">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </div>

    <template v-for="item in items">
      <v-list-tile
        :key="item.text"
        @click="redirect(item.link)"
        :class="currentRoute.name == item.name ? 'active': ''"
      >
        <v-tooltip right z-index="1000000">
          <v-list-tile-action slot="activator" class="pa-2">
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <span>{{ item.text }}</span>
        </v-tooltip>
        <v-list-tile-content>
          <v-list-tile-title>
            {{ item.text }}
          </v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </template>
    <div class="bottom-list">
      <v-btn
        v-if="mini_variant"
        icon
        @click.stop="unSetMiniVariant()"
      >
        <v-icon>chevron_right</v-icon>
      </v-btn>
      <v-btn
        v-else
        icon
        @click.stop="setMiniVariant()"
        style="margin-right: 20px;"
      >
        <v-icon>chevron_left</v-icon>
      </v-btn>
    </div>
  </v-list>
</template>

<script>
import request from '../../services/request.js';
import { mapstate, mapState } from 'vuex';

export default {
  props: {
    mini_variant: Boolean
  },
  data(){
    return {
      menu: false,
      message: false,
      hints: true,
      items: [
        {
          icon: "dashboard",
          text: "Dashboard",
          link: "/",
          name: "dashboard"
        },
        {
          icon: "developer_board",
          text: "Board",
        },
        {
          icon: "library_books",
          text: "Tasks",
          link: "/task/",
          name: "task"
        },
        {
          icon: "history",
          text: "Backlog"
        },
        {
          icon: "content_copy",
          text: "Duplicates"
        },
        {
          icon: "add",
          text: "Create Task",
        },
        { icon: "settings", text: "Settings" },
        { icon: "chat_bubble", text: "Send feedback" },
        { icon: "help", text: "Help" },
        { icon: "phonelink", text: "App downloads" },
        { icon: "keyboard", text: "Go to the old version" }
      ]
    }
  },
  methods: {
    redirect(to){
      return this.$router.push(to);
    },
    unSetMiniVariant(){
      this.$emit('unset-mini-variant');
    },
    setMiniVariant(){
      this.$emit('set-mini-variant');
    }
  },
  created(){
    request.get('project/')
    .then(response => {

    });
  },
  computed: {
    ...mapState([
      'currentRoute'
    ]),
  }
}
</script>

<style>
@media only screen and (min-width: 1201px) {
  /* v-navigation-drawer--mini-variant */
  .v-navigation-drawer--mini-variant .parent-list .v-list__group__header__prepend-icon {
    padding: 0 16px;
  }
  .parent-list .v-list__group__header__prepend-icon{
    padding-right: 9px;
    padding-left: 23px;
  }
}
.bottom-list {
  min-width: 48px;
  position: absolute;
  bottom: 10px;
  width: 100%;
  display: flex;
  justify-content: right;
}
.v-navigation-drawer--mini-variant .bottom-list {
  justify-content: center;
}
img.project_icon {
  width: 40px;
}
div.active, div.active i {
  color: #1565c0 !important;
  background: rgba(9, 30, 66, 0.04) !important;
}
.project-sidebar-item:hover {
  background: rgba(9, 30, 66, 0.04) !important;
}
.project-sidebar-item .v-menu.v-menu--inline {
  width: 100%;
}
</style>
