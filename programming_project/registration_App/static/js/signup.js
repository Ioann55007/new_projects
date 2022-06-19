$(function () {
  $('#signUpForm').submit(singUp);
});

const error_class_name = "has-error"



function singUp(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      window.location.href = form.data('href');
    },
    error: function (data) {
      error_process(data);
    }
  })
}

function error_process(data) {
  $(".help-block").remove()
  let groups = ['#email', '#password',  '#first-name', '#last-name']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.email) {
    help_block("#email", data.responseJSON.email)
  }
  if (data.responseJSON.password1) {
    help_block("#password", data.responseJSON.password1)
  }

  if (data.responseJSON.first_name) {
    help_block("#first-name", data.responseJSON.first_name)
  }
  if (data.responseJSON.last_name) {
    help_block("#last-name", data.responseJSON.last_name)
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
