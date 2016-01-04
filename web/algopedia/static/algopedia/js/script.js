$('#modal_implementation_detail').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget)
  var id = button.data('implementation-id')
  var modal = $(this)
  modal.find('.modal-title .modal-title-user').html(button.data('implementation-user'))
  modal.find('.modal-title .modal-title-lang').html(button.data('implementation-lang'))
  modal.find('.modal-body').html('<p>loading...</p>')
  modal.find('.modal-footer a').attr('href', button.attr('href'))
  $.ajax('/ajax/implementation/' + id)
    .done(function(data) {
      modal.find('.modal-body').html(data)
      init()
    })
    .fail(function() {
      modal.find('.modal-body').html('<div class="alert alert-danger">Error during loading page !<br>You may try to reload the page or go directly <a href="/implementation/' + id + '">there</a>.</div>');
    })

})

// back button close an opened modal https://gist.github.com/thedamon/9276193
$('div.modal').on('show.bs.modal', function() {
  var modal = this;
  window.location.hash = modal.id;
  window.onhashchange = function() {
    if (!location.hash)
      $(modal).modal('hide');
  }
});
$('div.modal').on('hide.bs.modal', function() {
  history.pushState('', document.title, window.location.pathname);
});

function init() {
  // star checkboxes
  $("input:checkbox.checkbox_star").change(function() {
    id=parseInt($(this).attr('name').split('_')[1])
    state = $(this).is(":checked")
    $.ajax({
      url: '/ajax/star/' + (state ? 'add/' : 'remove/') + id,
      type: 'GET',
    })
    .done(function(data){
      // update other checkboxes with same id
      $("input:checkbox.checkbox_star[name=star_"+id+"]").prop("checked", state)
    })
    .fail(function() {
      // reset
      $("input:checkbox.checkbox_star[name=star_"+id+"]").prop("checked", !state)
      alert("An error occured :-( Please try again later")
    })
  });
}
init();
