<template>
<v-container ma-0>
  <v-container pa-0>
    <v-layout row wrap>
      <v-flex grey lighten-4 xs3 pa-3 v-for="progress in tasks_progress" :key="progress.type">
        <v-card color="grey lighten-4" class="black--text mb-2">
          <v-card-actions>
            {{ progress.display }}
          </v-card-actions>
        </v-card>
      </v-flex>

      <v-flex xs12 v-if="isLoading">
        <v-progress-circular
          :size="60"
          :width="7"
          color="primary"
          indeterminate
          class="center-content"
        ></v-progress-circular>
      </v-flex>

      <v-flex
        v-else
        v-for="progress in tasks_progress"
        :key="progress.display"
        xs3 pa-3
      >
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
    <create-task ref="dialogCreateTask"></create-task>
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
      // Trigger dialog show
      this.$refs.dialogCreateTask.triggerDialogShow(
        true
      );
    }
  },
  created(){
    this.isLoading = true;
    request.get('task/')
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
