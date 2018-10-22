const resizeTaskContainer = () => {
  setTimeout(() => {
    var progress_display = document.getElementsByClassName('progress-display')[0];
    let client_rect = progress_display.getBoundingClientRect();
    progress_display = client_rect.top + client_rect.height;
    let scroll_target = document.getElementById('scroll-target');
    let max_height = document.body.offsetHeight - progress_display;
    scroll_target.style.maxHeight = `${max_height}px`;
  }, 500);
};

export { resizeTaskContainer };
