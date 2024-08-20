//Navbar

var style = "style";

function hideIconBar(){
    console.log("!!!");
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute(style, "display:none");
    navigation.classList.remove("hide");
}

function showIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute(style, "display:block");
    navigation.classList.add("hide");
}

function showComment() {
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.toggle("hide");
}


function showReply(id){
    var replyArea = document.getElementById(id);
    replyArea.classList.toggle("hide");
}