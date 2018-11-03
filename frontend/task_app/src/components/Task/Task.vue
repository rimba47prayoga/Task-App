<template>
    <v-layout row wrap mb-6px>
      <v-flex>
        <v-hover>
          <v-card
            slot-scope="{ hover }"
            class="white-card"
            :data-taskid="task.id"
          >
            <v-card-title class="primary-title task-title">
              <div>{{ task.title }}</div>
            </v-card-title>
            <v-card-actions class="pa-0 pl-2 pr-2">
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
                class="task-user-icon mr-1"
                slot="activator"
                >account_circle
                </v-icon>
                <span>{{ task.assignee.username }}</span>
              </v-tooltip>
              <!-- TODO: handle it if user has avatar image -->

              <div class="task-branch">
                <router-link :to="{
                  name: 'task-detail',
                  params: {
                    slug: $store.getters.selected_project.slug,
                    branch: task.branch
                  }
                }">
                  {{ task.branch }}
                </router-link>
              </div>
              <v-spacer></v-spacer>
              {{ task.deadline }}
            </v-card-actions>
          </v-card>
        </v-hover>
      </v-flex>
    </v-layout>
</template>

<script>
import TaskPriority from "../../constants/TaskPriority.js";
import TaskType from "../../constants/TaskType.js";

import * as TaskUtils from "./utils/task.js";

export default {
  data() {
    return {
      class_priority: {
        "task-priority-icon": true,
        "priority-lowest": this.task.priority == TaskPriority.LOWEST,
        "priority-low": this.task.priority == TaskPriority.LOW,
        "priority-medium": this.task.priority == TaskPriority.MEDIUM,
        "priority-high": this.task.priority == TaskPriority.HIGH,
        "priority-highest": this.task.priority == TaskPriority.HIGHEST
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
      return TaskUtils.getTaskTypeIcon(this.task.task_type);
    },
    getTaskPriorityIcon(){
      return TaskUtils.getTaskPriorityIcon(this.task.priority);
    }
  }
}
</script>

<style>
@media only screen and (max-width: 1200px) {
  .task-title {
    font-size: 14px !important;
    line-height: 1.42857143;
    max-height: 4.28571429em;
  }
}
.task-title {
  color: #172B4D !important;
  font-size: 15px;
  font-weight: 400;
  display: block;
  box-sizing: content-box;
  line-height: 1.4857143;
  max-height: 4em;
  overflow: hidden;
  padding: 10px !important;
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
/* .priority-medium, .theme--light.priority-medium{
  color: #FB8C00;
} */
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
.sub-task, .theme--light.sub-task {
  color:#64B5F6;
}
.white-card.v-card.theme--light {
  background: #ffffff !important;
  box-shadow: 0px 1px 2px 0px rgba(9, 30, 66, 0.25);
}
.v-card {
  border-radius: 2px;
}
.mb-6px {
  margin-bottom: 6px !important;
}
.task-branch a {
  color: #5E6C84;
  font-weight: 500;
  font-size: 15px;
  text-decoration: none;
}
.task-branch a:hover{
  text-decoration: underline;
}
</style>
