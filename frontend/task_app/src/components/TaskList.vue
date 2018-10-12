<template>
<v-container ma-0 style="max-width: unset;">
  <v-container pa-0 style="max-width: unset;">
    <v-layout align-start justify-start row fill-height>
      <v-flex grey lighten-4 w-19 m-5px pa-2 br-3px v-for="progress in tasks_progress" :key="progress.type">
        <v-card color="grey lighten-4" class="black--text mb-2">
          <v-card-actions>
            {{ progress.display }}
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout align-content-space-between justify-start row fill-height>
      <!-- Loading component -->
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
        w-19 m-5px pa-2 no-box-shadow br-3px
        class="grey lighten-4"
      >
        <v-card
          class="black--text mb-2 bg-none"
          >
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
    <create-task ref="dialogCreateTask" v-on:created-task="reloadTask()"></create-task>
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
    },
    reloadTask(){
      this.isLoading = true;
      request.get('task/')
      .then(response => {
        this.tasks = response.data;
        this.isLoading = false;
      });
    }
  },
  created(){
    this.reloadTask();
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
.flex.w-19 {
  -ms-flex-preferred-size: 16.666666666666664%;
  flex-basis: 19%;
  -webkit-box-flex: 0;
  -ms-flex-positive: 0;
  flex-grow: 0;
  max-width: 19%;
}
.flex.m-5px {
  margin: 5px;
}
.flex.no-box-shadow {
  box-shadow: none;
}
.flex.no-box-shadow > div {
  box-shadow: none;
}
.br-3px {
  border-radius: 3px;
}
.bg-none.v-card.theme--light {
  background: none;
}
</style>
