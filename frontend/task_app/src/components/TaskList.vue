<template>
<v-container ma-0 style="max-width: unset;">
  <v-snackbar
    v-model="showUndo"
    :multi-line="true"
    :right="true"
    :timeout="6000"
    :top="true"
    color="white"
    class="black--text"
    >
      Task has changed.
      <v-btn
        color="blue"
        flat
        @click="snackbar = false"
      >
        Undo
      </v-btn>
    </v-snackbar>
  <v-container pa-0 style="max-width: unset;">
    <v-layout class="align-start justify-start row fill-height progress-display pb-4">
      <v-flex
        class="white-grey-blue w-19 m-5px pa-2 br-3px"
        v-for="progress in tasks_progress"
        :key="progress.type"
      >
        {{ progress.display }}
      </v-flex>
    </v-layout>
    <v-layout align-content-space-between justify-start row fill-height>
      <!-- Loading component -->
      <v-flex xs12 v-if="isLoading">
        <v-progress-circular
          :size="60"
          :width="7"
          color="primary"
          indeterminate
          class="center-content"
        ></v-progress-circular>
      </v-flex>

      <v-flex
        v-else
        v-for="(obj, key) in tasks"
        :key="key"
        w-19 m-5px pa-2 no-box-shadow br-3px
        class="white-grey-blue relative"
      >
      <div
        :id="'blur_task_' + key"
        style="display:none;"
        class="blur-task"
      ></div>
      <draggable
        element="div"
        class="drag-area"
        v-model="tasks[key]"
        @choose="chooseTask"
        @start="start"
        @end="end"
        :move="move"
        :options="dragOptions"
        :data-progress="key"
      >
        <v-card
          v-for="task in tasks[key]" :key="task.id"
          class="black--text mb-2 bg-none"
          :data-taskid="task.id"
        >
          <task v-bind:task="task"></task>
        </v-card>
      </draggable>
      </v-flex>
    </v-layout>
  </v-container>
  <v-tooltip top lazy open-delay="800">
  <v-btn
    fab
    bottom
    right
    color="pink"
    dark
    fixed
    class="pa-3"
    @click="showDialogCreateTask()"
    slot="activator"
    >
      <v-icon>add</v-icon>
    </v-btn>
    <span>Create Task</span>
  </v-tooltip>
    <create-task ref="dialogCreateTask" v-on:created-task="reloadTask()"></create-task>
</v-container>
</template>

<script>
// components
import draggable from 'vuedraggable';
import Task from "./Task";
import CreateTask from "./CreateTask";

// constants
import TaskProgress from "../constants/TaskProgress.js";
import TaskType from "../constants/TaskType.js";
import TaskPriority from "../constants/TaskPriority.js";

// services & utils
import request from "../services/request.js";

