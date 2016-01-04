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

// back button and hashes
function pushHistory(hash) {
  if(history.pushState)
    history.pushState({}, document.title, '#'+hash);
  else
    location.hash = hash;
}
// modal
$('div.modal').on('show.bs.modal', function() {
  pushHistory('mod_'+this.id);
});
// tab
$('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
  pushHistory('tab_'+$(e.target).attr('href').substr(1))
});
// on hash change
window.onhashchange = function() {
  if(location.hash.substr(1, 3) == 'tab') {
    $('a[href="#' + location.hash.substr(5) + '"]').tab('show')
    $('div.modal').modal('hide');
  }
  else if(location.hash.substr(1, 3) == 'mod')
    ;// $('#' + location.hash.substr(5)).modal('show')
  else {
    $('div.modal').modal('hide');
    $('.tab-first').tab('show');
  }
}
// at load
if (location.hash !== '')
  window.onhashchange()

// called at load and after a modal loading
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
