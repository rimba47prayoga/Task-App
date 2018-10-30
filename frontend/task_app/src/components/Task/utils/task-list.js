const resizeTaskContainer = () => {
  setTimeout(() => {
    var progress_display = document.getElementsByClassName('progress-display')[0];
    if (typeof progress_display == 'undefined') {
      return;
    }
    let client_rect = progress_display.getBoundingClientRect();
    progress_display = client_rect.top + client_rect.height;
    let scroll_target = document.getElementById('scroll-target');
    let max_height = document.documentElement.clientHeight - progress_display;
    scroll_target.style.maxHeight = `${max_height}px`;
  }, 500);
};

export { resizeTaskContainer };
