<template>
  <v-dialog :value="isCreatingTask" width="800px">
    <v-card>
      <v-card-title
        class="grey lighten-4 py-4 title"
      >
        Create contact
      </v-card-title>
      <v-container grid-list-sm class="pa-4">
        <v-layout row wrap>
          <v-flex xs12 align-center justify-space-between>
            <v-layout align-center>
              <v-text-field
                placeholder="Name"
                prepend-icon="account_circle"
              ></v-text-field>
            </v-layout>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              prepend-icon="business"
              placeholder="Company"
            ></v-text-field>
          </v-flex>
          <v-flex xs6>
            <v-text-field
              placeholder="Job title"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              prepend-icon="mail"
              placeholder="Email"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              type="tel"
              prepend-icon="phone"
              placeholder="(000) 000 - 0000"
              mask="phone"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              prepend-icon="notes"
              placeholder="Notes"
            ></v-text-field>
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-btn flat color="primary">More</v-btn>
        <v-spacer></v-spacer>
        <v-btn flat color="primary" @click="closeDialogCreateTask()">Cancel</v-btn>
        <v-btn flat @click="dialog = false">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {mapState} from "vuex";

export default {
  methods: {
    closeDialogCreateTask(){
      this.$store.commit(
        'showDialogCreateTask',
        false
      )
    }
  },
  computed: {
    ...mapState([
      'isCreatingTask'
    ])
  }
}
</script>

<style>

</style>
