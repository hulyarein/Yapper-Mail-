document.addEventListener('DOMContentLoaded', function() {
    fetch('/email_calendar/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        const calendarBody = document.getElementById('calendar-body');
        
        for (let hour = 0; hour < 24; hour++) {
          const timeSlot = document.createElement('div');
          timeSlot.classList.add('time-slot');

          ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(day => {
            const dayCell = document.createElement('div');
            dayCell.classList.add('day-cell');  

            if (data[day] && data[day][hour]) {
              data[day][hour].forEach(email => {
                const emailBlock = document.createElement('div');
                emailBlock.classList.add('email-block');
                emailBlock.textContent = `${email.subject}: ${email.time}`;
                dayCell.appendChild(emailBlock);
              });
            }
            timeSlot.appendChild(dayCell);
          });

          calendarBody.appendChild(timeSlot);
        }
    })
    .catch(error => console.error('Error fetching email data:', error));
});


