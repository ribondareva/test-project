$(document).ready(function () {
  $('.dropdown-toggle').click(function (e) {
    let $parent = $(this).parent();
    if ($parent.hasClass('show')) {
      $parent.removeClass('show');
      $parent.find('.dropdown-menu').removeClass('show');
    } else {
      $parent.addClass('show');
      $parent.find('.dropdown-menu').addClass('show');
    }
    e.stopPropagation();
  });

  $(document).click(function () {
    $('.dropdown').removeClass('show');
    $('.dropdown-menu').removeClass('show');
  });
});
