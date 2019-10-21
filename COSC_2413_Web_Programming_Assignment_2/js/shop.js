var sum = 0.00;
function changeS1Sub(){
    var up1 = 17.00;
    var sn1 = document.getElementById('Q1').value;
    var s1sub = up1*sn1;
    sum += s1sub;
    document.getElementById('sub1').innerHTML = s1sub.toFixed(2);
    return s1sub
}
function changeS2Sub(){
    var up2 = 22.5;
    var sn2 = document.getElementById('Q2').value;
    var s2sub = up2*sn2;
    sum += s2sub;
    document.getElementById('sub2').innerHTML = s2sub.toFixed(2);
    return s2sub
}
function changeS3Sub(){
    var up3 = 26.75;
    var sn3 = document.getElementById('Q3').value;
    var s3sub = up3*sn3;
    sum += s3sub;
    document.getElementById('sub3').innerHTML = s3sub.toFixed(2);
    return s3sub;
}
function getTotal(){
    document.getElementById('total').innerHTML = 'Total: ' + (changeS3Sub() +changeS2Sub() +changeS1Sub());
}

getTotal();
document.getElementById("Q1").addEventListener("change", getTotal);
document.getElementById("Q2").addEventListener("change", getTotal);
document.getElementById("Q3").addEventListener("change", getTotal); 