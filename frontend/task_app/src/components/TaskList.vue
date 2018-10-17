<template>
<v-container ma-0 pt-0 pb-0 style="max-width: unset;">
  <v-snackbar
    v-model="showUndo"
    :absolute="true"
    :auto-height="true"
    :right="true"
    :timeout="6000"
    :top="true"
    color="white"
    class="black--text"
    style="height: 53px;font-size: 15px;"
    >
    <v-icon class="primary--text mr-3">warning</v-icon>
    Task has changed :
    <v-btn
      color="blue"
      flat
      @click="undoMovedTask()"
      class="ma-0 mr-3"
    >
      Undo
    </v-btn>
    <v-btn
      @click="showUndo = false"
      flat
      class="black--text"
    >
      <v-icon>clear</v-icon>
    </v-btn>
  </v-snackbar>

  <v-snackbar
    v-model="showError"
    :absolute="true"
    :auto-height="true"
    :right="true"
    :timeout="6000"
    :top="true"
    color="white"
    class="red--text"
    style="height: 53px;font-size: 15px;"
    >
    {{ error.message }}
    <v-btn
      @click="showUndo = false"
      flat
      class="black--text"
    >
      <v-icon>clear</v-icon>
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
    <v-container
      id="scroll-target"
      style="max-height: 490px;max-width: 100%;"
      class="scroll-y pa-0">

      <v-layout
      v-scroll:#scroll-target=""
      align-content-space-between justify-start row fill-height scroll-y
      >
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
          class="blur-task hide"
        ></div>
        <draggable
          element="div"
          class="drag-area"
          v-model="tasks[key]"
          @choose="chooseTask"
          @start="start"
          @end="end"
          @sort="sort"
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
  </v-container>
    <v-speed-dial
      v-model="fab"
      :top="top"
      :bottom="bottom"
      :right="right"
      :left="left"
      :direction="direction"
      :open-on-hover="hover"
      :transition="transition"
    >
      <v-btn
        slot="activator"
        v-model="fab"
        color="blue darken-2"
        dark
        fab
      >
        <v-icon>more_vert</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-tooltip left>
      <v-btn
        fab
        dark
        small
        color="indigo"
        slot="activator"
        @click="showDialogCreateTask()"
      >
      <v-icon>add</v-icon>
      </v-btn>
      <span>Add new task</span>
      </v-tooltip>
      <v-tooltip left>
      <v-btn
        fab
        dark
        small
        color="green"
        slot="activator"
        @click="reloadTask()"
      >
        <v-icon>refresh</v-icon>
      </v-btn>
      <span>Refresh</span>
      </v-tooltip>
      <v-tooltip left>
      <v-btn
        fab
        dark
        small
        color="blue darken-4"
        slot="activator"
      >
        <v-icon>person_add</v-icon>
      </v-btn>
      <span>Invite People</span>
      </v-tooltip>
      <v-tooltip left>
      <v-btn
        fab
        dark
        small
        color="white"
        slot="activator"
        class="black--text"
      >
        <v-icon>search</v-icon>
      </v-btn>
      <span>Search</span>
      </v-tooltip>
    </v-speed-dial>
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
      isMoved: false,
      showUndo: false,
      latestDragged:  {
        task_id: null,
        progress: null
      },
      showError: false,
      error: {
        message: null
      },
      direction: 'top',
      fab: false,
      fling: false,
      hover: false,
      tabs: null,
      top: false,
      right: true,
      bottom: true,
      left: false,
      transition: 'slide-y-reverse-transition'
    };
  },
  methods: {
    /** filter task by progress type --> TODO, IN Progress, etc ..
     * @param {number} progress
     * @returns {Object}
     */
    filterData(progress){
      return this.tasks.filter(task => {
        return task.progress == progress;
      });
    },
    sortTask(progress){
      this.tasks[progress] = this.tasks[progress].sort((one, two) => {
        return one.id - two.id;
      })
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

    /** get this.task[progress] (get tasks key by progress) in component data
     * @param {number} progress
     */
    getTaskByProgress(progress, return_key=false){
      if (progress == TaskProgress.TODO){
        if (return_key) {
          return 'todo'
        }
        return this.tasks.todo;
      } else if (progress == TaskProgress.IN_PROGRESS){
        if (return_key) {
          return 'in_progress'
        }
        return this.tasks.in_progress;
      } else if (progress == TaskProgress.IN_REPO){
        if (return_key) {
          return 'in_repo'
        }
        return this.tasks.in_repo;
      } else if (progress == TaskProgress.TEST){
        if (return_key) {
          return 'test'
        }
        return this.tasks.test;
      } else if (progress == TaskProgress.DONE){
        if (return_key) {
          return 'done'
        }
        return this.tasks.done;
      } else {
        throw new Error('uncategorize task progress');
      }
    },

    /** Update task progress after moved task
     * @param {number} task_id
     * @param {number} progress
     */
    updateTaskProgress(task_id, progress){
      var tasks = this.getTaskByProgress(progress);

      request.put(`task/${task_id}/update_progress`, {
        new_progress: progress
      })
      .then(response => {
        this.showUndo = true;
        tasks.map((task, index) => {
          if (task.id == task_id){
            task.progress = response.data.new_progress;
          }
        })
      })
      .catch(err => {
        let response = err.response;
        if (response.status == 400){
          this.showError = true;
          this.error.message = response.data.message;
        } else {
          Promise.reject(err);
        }
      })
    },

    undoMovedTask(){
      let task_id = Number(this.latestDragged.task_id);
      request.post(`task/${task_id}/undo_progress`)
      .then(response => {
        let tasks_after_undo = this.getTaskByProgress(Number(response.data.progress)); // tasks after undo
        let tasks_before_undo = this.getTaskByProgress(Number(this.latestDragged.progress));
        tasks_before_undo.map((task, index) => {
          if (task.id == task_id){
            tasks_before_undo.splice(index, 1);
            task.progress = response.data.progress;
            tasks_after_undo.push(task);
            let progress = this.getTaskByProgress(response.data.progress, true);
            this.sortTask(progress);

          }
        })
      })
      .catch(err => {
        if (err.response.status == 400){
          this.showError = true;
          var message = err.response.data.message;
          if (typeof message == "undefined"){
            message = err.response.data.detail;
          }
          this.error.message = message;
        }
      })
      .finally(() => {
        this.showUndo = false;
      })
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
    },

    /** get next drag element by task progress
     * @param {Object} from
     * @returns {Object}
     */
    getNextDraggingElement(target){
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

    removeFocusDragging(target){
      // remove blur effect
      let blur_tasks = document.getElementsByClassName('blur-task');
      Array.prototype.forEach.call(blur_tasks, (element, index) => {
        element.classList.add('hide');
      });
      let next_drag_element = this.getNextDraggingElement(target);
      if (!next_drag_element) return false;
      next_drag_element.drag_area.classList.remove('target-locked');
      Array.prototype.forEach.call(next_drag_element.drag_area.children, (task, index) => {
        task.classList.remove('hide')
      });
    },

    start(from){
      let next_drag_element = this.getNextDraggingElement(from.target);
      if (!next_drag_element) return false;
      next_drag_element.drag_area.classList.add('focus-next-drag');

      // hide task
      Array.prototype.forEach.call(next_drag_element.drag_area.children, (task, index) => {
        task.classList.add('hide')
      });

      // show blur effect
      let blur_tasks = document.getElementsByClassName('blur-task');
      Array.prototype.forEach.call(blur_tasks, (element, index) => {
        if (element.id != next_drag_element.blur_area.id){
          element.classList.remove('hide');
        }
      });
    },
    end(from){
      this.removeFocusDragging(from.target);
      if (this.isMoved) {
        this.updateTaskProgress(this.latestDragged.task_id, this.latestDragged.progress);
      }
      this.isMoved = false;
    },
    move(from){
      let drag_area = from.to;
      drag_area.classList.remove('focus-next-drag');
      drag_area.classList.add('target-locked');
      var progress = from.draggedContext.element.progress;
      if (progress == TaskProgress.DONE) return false;
      let task_id = Number(from.dragged.dataset.taskid);
      this.latestDragged = {
        task_id: task_id,
        progress: progress + 1
      };
      this.isMoved = true;
    },
    sort(from){
      let progress = from.target.dataset.progress;
      this.sortTask(progress);
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
    },
    activeFab () {
        switch (this.tabs) {
          case 'one': return { 'class': 'purple', icon: 'account_circle' }
          case 'two': return { 'class': 'red', icon: 'edit' }
          case 'three': return { 'class': 'green', icon: 'keyboard_arrow_up' }
          default: return {}
        }
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
  margin: 0 5px 0 5px;
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
  top: 120px;
  z-index: 100;
  background: #fff;
}
.drag-area {
  min-width: 50px;
  min-height: 100%;
}
.focus-next-drag, .target-locked {
  border: 2px dashed #1565c0 !important;
  border-radius: 3px;
}
.focus-next-drag {
  background: #b3d4fc !important;
}
.target-locked {
  background: #E8F5E9 !important;
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

.v-card.theme--light.white-card:hover {
  cursor:move;
  transition: background-color 140ms ease-in-out, border-color 75ms ease-in-out;
  background: #F4F5F7 !important;
}
.hide {
  display: none !important;
}

.v-speed-dial {
    position: absolute;
  }
.v-btn--floating {
    position: relative;
  }
.v-btn__content i.v-icon {
  left: unset !important;
  top: unset !important;
  line-height: -moz-block-height;
}
</style>
