$(function () {
  $('#myFor').click(modal_form);

});

  (function() {
            var dialog = document.getElementById('window');

            document.getElementById('show').onclick = function() {
                dialog.show();
            };
            document.getElementById('exit').onclick = function() {
                dialog.close();
            };

        })();







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

