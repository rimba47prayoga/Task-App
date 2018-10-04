<template>
    <v-layout row wrap mb-2>
      <v-flex>
        <v-card>
          <v-card-title class="primary-title pa-2">
            <div class="subheading font-weight-normal">{{ task.title }}</div>
          </v-card-title>
          <v-card-actions>
            <v-icon style="color:#64B5F6">branding_watermark</v-icon>
          </v-card-actions>
          <v-card-actions>
            <div class="grey--text">{{ task.branch }}</div>
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
.font-weight-normal {
  font-weight: normal;
}
</style>
