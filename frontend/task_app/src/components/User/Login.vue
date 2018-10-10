<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form
                v-model="valid"
                ref="form"
                @submit.prevent="submitForm"
                lazy-validation
                >
                  <v-text-field
                    :rules="default_rules"
                    v-model="username"
                    prepend-icon="person"
                    label="Username"
                    type="text"
                    required
                  ></v-text-field>
                  <v-text-field
                    :rules="default_rules"
                    v-model="password"
                    prepend-icon="lock"
                    label="Password"
                    type="password"
                    required
                    ></v-text-field>
                    <input ref="submitButton" type="submit" style="display:none" />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="$refs.submitButton.click()">Submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import request from '../../services/request.js';
import router from '../../router/index.js';
export default {
  data(){
    return {
      valid: true,
      username: '',
      password: '',

      default_rules: [
        v => !!v || 'This field is required',
      ]
    }
  },
  methods: {
    submitForm(){
      if (this.$refs.form.validate()){
        // TODO: submit login here with dispatch vuex
        this.$store.dispatch('login', {
          username: this.username,
          password: this.password
        }).then(() => {
          this.$router.push(this.$router.query.next || '/');
        })
      }
    }
  }
}
</script>

<style>

</style>
