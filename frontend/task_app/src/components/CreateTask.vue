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
      <v-container grid-list-sm class="scroll-y pa-4" id="scroll-target">
        <v-form
        v-scroll:#scroll-target=""
        v-model="valid"
        ref="formCreateTask"
        @submit.prevent.stop="submitForm($event)"
        lazy-validation
        class="create-task-form"
        >
          <v-layout row wrap>

            <!-- Title -->
            <v-flex xs12>
              <label class="input-label">
                Title
                <span class="required">*</span>
              </label>
              <v-flex xs10>
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

            <!-- Task Type -->
            <v-flex xs12>
              <label class="input-label">
                Task Type
                <span class="required">*</span>
              </label>
              <v-flex xs5>
                <v-autocomplete
                  v-model="selected_task_type"
                  :items="task_type"
                  :rules="default_rules"
                  required
                  hide-no-data
                  item-text="label"
                  item-value="type"
                  placeholder="Task Type"
                  clearable
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
          <!-- Priority -->
          <v-flex xs12>
            <label class="input-label">
              Priority
              <span class="required">*</span>
            </label>
            <v-flex xs5>
              <v-autocomplete
                v-model="selected_priority"
                :items="priority_items"
                :rules="default_rules"
                required
                hide-no-data
                item-text="label"
                item-value="type"
                placeholder="Priority"
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
            <v-flex xs5>
              <v-autocomplete
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
          <!-- Sub Task -->
          <v-flex xs12 v-if="typeIsSubTask">
            <label class="input-label">
              Parent Task
              <span class="required">*</span>
            </label>
            <v-flex xs10>
              <v-autocomplete
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
              label="Label"
              solo
              flat
              ></v-text-field>
            </v-flex>
          </v-flex>
            <!-- Descriptions -->
          <v-flex xs12>
            <label class="input-label">Descriptions</label>
            <v-flex xs10>
              <v-textarea
                v-model="descriptions"
                :auto-grow="true"
                row-height="14"
                name="input-7-4"
                label="Descriptions"
                prepend-inner-icon="description"
                solo
                flat
              ></v-textarea>
            </v-flex>
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
  transition: border-color .15s ease-in-out,-webkit-box-shadow .15s ease-in-out;
  transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
  transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out,-webkit-box-shadow .15s ease-in-out;
  width: 100%;
}

form.create-task-form .v-text-field--solo .v-input__slot {
  background-color: #F4F5F7 !important;
  border: 1px solid #e4e7ea;
  min-height: 42px;
}

form.create-task-form .v-text-field__details {
  margin: 0 !important;
}

label.input-label {
  color: #5e6c84;
  font-weight: bold;
  margin-left: 1px;
}
span.required {
  color: #ff5252;
}
</style>
