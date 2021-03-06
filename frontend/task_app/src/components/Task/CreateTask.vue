<template>

  <v-dialog
    :value="isCreatingTask"
    :persistent="true"
    :no-click-animation="true"
    :lazy="true"
    max-width="800px"
    scrollable
  >
    <v-card>
      <v-card-title
        class="blue darken-3 py-4 title white--text"
      >
      <v-icon class="ml-1 mr-3 white--text">playlist_add</v-icon>
        Create Task
      </v-card-title>
      <v-card-text grid-list-sm class="pa-4" style="max-height: 500px">
        <v-form
          v-model="valid"
          ref="formCreateTask"
          @submit.prevent.stop="submitForm($event)"
          lazy-validation
          class="create-task-form"
        >
        <v-layout row wrap>
          <!-- Project -->
          <v-flex xs11>
            <label class="input-label">
              Project
              <span class="required">*</span>
            </label>
            <v-flex xs4>
              <v-autocomplete
                append-icon="expand_more"
                v-model="selected_project"
                :items="project_items"
                :rules="default_rules"
                required
                hide-no-data
                item-text="name"
                item-value="id"
                placeholder="Project"
                solo
                flat
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
                  <img class="mr-1" style="width: 20px;" src="@/assets/project_icon.png" />
                  {{ item.name + ' (' + item.board_name + ')' }}
                </template>

                <!-- items in dropdown autocomplete -->
                <template
                  slot="item"
                  slot-scope="{ item, tile }"
                >
                  <img class="mr-1" style="width: 20px;" src="@/assets/project_icon.png" />
                  <v-list-tile-content>
                    <v-list-tile-title
                    v-text="item.name + ' (' + item.board_name + ')'"
                    ></v-list-tile-title>
                  </v-list-tile-content>
                </template>

              </v-autocomplete>
            </v-flex>
          </v-flex>

          <!-- Task Type -->
          <v-flex xs11 style="border-bottom: 1px solid #ddd;" class="mb-3">
            <label class="input-label">
              Task Type
              <span class="required">*</span>
            </label>
            <v-flex xs4>
              <v-autocomplete
                append-icon="expand_more"
                v-model="selected_task_type"
                :items="task_type"
                :rules="default_rules"
                required
                hide-no-data
                item-text="label"
                item-value="type"
                placeholder="Task Type"
                @change="changeTaskType"
                solo
                flat
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
                  <v-icon
                  :class="item.type == '0'
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
                  :class="item.type == '0'
                  ? 'mr-2 task'
                  : item.type == 1
                  ? 'mr-2 sub-task'
                  : 'mr-2 bug'">{{ item.icon }}</v-icon>
                  <v-list-tile-content>
                    <v-list-tile-title v-text="item.label"></v-list-tile-title>
                  </v-list-tile-content>
                </template>

              </v-autocomplete>
            </v-flex>
          </v-flex>

          <!-- Title -->
          <v-flex xs12>
            <label class="input-label">
              Title
              <span class="required">*</span>
            </label>
            <v-flex xs11>
              <v-layout align-center>
                <v-text-field
                  v-model="title"
                  prepend-inner-icon="short_text"
                  placeholder="Title"
                  :rules="default_rules"
                  required
                  solo
                  flat
                ></v-text-field>
              </v-layout>
            </v-flex>
          </v-flex>

          <!-- Descriptions -->
          <v-flex xs12>
            <label class="input-label">Descriptions</label>
            <v-flex xs11 class="mt-1">
              <quill-editor
                ref="my-text"
                v-model="descriptions"
                :options="quill.editorOption"
              ></quill-editor>
            </v-flex>
          </v-flex>

          <!-- Priority -->
          <v-flex xs12 class="mt-4">
            <label class="input-label">
              Priority
              <span class="required">*</span>
            </label>
            <v-flex xs4>
              <v-autocomplete
                append-icon="expand_more"
                v-model="selected_priority"
                :items="priority_items"
                :rules="default_rules"
                required
                hide-no-data
                item-text="label"
                item-value="type"
                placeholder="Priority"
                solo
                flat
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

              </v-autocomplete>
            </v-flex>
          </v-flex>

          <!-- Assignee -->
          <v-flex xs12>
            <label class="input-label">Assignee</label>
            <v-flex xs4>
              <v-autocomplete
                append-icon="expand_more"
                v-model="assignee_task"
                :items="assignee_items"
                :loading="isLoadingAssignee"
                :search-input.sync="search_assignee"
                hide-no-data
                item-text="username"
                item-value="id"
                placeholder="Assignee"
                clearable
                solo
                flat
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
          <v-flex xs12 sm6 md4>
            <label class="input-label">
              Deadline
              <span class="required">*</span>
            </label>
            <v-menu
              ref="select_deadline"
              :close-on-content-click="false"
              v-model="select_deadline"
              :nudge-right="40"
              :return-value.sync="deadline"
              lazy
              transition="fade-transition"
              offset-y
              full-width
              min-width="290px"
            >
              <v-text-field
                :rules="default_rules"
                slot="activator"
                v-model="formattedDate"
                placeholder="Deadline date"
                prepend-inner-icon="event"
                readonly
                flat
                solo
              ></v-text-field>
              <v-date-picker v-model="deadline" @input="$refs.select_deadline.save(deadline)"></v-date-picker>
            </v-menu>
          </v-flex>
          <!-- Sub Task -->
          <v-flex xs12 v-if="typeIsSubTask">
            <label class="input-label">
              Parent Task
              <span class="required">*</span>
            </label>
            <v-flex xs10>
              <v-autocomplete
                append-icon="expand_more"
                v-model="parent_task"
                :items="parent_task_items"
                :loading="isLoadingParentTask"
                :search-input.sync="search_parent_task"
                :rules="default_rules"
                required
                hide-no-data
                item-text="title"
                item-value="id"
                placeholder="Parent Task"
                prepend-inner-icon="assignment"
                clearable
                solo
                flat
              >
                <template slot="no-data">
                  <v-list-tile>
                    <v-list-tile-title>
                      Search for your favorite
                      <strong>Cryptocurrency</strong>
                    </v-list-tile-title>
                  </v-list-tile>
                </template>
                <template
                  slot="selection"
                  slot-scope="{ item, selected }"
                >
                  <v-chip
                    color="blue-grey"
                    class="white--text"
                  >
                    <v-icon left>mdi-coin</v-icon>
                    <span v-text="item.prefix_branch + '-' + item.branch"></span>
                  </v-chip>
                  {{ item.title }}
                </template>
                <template
                  slot="item"
                  slot-scope="{ item, tile }"
                >
                  <v-chip
                    color="blue-grey"
                    class="white--text"
                  >
                    <span v-text="item.prefix_branch + '-' + item.branch"></span>
                  </v-chip>
                  <v-list-tile-content>
                    <v-list-tile-title v-text="item.title"></v-list-tile-title>
                  </v-list-tile-content>
                  <v-list-tile-action>
                    <v-icon>mdi-coin</v-icon>
                  </v-list-tile-action>
                </template>
              </v-autocomplete>
            </v-flex>
          </v-flex>
            <!-- Label -->
          <v-flex xs12>
            <label class="input-label">Label</label>
            <v-flex xs10>
              <v-text-field
              v-model="label"
              type="text"
              prepend-inner-icon="label"
              placeholder="Label"
              solo
              flat
              ></v-text-field>
            </v-flex>
          </v-flex>
          </v-layout>
          <input style="display:none;" type="submit" ref="submitButton" />
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="pa-3">
        <v-btn flat color="primary">More</v-btn>
        <v-spacer></v-spacer>
        <v-btn flat color="primary" @click="closeDialogCreateTask">Cancel</v-btn>
        <v-btn flat @click="$refs.submitButton.click()">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor';

