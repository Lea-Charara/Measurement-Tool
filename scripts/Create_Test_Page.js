
function showdb(){
    $.ajax({
        url: "https://measurementtoolbackend.herokuapp.com/databases/getdatabases/",
    
        dataType: "json",
        success: function( response ) {
            var databasetype = [];
                for(i = 0;i < response.length;i++){
                    console.log(response[i].dbtype_id);
                    $("#db ul li:last").after('<input class= "checkbox '+ response[i].dbtype_id+'" type="checkbox" onchange="TextBoxAppear()"/> '+response[i].name+'<br />');
                    if(!databasetype.includes(response[i].dbtype_id)){
                        databasetype.push(response[i].dbtype_id);
                        $("#QueriesContainer").append('<input class="queries '+ response[i].dbtype_id+ ' '+ response[i].name+'" type="text" placeholder='+ response[i].name +'><br />');
                    }

                }
            }
});
}


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
    alert("Please enter a valid timeout number")
    return false;
}

function TextBoxAppear()
{
    
    var nbofchecked = 0
    var index = document.getElementsByClassName("checkbox");
    var textboxestype = [];
    var textboxes = document.getElementsByClassName("queries");
    for(i=0;i<index.length;i++){
        if(index[i].checked){
            nbofchecked++;
            classname = $(index[i]).attr('class').split(' ')[1];
            console.log(classname);
            textboxestype.push(classname);
            document.getElementsByClassName("queries "+classname)[0].style.visibility = "visible";
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
    for(i=0;i<textboxes.length;i++){
        classname = $(textboxes[i]).attr('class').split(' ')[1];
        if(!textboxestype.includes(classname)){
            textboxes[i].style.visibility = "hidden";
        }
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
        $.ajax({
            type: "POST",
            url: "https://measurementtoolbackend.herokuapp.com/tests/addtest/",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify({ name: document.getElementById("TestNameField").value,
            description: document.getElementById("DescriptionField").value,
            repetition: document.getElementById("QueryNBField").value,
            timeout: document.getElementById("TimeoutField").value }),
            contentType: "application/json; charset=utf-8",
            success: function(){

                var textboxes = document.getElementsByClassName("queries");
                for(i=0;i<textboxes.length;i++){
                    if(textboxes[i].style.visibility == "visible"){
                        $.ajax({
                            type: "POST",
                            url: "https://measurementtoolbackend.herokuapp.com/dbtests/adddbtest/",
                            // The key needs to match your method's input parameter (case-sensitive).
                            data: JSON.stringify({ testid : document.getElementById("TestNameField").value,
                            dbid: $(textboxes[i]).attr('class').split(' ')[2], query : textboxes[i].value}),
                            contentType: "application/json; charset=utf-8",
                            success: function(){
                                var x = document.getElementById("snackbar");
                                x.className = "show";
                                setTimeout(function(){ x.className = x.className.replace("show", ""); window.location.href = 'tests.html'; }, 1500);
                                        
                    }
                });}
                
            }
                
        }
            
            });
        
        
    }
}

function Cancel(){
    var res = confirm("Are you sure you want to leave?")
    if(res == true){
        window.location.href = 'tests.html';
    }

}