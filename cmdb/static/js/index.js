
$(document).on("click",".bom_regit",function (){
        $('#Modal_reg').modal('show');
    });

$(document).on("click",".bom_login",function (){
        $('#Modal_login').modal('show');
    });

// $(document).on("click",".sec_code",function () {
//     var reg_email = $("#email").val();
//          $.post("/reg/",
//     {
//       email:reg_email
//     });
//         var count = 60;
//         $(this).text( count + "s");
//         var countdown = setInterval(down,1000);
//         function down() {
//             count--;
//             $(".sec_code").text( count + "s");
//             if (count == 0) {
//                          $(".sec_code").text("发送验证码");
//                         clearInterval(countdown);
//                     }
//         }
//   });
//

//鼠标离开email的input框时触发判断事件
$('#email').blur(function () {
    var email = $(this).val();
    if (!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/))
  {
      $("#email_error").text("格式不正确！请重新输入");
         $("#email").addClass("border_color_red");
  }
    else
    {
         $("#email_error").text("");
         $("#email").addClass("border_color_green");
    }


});

//点击发送验证码时触发事件
$(document).on("click",".sec_code",function () {
    var reg_email = $("#email").val();

     if (!reg_email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/))
  {
      $("#email_error").text("格式不正确！请重新输入");
       $("#email").addClass("border_color_red");

  }
    else {
         var post_data = {
             email: reg_email
         };
//ajax post请求检查email是否被注册
         $.ajax({
             url: '/check/',
             type: "POST",
             data: post_data,
             success: function (data) {
                 data = JSON.parse(data);
                 if (data["status"] == 1) {
                     $("#email_error").text(data["result"]);
                 } else {

                      var count = 60;
                      $(".sec_code").text(count + "s");
                      var countdown = setInterval(down,1000);
                      function down() {
                             count--;
                              $(".sec_code ").text(count + "s");
                             // $(".sec_code").text( count + "s");
                             if (count == 0) {
                                   $(".sec_code").text("发送验证码");
                                   clearInterval(countdown);
                    }
        }
                 }
             }
         });
     }
});


//鼠标离开username的input框时触发判断事件
$('#username').blur(function () {
    var username = $("#username").val();
      var post_data = {
            username:username
         };
    vali_ajax('/validate_name/',post_data,'#username','#username_error')

});



//鼠标离开password的input框时触发判断事件
$('#password').blur(function () {
    var password = $("#password").val();
    if (password.length<6 || password.length >8){
         $("#pwd_error").text("密码长度必须6到8位");
        $("#password").addClass("border_color_red");
    }
    else {
                        $("#pwd_error").text("");
                        $("#password").addClass("border_color_green");
            }

});

//鼠标离开code的input框时触发判断事件
$('#code').blur(function () {
    var email = $("#email").val();
    var code = $("#code").val();
    if (code.length !== 6 ){
         $("#code_error").text("验证码为6位");
         $("#code").addClass("border_color_red");
    }
    else {
            post_data = {email:email,code:code};
             vali_ajax('/validate_code/',post_data,'#code','#code_error');

            }

});


//注册提交按钮，判断所有error框是否为空，判断所有input是否为空，
$(document).on("click","#reg_submit",function () {

        flag = 0
        $(".reg_content").each(function () {
            if (!$(this).val()) {
                $(this).parents().next(".reg_error").text("不能为空！");
                flag = 1;
                return false;
            }
        });

    $(".reg_error").each(function () {
        if ($(this).text()){
            $(this).text($(this).text());
            flag = 1;
            return false;
        }
    });
    if (flag == 0) {
        // $("#reg_form").submit()

           post_data = {
               email:$("#email").val(),
               username:$("#username").val(),
               password:$("#password").val()
           };

        //ajax 传值
         $.ajax( {
            url:'/reg/',
            type:"POST",
            data:post_data,
            success:function (data) {
            data = JSON.parse(data);
            if (data["status"] == 1) {

                $("#reg_form").text(data["result"]);
                 // $("#username").addClass("border_color_red");
            } else {
                 $("#reg_form").text(data["result"]);

            }
        }
    });
        //ajax传值
    }
});


function vali_ajax(url,post_data,input,input_error) {
      $.ajax( {
            url:url,
            type:"POST",
            data:post_data,
            success:function (data) {
            data = JSON.parse(data);
            if (data["status"] == 1) {
                $(input_error).text(data["result"]);
                 $(input).addClass("border_color_red");
            } else {
                        $(input_error).text("");
                        $(input).addClass("border_color_green");
            }
        }
    });
}