<template>
    <v-layout row wrap mb-2>
      <v-flex>
        <v-card>
          <v-card-title class="primary-title pa-2">
            <div class="subheading font-weight-normal">{{ task.title }}</div>
          </v-card-title>
          <v-card-actions>
            <v-icon v-bind:class="class_task_type">{{ getTaskTypeIcon() }}</v-icon>
            <v-icon v-bind:class="class_priority">{{ getTaskPriorityIcon() }}</v-icon>
          </v-card-actions>
          <v-card-actions>
            <v-tooltip
            v-if="task.assignee != null"
            bottom
            >
              <v-icon
              v-if="task.assignee.avatar == null"
              class="task-user-icon mr-2"
              slot="activator"
              >account_circle
              </v-icon>
              <span>{{ task.assignee.username }}</span>
            </v-tooltip>
            <!-- TODO: handle it if user has avatar image -->

            <div class="grey--text">{{ task.prefix_branch + '-' + task.branch }}</div>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
import TaskPriority from "../constants/TaskPriority.js";
import TaskType from "../constants/TaskType.js";

export default {
  data() {
    return {
      class_priority: {
        "task-priority-icon": true,
        "priority-medium": this.task.priority == TaskPriority.MEDIUM,
        "priority-high": this.task.priority == TaskPriority.HIGH
      },
      class_task_type: {
        "task-type-icon": true,
        "task": this.task.task_type == TaskType.TASK,
        "sub-task": this.task.task_type == TaskType.SUB_TASK,
        "bug": this.task.task_type == TaskType.BUG
      }
    }
  },
  props: {
    task: Object
  },
  methods: {
    getTaskTypeIcon(){
      let icon;
      switch(this.task.task_type){
        case TaskType.TASK:
          icon = "check_box";
          break;
        case TaskType.SUB_TASK:
          icon = "branding_watermark";
          break;
        case TaskType.BUG:
          icon = "bug_report";
          break;
      };
      return icon;
    },
    getTaskPriorityIcon(){
      let icon;
      switch(this.task.priority){
        case TaskPriority.LOWEST:
        case TaskPriority.LOW:
          icon = "arrow_downward";
          break;
        case TaskPriority.MEDIUM:
        case TaskPriority.HIGH:
        case TaskPriority.HIGHEST:
        icon = "arrow_upward"
      };
      return icon;
    }
  }
}
</script>

<style>
.font-weight-normal {
  font-weight: normal;
}
.task-user-icon, .theme--light.task-user-icon{
  font-size: 32px;
  color:#1565c0 !important
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
.sub-task, .theme--light.sub-task {
  color:#64B5F6;
}
</style>
