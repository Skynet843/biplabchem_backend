function uploadImage(){
    let imageInput=document.getElementById('customFile')
    
    if (imageInput.value==""){
        alert("Please Fill Require Data...")
    }else{
        document.getElementById('form1').submit()
    }
}
window.onload = function() {
    let profileImage=document.getElementById("profileImage")
    profileImage.src="/static/upload/profile_pic.png?"+new Date().getTime();
    
}




