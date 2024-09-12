//get elements from html

// Name input;
var uName = document.getElementById("uName");
var uNameErr = document.getElementById("uNameErr");
if (uName) {
    uName.addEventListener("blur", errValid);
}

// Phone input
var utel = document.getElementById("utel");
var utelErr = document.getElementById("utelErr");
if (utel) {
    utel.addEventListener("blur", errValid);
}

// Email input
var uEmail = document.getElementById("uEmail");
var uEmailErr = document.getElementById("uEmailErr");
if (uEmail) {
    uEmail.addEventListener("blur", errValid);
}

// Textarea input
var mess = document.getElementById("mess");
var messErr = document.getElementById("messErr");
if (mess) {
    mess.addEventListener("blur", errValid);
}

// Password input
var pass = document.getElementById("pass");
var passErr = document.getElementById("passErr");
if (pass) {
    pass.addEventListener("blur", errValid);
}

// Confirm password input
var rePass = document.getElementById("rePass");
var rePassErr = document.getElementById("rePassErr");
if (rePass) {
    rePass.addEventListener("blur", errValid);
}



$(document).ready(function(){
    'use strict';

    // banner slider
    $('.banner-slider').slick({
        arrows: false,
        autoplay: true,
        autoplaySpeed: 3500,
    });

    // animation css when scroll
    new WOW().init();

});


// a function for submit button;

function subm()
{

      // name field;
      if(uName.value == "")
      {
          uName.style.borderColor = "#008080";
          uNameErr.innerHTML = "Enter Your Username";
          uName.focus();
          return false;
      }
  
      // email field;
      if(uEmail.value == "")
      {
        uEmail.style.borderColor = "#008080";
        uEmailErr.innerHTML = "Enter Your User Email";
          uEmail.focus();
          return false;
      }

       // phone field;
       if(utel.value == "")
       {
         utel.style.borderColor = "#008080";
         utelErr.innerHTML = "Enter Your Phone Number";
           utel.focus();
           return false;
       }
  
      // textarea field;
      if(mess.value == "")
      {
          mess.style.borderColor = "#008080";
          messErr.innerHTML = "Enter Your Message";
          mess.focus();
          return false;
      }

}


// a function to remove error after fill up input feild;
function errValid()
{   
    // name error valid;
    if(uName.value != "")
    {
        uName.style.borderColor = "#000000";
        uNameErr.innerHTML = "";
    }

    // email error valid;
    if(uEmail.value != "")
    {
        uEmail.style.borderColor = "#5F7A61";
        uEmailErr.innerHTML = "";
    }

     // phone error valid;
     if(uEmail.value != "")
     {
         utel.style.borderColor = "#5F7A61";
         utel.innerHTML = "";
     }

    // password error valid;
    if(mess.value != "")
    {
        mess.style.borderColor = "#5F7A61";
        messErr.innerHTML = "";
    }

}


// Login form function for login In button

// a function for submit button;

function loginbtn()
{
  
      // email field;
      if(uEmail.value == "")
        {
          uEmail.style.borderColor = "#008080";
          uEmailErr.innerHTML = "Enter Your UserEmail";
            uEmail.focus();
            return false;
        }

      // password field;
      if(pass.value == "")
        {
            pass.style.borderBottomColor = "red";
            passErr.innerHTML = "Enter Your Password";
            pass.focus();
            return false;
        }

}

// a function to remove error after fill up input feild for Lognin button;
function errValidLogin()
{   

    // email error valid;
    if(uEmail.value != "")
    {
        uEmail.style.borderBottomColor = "#5F7A61";
        uEmailErr.innerHTML = "";
    }

    // password error valid;
    if(pass.value != "")
    {
        pass.style.borderBottomColor = "#5F7A61";
        passErr.innerHTML = "";
    }
}

// Sign up form function for Sign up button

// a function for signup button;

