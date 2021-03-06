var ozController = {

  map: null,

  oz_layer: null,

  api_url: '/api/adoptions/?format=json&page_size=5000',
  adoptions: {},

  oz_url: 'https://services1.arcgis.com/DnZ5orhsUGGdUZ3h/ArcGIS/rest/services/OZ2013_LowRes/FeatureServer/0',

  totalAmountOfOmegaZones: 4175,

  urlOptions: {},

  init: function(){

    // Processing options from the URL
    var urlOptionsRaw = window.location.hash.replace('#', '').split('&'),
        urlOptionDefaults = {
          // esri's library smartly 'uglifies' polygons for us for performance
          // reduce for prettier maps, increase for faster ugly
          uglify: 1,

          // turkey focussed map
          lat: 39.9167,
          lon: 32.8333,
          zoom: 5

          // NL focussed map
          // lat: 52.3667,
          // lon: 4.9000,
          // zoom: 7
        };

    for (var i = urlOptionsRaw.length - 1; i >= 0; i--) {
      var urlOption = urlOptionsRaw[i].split('=');
      this.urlOptions[urlOption[0]] = urlOption[1];
    };

    for(var key in urlOptionDefaults){
      if(!this.urlOptions.hasOwnProperty(key)){
        this.urlOptions[key] = urlOptionDefaults[key];
      }
    };

    console.log('this.urlOptions =', this.urlOptions);

    this.map = L.map('map', {
      minZoom: 2,
      reuseTiles: true
    }).setView([this.urlOptions.lat, this.urlOptions.lon], this.urlOptions.zoom),

    L.tileLayer('http://api.tiles.mapbox.com/v4/{mapid}/{z}/{x}/{y}.jpg90?access_token=pk.eyJ1Ijoiam9zaHVhZGVsYW5nZSIsImEiOiJ3RU1SemNzIn0.CyG3f36Z16ov1JEDHw2gDQ', {
      mapid: 'joshuadelange.j5igjfc7',
    }).addTo(this.map);

    // fetching current adoptions from the django server
    this.fetchAdoptions($.proxy(function(){
  
      this.addOzLayer() ;

      this.connectToServer();

    }, this));

    return this ;

  },

  connectToServer: function(){

    var socket = io('http://' + window.location.hostname + ':4000');
    socket.on('connect', $.proxy(function (data) {

      socket.on('newAdoptions', $.proxy(function(newAdoptions){

        for (var i in newAdoptions) {

              //shortcut to adoption
          var adoption = newAdoptions[i],
              //get oz path
              $oz = $('.oz-' + adoption['worldid']),
              //get oz class, if any
              ozClass = $oz.attr('class'),
              //set default target year
              currentTargetYear = 3000 ; //the year 3000. when the world will be saved.

          //if there is an ozclass present
          if(ozClass){
            //update the currenttargetyear with the latest, regex'ed fromt the class
            var possibleTargetYear = $oz.attr('class').match(/adopted-(\d+)/);
            if(possibleTargetYear){
              currentTargetYear = parseInt(possibleTargetYear[1]);
            }
          }

          // if the new targetyear is earlier than the currenttarget year
          if(adoption['targetyear'] < currentTargetYear) {

            //add to adoptions array
            this.adoptions[adoption['worldid']] = adoption['targetyear'];

            //a good moment to update the countdown
            this.updateCountdown();

            //apply change to path
            $oz.attr('class', 'oz-' + adoption['worldid'] + ' adopted adopted-' + adoption['targetyear']);

          }

          this.addAdoptionToStream(adoption);

        };

      }, this));

    }, this));

  },

  addAdoptionToStream: function(adoption){

    var adoptionHTML = '<li><span class="adoption-user">' + adoption.user_display_name + '</span> adopted <span class="adoption-oz">' + adoption.oz_zone_name + ', ' + adoption.oz_country_name + '</span></li>';
    $(adoptionHTML).fadeIn(200).prependTo('.stream');

    //remove elements from stream for performance
    //only shows last 30
    $('.stream li:gt(30)').remove();

  },

  fetchAdoptions: function(cb){

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

      this.updateCountdown();

      cb();

    }, this));

  },

  addOzLayer: function(){

    this.oz_layer = L.esri.featureLayer(this.oz_url, {

      // only load specific fields to reduce redundant data being sent back and forth
      fields: ['OBJECTID', 'WorldID'],

      simplifyFactor: this.urlOptions.uglify,

      // initially style adopted oz's + give world id class name for later lookup
      style: $.proxy(function(feature){

        // give it a class name we can look up later
        var style = {
          // eg; oz-NLD-NOH
          className: 'oz-' + feature.properties.WorldID
        } ;

        // if oz is adopted already, give class
        if(this.adoptions.hasOwnProperty(feature.properties.WorldID)){
          style['className'] = style['className'] + ' adopted adopted-' + this.adoptions[feature.properties.WorldID]
        }

        return style ;

      }, this)

    });

    this.oz_layer.addTo(this.map);

  },

  updateCountdown: function(){
    $('.countdown').html(this.totalAmountOfOmegaZones - Object.keys(this.adoptions).length);
  }

} ;