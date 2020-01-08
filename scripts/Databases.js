
//https://measurementtoolbackend.herokuapp.com/databases/affectedtests/ returns a list the [0] is total of affected queries and [1] is those that will be left with no queries

//https://measurementtoolbackend.herokuapp.com/databases/getaffectedtests/ returns a list that contains 2 list the first one contains the name of the tests that will still have queries and the second list contains the name of the tests with no queries left

$(window).on('load',function(){
    $("#no_DBs").hide();
    $("#databases").hide();
    $("#newDB").hide();
    $.ajax({
        url: "https://measurementtoolbackend.herokuapp.com/databases/getdatabases/",
    
        dataType: "json",
        success: function( response ) {
            $("#loading").hide();
            if(response.length == 0){
                $("#no_DBs").show();
            }else{
                $("#databases").show();
                $("#newDB").show();
                for(i = 0;i < response.length;i++){
                    var Database = response[i][0];
                    var state = response[i][1];
                    $("#databases").append('<div class ="db " id="db-'+Database.id+'"><div class="inner"><p>'+Database.name+'</p><div><button type="button" class="button" id="edit" onClick="Edit('+Database.id+')" '+((state)? "disabled":"")+'><i class="fa fa-edit" style="font-size:20px;text-shadow:5px 4px 6px #000000;"></i></button><button type="button" id="delete" class="button" onclick="deletedb('+Database.id+')" style="color:red;" '+((state)? "disabled":"")+'><i class="fa fa-trash" style="font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button></div></div>')
                }
                if(response.length > 6)
                    $("#databases").mCustomScrollbar({
                        axis:"y",
                        theme: "minimal",
                        setHeight: "20%",
                        advanced: {updateOnContentResize: true},
                        scrollInertia: 60
                    });
            }
        },
        error:function(){
            $("#no_DBs").find("p").text("Connection error.");
            $("#no_DBs").show();
            $("#loading").hide();
        }
    });
    
});

function Edit(db_id){
    location.href='Edit_Database_Page.html?db_id='+db_id;
}

function deletedb(db_id){
    var db = $("#db-"+db_id);
    var dbs = $(db).siblings().length;
    var affected = 0;
    var noquery = 0;
    $.ajax({
        type: "POST",
        url: "https://measurementtoolbackend.herokuapp.com/databases/affectedtests/",
        data : { id : db_id},
        success: function( response ){
            if(response.length != 0){
                affected = response[0];
                noquery = response[1];

                Swal.fire({
                    title: `Are you sure you want to delete ${$(db).children().find("p").text()}?`,
                    html: ((affected != 0)? `<font size="+2">This action will ${((affected > noquery)? `affect <u>${affected} test/s</u>${((noquery !=0)? ` of which <u>${noquery}</u> will be left without a query and get deleted`:``)}.`:`delete <u>${noquery} test/s</u> that will be left without a query.</font>`)}`:""),
                    showCancelButton: true,
                    confirmButtonColor: 'rgb(0,136,169)',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes',
                    footer: ((affected!=0)? `<u><a href="affected_tests.html?db_id=${db_id}" style="color:#00aad4">More details</a></u>`:'')
                }).then((result) => {
                    if(result.value){
                      // $(db).children().find(".button").attr("disabled", true);
                        $(db).fadeOut(200, function() {
                            if(dbs <= 6)
                            $("#databases").mCustomScrollbar("destroy");
                        });
                        $.ajax({
                            type: "DELETE",
                            url: "https://measurementtoolbackend.herokuapp.com/databases/removedatabase/",
                            data : { id : db_id},
                            success: function(){
                                $(db).remove();
                            }
                        })  
                    }
                })
            }
        }
    })
}