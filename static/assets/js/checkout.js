// Скрипт для окна сверху с ошибками
let messagesContainer = document.querySelector('.messages-container');
let messagesList = document.querySelector('.messages');

if (messagesList) {
  if (messagesList.children.length > 0) {
    messagesContainer.classList.add('show');
    setTimeout(function() {
      messagesContainer.classList.add('hide');
      messagesContainer.classList.remove('show');
    }, 2000);
  }
}

// Скрипт для модального окна
document.addEventListener('DOMContentLoaded', function () {
    const confirmBtn = document.getElementById('confirmBtn');
    const modal = document.getElementById('confirmModal');
    const yesBtn = document.getElementById('confirmYes');
    const noBtn = document.getElementById('confirmNo');

    if (confirmBtn && modal && yesBtn && noBtn) {
        confirmBtn.addEventListener('click', () => {
            modal.style.display = 'block';
            modal.classList.add('fade-in');
            document.body.classList.add('no-scroll'); 
        });

        yesBtn.addEventListener('click', () => {
            confirmBtn.closest('form').submit();
        });

        noBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            document.body.classList.remove('no-scroll');  
        });

        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
                document.body.classList.remove('no-scroll');
            }
        });
    }
});
