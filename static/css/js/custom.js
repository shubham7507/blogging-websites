$('#my_form').submit(function(){
    var username = $('#username').val();
    if (username == ''){
       alert('please enter username');
       return false;
    }
