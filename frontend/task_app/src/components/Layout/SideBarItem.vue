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
            <span>{{ selectedProject.name }}</span>
          </v-tooltip>
          <v-list-tile-content>
            <v-list-tile-title style="font-size:17px;">
              {{ selectedProject.name }}
            </v-list-tile-title>
            <span style="font-size: 12px; color: #616161;">{{ selectedProject.project_type }}</span>
          </v-list-tile-content>
        </v-list-tile>

        <v-card>
          <v-list v-for="project in projects" :key="project.id">
            <v-list-tile avatar>
              <v-list-tile-avatar>
                <img class="project_icon" src="@/assets/project_icon.png" />
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>{{ project.name }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ project.project_type }}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>

          <v-list>
            <v-list-tile avatar @click="redirect('/project/create-project')">
              <v-list-tile-avatar>
                <v-icon>add</v-icon>
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>Create Project</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-card>
      </v-menu>
    </div>

    <template v-for="item in items">
      <v-list-tile
        :key="item.text"
        @click="item.link
        ? redirect(item.link)
        : item.event ? item.event() : ''"
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
        id="set_mini_variant"
        @click.stop="setMiniVariant()"
        style="display: none;"
      >
      </v-btn>
    </div>
  </v-list>
</template>

<script>
import request from '../../services/request.js';
import { mapState } from 'vuex';
import ProjectType from '../../constants/ProjectType.js';

export default {
  props: {
    mini_variant: Boolean
  },
  data(){
    return {
      menu: false,
      message: false,
      hints: true,
      isCreateProject: false,
      projects: [],
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
          link: "/task/list",
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
          event: this.createTask
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
      return request.redirect(to);
    },
    setMiniVariant(){
      this.$emit('set-mini-variant');
    },
    createTask(){
      this.$store.commit(
        'showDialogCreateTask', true
      );
    }
  },
  created(){
    var projects = localStorage.getItem('projects')
    if (projects == null || !projects) {
      return;
    }
    projects = JSON.parse(projects);
    projects.map((item, index) => {
      item.project_type = ProjectType.getProjectDisplay(item.project_type);
    });
    this.projects = projects;
  },
  computed: {
    ...mapState([
      'currentRoute',
      'set_project'
    ]),
    selectedProject(){
      return this.$store.getters.selected_project || {
        name: 'Project Name',
        project_type: 'Software Project'
      }
    }
  },
  mounted(){
    let border = document.querySelector('aside .v-navigation-drawer__border');
    let btn_set = document.getElementById('set_mini_variant');
    border.addEventListener('click', () => {
      btn_set.click();
    })
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
