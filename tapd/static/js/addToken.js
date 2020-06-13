    /**
 * Created by wawa on 6/11/20.
 */
window.οnlοad=function(){
    //回车键提交表单登录
        $(document).ready(function() {
            $(document).keydown(function(event) {
                //keycode==13为回车键
                if (event.keyCode == 13) {
                        $('#submit').addClass('disabled');
                        $('#submit').prop('disabled', true);
                    addToken();
                }
            });
        });

$('#submit').click(function(){
	$('#submit').addClass('disabled');
	$('#submit').prop('disabled', true);
	addToken();
});

function addToken() {
	var txt_projectName = $('#txt_projectName');
	var txt_projectId = $('#txt_projectId');
    var txt_robotToken = $('#txt_robotToken');
	var txt_createUser = $('#txt_createUser');
    $.ajax({
        type: "post",
        url: "/add_pro_token/",
        contentType: "application/json",
        dataType: "json",
        data_dict: {
			projectName: txt_projectName.val(),
            projectId: txt_projectId.val(),
            robotToken: txt_robotToken.val(),
            userName: txt_createUser.val()
        },
        complete: function () {
        	$('#submit').removeClass('disabled');
        	$('#submit').prop('disabled', false);
        },
        success: function (data) {
			if (data.status == 0) {
				$(location).attr('href','/projects/');
			} else {
				$('#wrongpwd-modal-body').html(data.msg);
				$('#wrongpwd-modal').modal({
        			keyboard: true
    			});
			}
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
        }
    });
};
}