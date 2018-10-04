<template>
<v-container>
  <v-container>
    <v-layout row wrap>
      <v-flex xs3>
        <v-card color="blue-grey darken-2" class="white--text">
          <v-card-actions>
            TODO
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
  <v-container>
    <task v-for="task in tasks" :key="task.id" v-bind:task="task"></task>
  </v-container>
</v-container>
</template>

<script>
import Task from "./Task";
import TaskType from "./TaskType.js";

export default {
  components: {
    Task
  },
  data: () => {
    return {
      tasks: [
        {
          id: 1,
          title: "Task A",
          type: TaskType.TODO,
          description: "This is description a for task a"
        }
      ]
    };
  }
};
</script>

<style>
</style>
