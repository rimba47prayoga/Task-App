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
        {{ $store.getters.selected_project.board_name }} Board /
        <div class="subheading">
          <v-icon class="ml-1 mr-1 white--text" style="font-size: 19px;">{{ task.task_type_icon }}</v-icon>
          {{ task.branch }}
        </div>
        <v-spacer></v-spacer>
        <v-btn icon depressed class="ma-0 mr-3" @click.prevent>
          <v-icon class="white--text">visibility</v-icon>
        </v-btn>
        <v-btn icon depressed class="ma-0" @click="closeDialog()">
          <v-icon class="white--text">clear</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text grid-list-sm class="pa-4" style="max-height: 700px">
        <v-layout>
          <v-flex xs8>
            <v-flex xs12 class="mb-3">
              <v-textarea
                slot="activator"
                auto-grow
                rows="1"
                v-model="task.title"
                placeholder=""
                flat
                solo
                hide-details
                class="input-hover textarea-title"
                style="font-size: 23px;font-weight: 500;"
              ></v-textarea>
            </v-flex>

            <v-flex xs12>
              <template v-if="quill.show">
                <quill-editor
                  ref="my-text"
                  v-model="descriptions"
                  :options="quill.editorOption"
                ></quill-editor>

                <div class="mt-2">
                  <v-btn
                    color="primary"
                    depressed
                    @click="editDescriptions()"
                    class="ml-0"
                    style="padding: 0 16px;min-width: 60px;border-radius: 3px;"
                  >
                      Save
                    </v-btn>
                  <v-btn flat @click="cancelEditDescriptions()" class="mr-0 ml-0">Cancel</v-btn>
                </div>
              </template>
              <div v-else
                @click="quill.show = true;"
                class="v-input input-hover v-text-field v-text-field--single-line v-text-field--solo v-text-field--solo-flat v-text-field--enclosed v-input--hide-details theme--light">
                <div class="v-input__control">
                  <div class="v-input__slot">
                    <div class="v-text-field__slot">
                      <label
                        v-if="!task.descriptions"
                        aria-hidden="true"
                        class="v-label theme--light"
                        style="left: 0px; right: auto; position: absolute;"
                      >
                        Add descriptions...
                      </label>
                      <template v-else>
                        <div style="width: 100%;height: 100%;" v-html="task.descriptions"></div>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </v-flex>
          </v-flex>

          <v-spacer></v-spacer>

          <v-flex xs3 class="mr-3">

            <!-- Assignee -->
            <v-flex xs12 class="my-3">
              <label class="input-label ml-2">Assignee</label>
              <v-flex xs12>
                <v-autocomplete
                  append-icon=""
                  v-model="task.assignee"
                  :items="assignee.items"
                  :loading="assignee.is_loading"
                  :search-input.sync="assignee.search"
                  hide-no-data
                  hide-details
                  item-text="username"
                  item-value="id"
                  placeholder="Assignee"
                  solo
                  flat
                  class="input-hover"
                  @change="editAssignee()"
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

            <!-- Deadline -->
            <v-flex xs12 class="my-3">
              <label class="input-label ml-2">
                Deadline
              </label>
              <v-menu
                ref="select_deadline"
                :close-on-content-click="false"
                v-model="deadline.menu"
                :nudge-right="40"
                :return-value.sync="task.deadline"
                lazy
                transition="fade-transition"
                offset-y
                full-width
                min-width="290px"
              >
                <v-text-field
                  slot="activator"
                  v-model="deadlineFormattedDate"
                  placeholder="Deadline date"
                  prepend-inner-icon="event"
                  readonly
                  flat
                  solo
                  hide-details
                  class="input-hover"
                ></v-text-field>
                <v-date-picker v-model="task.deadline" @input="$refs.select_deadline.save(task.deadline); editDeadline()"></v-date-picker>
              </v-menu>
            </v-flex>

            <!-- Task Type -->
            <v-flex xs12>
              <label class="input-label ml-2">
                Task Type
              </label>
              <v-flex xs12>
                <v-combobox
                  append-icon=""
                  v-model="task.task_type"
                  :items="task_type.items"
                  required
                  hide-no-data
                  hide-details
                  item-text="label"
                  item-value="type"
                  label="Task Type"
                  @change="editTaskType()"
                  solo
                  flat
                  class="input-hover"
                >

                  <!-- items that have been selected -->
                  <template
                    slot="selection"
                    slot-scope="{ item, selected }"
                  >
                    <v-icon
                    :class="item.type == 0
                    ? 'mr-2 task'
                    : item.type == 1
                    ? 'mr-2 sub-task'
                    : 'mr-2 bug'"
                    >{{ item.icon }}</v-icon>
                    {{ item.label }}
                  </template>

                  <!-- items in dropdown autocomplete -->
                  <template
                    slot="item"
                    slot-scope="{ item, tile }"
                  >
                    <v-icon
                    :class="item.type == 0
                    ? 'mr-2 task'
                    : item.type == 1
                    ? 'mr-2 sub-task'
                    : 'mr-2 bug'">{{ item.icon }}</v-icon>
                    <v-list-tile-content>
                      <v-list-tile-title v-text="item.label"></v-list-tile-title>
                    </v-list-tile-content>
                  </template>

                </v-combobox>
              </v-flex>
            </v-flex>

            <!-- Progress -->
            <v-flex xs12 class="my-3">
              <label class="input-label ml-2">
                Progress
              </label>
              <v-combobox
                v-model="task.progress"
                :items="progress.items"
                hide-no-data
                hide-details
                item-text="display"
                item-value="type"
                label="Progress"
                solo
                flat
                class="input-hover"
                prepend-icon=""
                append-icon=""
                @change="editProgress()"
              >

                <template
                  slot="selection"
                  slot-scope="{ item, selected }"
                >
                  <div :class="getClassProgress(item.type)">
                    {{ item.display }}
                  </div>
                </template>

                <template
                  slot="item"
                  slot-scope="{ item, tile }"
                >
                  <v-list-tile-content>
                    <div class="d-inline">
                      Move to
                      <v-icon>arrow_right_alt</v-icon>
                      <div
                        :class="getClassProgress(item.type) + ' d-inline'"
                      >
                        {{ item.display }}
                      </div>
                    </div>
                  </v-list-tile-content>
                </template>
              </v-combobox>
            </v-flex>

            <!-- Priority -->
            <v-flex xs12 class="my-3">
              <label class="input-label ml-2">
                Priority
              </label>
              <v-flex xs12>
                <v-combobox
                  append-icon=""
                  v-model="task.priority"
                  :items="priority.items"
                  required
                  hide-no-data
                  hide-details
                  item-text="label"
                  item-value="type"
                  placeholder="Priority"
                  solo
                  flat
                  class="input-hover"
                  @change="editPriority()"
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
                    <v-icon :class="item.type == '0'
                    ? 'mr-2 priority-lowest'
                    : item.type == 1
                    ? 'mr-2 priority-low'
                    : item.type == 2
                    ? 'mr-2 priority-medium'
                    : item.type == 3
                    ? 'mr-2 priority-high'
                    : 'mr-2 priority-highest'">{{ item.icon }}</v-icon>
                    {{ item.label }}
                  </template>

                  <!-- items in dropdown autocomplete -->
                  <template
                    slot="item"
                    slot-scope="{ item, tile }"
                  >
                    <v-icon
                    :class="item.type == '0'
                    ? 'mr-2 priority-lowest'
                    : item.type == 1
                    ? 'mr-2 priority-low'
                    : item.type == 2
                    ? 'mr-2 priority-medium'
                    : item.type == 3
                    ? 'mr-2 priority-high'
                    : 'mr-2 priority-highest'">{{ item.icon }}</v-icon>
                    <v-list-tile-content>
                      <v-list-tile-title v-text="item.label"></v-list-tile-title>
                    </v-list-tile-content>
                  </template>

                </v-combobox>
              </v-flex>
            </v-flex>

            <!-- Label -->
            <v-flex xs12 class="my-3">
              <label class="input-label ml-2">Label</label>
              <v-flex xs12>
                <v-text-field
                  v-model="task.label"
                  type="text"
                  prepend-icon=""
                  label="None"
                  solo
                  flat
                  hide-details
                  class="input-hover"
                ></v-text-field>
              </v-flex>
            </v-flex>

            <!-- Created By -->
            <v-flex xs12 class="my-3">
              <v-flex xs12>
                <label class="input-label ml-2">Created By</label>
                <div class="v-input__slot" style="line-height: 18px;font-size: 16px;margin-top: 10px; padding-bottom: 10px !important">
                  <div class="v-select__slot">
                    <div class="v-select__selections">
                      <v-icon color="primary" class="mr-2">account_circle</v-icon>
                      {{ task.created_by.username }}
                    </div>
                  </div>
                </div>
              </v-flex>
            </v-flex>

            <!-- Updated By -->
            <v-flex xs12 class="my-3">
              <v-flex xs12>
                <label class="input-label ml-2">Updated By</label>
                <div class="v-input__slot" style="line-height: 18px;font-size: 16px;margin-top: 10px; padding-bottom: 10px !important">
                  <div class="v-select__slot">
                    <div class="v-select__selections">
                      <template v-if="task.modified_by">
                        <v-icon color="primary" class="mr-2">event</v-icon>
                        {{ task.created_date }}
                      </template>
                      <div v-else class="none-value">
                        None
                      </div>
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
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor';

