let params = new URLSearchParams(location.search);
db_id = params.get('db_id');
const Toast = Swal.mixin({
    toast: true,
    position: 'bottom',
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true
});

function Cancel(){
    location.href = "Databases.html";
}

function Delete(){      
    $.ajax({
        type: "DELETE",
        url: "https://measurementtoolbackend.herokuapp.com/databases/removedatabase/",
        data : { id : db_id},
        success: function(){
            Toast.fire({
                title: 'Database Deleted'
            }).then(() => { location.href = 'Databases.html';});
        }
    })
}


$(window).on('load',function(){
    if(db_id)
    $.ajax({
        type: "POST",
        url: "https://measurementtoolbackend.herokuapp.com/databases/getaffectedtests/",
        data: JSON.stringify({id : db_id}),
        contentType: "application/json",
        success: function(response){
            affected = response[0];
            noquery = response[1];
            if(affected.length == 0 && noquery.length == 0)
                location.href = "Databases.html";
            if(affected.length != 0){
                for(i = 0; i< affected.length; i++)
                    $("#affected-tests").append(`<div class="test"><span>${affected[i]}</span></div>`);
                $("#affected-container").show();
            }
            if(noquery.length != 0){
                for(i = 0; i< noquery.length; i++)
                    $("#noquery-tests").append(`<div class="test"><span>${noquery[i]}</span></div>`);
                $("#noquery-container").show();
            }
        }
    });
    else
    location.href = "Databases.html";
})