import { mapState } from "vuex";
import { EventBus } from '../../event-bus.js';

import TaskType from "../../constants/TaskType.js";
import TaskPriority from "../../constants/TaskPriority.js";

import request from '../../services/request.js';

export default {
  components: {
    quillEditor
  },
  data(){
    return {
      valid: true, // model form

      default_rules: [
        v => {
          v = v.toString();
          return !!v || "This field is required"
        }
      ],
      selected_project: null,
      project_items: [],
      title: '',
      selected_task_type: TaskType.TASK.toString(),
      selected_priority: TaskPriority.MEDIUM,
      priority_items: TaskPriority.getPriorityDisplay(),
      task_type: TaskType.getTaskTypeDisplay(),
      typeIsSubTask: false,
      isLoadingParentTask: false,
      parent_task: null,
      parent_task_items: [],
      search_parent_task: null,

      isLoadingAssignee: false,
      assignee_task: null,
      assignee_items: [],
      search_assignee: null,

      deadline: null,
      select_deadline: false,
      label: '',
      descriptions: '',
      quill: {
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
    closeDialogCreateTask(){
      this.$store.commit(
        'showDialogCreateTask',
        false
      );
      this.clearForm();
    },
    changeTaskType(value){
      if (typeof value != "undefined" && value == TaskType.SUB_TASK){
        this.typeIsSubTask = true;
        this.parent_task = null;
        this.parent_task_items = [];
      } else {
        this.typeIsSubTask = false;
      }
    },
    clearForm(){
      this.$refs.formCreateTask.reset();
    },
    submitForm(event){
      if(this.$refs.formCreateTask.validate()){
        console.log(event)
        if (event.explicitOriginalTarget.type != 'button'){
          return false;
        }
        let payload = {
          project: this.selected_project,
          title: this.title,
          prefix_branch: this.selected_prefix,
          branch: this.branch,
          task_type: this.selected_task_type,
          priority: this.selected_priority,
          assignee: this.assignee_task,
          label: this.label,
          deadline: this.deadline,
          descriptions: this.descriptions
        }
        if (this.task_type == TaskType.SUB_TASK){
          payload.parent_task = this.parent_task;
        }

        request.post('task/list', payload)
        .then(response => {
          this.closeDialogCreateTask();
          EventBus.$emit('created-task');
        }).catch(err => {
          console.log(err);
        })
      }
    },
    formatDate(date){
      if (!date) return;
      let [year, month, day] = date.split('-');
      return `${day}/${month}/${year}`;
    }
  },
  watch: {
    search_parent_task(val){
      if (this.parent_task_items.length) return;
      if (this.isLoadingParentTask) return;
      this.isLoadingParentTask = true;
      request.get('task/list/parent_task')
      .then(response => {
        this.parent_task_items = response.data;
      })
      .finally(response => {
        this.isLoadingParentTask = false;
      })
    },
    search_assignee(val){
      if (this.assignee_items.length || this.isLoadingAssignee) return;
      this.isLoadingAssignee = true;
      request.get('task/list/assignee_task')
      .then(response => {
        this.assignee_items = response.data;
      })
      .finally(response => {
        this.isLoadingAssignee = false;
      })
    },
    isCreatingTask(val){
      if (val){
        var projects = localStorage.getItem('projects');
        if (projects == null || projects == "[]"){
          return;
        }
        projects = JSON.parse(projects);
        this.project_items = projects;
        this.selected_project = this.$store.getters.selected_project.id;
        this.selected_task_type = TaskType.TASK.toString(),
        this.selected_priority = TaskPriority.MEDIUM
      }
    }
  },
  computed: {
    ...mapState([
      'isCreatingTask'
    ]),
    formattedDate(){
      return this.formatDate(this.deadline);
    }
  }
}
</script>

<style>
.v-input__icon.v-input__icon--clear i{
  font-size: 15px;
}

.form-control {
  -webkit-transition: border-color .15s ease-in-out,-webkit-box-shadow .15s ease-in-out;
  background-clip: padding-box;
  background-color: #F4F5F7 !important;
  border: 1px solid #e4e7ea;
  border-radius: .25rem;
  color: #5c6873;
  display: block;
  font-size: .9rem;
  height: calc(2.2625rem + 2px);
  /* line-height: 1.5; */
  padding: .375rem .75rem;
  width: 100%;
}

form.create-task-form .v-text-field--solo .v-input__slot {
  background-color: #F4F5F7 !important;
  border: 1px solid #e4e7ea;
  min-height: 39px;
  transition: .05s ease-in-out;
}
form.create-task-form .v-text-field--solo .v-input__slot:hover {
  background-color: #ebecf0 !important;
}
</style>
