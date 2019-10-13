$("#databases").on('click','#delete', function(){});

$(window).on('load',function(){
    $.ajax({
        url: "https://measurementtoolbackend.herokuapp.com/databases/getdatabases/",
    
        dataType: "json",
        success: function( response ) {
            if(response.length == 0){
                $("#no_DBs").show();
                $("#databases").hide();
                $("#newDB").hide();
            }else{
                $("#no_DBs").hide();
                $("#databases").show();
                $("#newDB").show();
                for(i = 0;i < response.length;i++){
                    
                    var Database = response[i];
                    $("#databases").append('<div class ="db" id="db-'+Database.id+'"><div class="inner"><p>'+Database.name+'</p><div><a id="edit" href="Create_Database_Page.html"><i class="fa fa-edit" style="font-size:20px;text-shadow:5px 4px 6px #000000;"></i></a><button type="button" id="delete" class="button"><i class="fa fa-trash" style="color:red;font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button></div></div>')
                }
                $(".databases").mCustomScrollbar({
                    axis:"y",
                    theme: "minimal",
                    setHeight: "20%"
                });
            }
        }     
    });
    
});