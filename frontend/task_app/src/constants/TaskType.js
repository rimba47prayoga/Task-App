export default {
  TASK: 0,
  SUB_TASK: 1,
  BUG: 2,

  getTaskTypeDisplay(task_type = null) {
    const result =  [
      {
        type: this.TASK,
        label: 'Task',
        icon: 'check_box'
      },
      {
        type: this.SUB_TASK,
        label: 'Sub Task',
        icon: 'branding_watermark'
      },
      {
        type: this.BUG,
        label: 'Bug',
        icon: 'bug_report'
      }
    ];
    if (task_type != null) {
      return result.filter(item => {
        return item.type == task_type
      })[0];
    }
    return result;
  }
};
