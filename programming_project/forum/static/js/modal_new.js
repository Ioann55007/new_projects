$(function () {
  $('#myFor').click(modal_form);

});
$(function () {
  $('.click me').click(mod_for);

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

function mod_for(e) {

  e.preventDefault();
  let button = $(this)
  $.ajax({
    type: 'GET',
    url: button.data('id'),
    success: function (data) {
     console.log('success', data)
     },
    error: function (data) {
     console.log('error', data)
     }
  })
}



(function() {
            var dialog = document.getElementById('wqo');
            document.getElementById('sw').onclick = function() {
              dialog.show();
            };
            document.getElementById('clos').onclick = function() {
              dialog.close();
            };

        })();