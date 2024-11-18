import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.4/firebase-app.js";
import { getAuth, RecaptchaVerifier, signInAnonymously, signInWithPhoneNumber } from "https://www.gstatic.com/firebasejs/9.6.4/firebase-auth.js";

  const firebaseConfig = {
    apiKey: "AIzaSyDGqPLEP536VoJM9AqwbrkJb0hCYFap4oA",
    authDomain: "yapper-1d02b.firebaseapp.com",
    projectId: "yapper-1d02b",
    storageBucket: "yapper-1d02b.firebasestorage.app",
    messagingSenderId: "557683908066",
    appId: "1:557683908066:web:5b712691670bc109bbedbb"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);

//   // Initialize Firebase
// firebase.initializeApp(firebaseConfig);

  const recaptchaVerifier = new RecaptchaVerifier(
    "recaptcha-container",
    {
      size: "invisible",
      callback: (response) => {
        console.log("reCAPTCHA verified:", response);
      },
    },
    auth
  );
  recaptchaVerifier.render().then((widgetId) => {
    window.recaptchaWidgetId = widgetId;
  });

//   document.getElementById("sendOtpButton").addEventListener("click", function (event) {
//     event.preventDefault(); // Prevent form submission
  
//     const phoneNumber = document.getElementById("phone_number").value;
//     const appVerifier = window.recaptchaVerifier;
  
//     signInWithPhoneNumber(auth, phoneNumber, appVerifier)
//       .then((confirmationResult) => {
//         // Store `confirmationResult` for verifying the code later
//         window.confirmationResult = confirmationResult;
//         document.getElementById("otpStatusMessage").textContent = "OTP sent. Please check your phone.";
//       })
//       .catch((error) => {
//         document.getElementById("otpStatusMessage").textContent = `Error: ${error.message}`;
//       });
//   });

  // function sendVerificationCode() {
  //   if (cooldownActive) return;

  //   const phoneNumber = document.querySelector('input[name="phonenumber"]').value;
    
  //   if (appVerifier) {
  //     appVerifier.clear();
  //   }
  //   appVerifier = new RecaptchaVerifier('recaptcha-container', {
  //     'size': 'invisible',
  //   }, auth);

  //   signInWithPhoneNumber(auth, phoneNumber, appVerifier)
  //   .then((confirmationResult) => {
  //     // Store the confirmation result to verify the code later
  //     window.confirmationResult = confirmationResult;
  //     startCooldown();
  //   })
  //   .catch((error) => {
  //     console.error("Error during verification:", error);
  //     // Optionally show an error message to the user
  //   });
  // }

  let confirmationResult;

  // function sendVerificationCode(phoneNumber) {
  //   const appVerifier = recaptchaVerifier;
  //   firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier)
  //     .then((confirmationResult) => {
  //       // SMS sent. Prompt user to type the code from the message
  //       window.confirmationResult = confirmationResult;
  //     })
  //     .catch((error) => {
  //       // Handle errors here
  //       console.error('Error during sign-in:', error.message);
  //     });
  // }

  function sendVerificationCode() {
    const phoneNumber = document.getElementById('phonenumber').value;
    const appVerifier = recaptchaVerifier;
    firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier)
      .then((confirmationResult) => {
        window.confirmationResult = confirmationResult;
        console.log('Verification code sent');
      })
      .catch((error) => {
        console.error('Error during sign-in:', error.message);
      });
  }


  function verifyCode(verificationCode) {
    confirmationResult.confirm(verificationCode)
      .then((result) => {
        // User signed in successfully
        const user = result.user;
        console.log('User:', user);
      })
      .catch((error) => {
        // Handle errors here
        console.error('Error during verification:', error.message);
      });
  }

  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      // User is signed in
      console.log('User is signed in:', user);
    } else {
      // No user is signed in
      console.log('No user is signed in');
    }
  });
  // function startCooldown() {
  //   cooldownActive = true;
  //   const link = document.getElementById("sendOtpButton");
  //   link.classList.add("text-gray-500"); // Style the link as disabled
  //   link.classList.remove("text-[#f37d84]");
  //   link.textContent = `Resend in ${cooldownTime}s`;

  //   const interval = setInterval(() => {
  //     cooldownTime--;
  //     link.textContent = `Resend in ${cooldownTime}s`;

  //     if (cooldownTime <= 0) {
  //       clearInterval(interval);
  //       cooldownActive = false;
  //       cooldownTime = 300;
  //       link.textContent = "Send Verification";
  //       link.classList.remove("text-gray-500");
  //       link.classList.add("text-[#f37d84]");
  //     }
  //   }, 1000);
  // }

  // document.getElementById('sendOtpButton').addEventListener('click', (event) => {
  //   event.preventDefault(); // Prevent default anchor behavior
  //   sendVerificationCode();
  // });

