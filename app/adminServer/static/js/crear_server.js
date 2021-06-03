var $ = jQuery.noConflict();
  function abrir_modal_edicion(url){
    $('#edicion').load(url, function (){
      $(this).modal('show');
    });
  }
  function abrir_modal_creacion(url){
    $('#creacion').load(url,function(){
      $(this).modal('show');
    });
  }