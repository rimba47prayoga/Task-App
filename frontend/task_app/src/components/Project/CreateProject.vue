<template>
<v-container>
  <div class="headline mb-4">
    Create Project
  </div>
  <v-form
    v-model="valid"
    ref="createProject"
    class="create_project"
  >
    <v-layout row wrap>
      <v-flex xs6>
        <v-flex xs12>
          <label class="input-label">
            Project Name
            <span class="required">*</span>
          </label>
          <v-flex xs8 mt-1>
            <v-layout align-center>
              <v-text-field
                v-model="name"
                placeholder="Enter Project Name"
                :rules="default_rules"
                required
                solo
                flat
              ></v-text-field>
            </v-layout>
          </v-flex>
        </v-flex>

        <v-flex xs12>
          <label class="input-label">
            Project Type
            <span class="required">*</span>
          </label>
          <v-flex xs5 mt-1>
            <v-layout align-center>
              <v-select
              v-model="project_type"
              :items="project_type_items"
              item-text="label"
              item-value="type"
              placeholder="Choose Project Type"
              required
              solo
              flat
            ></v-select>
            </v-layout>
          </v-flex>
        </v-flex>

        <v-flex xs12>
          <label class="input-label">
            Key
            <span class="required">*</span>
          </label>
          <v-flex xs5>
            <v-text-field
              v-model="board_name"
              :rules="default_rules"
              placeholder="Enter Prefix key"
              required
              solo
              flat
              hint="The Prefix key is used for prefix each task branch"
              persistent-hint
            >
            </v-text-field>
          </v-flex>
        </v-flex>
        <v-flex xs8>
          <v-card-actions class="pt-3 pr-0 pl-0">
            <v-spacer></v-spacer>
            <v-btn
              :loading="loading"
              :disabled="loading"
              depressed
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-flex>
      </v-flex>

    </v-layout>
  </v-form>
</v-container>
</template>

<script>
import request from '../../services/request.js';

export default {
  data(){
    return {
      name: '',
      board_name: '',
      project_type: null,
      project_type_items: [
        {
          type: 0,
          label: 'Software Project'
        },
        {
          type: 1,
          label: 'Web Services Project'
        }
      ],
      valid: true, // model form
      default_rules: [
        v => !!v || "This field is required"
      ],
      loading: false
    }
  },
  method: {
    submitForm(){
      if (this.$refs.createProject.validate()){
        this.loading = true;
        request.post('project/', {
          name: this.name,
          board_name: this.board_name,
          project_type: this.project_type
        })
        .then(response => {
          // TODO: after it should be show snackbar info success created project
          // and, show button for set it as default project
        })
        .finally(() => {
          this.loading = false;
        })
      }
    }
  }
}
</script>

<style>
form.create_project .v-text-field--solo .v-input__slot {
  background-color: #F4F5F7 !important;
  border: 1px solid #e4e7ea;
  min-height: 39px;
  transition: .05s ease-in-out;
}
form.create_project .v-text-field--solo .v-input__slot:hover {
  background-color: rgb(240, 241, 243) !important;
}
form.create_project .v-text-field__details {
  max-width: unset;
  width: -moz-max-content;
  padding: 0 !important;
}
</style>