function signupbtn()
{
  
       // name field;
       if(uName.value == "")
        {
            uName.style.borderColor = "#008080";
            uNameErr.innerHTML = "Enter Your Username";
            uName.focus();
            return false;
        }
    
        // email field;
        if(uEmail.value == "")
        {
          uEmail.style.borderColor = "#008080";
          uEmailErr.innerHTML = "Enter Your User Email";
            uEmail.focus();
            return false;
        }

      
       // password field;
       if(pass.value == "")
        {
            pass.style.borderBottomColor = "red";
            passErr.innerHTML = "Enter Your Password first";
            pass.focus();
            return false;
        }
    
        // password length;
        if(pass.value.length < 6)
        {
            pass.style.borderBottomColor = "red";
            passErr.innerHTML = "Enter at least 6 Characters";
            pass.focus();
            return false;
        }
    
        // confirm password field;
        if(rePass.value == "")
        {
            rePass.style.borderBottomColor = "red";
            rePassErr.innerHTML = "Confirm Your Password";
            rePass.focus();
            return false;
        }
    
        // confirm password length;
        if(rePass.value != pass.value)
        {
            rePass.style.borderBottomColor = "red";
            rePassErr.innerHTML = "Password did not match";
            rePass.focus();
            return false;
        }

}


// a function to remove error after fill up input feild;
function errValid()
{   
    // name error valid;
    if(uName.value != "")
    {
        uName.style.borderBottomColor = "#5F7A61";
        uNameErr.innerHTML = "";
    }

    // email error valid;
    if(uEmail.value != "")
     {
        uEmail.style.borderBottomColor = "#5F7A61";
        uEmailErr.innerHTML = "";
     }
    
     // password error valid;
    if(pass.value != "")
     {
        pass.style.borderBottomColor = "#5F7A61";
        passErr.innerHTML = "";
    }

     // confirm password error valid;
     if(rePass.value != "")
     {
        rePass.style.borderBottomColor = "#5F7A61";
        rePassErr.innerHTML = "";
     }
}


//create portfoilo page function are here

document.addEventListener('DOMContentLoaded', function () {
    // Handle navigation between steps
    document.querySelectorAll('.next-step').forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = this.closest('.step');
            const nextStep = currentStep.nextElementSibling;
            if (nextStep && nextStep.classList.contains('step')) {
                currentStep.style.display = 'none';
                nextStep.style.display = 'block';
                updateProgressBar(nextStep);
            }
        });
    });

    document.querySelectorAll('.prev-step').forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = this.closest('.step');
            const prevStep = currentStep.previousElementSibling;
            if (prevStep && prevStep.classList.contains('step')) {
                currentStep.style.display = 'none';
                prevStep.style.display = 'block';
                updateProgressBar(prevStep);
            }
        });
    });

    // Handle the confirmation dialog
    const delButton = document.getElementById('delete-button');
    if (delButton) {
        delButton.addEventListener('click', function () {
            document.getElementById('confirmation-dialog').style.display = 'block';
        });
    }
    const cancelButton = document.getElementById('cancel-button');
    if (cancelButton) {
        cancelButton.addEventListener('click', function () {
            document.getElementById('confirmation-dialog').style.display = 'none';
        });
    }

    // Add and remove share forms
    const addShareBtn = document.getElementById('addShareBtn');
    if (addShareBtn) {
        addShareBtn.addEventListener('click', function() {
            let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
            let formNum = parseInt(totalForms.value);
            const template = document.getElementById('template-form').innerHTML;
            const newFormHtml = template.replace(/__prefix__/g, formNum);
            const container = document.getElementById('sharesContainer');
            container.insertAdjacentHTML('beforeend', newFormHtml);
            formNum++;
            totalForms.value = formNum;
        });
    }

    // Remove share form
    document.getElementById('sharesContainer').addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-share')) {
            e.target.closest('.share-card').remove();
            let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
            let formNum = parseInt(totalForms.value);
            formNum--;
            totalForms.value = formNum;
        }
    });
});

// Update progress bar based on the current step
function updateProgressBar(step) {
    const steps = document.querySelectorAll('.step');
    const stepIndex = Array.from(steps).indexOf(step);
    const progress = ((stepIndex + 1) / steps.length) * 100;
    document.querySelector('.progress-bar').style.width = `${progress}%`;
}
