<template>
    <v-layout row wrap>
      <v-flex xs3>
        <v-card color="blue-grey darken-2" class="white--text">
          <v-card-title primary-title>
            <div class="headline">{{ task.title }}</div>
            <div>{{ task.description }}</div>
          </v-card-title>
          <v-card-actions>
            <v-btn flat dark>Listen now</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
</template>

<script>
export default {
  props: {
    task: Object
  }
};
</script>

<style>
</style>
