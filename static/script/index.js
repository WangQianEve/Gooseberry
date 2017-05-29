function getInv(){
  $.ajax({
    type: "POST",
    url: "/getinv/",
    success: function(data) {
      $(#invTbody).append("<tr><td><a href=\"{{url_for('invitation',inv_id='001')}}\"> invitation 001 </a></td><td>voting</td><td>evelyn</td></tr>");
    }
  });
  return true;
}
