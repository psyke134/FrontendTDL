function taskEntryHoverRegister() {
  const taskEntries = document.querySelectorAll('.task-entry');

  taskEntries.forEach((task) => {
    const delBtn = task.querySelector('.delete-button');
    task.addEventListener('mouseenter', () => {
      delBtn.style.display = "block";
    });
  
    task.addEventListener('mouseleave', () => {
      delBtn.style.display = "none";
    });
  });
}

taskEntryHoverRegister()
