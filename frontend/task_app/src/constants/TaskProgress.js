export default {
  TODO: 0,
  IN_PROGRESS: 1,
  IN_REPO: 2,
  TEST: 3,
  DONE: 4,

  getProgressDisplay(progress = null) {
    const result = [
      {
        display: 'TO DO',
        type: this.TODO
      },
      {
        display: 'IN PROGRESS',
        type: this.IN_PROGRESS
      },
      {
        display: 'IN REPOSITORY',
        type: this.IN_REPO
      },
      {
        display: 'TEST',
        type: this.TEST
      },
      {
        display: 'DONE',
        type: this.DONE
      }
    ];
    if (progress != null) {
      progress = Number(progress);
      return result.filter(item => {
        return item.type == progress;
      })[0];
    }
    return result;
  }
};
