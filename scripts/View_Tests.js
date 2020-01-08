var url = window.location.href
var id = url.substring(url.lastIndexOf('=') + 1);

var today = new Date();




$(window).on('load',function(){

  $.ajax({
    url: "http://127.0.0.1:8000/dbtests/Times/",
    type:"POST",
    data:{testid: id},
    dataType:"json",
    beforeSend: function(x) {
      if (x && x.overrideMimeType) {
        x.overrideMimeType("application/j-son;charset=UTF-8");
      }
    },
    success: function(response) {
      $("#description").append('<h2>Description: '+response.Descriptions+'</h2>');
      $("#Test_name").append('<p>'+response.test_name+'<p>');
          console.log(response);
         for(i=0;i<response.db_name.length;i++)
         {
          var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
          
          var dateTime = date;
         
         $("#Database_name").append('<div  class="col"><p>'+response.db_name[i]+'</p><br/><div class="column Last"align="Center"><p align="left" id="rcorners1">'+response.test_query[i]+'</p><br/><br/><table style="width: 100%; height: 50%" ><tr><th>Loading</th> <th>Time</th></tr><tr><td><div class="loadbar w3-round-xlarge" id="barDiv" style="width: 100%;height:20px"><div id="bar" class="started w3-round-xlarge" style="width:50%;height: 20px"></div></div></td><td align="center" id="time" >'+response.Test_Duration[i]+'</td></tr></table><div class="row"><div id="done date" class="colu" ><h2>Test date</h2><p>'+dateTime+'</p></div><div id="Repetition" class="colu" ><h2>Repetition</h2><p>'+response.NB_Query[i]+'</p></div><div id="Average" class="colu" ><h2>Average time of the query</h2><p>'+response.average[i]+'</p></div></div></div></div>');
          UpdateTest(id);
         }
    }

  
   



  });
  

});


function openTab(tabName) {
  var i, x;
  x = document.getElementsByClassName("containerTab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(tabName).style.display = "block";
}

function UpdateTest(id){
  var done =100;
  $.ajax({
    url: "https://127.0.0.1:8000/dbtests/GetProgress/",
    type:"POST",
    data:{testid: id},
    dataType:"json",

    success: function(response) {

      done = response.prog;
      
    },
    error:function(errors){
      if(errors.status==400){
        connectionError();
      }
      if(errors.status==404){
        DeletedTestError();
      }
      
     $(bar).css('width', done + '%');
      
    }
    

  });

}


function connectionError(){
  if(!err){
      err = true;
      Swal.fire({
          title: `Connection Error`,
          html: 'Please check your internet connection and try again.<br><br><b>The page will now reload.</b>'
      }).then(() => {
          window.location.reload()
      });
  }
}


function DeletedTestError(){
  if(!err){
      err = true;
      Swal.fire({
          title: `The test has been deleted`,
          html: 'The page will now reload.</b>'
      }).then(() => {
          window.location.reload()
      });
  }
}