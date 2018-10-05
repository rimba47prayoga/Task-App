<template>
    <v-layout row wrap mb-2>
      <v-flex>
        <v-card>
          <v-card-title class="primary-title pa-2">
            <div class="subheading font-weight-normal">{{ task.title }}</div>
          </v-card-title>
          <v-card-actions>
            <v-icon class="task-type-icon" style="color:#64B5F6">branding_watermark</v-icon>
            <v-icon v-bind:class="class_priority">arrow_upward</v-icon>
          </v-card-actions>
          <v-card-actions>
            <v-icon class="task-user-icon mr-2" style="color:#1565c0 !important">account_circle</v-icon>
            <div class="grey--text">{{ task.branch }}</div>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
import TaskPriority from "../constants/TaskPriority.js";

export default {
  data() {
    return {
      class_priority: {
        "task-priority-icon": true,
        "priority-medium": this.task.priority.type == TaskPriority.MEDIUM,
        "priority-high": this.task.priority.type == TaskPriority.HIGH
      }
    }
  },
  props: {
    task: Object
  }
};
</script>

<style>
.font-weight-normal {
  font-weight: normal;
}
.task-user-icon{
  font-size: 32px;
}
.task-type-icon {
  font-size: 20px;
}
.task-priority-icon{
  font-size: 23px;
}
.priority-medium, .theme--light.priority-medium{
  color: #FB8C00;
}
</style>
