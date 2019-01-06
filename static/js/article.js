function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// 2.定义不需要csrftoken的请求方式
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

let csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function add_col(obj) {
    let index = layer.open({
        type: 1,
        skin: 'layui-lay-rim',
        area: ['400px', '200px'],
        title: '新增栏目',
        content: "<div class='text-center' style='margin-top: 20px'><label for='new_column'>请输入新的栏目名称: </label><input type='text' id='new_column' ></div>",
        btn: ['确定', '取消'],
        yes: function (index, layer) {
            let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

            $.post($(obj).data('href'), {
                "column": $('#new_column').val().trim(),
                'csrfmiddlewaretoken': csrf_token
            }, function (res) {
                if (res.code === 200) {
                    parent.location.reload();
                    layer.msg(res.msg)
                } else if (res.code === 400) {
                    layer.msg(res.msg)
                }
            });
        },
        no: function (index, layer) {
            layer.close(index);
        }
    });
}


function edit_col(obj) {
    let column = $(obj).parent().prev('td').text();
    let url = $(obj).parent().data('url');
    let index = layer.open({
        type: 1,
        skin: 'layui-lay-rim',
        area: ['400px', '200px'],
        title: '编辑栏目',
        content: "<div class='text-center' style='margin-top: 20px'><label for='new_column'>请输入新的栏目名称: </label><input type='text' id='edit_column' value='" + column + "'></div>",
        btn: ['确定', '取消'],
        yes: function (index, layer) {
            let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

            $.post(url, {"column": $('#edit_column').val().trim(), 'csrfmiddlewaretoken': csrf_token}, function (res) {
                if (res.code === 200) {
                    parent.location.reload();
                    layer.msg(res.msg)
                } else if (res.code === 400) {
                    layer.msg(res.msg)
                }
            });
        },
        no: function (index, layer) {
            layer.close(index);
        }
    });
}

function del_col(obj) {
    let id = $(obj).parent().data('id');
    let url = $(obj).parent().data('del_url');
    let ind = layer.confirm('是否确认删除？', {
        btn: ['确认', '取消'], icon: 3
    }, function (index, layero) {
        $.ajax({
            url: url,
            type: "DELETE",
            data: {id: id,},
            success: function (res) {
                if (res.code === 200) {
                    $(obj).parents('tr').remove();
                    // parent.location.reload();
                    layer.close(ind);
                } else {
                    layer.alert(res.msg)
                }

            }
        })
    }, function () {
        layer.close(ind);
        return false;
    });
}


function article_post(obj) {
    let url = $(obj).data('action');
    let title = $('#id_title').val().trim();
    let body = $('#id_body').val().trim();
    let column = $('#which_column').val().trim();
    if (!title || !body || !column) {
        layer.alert('请完整填写内容', {icon: 5});
    }

    $.post(url, $(obj).serializeArray(), function (res) {
        if (res.code === 200) {
            layer.msg(res.msg, {icon: 6})
            if (res.url) {
                window.location.href = res.url;
            }
        } else {
            layer.alert(res.error, {icon: 3})
        }
    });
}

function review(pk, feedback, url) {
    $.post(url, {'pk': pk, 'action': feedback}, function(res){
       console.log(res);
       $('.thumb-up-count').each(function(){
           $(this).text(res.count);
       });
       if (res.code === 200) {
           layer.msg(res.msg, {icon: 6},1000);
       } else {
           layer.msg(res.msg, {icon: 5},1000);
       }

    });
}

function submitComment(obj, url){
    $.post(url, $(obj).serializeArray(), function(res){
        console.log(res);
        if (res.code === 200) {
            $('.no-comment').remove();
            layer.msg(res.msg, {icon: 6})

            let text = `
                <div>
                    <p><strong>` + res.data.name +`</strong></p>
                    <p style="margin-left:40px">`+ res.data.body +`</p>
                </div>
            `;
            $(obj)[0].reset();
            $('#comments').append(text)
        } else {
            layer.msg(res.msg, {icon: 5}, 1000)
        }
    });
}


$('#article-post-form').on('submit', function () {
    event.preventDefault();
    article_post(this);
});


$('.add-column').on('click', function () {
    add_col(this);
});

$('.del-post').on('click', function () {
    del_col(this)
});


$('.edit-column').on('click', function () {
    edit_col(this);
});


$('.del-column').on('click', function () {
    del_col(this);
});

$('.thumb-up').on('click', function(){
    let url = $(this).parent().data('url')
    let pk = $(this).parent().data('id')
    if($(this).hasClass('thumb-up')){
        review( pk, 'like', url);
    } else {
        review( pk, 'unlike', url);
    }
});

$('.thumb-down').on('click', function(){
    let url = $(this).parent().data('url')
    let pk = $(this).parent().data('id')
    if($(this).hasClass('thumb-up')){
        review( pk, 'like', url);
    } else {
        review( pk, 'unlike', url);
    }
});

$('#comment_form').on('submit', function(){
    event.preventDefault();
    let url = $(this).find('.btn').data('action');
    submitComment(this, url);
})