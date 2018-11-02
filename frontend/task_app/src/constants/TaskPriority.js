export default {
  LOWEST: 0,
  LOW: 1,
  MEDIUM: 2,
  HIGH: 3,
  HIGHEST: 4,

  getPriorityDisplay (priority = null) {
    const result = [
      {
        type: this.LOWEST.toString(),
        label: "Lowest",
        icon: "arrow_downward",
      },
      {
        type: this.LOW,
        label: "Low",
        icon: "arrow_downward",
      },
      {
        type: this.MEDIUM,
        label: "Medium",
        icon: "arrow_upward",
      },
      {
        type: this.HIGH,
        label: "High",
        icon: "arrow_upward",
      },
      {
        type: this.HIGHEST,
        label: "Highest",
        icon: "arrow_upward",
      }
    ];

    if (priority) {
      priority = Number(priority);
      return result.filter(item => {
        return item.type == priority;
      })[0];
    }
    return result;
  }
};
