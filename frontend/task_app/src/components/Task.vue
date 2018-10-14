<template>
    <v-layout row wrap mb-6px>
      <v-flex>
        <v-hover>
          <v-card
            slot-scope="{ hover }"
            class="white-card"
            :data-taskid="task.id"
          >
            <v-tooltip right open-delay="800">
              <v-card-title class="primary-title pa-2" slot="activator">
                <div class="subheading font-weight-normal">{{ task.title }}</div>
              </v-card-title>
              <span>{{ task.title }}</span>
            </v-tooltip>
            <v-card-actions class="pa-0 pl-2 pr-2">
              <v-icon v-bind:class="class_task_type">{{ getTaskTypeIcon() }}</v-icon>
              <v-icon v-bind:class="class_priority">{{ getTaskPriorityIcon() }}</v-icon>
            </v-card-actions>
            <v-card-actions class="pa-0 pl-2 pr-2 pt-2">
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
        </v-hover>
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
  font-size: 30px;
  color:#1565c0 !important
}
.task-type-icon {
  font-size: 18px;
}
.task-priority-icon{
  font-size: 18px;
}
.priority-medium, .theme--light.priority-medium{
  color: #FB8C00;
}
.sub-task, .theme--light.sub-task {
  color:#64B5F6;
}
.white-card.v-card.theme--light {
  background: #ffffff !important;
  box-shadow: 0px 1px 2px 0px rgba(9, 30, 66, 0.25);
}
.v-card {
  border-radius: 3px;
}
.mb-6px {
  margin-bottom: 6px !important;
}
</style>
