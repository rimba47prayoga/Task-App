export default {
  SOFTWARE: 0,
  WEB_SERVICES: 1,

  getProjectDisplay (type) {
    switch (type) {
      case this.SOFTWARE:
        return "Software Project";
      case this.WEB_SERVICES:
        return "Web Services Project"
    }
  }
}
