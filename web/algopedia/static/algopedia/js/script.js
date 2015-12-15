$('#modal_implementation_detail').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('implementation-id') // Extract info from data-* attributes
  var modal = $(this)
  modal.find('.modal-title .modal-title-user').html(button.data('implementation-user'))
  modal.find('.modal-title .modal-title-lang').html(button.data('implementation-lang'))
  modal.find('.modal-body').html("<p>loading...</p>")
  $.ajax('/ajax/implementation/' + id)
    .done(function(data) {
      modal.find('.modal-body').html(data)
    })
    .fail(function() {
      modal.find('.modal-body').html('<div class="alert alert-danger">Error during loading page !<br>You may try to reload the page or go directly <a href="/implementation/' + id + '">there</a>.</div>');
    })

})
