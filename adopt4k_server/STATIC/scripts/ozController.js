var ozController = {

  map: null,
  base_layer: null,
  oz_layer: null,

  oz_url_lq: 'https://services1.arcgis.com/DnZ5orhsUGGdUZ3h/arcgis/rest/services/OZLowRes2/FeatureServer/0',
  oz_url_hq: 'https://services1.arcgis.com/DnZ5orhsUGGdUZ3h/ArcGIS/rest/services/OZ2014/FeatureServer/0',
  oz_url: this.oz_url_lq,

  lq_oz_start_at_level: 1,
  hq_oz_start_at_level: 6,

  init: function(){

    this.map = L.map('map', {
      minZoom: 2
    }).setView([52.3667, 4.9000], 7),
    // }).setView([0, 0], 2),
    // this.base_layer = L.esri.basemapLayer('DarkGray').addTo(this.map) ;
    this.map.on('zoomend', $.proxy(this.zoomend, this)) ;

    // this.addOzLayer() ;
    this.setAppropiateOzQuality() ;

    return this ;

  },

  addOzLayer: function(){

    this.oz_layer = L.esri.featureLayer(this.oz_url, {

      fields: ['WorldID', 'OBJECTID', 'OBJECTID_1', 'World', 'FID'],

      // simplifyFactor: 0.9,
      simplifyFactor: 1,

      style: function(feature){

        return {
          className: 'oz-' + feature.properties.WorldID
        }

      }

    });

    this.oz_layer.addTo(this.map);

    // this.oz_layer.on('load', function(){

    //   console.log(Snap('svg path')) ;

    //   Snap('svg path[class*=oz-]').hover(function(){
    //     console.log('hover!', arguments);
    //   });

    // });

  },

  removeOzLayer: function(){
    if(this.oz_layer !== null){
      this.map.removeLayer(this.oz_layer) ;
    }
  },

  reloadOzLayer: function(){
    this.removeOzLayer() ;
    this.addOzLayer() ;
  },

  zoomend: function(ev){
    this.setAppropiateOzQuality() ;
    optionsController.render() ;
  },

  setAppropiateOzQuality: function(){

    var z = this.map.getZoom() ;

    if(z >= this.lq_oz_start_at_level
    && z < this.hq_oz_start_at_level) {

      //only if something changes, or else pointless/ugly reload
      if(this.oz_url !== this.oz_url_lq) {
        this.oz_url = this.oz_url_lq ;
        this.reloadOzLayer() ;
      }

    }

    if(z >= this.hq_oz_start_at_level) {

      //only if this is new
      if(this.oz_url !== this.oz_url_hq) {
        this.oz_url = this.oz_url_hq ;
        this.reloadOzLayer() ;            
      }

    }

    //#yolo!
    if(z < this.lq_oz_start_at_level) {
      this.oz_url = null ;
      this.removeOzLayer() ;
    }

  }

} ;