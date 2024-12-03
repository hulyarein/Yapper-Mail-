// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAuth, RecaptchaVerifier, signInWithPhoneNumber   } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js"
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

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


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const verifyForm = document.getElementById('verify-otp-form');



const auth = getAuth();
auth.useDeviceLanguage();

const myModal = new bootstrap.Modal('#verifyModal', {});



// Replace this with your sign-in-button
document.getElementById('sendOtpButton').addEventListener('click', function() {
    // Phone number field
    const phoneNumber = document.getElementById('phone-number').value;

    const appVerifier = new RecaptchaVerifier(auth, 'sendOtpButton', {
      'size': 'invisible',
      'callback': (response) => {
        // reCAPTCHA solved, allow signInWithPhoneNumber.
        onSignInSubmit();
      }
    });

    signInWithPhoneNumber(auth, phoneNumber, appVerifier)
        .then((confirmationResult) => {
        // SMS sent. Prompt user to type the code from the message, then sign the
        // user in with confirmationResult.confirm(code).
        window.confirmationResult = confirmationResult;
        myModal.show();
        alert('OTP is sent')
        console.log(confirmationResult)
        // ...
            }).catch((error) => {
            // Error; SMS not sent
            console.log(error)
            alert('Error while sending the OTP')
            location.reload()
            // ...
        });
});    

function getOTP() {
  // Select all input fields with the class 'otp-digit'
  const otpDigits = document.querySelectorAll('.otp-digit');
  let otp = '';
  
  // Loop through the inputs and concatenate their values
  otpDigits.forEach(input => {
      otp += input.value;
  });
  
  // Output or return the concatenated OTP
  console.log("OTP:", otp); // For debugging
  return otp;
}

verifyForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const code = getOTP();

    confirmationResult.confirm(code).then((result) => {
      // User signed in successfully.
      const user = result.user;


      const formData = new FormData(verifyForm);

      // Send Firebase ID Token to Django
      const idToken = result.user.getIdToken();
      fetch(verifyForm.action, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': formData.get('csrfmiddlewaretoken')
          },
          body: new URLSearchParams({
            'phone_number': document.getElementById('phone-number').value
          })
      })
      .then(response => response.json())
      .then(data => {
        if(data.message == null){
          window.location.href = data.redirect_url
        } else {
          alert(data.message)
        }
        
      })
      .catch(error => alert(error));
      // ...
    }).catch((error) => {
      // User couldn't sign in (bad verification code?)
      alert(error);
      // ...
    });
});   