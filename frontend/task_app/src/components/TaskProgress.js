export default {
  TODO: 1,
  IN_PROGRESS: 2,
  IN_REPO: 3,
  TEST: 4,
  DONE: 5,

  getProgressDisplay () {
    return [
      {
        display: "TO DO",
        type: this.TODO
      },
      {
        display: "IN PROGRESS",
        type: this.IN_PROGRESS
      },
      {
        display: "IN REPOSITORY",
        type: this.IN_REPO
      },
      {
        display: "TEST",
        type: this.TEST
      }
    ]
  }
};
