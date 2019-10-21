function rememberMe(){
    if(document.checkout.RM.checked==true){
    localStorage.setItem('firstName',document.forms["checkout"]["firstName"].value);
    localStorage.setItem('lastName',document.forms["checkout"]["lastName"].value);
    localStorage.setItem('address',document.forms["checkout"]["address"].value);
    localStorage.setItem('email',document.forms["checkout"]["email"].value);
    localStorage.setItem('phone',document.forms["checkout"]["phone"].value);
    }else{
        localStorage.clear(); 
    }

    var formYear = document.getElementById("creditCardExpireDate").value.split('-')[0];
    var formMonth = document.getElementById("creditCardExpireDate").value.split('-')[1];
    var testDate = new Date();
    var testYear = testDate.getFullYear();
    var testMonth = testDate.getMonth()+1;
    
     if(formYear<testYear){
         console.log("Bigger Year");
         return false;
     }else if(formYear=testYear){
         if(formMonth<testMonth){
             console.log("Bigger Month");
             return false;
         }
     }else{

     }
}

function autorefill(){
    document.getElementById('firstName').value=localStorage.getItem('firstName');
    document.getElementById('lastName').value=localStorage.getItem('lastName');
    document.getElementById('address').value=localStorage.getItem('firstName');
    document.getElementById('email').value=localStorage.getItem('email');
    document.getElementById('phone').value=localStorage.getItem('phone');
}
window.onload=function(){
    autorefill();
    
}
