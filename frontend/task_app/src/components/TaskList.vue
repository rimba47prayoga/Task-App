<template>
<v-progress-circular
    v-if="isLoading"
    :size="60"
    :width="7"
    color="primary"
    indeterminate
    class="center-content"
  ></v-progress-circular>
<v-container ma-0 v-else>
  <v-container pa-0>
    <v-layout row wrap>
      <v-flex grey lighten-4 xs3 pa-3 v-for="progress in tasks_progress" :key="progress.type">
        <v-card color="grey lighten-4" class="black--text mb-2">
          <v-card-actions>
            {{ progress.display }}
          </v-card-actions>
        </v-card>
      </v-flex>

      <v-flex xs3 pa-3 v-for="progress in tasks_progress" :key="progress.display">
        <v-card color="grey lighten-4" class="black--text mb-2">
          <task v-for="task in filterData(progress.type)" :key="task.id" v-bind:task="task"></task>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
  <v-tooltip top lazy open-delay="800">
  <v-btn
    fab
    bottom
    right
    color="pink"
    dark
    fixed
    class="pa-3"
    @click="showDialogCreateTask()"
    slot="activator"
    >
      <v-icon>add</v-icon>
    </v-btn>
    <span>Create Task</span>
  </v-tooltip>
    <create-task></create-task>
</v-container>
</template>

<script>
// components
import Task from "./Task";
import CreateTask from "./CreateTask";

// constants
import TaskProgress from "../constants/TaskProgress.js";
import TaskType from "../constants/TaskType.js";
import TaskPriority from "../constants/TaskPriority.js";

// services & utils
import request from "../services/request.js";
import apiUrl from "../utils/api-urls.js";

export default {
  components: {
    Task,
    CreateTask
  },
  data: () => {
    return {
      isLoading: false,
      tasks: [],
      tasks_progress: TaskProgress.getProgressDisplay()
    };
  },
  methods: {
    /** filter task by progress type --> TODO, IN Progress, etc ..
     * @param {number} progress
     */
    filterData(progress){
      return this.tasks.filter(task => {
        return task.progress == progress;
      });
    },
    showDialogCreateTask(){
      this.$store.commit(
        'showDialogCreateTask',
        !this.$store.getters.isCreatingTask
      )
    }
  },
  created(){
    this.isLoading = true;
    request.get(apiUrl() + 'task/')
    .then(response => {
      this.tasks = response.data;
      this.isLoading = false;
    })
  }
};
</script>

<style>
.center-content{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
