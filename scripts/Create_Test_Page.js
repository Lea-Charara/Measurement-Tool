function checkName(){
    if(document.getElementById("TestNameField").value.length > 0){
        return true;
    }
    alert("Please enter a Name");
    return false;
    
}

function checkQueryNB(){
    if(document.getElementById("QueryNBField").value.length > 0 && document.getElementById("QueryNBField").value <= 30 && document.getElementById("QueryNBField").value > 0){
        return true;
    }
    alert("Number of query repetitions should be less than 30");
    return false;
}

function checkTimeout(){
    if(document.getElementById("TimeoutField").value.length > 0 && document.getElementById("TimeoutField").value > 0){
        return true;
    }
    return false;
}

function TextBoxAppear()
{
    
    var nbofchecked = 0
    var index = document.getElementsByClassName("checkbox");
    var textboxes = document.getElementsByClassName("queries");
    console.log(textboxes.length);
    for(i=0;i<index.length;i++){
        if(index[i].checked){
            nbofchecked++;
         }
    }
    if(nbofchecked>0){
        
        document.getElementById("QueryLabel").style.visibility = "visible";
        document.getElementById("QueriesContainer").style.visibility = "visible";

    }
    else{
        document.getElementById("QueryLabel").style.visibility = "hidden";
        document.getElementById("QueriesContainer").style.visibility = "hidden";

    }
    console.log(nbofchecked);
    for(i=0;i<nbofchecked;i++){
       textboxes[i].style.visibility = "visible";
    }
    for(i=nbofchecked;i<textboxes.length;i++){
        textboxes[i].style.visibility = "hidden";
    }
}

function checkQueries(){
    var nbofchecked = 0;
    var nbofentered = 0;
    var textboxes = document.getElementsByClassName("queries");
    for(i=0;i<textboxes.length;i++){
        if(textboxes[i].style.visibility=="visible"){
            nbofchecked++;
            if(textboxes[i].value.length > 0){
                nbofentered++;
            }
         }
    }
    console.log(nbofchecked +" "+ nbofentered )
    if(nbofchecked == 0){
        alert("Please choose at least one of the available databases");
        return false;
    }
    if(nbofentered == nbofchecked){
        return true;
        
    alert("please enter all the queries fields");
    return false;
}
}
function checkAll(){
    if(checkName() && checkQueryNB() && checkTimeout() && checkQueries()) 
    {
        localStorage.clear();
        if (typeof(Storage) !== "undefined") {
            if(localStorage.length == 0){
                localStorage.setItem(localStorage.length,[document.getElementById("TestNameField").value])
                
            }
            else{
                localStorage.setItem(localStorage.length,[document.getElementById("TestNameField").value])
            }
    }
        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); window.location.href = 'tests.html'; }, 1500);

    }
}

function Cancel(){
    var res = confirm("Are you sure you want to leave?")
    if(res == true){
        window.location.href = 'tests.html';
    }

}