export default {
  components: {
    Task,
    CreateTask,
    draggable
  },
  data: () => {
    return {
      isLoading: false,
      tasks: {
        todo: [],
        in_progress: [],
        in_repo: [],
        test: [],
        done: []
      },
      tasks_progress: TaskProgress.getProgressDisplay(),
      isDragged: false,
      showUndo: false,
      latestDragged: null
    };
  },
  methods: {
    /** filter task by progress type --> TODO, IN Progress, etc ..
     * @param {number} progress
     */
    filterData(progress){
      return this.tasks.filter(task => {
        return task.progress == progress;
      });
    },
    showDialogCreateTask(){
      this.$store.commit(
        'showDialogCreateTask',
        !this.$store.getters.isCreatingTask
      )
      // Trigger dialog show
      this.$refs.dialogCreateTask.triggerDialogShow(
        true
      );
    },
    reloadTask(){
      this.isLoading = true;
      request.get('task/')
      .then(response => {
        let data = response.data;
        if (!data.length) {
          return;
        }
        data.map((obj, index) => {
          if (obj.progress == TaskProgress.TODO){
            this.tasks.todo.push(obj);
          } else if (obj.progress == TaskProgress.IN_PROGRESS){
            this.tasks.in_progress.push(obj);
          } else if(obj.progress == TaskProgress.IN_REPO){
            this.tasks.in_repo.push(obj);
          } else if (obj.progress == TaskProgress.TEST){
            this.tasks.test.push(obj);
          } else {
            this.tasks.done.push(obj);
          }
        })
        this.isLoading = false;
      });
    },

    chooseTask (choose){
      let item = choose.item;
      let task_id = item.dataset.taskid;
      let cards = document.querySelectorAll('.v-card.theme--light.white-card');
      Array.prototype.forEach.call(cards, (card, index) => {
        if (card.dataset.taskid == task_id){
          card.style.setProperty("background-color", "#DEEBFF", "important");
        } else {
          card.style.setProperty("background-color", "");
        }
      })
      let card = item.querySelector(`[data-taskid="${task_id}"]`);
      card.style.setProperty("background-color", "#DEEBFF", "important");
    },

    getNextDraggingElement(from){
      let target = from.target;
      if (target.dataset.progress == 'todo'){
        return {
          blur_area: document.getElementById('blur_task_in_progress'),
          drag_area: document.querySelector('div.drag-area[data-progress="in_progress"]')
        }
      } else if (target.dataset.progress == 'in_progress'){
        return {
          blur_area: document.getElementById('blur_task_in_repo'),
          drag_area: document.querySelector('div.drag-area[data-progress="in_repo"]')
        }
      } else if (target.dataset.progress == 'in_repo') {
        return {
          blur_area: document.getElementById('blur_task_test'),
          drag_area: document.querySelector('div.drag-area[data-progress="test"]')
        }
      } else if (target.dataset.progress == 'test') {
        return {
          blur_area: document.getElementById('blur_task_done'),
          drag_area: document.querySelector('div.drag-area[data-progress="done"]')
        }
      } else if (target.dataset.progress == 'done') {
        return false;
      }

      // to handle if fucking user remove attribute data-progress
      let next_drag_container = from.target.parentElement.nextElementSibling;
      Array.prototype.forEach.call(next_drag_container.children, function(children, index){
        if(children.classList.contains('drag-area')){
          return children;
        }
      });
    },

    removeFocusDragging(from){
      let next_drag_element = this.getNextDraggingElement(from);
      next_drag_element.drag_area.classList.remove('focus-next-drag');
    },

    start(from){
      let next_drag_element = this.getNextDraggingElement(from);
      next_drag_element.drag_area.classList.add('focus-next-drag');

      let blur_tasks = document.getElementsByClassName('blur-task');
      Array.prototype.forEach.call(blur_tasks, (element, index) => {
        if (element.id != next_drag_element.blur_area.id){
          element.style.display = '';
        }
      });
    },
    end(from){
      let blur_tasks = document.getElementsByClassName('blur-task');
      Array.prototype.forEach.call(blur_tasks, (element, index) => {
        element.style.display = 'none';
      });
      this.removeFocusDragging(from);
      if (this.isDragged){
        setTimeout(() => {
          this.showUndo = true;
        }, 500);
      }
      this.isDragged = false;
    },
    move(from){
      this.isDragged = true;
      this.latestDragged = from.dragged.dataset.taskid;
    }
  },
  computed: {
    dragOptions(){
      return {
        animation: 150,
        group: {name: "task_progress_group"},
        disabled: false,
        ghostClass: "ghost",
      };
    }
  },
  created(){
    this.reloadTask();
  }
};
</script>

<style>
.center-content{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.flex.w-19 {
  -ms-flex-preferred-size: 16.666666666666664%;
  flex-basis: 19%;
  -webkit-box-flex: 0;
  -ms-flex-positive: 0;
  flex-grow: 0;
  max-width: 19%;
  width: 19%;
}
.flex.m-5px {
  margin: 5px;
}
.flex.no-box-shadow {
  box-shadow: none;
}
.flex.no-box-shadow > div {
  box-shadow: none;
}
.br-3px {
  border-radius: 3px;
}
.bg-none.v-card.theme--light {
  background: none;
  box-shadow: none !important;
}
.white-grey-blue {
  background: #F4F5F7 !important;
}
.relative {
  position: relative;
}
.progress-display {
  position: sticky;
  top: 65px;
  z-index: 100;
  background: #fff;
}
.drag-area {
  min-width: 50px;
  min-height: 100%;
}
.focus-next-drag {
  border: 2px dashed #1565c0 !important;
  border-radius: 3px;
  background: #b3d4fc !important;
}
.blur-task {
  width:100%;
  height:100%;
  background:rgb(244, 245, 247, 0.7) none repeat scroll 0% 0%;
  z-index:2;
  position:absolute;
  top: 0;
  left: 0;
  right: 0;
}
.v-card.theme--light.white-card.task-choosed {
  background: #DEEBFF !important;
}
</style>
