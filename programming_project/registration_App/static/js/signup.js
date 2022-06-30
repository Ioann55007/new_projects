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



const error_class_name = "has-error"



function error_process(data) {
  $(".help-block").remove()
  let groups = ['#firstNameGroup', '#lastNameGroup', '#usernameGroup', '#emailGroup',  '#passwordGroup']
  for (let group of groups) {
    $(group).removeClass(error_class_name)
  };
  var element = document.getElementById('first_name');
  var html = element.outerHTML;
  var data = { html: html };
  var json = JSON.stringify(data);
  if (data.responseJSON.element) {
    help_block("#fistNameGroup", data.responseJSON.element)
  }
    var melement = document.getElementById('last_name');
    var html = melement.outerHTML;
    var data = { html: html };
    var json = JSON.stringify(data);
  if (data.responseJSON.melement) {
    help_block("#lastNameGroup", data.responseJSON.melement)
  }
  var nelement = document.getElementById('username');
  var html = nelement.outerHTML;
  var data = { html: html };
  var json = JSON.stringify(data);

  if (data.responseJSON.nelement) {
    help_block("#usernameGroup", data.responseJSON.nelement)
  }
  var zelement = document.getElementById('email');
  var html = zelement.outerHTML;
  var data = { html: html };
  var json = JSON.stringify(data);
 if (data.responseJSON.zelement) {
    help_block("#email", data.responseJSON.zelement)
  }
  var lelement = document.getElementById('password');
  var html = lelement.outerHTML;
  var data = { html: html };
  var json = JSON.stringify(data);
  if (data.responseJSON.lelement) {
    help_block("#password", data.responseJSON.lelement)
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
