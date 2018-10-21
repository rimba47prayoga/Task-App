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
              @click="submitForm()"
            >
              Create
            </v-btn>
          </v-card-actions>

          <v-card-actions v-if="created" class="pt-3 pr-0 pl-0">
            <v-spacer></v-spacer>
            Your Project created successfully
            <v-icon color="#4CAF50" class="ml-2">done</v-icon>
          </v-card-actions>
        </v-flex>
      </v-flex>
      <v-flex xs6>
        <v-img
          :src="require('@/assets/icon-team-project.jpg')"
          width="250px"
        >
          <v-layout
            slot="placeholder"
            fill-height
            align-center
            justify-center
            ma-0
          >
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-layout>
        </v-img>
        <v-card-actions>
          <div style="color: rgba(0,0,0,.54)">
            Build your team projects here. <br>
            Get started and invite them
          </div>
        </v-card-actions>
      </v-flex>
    </v-layout>
  </v-form>

  <v-snackbar
    v-model="created"
    :absolute="true"
    :auto-height="true"
    :right="true"
    :timeout="100000"
    :bottom="true"
    color="white"
    class="black--text task-snackbar"
    >
    <v-icon class="green--text mr-3">done</v-icon>
    <v-btn
      color="black"
      flat
      class="ma-0 mr-3"
      @click="setProject()"
    >
      Set it as default project
    </v-btn>
    <v-btn
      flat
      class="black--text"
    >
      <v-icon>clear</v-icon>
    </v-btn>
  </v-snackbar>
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
      loading: false,
      created: false,
    }
  },
  methods: {
    submitForm(){
      if (this.$refs.createProject.validate()){
        this.loading = true;
        request.post('project/', {
          name: this.name,
          board_name: this.board_name,
          project_type: this.project_type
        })
        .then(response => {
          if (localStorage.getItem('projects') != null){
            let existing_projects = JSON.parse(localStorage.getItem('projects'))
            existing_projects.push(response.data)
            localStorage.setItem('projects', JSON.stringify(existing_projects));
          } else {
            localStorage.setItem('projects', JSON.stringify([response.data]))
          }
          this.created = true;
        })
        .finally(() => {
          this.loading = false;
        })
      }
    },
    setProject(){
      let projects = JSON.parse(
        localStorage.getItem('projects')
      );
      let selected_project = projects[projects.length - 1];
      localStorage.setItem('selected_project', JSON.stringify(selected_project));
      this.$router.push({
        name: 'task'
      });
      this.$store.commit('setProject', selected_project);
      this.created = false;
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
.task-snackbar {
  height: 53px;
  font-size: 15px;
}
.task-snackbar .v-snack__content {
  padding: 10px 24px;
}
.task-snackbar .v-snack__wrapper {
  border-radius: 4px;
}
</style>