import request from "../../services/request.js";
import * as TaskUtils from "./utils/task.js";

import TaskProgress from '../../constants/TaskProgress.js';
import TaskPriority from '../../constants/TaskPriority.js';
import TaskType from '../../constants/TaskType.js';


export default {
  components: {
    quillEditor
  },
  props: {
    show: Boolean,
    id: Number
  },
  data(){
    return {
      show_dialog: false,
      task: {
        created_by: {
          username: null
        },
        descriptions: ''
      },
      descriptions: '',  // for quill editor
      task_type: {
        items: TaskType.getTaskTypeDisplay()
      },
      assignee: {
        items: [],
        is_loading: false,
        search: []
      },
      deadline: {
        formatDate: null,
        date: null,
        menu: false
      },
      progress: {
        items: TaskProgress.getProgressDisplay()
      },
      priority: {
        items: TaskPriority.getPriorityDisplay()
      },
      quill: {
        show: false,
        editorOption: {
          modules: {
            toolbar: [
              ['bold', 'italic', 'strike'],        // toggled buttons
              ['blockquote', 'code-block'],

              [{ 'list': 'ordered'}, { 'list': 'bullet' }],
              [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent

              [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown

              [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
              [{ 'align': [] }],

              ['clean'],                                         // remove formatting button
            ]
          }
        }
      }
    }
  },
  methods: {
    closeDialog(){
      this.show_dialog = false;
      this.$emit('close-dialog-detail');
    },
    getClassProgress(progress){
      let class_list = ['progress'];
      switch (progress) {
        case TaskProgress.TODO:
          class_list.push('progress-todo');
          break;
        case TaskProgress.IN_PROGRESS:
          class_list.push('progress-in-progress');
          break;
        case TaskProgress.IN_REPO:
          class_list.push('progress-in-repository');
          break;
        case TaskProgress.TEST:
          class_list.push('progress-test');
          break;
        case TaskProgress.DONE:
          class_list.push('progress-done');
          break;
      }
      return class_list.join(' ');
    },
    submitEdit(data){
      return request.patch(`task/list/${this.id}`, data)
    },
    editDescriptions(){
      this.submitEdit({
        descriptions: this.descriptions
      })
      .then(response => {
        this.task.descriptions = response.data.descriptions;
        this.quill.show = false;
      })
    },
    cancelEditDescriptions(){
      this.quill.show = false;
      this.descriptions = this.task.descriptions;
    },

    editTaskType(){
      this.submitEdit({
        task_type: this.task.task_type.type
      })
    },

    editAssignee(){
      this.submitEdit({
        assignee: this.task.assignee
      })
    },
    editDeadline(){
      this.submitEdit({
        deadline: this.task.deadline
      })
    },
    editProgress(){
      this.submitEdit({
        progress: this.task.progress.type
      })
      .then(response => {
        this.$emit('edit-task');
      })
    },
    editPriority(){
      this.submitEdit({
        priority: this.task.priority.type
      })
      .then(response => {
        this.$emit('edit-task');
      })
    }
  },
  watch: {
    show(val){
      if (val){
        request.get(`task/list/${this.id}`)
        .then(response => {
          let task = response.data;
          task.priority_icon = TaskUtils.getTaskPriorityIcon(task.priority);
          let format_deadline = task.deadline.split('/').reverse().join('-');
          task.deadline = format_deadline;
          task.task_type_icon = TaskUtils.getTaskTypeIcon(task.task_type);
          task.progress = TaskProgress.getProgressDisplay(task.progress);
          task.priority = TaskPriority.getPriorityDisplay(task.priority);
          task.task_type = TaskType.getTaskTypeDisplay(task.task_type);
          this.task = task;
          this.descriptions = task.descriptions;
          this.show_dialog = true;
        });

        request.get('task/list/assignee_task')
        .then(response => {
          this.assignee.items = response.data;
        });
      }
    }
  },
  computed: {
    deadlineFormattedDate(){
      return TaskUtils.FormatDate(this.task.deadline);
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
.none-value, .dialog-detail-task .v-label {
  color: rgb(137, 147, 164);
  font-weight: 500;
}
.progress {
  border-radius: 3px;
  box-sizing: border-box;
  padding: 3px 5px;
  font-size: 13px;
  font-weight: 700;
}
.progress-todo {
  background-color: rgb(223, 225, 230);
  color: rgb(66, 82, 110);
}
.progress-in-progress, .progress-in-repository {
  background-color: rgb(222, 235, 255);
  color: rgb(7, 71, 166);
}
.progress-test {
  background-color: #D1C4E9;
  color: #5E35B1;
}
.progress-done {
  background-color: rgb(227, 252, 239);
  color: rgb(0, 102, 68);
}

.ql-snow .ql-editor pre.ql-syntax, pre.ql-syntax {
  font-size: 12px;
  background: rgb(244, 245, 247) none repeat scroll 0% 0%;
  color: rgb(23, 43, 77);
  border-radius: 3px;
  display: inline;
  overflow-x: auto;
  padding: 2px 4px;
  transform: translate3d(0px, 0px, 0px);
}

.textarea-title textarea {
  line-height: 1.25em;
  margin: 0 !important;
}

.quill-editor {
  border: 1px solid rgb(223, 225, 230);
  border-radius: 4px;
}
.ql-toolbar.ql-snow, .ql-container.ql-snow {
  border: none !important;
}
.ql-container.ql-snow {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
