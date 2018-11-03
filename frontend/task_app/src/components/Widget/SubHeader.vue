<template>
  <v-layout align-center justify-space-between row fill-height pa-0 ml-1 mr-1>
    <v-flex xs8 class="headline subheader-text">
      {{ text }}
    </v-flex>
    <slot></slot>
  </v-layout>
</template>

<script>
export default {
  props: {
    text: String
  }
}
</script>

<style>
.subheader-text {
  color: #616161 !important;
}
</style>
