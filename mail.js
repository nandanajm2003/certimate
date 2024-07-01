const firebaseConfig = {
    apiKey: "AIzaSyBkcRIr8RmSshBaTTfW7C4kk0EnoWhGf_8",
    authDomain: "certimate-c5a59.firebaseapp.com",
    databaseURL: "https://certimate-c5a59-default-rtdb.firebaseio.com",
    projectId: "certimate-c5a59",
    storageBucket: "certimate-c5a59.appspot.com",
    messagingSenderId: "640247527076",
    appId: "1:640247527076:web:15c88775b2836981955831",
    measurementId: "G-XGBG0D32NY"
  };

  // Initialize firebase
firebase.initializeApp(firebaseConfig);

// Reference your database
var CertimateDB = firebase.database().ref('Certimate');

// Attach the event listener to the form
document.querySelector('#Feedbackform').addEventListener("submit", submitForm);

// Define the submitForm function
function submitForm(e) {
    e.preventDefault();

    var fname = getElementVal('fname');
    var lname = getElementVal('lname');
    var country = getElementVal('country');
    var subject = getElementVal('subject');
    saveMessages(fname, lname, country, subject);
    document.querySelector('.alert').style.display = "block";
    setTimeout(() => {
        document.querySelector('.alert').style.display = "none";
    }, 3000); // Corrected timeout value

    // Reset the form
    document.querySelector('Feedbackform').reset();
}

const saveMessages = (fname, lname, country, subject) => {
    var newsubmitForm = CertimateDB.push();
    newsubmitForm.set({
        fname: fname,
        lname: lname,
        country: country,
        subject: subject,
    });
};


// Define a function to get element values by ID
const getElementVal = (id) => {
    return document.getElementById(id).value;
};