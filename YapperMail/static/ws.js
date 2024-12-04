// document.addEventListener("DOMContentLoaded", function () {
//     const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

//     socket.onmessage = (e) => {
//         const result = JSON.parse(e.data).result;
//         document.querySelector('.toast-body').innerText = "Server: " + result;
//         const toast = new bootstrap.Toast(document.getElementById('liveToast'));
//         toast.show();
//     };

//     socket.onclose = () => {
//         console.log("Socket closed!");
//     };

//     document.querySelector("#submitButton").addEventListener('click', function (e) {
//         // Prevent form from submitting
//         e.preventDefault();

//         // Get form values
//         const toUser = document.querySelector("[name='toUser']").value;
//         const subject = document.querySelector("[name='subject']").value;
//         const description = document.querySelector("[name='description']").value;

//         // Send data to WebSocket
//         socket.send(JSON.stringify({
//             email: {
//                 fromUser: 1, // You can hardcode or dynamically get this user ID
//                 toUser: toUser,
//                 subject: subject,
//                 content: description
//             }
//         }));

//         // Optionally clear the form or show confirmation in the UI
//         document.querySelector("#emailForm").reset();
//     });
// });

console.log("In");

document.addEventListener("DOMContentLoaded", function () {
    const socket = new WebSocket('ws://localhost:8000/ws/notification/');
    const notificationList = document.querySelector("#notificationList");
    const notificationBadge = document.querySelector("#notificationBadge");

    let notificationCount = 0;

    socket.onmessage = (e) => {
        const response = JSON.parse(e.data);

        // Check if there's a notification-related response
        if (response.result) {
            notificationCount++;

            // Show the badge and update the count
            notificationBadge.style.display = "inline-block";
            notificationBadge.textContent = notificationCount;

            // Add a new notification item
            const newNotification = document.createElement("li");
            newNotification.className = "dropdown-item";
            newNotification.textContent = response.result;

            // Remove the "No notifications" placeholder if present
            if (notificationList.children[0]?.classList.contains("text-muted")) {
                notificationList.innerHTML = "";
            }

            // Add the new notification to the list
            notificationList.prepend(newNotification);

            // Optionally, limit the number of notifications displayed
            if (notificationList.children.length > 10) {
                notificationList.removeChild(notificationList.lastChild);
            }
        }
    };

    socket.onclose = () => {
        console.log("Socket closed!");
    };


    document.querySelector("#submitButton").addEventListener('click', function (e) {
        // Prevent form from submitting
        e.preventDefault();

        // Get form values
        const toUser = document.querySelector("[name='toUser']").value;
        const subject = document.querySelector("[name='subject']").value;
        const description = document.querySelector("[name='description']").value;

        // Send data to WebSocket
        socket.send(JSON.stringify({
            email: {
                fromUser: 1, // You can hardcode or dynamically get this user ID
                toUser: toUser,
                subject: subject,
                content: description
            }
        }));

        // Optionally clear the form or show confirmation in the UI
        document.querySelector("#emailForm").reset();
    });

    // Optional: Clear badge and mark notifications as seen on dropdown toggle
    document.querySelector("#notificationDropdown").addEventListener("click", () => {
        notificationCount = 0;
        notificationBadge.style.display = "none";
    });
});
