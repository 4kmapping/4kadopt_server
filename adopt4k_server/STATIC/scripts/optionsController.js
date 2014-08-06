var optionsController = {

  init: function(){

    this.render() ;

    $('#options input').change(this.submit) ;

    return this;

  },

  render: function(){
    $('#current_zoom').val(ozController.map.getZoom()) ;
    $('#lq_start_layer').val(ozController.lq_oz_start_at_level) ;
    $('#hq_start_layer').val(ozController.hq_oz_start_at_level) ;
  },

  submit: function(){
    ozController.lq_oz_start_at_level = $('#lq_start_layer').val() ;
    ozController.hq_oz_start_at_level = $('#hq_start_layer').val() ;
    ozController.setAppropiateOzQuality() ;
  }

} ;