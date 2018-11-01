<template>
  <v-dialog
    v-model="show_dialog"
    :persistent="true"
    :no-click-animation="true"
    :lazy="true"
    max-width="950px"
    scrollable
  >
    <v-card class="dialog-detail-task">
      <v-card-title
        class="blue darken-3 py-3 title white--text mb-2"
      >
        <v-icon class="ml-1 mr-3 white--text">{{ task.task_type_icon }}</v-icon>
        {{ task.branch }}
        <v-spacer></v-spacer>
        <v-btn icon depressed class="ma-0" @click="closeDialog()">
          <v-icon class="white--text">clear</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text grid-list-sm class="pa-4" style="max-height: 500px">
        <v-layout>
          <v-flex xs8>
            <div class="title input-hover px-2 py-3">
              {{ task.title }}
            </div>
          </v-flex>
          <v-spacer></v-spacer>
          <v-flex xs3 class="mr-2">
            <v-flex xs12>
              <label class="input-label ml-2">Assignee</label>
              <v-flex xs12>
                <v-autocomplete
                  append-icon=""
                  v-model="task.assignee"
                  :items="assignee.items"
                  :loading="assignee.is_loading"
                  :search-input.sync="assignee.search"
                  hide-no-data
                  item-text="username"
                  item-value="id"
                  placeholder="Assignee"
                  solo
                  flat
                  class="input-hover"
                >
                  <template slot="no-data">
                    <v-list-tile>
                      <v-list-tile-title>
                        Search for your favorite
                        <strong>Cryptocurrency</strong>
                      </v-list-tile-title>
                    </v-list-tile>
                  </template>

                  <!-- items that have been selected -->
                  <template
                    slot="selection"
                    slot-scope="{ item, selected }"
                  >
                    <!-- TODO: display status user : check if user is assigneeble (not bussy) -->
                    <v-icon
                    v-if="item.avatar == null"
                    class="mr-2"
                    style="color: #1565c0 !important"
                    >account_circle</v-icon>
                    {{ item.username }}
                  </template>

                  <!-- items in dropdown autocomplete -->
                  <template
                    slot="item"
                    slot-scope="{ item, tile }"
                  >
                    <v-icon
                    v-if="item.avatar == null"
                    class="mr-2"
                    style="color:#1565c0 !important">account_circle</v-icon>
                    <v-list-tile-content>
                      <v-list-tile-title v-text="item.username"></v-list-tile-title>
                    </v-list-tile-content>
                  </template>
                </v-autocomplete>
              </v-flex>
            </v-flex>
            <v-flex xs12>
              <v-flex xs12>
                <label class="input-label ml-2">Created By</label>
                <div class="v-input__slot" style="line-height: 18px;font-size: 16px;margin-top: 10px;">
                  <div class="v-select__slot">
                    <div class="v-select__selections">
                      <v-icon color="primary" class="mr-2">account_circle</v-icon>
                      {{ task.created_by.username }}
                    </div>
                  </div>
                </div>
              </v-flex>
            </v-flex>
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import request from "../../services/request.js";
import * as TaskUtils from "./utils/task.js";


export default {
  props: {
    show: Boolean,
    id: Number
  },
  data(){
    return {
      show_dialog: false,
      task: {},
      assignee: {
        items: [],
        is_loading: false,
        search: []
      }
    }
  },
  methods: {
    closeDialog(){
      this.show_dialog = false;
      this.$emit('close-dialog-detail');
    }
  },
  watch: {
    show(val){
      if (val){
        request.get(`task/list/${this.id}`)
        .then(response => {
          let task = response.data;
          task.priority_icon = TaskUtils.getTaskPriorityIcon(task.priority);
          task.task_type_icon = TaskUtils.getTaskTypeIcon(task.task_type);
          this.task = task;
          this.show_dialog = true;
        });

        request.get('task/list/assignee_task')
        .then(response => {
          this.assignee.items = response.data;
        });
      }
    }
  }
}
</script>

<style>
.dialog-detail-task .v-input__slot {
  padding: 0 7px !important;
}
.input-hover {
  -webkit-transition: background .5s cubic-bezier(.25,.8,.5,1);
  transition: background .5s cubic-bezier(.25,.8,.5,1);
}
.input-hover .v-input__slot:hover, .title.input-hover:hover {
  background-color: #ebecf0 !important;
}
</style>
