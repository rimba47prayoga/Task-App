<template>
  <v-container ma-0 pa-0 style="max-width: unset;">
    <sub-header text="Dashboard" class="px-4 mt-2"></sub-header>
    <v-layout align-start justify-start row fill-height class="px-4 pt-2 ma-2">
        <v-flex xs6 class="mr-3">
          <v-card style="border-top: 5px solid #1565c0">
            <v-card-title class="pt-3 pb-0 pr-4 pl-4 ma-0">
              <div class="headline" style="font-size: 19px !important;font-weight: bold;">Introduction</div>
            <v-spacer></v-spacer>
              <v-icon @click.prevent>more_horiz</v-icon>
            </v-card-title>
            <v-card-title primary-title class="pb-1 pl-5 pr-5">
              <div class="headline">Welcome to Task App</div>
            </v-card-title>

            <v-card-actions class="pl-5 pr-5">
              <div>
                <img src="@/assets/task_icon.png" style="width: 70px" />
              </div>
            </v-card-actions>
            <v-card-actions class="pl-5 pr-5">
              <div>Lets create Project and manage your Task here</div>
            </v-card-actions>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn flat @click="redirect('/project/create-project')">
                Create Project
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>

        <v-flex xs6 class="ml-3">
          <v-card style="border-top: 5px solid #1565c0">
            <v-card-title class="pt-3 pb-0 pr-4 pl-4 ma-0">
              <div class="headline" style="font-size: 19px !important;font-weight: bold;">Assigned to Me</div>
            <v-spacer></v-spacer>
              <v-icon @click.prevent>more_horiz</v-icon>
            </v-card-title>

            <v-list style="font-size: 15px">
              <v-list-tile style="border-bottom: 1px solid #ddd" class="mb-2">
                <v-flex xs1 class="assignee-title">
                  T
                </v-flex>
                <v-flex xs2 class="assignee-title">
                  Branch
                </v-flex>
                <v-flex xs8 class="assignee-title">
                  Title
                </v-flex>
                <v-flex xs1 class="assignee-title">
                  P
                </v-flex>
              </v-list-tile>

              <v-list-tile
                v-for="task in tasks"
                :key="task.id"
                class="assignee-items-container"
              >
                <v-flex xs1 class="assignee-items">
                  <v-icon
                    style="font-size: 19px"
                    :class="task.task_type == 0
                    ? 'task'
                    : task.task_type == 1
                    ? 'sub-task'
                    : 'bug'"
                  >
                    {{ getTaskTypeIcon(task.task_type) }}
                  </v-icon>
                </v-flex>
                <v-flex xs2 class="assignee-items" style="font-size: 14px !important">
                  {{ task.branch_name }}
                </v-flex>
                <v-flex xs8 class="assignee-items">
                  {{ task.title }}
                </v-flex>
                <v-flex xs1>
                  <v-icon
                    :class="task.priority == '0'
                      ? 'assignee-items priority-lowest'
                      : task.priority == 1
                      ? 'assignee-items priority-low'
                      : task.priority == 2
                      ? 'assignee-items priority-medium'
                      : task.priority == 3
                      ? 'assignee-items priority-high'
                      : 'assignee-items priority-highest'"
                      style="font-size: 20px !important"
                  >
                    {{ getTaskPriorityIcon(task.priority) }}
                  </v-icon>
                </v-flex>
              </v-list-tile>
              <v-list-tile class="mt-3">
                <v-spacer></v-spacer>
                <v-pagination
                  v-model="pagination.current_page"
                  :length="pagination.total_pages"
                  circle
                ></v-pagination>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import SubHeader from './Widget/SubHeader';

import request from '../services/request.js';

import * as TaskUtils from "./Task/utils/task.js";
import { addQueryParam } from "../utils/common.js";

export default {
  components: {
    SubHeader
  },
  data(){
    return {
      tasks: [],
      pagination: {
        next: null,
        prev: null,
        total_pages: 0,
        current_page: 1
      }
    }
  },
  methods: {
    redirect(to){
      return request.redirect(to);
    },
    getTaskTypeIcon(task_type){
      return TaskUtils.getTaskTypeIcon(task_type);
    },
    getTaskPriorityIcon(priority){
      return TaskUtils.getTaskPriorityIcon(priority);
    },
    reloadTask(page){
      var url = 'task/list/dashboard';
      if (page){
        url = addQueryParam(url, {
          page: page
        })
      }
      request.get(url)
        .then(response => {
        this.tasks = response.data.results;
        this.pagination.next = response.data.next;
        this.pagination.prev = response.data.previous;
        this.pagination.total_pages = response.data.total_pages;
        this.pagination.current_page = response.data.current_page;
      })
    }
  },
  created(){
    this.reloadTask();
  },
  watch: {
    'pagination.current_page'(page){
      this.reloadTask(page);
    }
  }
}
</script>

<style>
.input-label {
  color: #5e6c84;
  font-weight: 500 !important;
}
.assignee-title {
  color: #5e6c84;
  font-weight: bold !important;
}
.assignee-items {
  color: #5e6c84;
  font-weight: 500 !important;
  font-size: 15px !important;
}
.v-pagination button {
  box-shadow: none !important;
}
.v-pagination button:not(.v-pagination__item--active):hover,
.assignee-items-container:hover {
  background-color: #ebecf0 !important;
}
</style>
