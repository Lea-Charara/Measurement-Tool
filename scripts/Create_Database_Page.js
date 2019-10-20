function myFunction() {
    var x = document.getElementById("myInput");
    if (x.type === "password") {
    x.type = "text";
    } else {
    x.type = "password";
    }
 }

 function CheckedType(){
       var types = document.getElementsByClassName("radio");
       for (i=0;i<types.length;i++){
             if (types[i].checked){
                   return types[i].value
             }

       }
 }
    function CheckFields(){
    
    var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    var a = document.getElementById("myInput");
    var b = document.getElementById("InputUser");
    var c = document.getElementById("InputPort");
    var d = document.getElementById("InputHost");
    var e = document.getElementById("InputName");
    var IpAddr=d.value;
   if (a.value.length == 0 || b.value.length == 0 || e.value.length == 0)
   {
         alert("Not all fields have been entered")
         
   }
   else if(isNaN(c.value)) 
   {
         alert("Port Field is not a valid number")
   }
   else if(!IpAddr.match(ipformat))
   {
        alert("Host is not a valid IP Address")
   }
   else
   {
         console.log(CheckedType())
      $.ajax({
            type: "POST",
            url: "measurementtoolbackend.herokuapp.com/databases/adddatabase/",
            // The key needs to match your method's input parameter (case-sensitive).
            data:JSON.stringify({name:document.getElementById("InputName").value,
            user: document.getElementById("InputUser").value,
            dbtype: CheckedType(),
            password: document.getElementById("myInput").value,
            host: document.getElementById("InputHost").value,
            port:  document.getElementById("InputPort").value}),
            
      
                  
            contentType: "application/json; charset=utf-8",
            success: function(){
                  var x = document.getElementById("snackbar");
                  x.className = "show";
                  setTimeout(function(){ x.className = x.className.replace("show", ""); window.location.href = 'Databases.html'; }, 1500);
    

   }

 }
      )}}