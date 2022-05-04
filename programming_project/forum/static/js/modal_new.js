$(function () {
  $('#myFor').click(modal_form);

});

function modal_form(e) {

  e.preventDefault();
  let button = $(this)
  $.ajax({
    type: 'GET',
    url: button.data('onclick'),
    success: function (data) {
     console.log('success', data)
     },
    error: function (data) {
     console.log('error', data)
     }
  })
}

