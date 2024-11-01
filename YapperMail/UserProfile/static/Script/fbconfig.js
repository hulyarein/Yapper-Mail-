// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.4/firebase-app.js";
import {
  getAuth,
  RecaptchaVerifier,
  signInAnonymously,
  signInWithPhoneNumber,
} from "https://www.gstatic.com/firebasejs/9.6.4/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDEbcETreJpHzKgz-nsjpvQXVddlFvg1ls",
  authDomain: "yapper-c977e.firebaseapp.com",
  projectId: "yapper-c977e",
  storageBucket: "yapper-c977e.firebasestorage.app",
  messagingSenderId: "1031580612372",
  appId: "1:1031580612372:web:a483e7c8d0991407657401",
  measurementId: "G-ZPLMLG7DGP",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

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

export function sendVerificationCode(phoneNumber) {
  const sendCodeButton = document.getElementById("krazy");
  sendCodeButton.disabled = true;

  signInWithPhoneNumber(auth, phoneNumber, recaptchaVerifier)
    .then((confirmationResult) => {
      window.confirmationResult = confirmationResult;
      console.log("SMS sent successfully!");
    })
    .catch((error) => {
      console.error("Error during sending verification code:", error.message);

      if (error.message.includes("TOO_MANY_ATTEMPTS_TRY_LATER")) {
        alert("Too many attempts. Please try again later.");
      }

      sendCodeButton.disabled = false; // Re-enable button if there's an error
    });

  // Re-enable after 30 seconds to prevent multiple quick attempts
  setTimeout(() => {
    sendCodeButton.disabled = false;
  }, 30000);
}

// Function to verify the code
export function verifyCode(verificationCode) {
  if (window.confirmationResult) {
    window.confirmationResult
      .confirm(verificationCode)
      .then((result) => {
        const user = result.user;
        console.log("User signed in:", user);
      })
      .catch((error) => {
        console.error("Error during verification:", error.message);
      });
  } else {
    console.error(
      "No confirmation result found. Make sure you've sent the code first."
    );
  }
}
