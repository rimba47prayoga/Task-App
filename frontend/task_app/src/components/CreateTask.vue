<template>

  <v-dialog
  :value="isCreatingTask"
  :persistent="true"
  :no-click-animation="true"
  :lazy="true"
  width="700px"
  >
    <v-card>
      <v-card-title
        class="blue darken-3 py-4 title white--text"
      >
      <v-icon class="ml-1 mr-3 white--text">playlist_add</v-icon>
        Create Task
      </v-card-title>
      <v-container grid-list-sm class="pa-4">
        <v-form
        v-model="valid"
        ref="formCreateTask"
        @submit.prevent.stop="submitForm($event)"
        lazy-validation
        >
          <v-layout row wrap>

            <!-- Title -->
            <v-flex xs12 align-center justify-space-between mb-1>
              <v-layout align-center>
                <v-text-field
                  v-model="title"
                  prepend-icon="short_text"
                  label="Title"
                  :rules="default_rules"
                  required
                ></v-text-field>
              </v-layout>
            </v-flex>

            <!-- Branch -->
            <v-flex xs3 mb-1>
              <v-select
                v-model="selected_prefix"
                :items="prefix_items"
                :rules="default_rules"
                label="Prefix"
                prepend-icon="share"
                required
              ></v-select>
            </v-flex>

            <v-flex xs2 mb-1>
              <v-text-field
                v-model="branch"
                disabled
                label="Branch"
                :rules="default_rules"
                required
              ></v-text-field>
            </v-flex>

            <!-- Task Type -->
              <v-flex xs5 mb-1>
                <v-autocomplete
                  v-model="selected_task_type"
                  :items="task_type"
                  :rules="default_rules"
                  required
                  hide-no-data
                  item-text="label"
                  item-value="type"
                  label="Task Type"
                  prepend-icon="null"
                  clearable
                  @change="changeTaskType"
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

            <!-- Sub Task -->
            <v-flex xs10 mb-1>
              <v-autocomplete
                v-if="typeIsSubTask"
                v-model="parent_task"
                :items="parent_task_items"
                :loading="isLoadingParentTask"
                :search-input.sync="search_parent_task"
                :rules="default_rules"
                required
                hide-no-data
                item-text="title"
                item-value="id"
                label="Parent Task"
                prepend-icon="assignment"
                return-object
                clearable
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

          <!-- Priority -->
            <v-flex xs5 mb-1>
              <v-autocomplete
                v-model="selected_priority"
                :items="priority_items"
                :rules="default_rules"
                required
                hide-no-data
                item-text="label"
                item-value="type"
                label="Priority"
                prepend-icon="null"
                clearable
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

          <!-- Assignee -->
            <v-flex xs5 mb-1>
              <v-autocomplete
                v-model="assignee_task"
                :items="assignee_items"
                :loading="isLoadingAssignee"
                :search-input.sync="search_assignee"
                hide-no-data
                item-text="username"
                item-value="id"
                label="Assignee"
                prepend-icon="null"
                clearable
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

            <!-- Label -->
            <v-flex xs10>
              <v-text-field
              v-model="label"
              type="text"
              prepend-icon="label"
              label="Label"
              ></v-text-field>
            </v-flex>

            <!-- Descriptions -->
            <v-flex xs12>
              <v-textarea
                v-model="descriptions"
                :auto-grow="true"
                row-height="14"
                name="input-7-4"
                label="Descriptions"
                prepend-icon="description"
              ></v-textarea>
            </v-flex>
          </v-layout>
          <input style="display:none;" type="submit" ref="submitButton" />
        </v-form>
      </v-container>
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
import {mapState} from "vuex";

import TaskType from "../constants/TaskType.js";
import TaskPriority from "../constants/TaskPriority.js";

import request from '../services/request.js';

export default {
  data(){
    return {
      valid: true, // model form

      default_rules: [
        v => !!v || "This field is required"
      ],

      prefix_items: [
        "NA"
      ],
      title: '',
      selected_prefix: null,
      selected_task_type: TaskType.TASK.toString(),
      selected_priority: TaskPriority.MEDIUM,
      priority_items: [
        {
          type: TaskPriority.LOWEST.toString(),
          label: "Lowest",
          icon: "arrow_downward",
        },
        {
          type: TaskPriority.LOW,
          label: "Low",
          icon: "arrow_downward",
        },
        {
          type: TaskPriority.MEDIUM,
          label: "Medium",
          icon: "arrow_upward",
        },
        {
          type: TaskPriority.HIGH,
          label: "High",
          icon: "arrow_upward",
        },
        {
          type: TaskPriority.HIGHEST,
          label: "Highest",
          icon: "arrow_upward",
        }
      ],
      branch: '',
      task_type: [
        {
          type: TaskType.TASK.toString(),
          label: "Task",
          icon: "check_box"
        },
        {
          type: TaskType.SUB_TASK.toString(),
          label: "Sub Task",
          icon: "branding_watermark"
        },
        {
          type: TaskType.BUG.toString(),
          label: "Bug",
          icon: "bug_report"
        }
      ],
      typeIsSubTask: false,
      isLoadingParentTask: false,
      parent_task: null,
      parent_task_items: [],
      search_parent_task: null,

      isLoadingAssignee: false,
      assignee_task: null,
      assignee_items: [],
      search_assignee: null,
      label: '',
      descriptions: ''
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
      this.title = '';
      this.assignee_task = '';
      this.label = '';
      this.descriptions = '';
    },
    triggerDialogShow(show){
      // TODO: or won't do: change vuex storage to component storage
      if(show){
        request.get('task/generate_branch')
        .then(response => {
          this.branch = response.data.branch;
        })
      }
    },
    submitForm(event){
      if(this.$refs.formCreateTask.validate()){
        if (event.explicitOriginalTarget.type != 'button'){
          return false;
        }
        let payload = {
          title: this.title,
          prefix_branch: this.selected_prefix,
          branch: this.branch,
          task_type: this.selected_task_type,
          priority: this.selected_priority,
          assignee: this.assignee_task,
          label: this.label,
          descriptions: this.descriptions
        }
        if (this.task_type == TaskType.SUB_TASK){
          payload.parent_task = this.parent_task;
        }

        request.post('task/', payload)
        .then(response => {
          this.closeDialogCreateTask();
          this.$emit('created-task');
        }).catch(err => {
          console.log(err);
        })
      }
    }
  },
  watch: {
    search_parent_task(val){
      if (this.parent_task_items.length) return;
      if (this.isLoadingParentTask) return;
      this.isLoadingParentTask = true;
      request.get('task/parent_task')
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
      request.get('task/assignee_task')
      .then(response => {
        this.assignee_items = response.data;
      })
      .finally(response => {
        this.isLoadingAssignee = false;
      })
    }
  },
  computed: {
    ...mapState([
      'isCreatingTask'
    ])
  }
}
</script>

<style>
.sub-task, .theme--light.sub-task,
.task, .theme--light.task {
  color:#64B5F6;
}
.bug, .theme--light.bug {
  color: #E53935;
}

.priority-lowest, .theme--light.priority-lowest {
  color: #66BB6A;
}
.priority-low, .theme--light.priority-low {
  color: #2E7D32;
}
.priority-medium, .theme--light.priority-medium {
  color: #F57C00;
}
.priority-high, .theme--light.priority-high {
  color: #E53935;
}
.priority-highest, .theme--light.priority-highest {
  color: #B71C1C;
}

.v-input__icon.v-input__icon--clear i{
  font-size: 15px;
}
</style>
