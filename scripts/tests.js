var intervals = {};

// Edit button

function Edit(test_id){
    location.href = "Edit_Test_Page.html?var="+test_id;
}

//  View Button

function View(test_id){
    location.href = "View_Tests.html?test_id="+test_id;
};

//  Delete Button

function DeleteTest(test_id){
    var test = $("#test-"+test_id);

    Swal.fire({
        title: `Are you sure you want to delete ${$(test).children().find("p").text()}?`,
        showCancelButton: true,
        confirmButtonColor: 'rgb(0,136,169)',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if(result.value){
          // $(test).children().find(".button").attr("disabled", true);
            $(test).fadeOut(200);
            $.ajax({
                type: "DELETE",
                url: "https://measurementtoolbackend.herokuapp.com/tests/removetest/",
                data : { id : test_id},
                success: function(){
                    $(test).remove();
                }
            })  
        }
    })
}

//  Start Button
function StartTest(test_id){
    done = 0;
    var elems = $("#test-"+test_id).children();
    var bar = $(elems).find("#barDiv").children()[0];
    var prog = $(elems).find("#prog");
    
    try{
    //  New start
    if($(bar).hasClass("loadbar"))    
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "https://measurementtoolbackend.herokuapp.com/tests/begintest/",
            data : JSON.stringify({id : test_id}),
            contentType: "application/json; charset=utf-8"
        })
    //  Unpause
    else if($(bar).hasClass("paused"))
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "https://measurementtoolbackend.herokuapp.com/tests/continuetest/",
            data : JSON.stringify({id : test_id}),
            contentType: "application/json; charset=utf-8"
        })

    $(elems).find("#start").attr("disabled", true);
    $(elems).find("#pause").attr("disabled", false);
    $(elems).find("#stop").attr("disabled", false);
    $(elems).find("#delete").attr("disabled", true);
    $(elems).find("#edit").attr("disabled", true);
    $(bar).removeClass("loadbar paused stopped").addClass("started");
    done = UpdateTest(test_id);
    intervals[test_id] = setInterval(function() {
        if(done!= 100){
            done = UpdateTest(test_id);
            $(bar).css('width', done + '%');
            $(prog).text(done * 1  + '%');
        }
        else
        {
            clearInterval(intervals[test_id]);
            intervals[test_id] = null;
            $(elems).find("#start").hide();
            $(elems).find("#pause").hide();
            $(elems).find("#stop").hide();
            $(elems).find("#edit").attr("disabled", false);
            $(elems).find("#restart").show();
        } 
    }, 1);
}
    catch(e){
        console.log(e);
    }
}

//  Restart
function RestartTest(test_id) {
    // Placeholder
    var elems = $("#test-"+test_id).children();
    $(elems).find("#start").show();
    $(elems).find("#pause").show();
    $(elems).find("#stop").show();
    $(elems).find("#edit").attr("disabled", true);
    $(elems).find("#restart").hide();
}


//  Pause Button
function PauseTest(test_id) {
    var elems = $("#test-"+test_id).children();
    var bar = $(elems).find("#barDiv").children()[0];
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "https://measurementtoolbackend.herokuapp.com/tests/abletorun/",
        data : JSON.stringify({id : test_id}),
        contentType: "application/json; charset=utf-8"
    })
    $(elems).find("#pause").attr("disabled", true);
    $(elems).find("#start").attr("disabled", false);
    $(elems).find("#stop").attr("disabled", false);
    $(elems).find("#delete").attr("disabled", false);
    clearInterval(intervals[test_id]);
    $(bar).removeClass("loadbar started stopped").addClass("paused");
}

