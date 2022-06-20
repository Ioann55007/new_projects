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
  let groups = ['#firstNameGroup', '#lastNameGroup', '#usernameGroup', '#emailGroup',  '#passwordGroup']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.first_name) {
    help_block("#fistNameGroup", data.responseJSON.first_name)
  }

  if (data.responseJSON.last_name) {
    help_block("#lastNameGroup", data.responseJSON.last_name)
  }
  if (data.responseJSON.username) {
    help_block("#usernameGroup", data.responseJSON.username)
  }
 if (data.responseJSON.email) {
    help_block("#email", data.responseJSON.email)
  }
  if (data.responseJSON.password) {
    help_block("#password", data.responseJSON.password)
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
