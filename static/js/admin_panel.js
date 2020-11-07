function uploadImage(){
    let imageInput=document.getElementById('customFile')
    
    if (imageInput.value==""){
        alert("Please Fill Require Data...")
    }else{
        document.getElementById('form1').submit();
    }
}
function check_input(){
        document.getElementById("publicationForm").submit();
}
function uploadImageGallery(){
    console.log("TRest")
    let imageInput=document.getElementById('customFileGallery')
    
    if (imageInput.value==""){
        alert("Please Fill Require Data...")
    }else{
        document.getElementById('addGalleryForm').submit();
    }
}
// function uploadImageResearch(){
//     console.log("TRest")
//     let imageInput=document.getElementById('customFileResearch')
    
//     if (imageInput.value==""){
//         alert("Please Enter the Research Image...")
//     }else{
//         document.getElementById('addGalleryForm').submit();
//     }
// }
window.onload = function() {
    let profileImage=document.getElementById("profileImage")
    profileImage.src="/static/upload/profile_pic.png?"+new Date().getTime();
    
}



    


