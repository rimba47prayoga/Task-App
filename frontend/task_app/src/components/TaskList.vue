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

      <v-flex xs3 pa-3 v-for="progress in tasks_progress" :key="progress.display">
        <v-card color="grey lighten-4" class="black--text mb-2">
          <task v-for="task in getData(progress.type)" :key="task.id" v-bind:task="task"></task>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</v-container>
</template>

<script>
import Task from "./Task";
import TaskProgress from "../constants/TaskProgress.js";
import TaskType from "../constants/TaskType.js";
import TaskPriority from "../constants/TaskPriority.js";
import request from "../services/request.js";

export default {
  components: {
    Task
  },
  data: () => {
    return {
      tasks: [
        // {
        //   id: 1,
        //   title: "Create Micro services for notifications",
        //   type: {
        //     name: TaskType.SUB_TASK,
        //     icon: "branding_watermark"
        //   },
        //   progress: TaskProgress.TODO,
        //   branch: "NAV-0001",
        //   priority: {
        //     type: TaskPriority.MEDIUM
        //   },
        //   description: "This is description a for task a"
        // },
        // {
        //   id: 2,
        //   title: "Task B",
        //   type: {
        //     name: TaskType.SUB_TASK,
        //     icon: "branding_watermark"
        //   },
        //   progress: TaskProgress.TODO,
        //   branch: "NAV-0002",
        //   priority: {
        //     type: TaskPriority.MEDIUM
        //   },
        //   description: "This is description a for task b"
        // }
      ],
      tasks_progress: TaskProgress.getProgressDisplay()
    };
  },
  methods: {
    getData(progress){
      return this.tasks.filter(task => {
        return task.progress == progress;
      });
    },
    setTaskType(type){
      var icon;
      switch(type){
        case TaskType.TASK:
          icon = null;
          break;
        case TaskType.SUB_TASK:
          icon = "branding_watermark";
          break;
        case TaskType.BUG:
          icon = null;
          break;
      };
      return {
        name: type,
        icon: icon
      }
    }
  },
  created(){
    request.get('/api/task/')
    .then(response => {
      let result = response.data
      result.map(data => {
        data.type = this.setTaskType(data.task_type);
      });
      this.tasks = result;
    })
  }
};
</script>

<style>
</style>
