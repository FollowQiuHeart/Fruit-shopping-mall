$.get(url="/index/check_login",function(res){
    if (res.login_state == 1){
        window.location.href = "/index/"
    }
})