//  Stop Button
function StopTest(test_id) {
    var elems = $("#test-"+test_id).children();
    var bar = $(elems).find("#barDiv").children()[0];
    var prog = $(elems).find("#prog");
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "https://measurementtoolbackend.herokuapp.com/tests/stoptest/",
        data : JSON.stringify({id : test_id}),
        contentType: "application/json; charset=utf-8"
    })

    $(elems).find("#stop").attr("disabled", true);
    $(elems).find("#start").attr("disabled", true);
    $(elems).find("#pause").attr("disabled", true);
    $(elems).find("#edit").attr("disabled", false);
    $(elems).find("#delete").attr("disabled", false);
    $(bar).removeClass("loadbar started paused").addClass("stopped");

    clearInterval(intervals[test_id]);
    setTimeout(function(){
    $(bar).fadeOut();
    $(bar).css('width', '0%'); 
    $(prog).text('0%'); 
    $(bar).removeClass("stopped started paused").addClass("loadbar");
    $(bar).fadeIn();
    $(elems).find("#start").attr("disabled", false);
    }, 355);

}

//  Percentage of queries completed
function UpdateTest(test_id){
    var done = 0;
    $.ajax({
        async: false,
        type: "POST",
        url: "https://measurementtoolbackend.herokuapp.com/tests/progress/",
        data : JSON.stringify({id : test_id}),
        contentType: "application/json; charset=utf-8",
        success: function(response) {
            done = response
        }
    })
    return done;   
}

$(window).on("load",function(){
    $("#no_tests").hide();
    $("#tests").hide();
    $("#newTest").hide();
    $.ajax({
        url: "https://measurementtoolbackend.herokuapp.com/tests/gettests/", //https://measurementtoolbackend.herokuapp.com/ http://127.0.0.1:8000/
        dataType: "json",
        success: function( response ) {
            $("#loading").hide();
            if(response.length == 0){
                $("#no_tests").show();
            }else{
                $("#tests").show();
                $("#newTest").show();
                for(i = 0;i < response.length;i++){
                    var test = response[i]; //style="padding-left: 89%;"
                    intervals[test.id]=null;

                    $("#tests").append('<div class ="test" id="test-'+test.id+'"><div class="up"><p>'+test.name+'</p><button type="button" id="delete" class="button" onclick="DeleteTest('+test.id+')" style="float: right; color: red;"><i class="fa fa-times" style="font-size:20px;text-shadow:5px 4px 6px #000000;"></i></button></div><div class="inner"><div class="loadbar w3-round-xlarge" id="barDiv" style="width: 70%"><div id="bar" class="'+((test.Progress > 0 && test.Progress < 100)? "paused" : (test.Progress == 100)?"started":"loadbar")+' w3-round-xlarge" style="width:'+test.Progress+'%;height: 20px; padding:0"></div></div>&emsp;<span id="prog" style="width:5%;">'+test.Progress+'%</span>&emsp;<button type="button" id="start" class="button" onclick="StartTest('+test.id+')"'+((test.Progress == 100)?'style="display:none;"':'')+'><i class="fa fa-play" style="font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button><button type="button" id="pause" class="button" onclick="PauseTest('+test.id+')"'+((test.Progress == 100)?'style="display:none;"':'')+' disabled><i class="fa fa-pause" style="font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button><button type="button" id="stop" class="button" onclick="StopTest('+test.id+')"'+((test.Progress == 100)?'style="display:none;"':(test.Progress == 0)?"disabled":'')+'><i class="fa fa-stop" style="font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button><button type="button" id="restart" class="button" onclick="RestartTest('+test.id+')"'+ ((test.Progress != 100)?'style="display:none;"':'')+'><i class="fa fa-repeat" style="font-size:17px;text-shadow:5px 4px 6px #000000;"></i></button>&emsp;&emsp;<button type="button" id="edit" class="button" onClick="Edit('+test.id+')"'+((test.Progress > 0 && test.Progress < 100)? "disabled":"")+'><i class="fa fa-edit" style="font-size:20px;text-shadow:5px 4px 6px #000000;"></i></button><button type="button" id="view" class="button" onClick="View('+test.id+')"><i class="fa fa-eye" style="font-size:20px;text-shadow:5px 4px 6px #000000;"></i></button></div>');
                    if(test.Progress > 0 && test.Progress < 100)
                    PauseTest(test.id);
                }
            }
            $(".tests").mCustomScrollbar({
                axis:"y",
                theme: "minimal",
                setHeight: "20%"
            });
        },        
        error:function(){
            $("#no_tests").show();
            $("#loading").hide();
        }
        
    });  
    
});