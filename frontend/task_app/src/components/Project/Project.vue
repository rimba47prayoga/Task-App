<template>
  <task-list></task-list>
</template>

<script>
import TaskList from "../Task/TaskList";

export default {
  components: {
    TaskList
  },
  data(){
    return {
      project: {}
    }
  },
  created(){
    let project_slug = this.$route.params.slug;
    var projects = localStorage.getItem('projects');
    if (!projects){
      this.$router.push({
        name: 'dashboard'
      })
      return;
    }
    projects = JSON.parse(projects);
    let is_exists = projects.filter(project => {
      return project_slug == project.slug.toLowerCase();
    });
    if (!is_exists.length){ // TODO: redirect to 404 page
      this.$router.push({
        name: 'dashboard'
      })
      return;
    }
    this.project = is_exists[0];
  }
}
</script>

<style>

</style>
