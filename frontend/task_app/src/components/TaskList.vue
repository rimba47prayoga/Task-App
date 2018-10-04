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
import TaskProgress from "./TaskProgress.js";

export default {
  components: {
    Task
  },
  data: () => {
    return {
      tasks: [
        {
          id: 1,
          title: "Create Micro services for notifications",
          type: TaskProgress.TODO,
          branch: "NAV-0001",
          description: "This is description a for task a"
        },
        {
          id: 2,
          title: "Task B",
          type: TaskProgress.TODO,
          branch: "NAV-0002",
          description: "This is description a for task b"
        }
      ],
      tasks_progress: TaskProgress.getProgressDisplay()
    };
  },
  methods: {
    getData(type){
      return this.tasks.filter(task => {
        return task.type == type;
      });
    }
  }
};
</script>

<style>
</style>
