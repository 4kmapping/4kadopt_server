var ozController = {

  map: null,
  base_layer: null,
  oz_layer: null,

  api_url: '/api/adoptions/?format=json',
  adoptions: {},

  oz_url_lq: 'https://services1.arcgis.com/DnZ5orhsUGGdUZ3h/arcgis/rest/services/OZLowRes2/FeatureServer/0',
  oz_url_hq: 'https://services1.arcgis.com/DnZ5orhsUGGdUZ3h/ArcGIS/rest/services/OZ2014/FeatureServer/0',
  oz_url: this.oz_url_lq,

  lq_oz_start_at_level: 1,
  hq_oz_start_at_level: 100, //no hq!

  init: function(){

    this.fetchAdoptions();

    this.map = L.map('map', {
      minZoom: 2
    // }).setView([52.3667, 4.9000], 7), // amsterdam
    }).setView([39.9167, 32.8333], 5), // turkey
    // }).setView([0, 0], 2), //center

    // load basemap
    this.base_layer = L.esri.basemapLayer('DarkGray').addTo(this.map) ;

    this.map.on('zoomend', $.proxy(this.zoomend, this)) ;


    // this.addOzLayer() ;
    this.setAppropiateOzQuality() ;

    return this ;

  },

  fetchAdoptions: function(){

    // fetching from the api
    // proxy to retain 'this' context
    $.getJSON(this.api_url, $.proxy(function(response){

      /*
        reformatting data like below for quick access when rendering the map
        {
          'NLD-NOH': 2013,
          'NLD-FRI': 2020
        }
      */
      for (var i = response.results.length - 1; i >= 0; i--) {

        //shortcut for clarity
        var adoption = response.results[i] ;
        this.adoptions[adoption['worldid']] = adoption['targetyear'];

      };

    }, this));

  },

  addOzLayer: function(){

    this.oz_layer = L.esri.featureLayer(this.oz_url, {

      // only load specific fields to reduce redundant data being sent back and forth
      // 'WorldID', 'OBJECTID' are for HQ OZ2014 layer
      // ''OBJECTID_1', 'World', 'FID' are for LQ OZ2008 layer
      fields: ['WorldID', 'OBJECTID', 'OBJECTID_1', 'World', 'FID'],

      // esri's library smartly 'uglifies' polygons for us for performance
      // reduce for prettier maps, increase for faster ugly
      simplifyFactor: 1,

      // initially style adopted oz's + give world id class name for later lookup
      style: $.proxy(function(feature){

        // give it a class name we can look up later
        var style = {
          // eg; oz-NLD-NOH
          className: 'oz-' + feature.properties.WorldID
        } ;

        // if oz is adopted already, give class
        if(this.adoptions.hasOwnProperty(feature.properties.WorldID)){
          style['className'] = style['className'] + ' adopted-1'
        }

        return style ;

      }, this)

    });

    this.oz_layer.addTo(this.map);

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