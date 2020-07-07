$('#myForm').submit(function(e){
    e.preventDefault();
    $.ajax({
        url:'/Car/Edit/17/',
        type:'post',
        data:$('#myForm').serialize(),
        success:function(){
            //whatever you wanna do after the form is successfully submitted
        }
    });
});
