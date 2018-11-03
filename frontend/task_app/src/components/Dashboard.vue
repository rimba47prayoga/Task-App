<template>
  <v-container ma-2>
  <v-layout align-start justify-start row fill-height>
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
            <div class="headline" style="font-size: 19px !important;font-weight: bold;">Assigned to me</div>
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
  </v-layout>
  </v-container>
</template>

<script>
import request from '../services/request.js';

export default {
  methods: {
    redirect(to){
      return request.redirect(to);
    }
  }
}
</script>

<style>

</style>
