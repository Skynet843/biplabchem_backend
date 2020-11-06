function uploadImage(){
    let imageInput=document.getElementById('customFile')
    
    if (imageInput.value==""){
        alert("Please Fill Require Data...")
    }else{
        document.getElementById('form1').submit();
    }
}
function check_input(){
    let pubDoc = document.getElementById("publicationDoc");
    let pubImg = document.getElementById("publicationImg");
    console.log("Master");
    if(pubDoc.value == ""){
        alert("Please Enter the Document File");
    }
    else if(pubImg.value == ""){
        alert("Please Enter the Image file");
    }
    else{
        document.getElementById("publicationForm").submit();
    }
}
window.onload = function() {
    let profileImage=document.getElementById("profileImage")
    profileImage.src="/static/upload/profile_pic.png?"+new Date().getTime();
    
}


    


