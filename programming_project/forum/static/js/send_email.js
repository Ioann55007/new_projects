$(function () {
  $('#send_emailForm).submit(singUp);
});


function singUp(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
     console.log('success', data)
     },
    error: function (data) {
     console.log('error', data)
     },
  })
}