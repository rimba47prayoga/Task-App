<template>
  <v-list dense>
    <template v-for="item in items">
      <v-layout
        v-if="item.heading"
        :key="item.heading"
        row
        align-center
      >
        <v-flex xs6>
          <v-subheader v-if="item.heading">
            {{ item.heading }}
          </v-subheader>
        </v-flex>
        <v-flex xs6 class="text-xs-center">
          <a href="#!" class="body-2 black--text">EDIT</a>
        </v-flex>
      </v-layout>
      <v-list-group
        v-else-if="item.children"
        v-model="item.model"
        :key="item.text"
        :prepend-icon="item.model ? item.icon : item['icon-alt']"
        append-icon=""
        class="parent-list"
      >
        <v-list-tile slot="activator">
          <v-list-tile-content>
            <v-list-tile-title>
              {{ item.text }}
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          v-for="(child, i) in item.children"
          :key="i"
          @click.prevent
        >
          <v-list-tile-action v-if="child.icon" class="pa-2">
            <v-icon>{{ child.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              {{ child.text }}
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list-group>
      <v-list-tile v-else :key="item.text" @click="redirect(item.link)">
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
export default {
  props: {
    mini_variant: Boolean
  },
  data(){
    return {
      items: [
        {
          text: "Project"
        },
        {
          icon: "dashboard",
          text: "Dashboard",
          link: "/"
        },
        {
          icon: "developer_board",
          text: "Board",
        },
        {
          icon: "library_books",
          text: "Tasks",
          link: "/task/"
        },
        { icon: "history", text: "Frequently contacted" },
        { icon: "content_copy", text: "Duplicates" },
        {
          icon: "keyboard_arrow_up",
          "icon-alt": "keyboard_arrow_down",
          text: "Labels",
          model: true,
          // eslint-disable-next-line
          children: [
            { icon: "add", text: "Create label" }
          ]
        },
        {
          icon: "keyboard_arrow_up",
          "icon-alt": "keyboard_arrow_down",
          text: "More",
          model: false,
          children: [
            { text: "Import" },
            { text: "Export" },
            { text: "Print" },
            { text: "Undo changes" },
            { text: "Other contacts" }
          ]
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

</style>
