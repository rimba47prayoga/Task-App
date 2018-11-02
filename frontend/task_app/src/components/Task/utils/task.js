import TaskType from "../../../constants/TaskType";
import TaskPriority from "../../../constants/TaskPriority";

function getTaskTypeIcon (task_type) {
  let icon;
  switch (task_type) {
    case TaskType.TASK:
      icon = "check_box";
      break;
    case TaskType.SUB_TASK:
      icon = "branding_watermark";
      break;
    case TaskType.BUG:
      icon = "bug_report";
      break;
  };
  return icon;
}
function getTaskPriorityIcon(priority){
  let icon;
  switch (priority) {
    case TaskPriority.LOWEST:
    case TaskPriority.LOW:
      icon = "arrow_downward";
      break;
    case TaskPriority.MEDIUM:
    case TaskPriority.HIGH:
    case TaskPriority.HIGHEST:
      icon = "arrow_upward"
  };
  return icon;
}

function FormatDate (date) {
  if (!date) return;
  let [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

export { getTaskTypeIcon, getTaskPriorityIcon, FormatDate }
