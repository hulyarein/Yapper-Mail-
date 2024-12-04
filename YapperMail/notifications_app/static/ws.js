console.log("In");

document.addEventListener("DOMContentLoaded", function () {
    let url = `ws://${window.location.host}/ws/socket-server/`;  // Connect to the WebSocket server
    const socket = new WebSocket(url);
    const submitButton = document.querySelector("#submitButton");

    socket.onopen = () => {
        console.log("Connected!");
    };

    socket.onclose = () => {
        console.log("Socket closed!");
    };

    async function processEmail(email) {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        try {
            const response = await fetch('/get_user_id/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ email }) // Send email in request body
            });

            if (response.ok) {
                console.log("Email processed successfully.");
                return true;
            } else {
                const errorData = await response.json();
                console.error("Error processing email:", errorData.error);
                return false;
            }
        } catch (error) {
            console.error("Error in processEmail:", error);
            return false;
        }
    }

    async function fetchUserIds() {
        try {
            const response = await fetch('/get_user_id/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                return {
                    loggedInUserId: data.logged_in_user_id,
                    emailUserId: data.email_user_id
                };
            } else {
                console.error("Failed to fetch user IDs. Status:", response.status);
                return null;
            }
        } catch (error) {
            console.error("Error fetching user IDs:", error);
            return null;
        }
    }

    if (submitButton) {
        submitButton.onclick = function (e) {
            // Prevent form from submitting
            e.preventDefault();

            // Get form values
            const toUserElement = document.querySelector("[name='toUser']");
            const subjectElement = document.querySelector("[name='subject']");
            const descriptionElement = document.querySelector("[name='description']");

            if (toUserElement && subjectElement && descriptionElement) {
                const toUser = toUserElement.value; // The email to process
                const subject = subjectElement.value;
                const description = descriptionElement.value;

                console.log("User (toUser):", toUser);
                console.log("Subject:", subject);
                console.log("Description:", description);

                // Step 1: Post the email to process and find the associated user ID
                processEmail(toUser).then(isEmailProcessed => {
                    if (isEmailProcessed) {
                        console.log("Email successfully processed.");

                        // Step 2: Fetch both logged-in user ID and the processed email ID
                        fetchUserIds().then(userIds => {
                            if (userIds) {
                                console.log("Logged-in user ID:", userIds.loggedInUserId);
                                console.log("Email user ID:", userIds.emailUserId);

                                // Step 3: Send data to WebSocket
                                socket.send(JSON.stringify({
                                    email: {
                                        fromUser: userIds.emailUserId,  // Use the logged-in user's ID
                                        toUser: toUser, // Use the ID associated with the processed email
                                        subject: subject,
                                        content: description
                                    }
                                }));
                            } else {
                                console.error("Failed to fetch valid user IDs.");
                            }
                        });
                    } else {
                        console.error("Failed to process the email.");
                    }
                });
            } else {
                console.error("One or more elements (toUser, subject, description) not found!");
            }

            // Optionally clear the form or show confirmation in the UI
            document.querySelector("#emailForm").reset();
        };
    }
});