//   export function sendVerificationCode(phoneNumber) {
//     const sendCodeButton = document.getElementById("sendOtpButton");
//     sendCodeButton.disabled = true;
    
//     signInWithPhoneNumber(auth, phoneNumber, recaptchaVerifier)
//       .then((confirmationResult) => {
//         window.confirmationResult = confirmationResult;
//         console.log("SMS sent successfully!");
//         // Redirect to OTP input page on success
//         window.location.href = "/verify-otp/"; // Replace with your Django URL pattern for the OTP input page
//       })
//       .catch((error) => {
//         console.error("Error during sending verification code:", error.message);
//         if (error.message.includes("TOO_MANY_ATTEMPTS_TRY_LATER")) {
//           alert("Too many attempts. Please try again later.");
//         }
//         sendCodeButton.disabled = false; // Re-enable button if there's an error
//       });

//     // Re-enable button after 30 seconds, even if no error
//     setTimeout(() => {
//         sendCodeButton.disabled = false;
//     }, 30000);
// }

// Event listener for the send OTP button
// document.addEventListener("DOMContentLoaded", () => {
//     const sendCodeButton = document.getElementById("sendOtpButton");
//     sendCodeButton.addEventListener("click", () => {
//       const phoneNumber = document.getElementById("phone_number").value; // Assuming you have an input with ID 'phoneNumberInput'
//       if (phoneNumber) {
//         sendVerificationCode(phoneNumber);
//       } else {
//         alert("Please enter a phone number.");
//       }
//     });
//   });

// export function verifyCode(verificationCode) {
//     if (window.confirmationResult) {
//       window.confirmationResult
//         .confirm(verificationCode)
//         .then((result) => {
//           const user = result.user;
//           console.log("User signed in:", user);
//         })
//         .catch((error) => {
//           console.error("Error during verification:", error.message);
//         });
//     } else {
//       console.error(
//         "No confirmation result found. Make sure you've sent the code first."
//       );
//     }
//   }


document.getElementById("sendOtpButton").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission
  
    const phoneNumber = document.getElementById("phone_number").value;
    const appVerifier = window.recaptchaVerifier;
  
    signInWithPhoneNumber(auth, phoneNumber, appVerifier)
      .then((confirmationResult) => {
        // Store `confirmationResult` for verifying the code later
        window.confirmationResult = confirmationResult;
        document.getElementById("otpStatusMessage").textContent = "OTP sent. Please check your phone.";
      })
      .catch((error) => {
        document.getElementById("otpStatusMessage").textContent = `Error: ${error.message}`;
      });
  });


  function moveFocus(currentInput, direction) {
    const inputs = document.querySelectorAll(".otp-digit");
    const index = Array.from(inputs).indexOf(currentInput);
    if (currentInput.value && direction === "next" && index < inputs.length - 1) {
      inputs[index + 1].focus();
    } else if (!currentInput.value && direction === "prev" && index > 0) {
      inputs[index - 1].focus();
    }
  }

  function getOtp() {
    const otp = Array.from(document.querySelectorAll(".otp-digit"))
                      .map(input => input.value)
                      .join("");
    return otp;
  }
