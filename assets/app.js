/**
 * App module
 *
 * API docs for YouTube iframe https://developers.google.com/youtube/iframe_api_reference
 */
var app = angular.module("mrPlayer", [
  "youtube-embed"
]);

/**
 * App config
 */
app.config(function ($qProvider, $locationProvider, $compileProvider) {
  $qProvider.errorOnUnhandledRejections(false);
  $locationProvider.hashPrefix("");
  $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|telto):/);
});

/**
 * App run
 */
app.run(function ($rootScope, $anchorScroll, $window) {
  /**
   * Scroll up on each page view
   */
  $rootScope.$on("$viewContentLoaded", function () {
    $anchorScroll();
  });
  /**
   * Player config
   */
  $rootScope.playerConfig = {
    autoplay: 1,
    widget_referrer: $window.location.origin
  };
});

/**
 * API service
 */
app.service("API", function ($http) {

  var service = {};

  var methods = ["post", "get", "put", "delete"];

  var headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  };

  var apiUrl = "/api/";

  /**
   * @param {string} method
   * @param {string} endpoint
   * @param {object|null} payload
   * @param {object|null} params
   * @param {function} success
   * @param {function} fail
   */
  var http = function (method, endpoint, payload, params, success, fail) {
    return $http({
      url: apiUrl + endpoint + "/",
      headers: headers,
      method: method,
      data: payload,
      params: params
    }).then(success, fail);
  };

  angular.forEach(methods, function (method) {
    service[method] = function (endpoint, payload, params, success, fail) {
      return http(method, endpoint, payload, params, success, fail);
    };
  });

  return service;
});

/**
 * Song class
 */
app.service("Song", function ($http) {
  return function (data) {
    var self = this;
    self.id = data.id;
    self.user = data.user;
    self.party = data.party;
    self.url = data.url;
    self.title = null;
    self.thumbnail = null;
    self.isValid = false;
    self.isFromUser = function (user) {
      return self.user === user;
    };
    self.isFromParty = function (party) {
      return self.party === party;
    };
    self.init = function () {
      $http.get("https://noembed.com/embed?url=https://www.youtube.com/watch?v=" + self.url).then(function (data) {
        self.title = data.data.title;
        self.thumbnail = data.data.thumbnail_url.replace("hq", "mq");
        self.isValid = data.data.error ? false : true;
      });
    };
    self.init();
  };
});

/**
 * Main controller
 */
app.controller("MainController", function (API, Song, $interval, $scope, $window) {

  /**
   * Loaded controller
   */
  $scope.loaded = true;

  /**
   * Main user object
   */
  $scope.user = null;

  /**
   * Party code in URL
   */
  $scope.party = null;

  /**
   * All songs in party
   */
  $scope.songs = [];

  /**
   * Current song playing
   */
  $scope.currentSong = null;

  /**
   * Get party and songs
   */
  var getParty = function (newParty) {
    /**
     * Party in URL
     */
    var urlPary = $window.location.hash.split("/")[1];
    /**
     * Don't get the party from parameter, already got it
     */
    if ($scope.party && $scope.party === newParty) {
      return;
    }
    /**
     * Don't get the party frol URL, already got it
     */
    if ($scope.party && $scope.party === urlPary) {
      return;
    }
    /**
     * Should join a new party (from param)
     */
    if (newParty) {
      $scope.party = newParty;
    }
    /**
     * Should join party from URL
     */
    else if (urlPary) {
      $scope.party = $window.location.hash.split("/")[1];
    }
    /**
     * Should generate a new party
     */
    else if (!newParty) {
      console.log("Generating new party...");
      API.get("generate", null, null, function (data) {
        console.log("Generated party");
        getParty(data.data.party);
      });
      return;
    }
    /**
     * Get the party from parameter (changed elsewhere)
     */
    else {
      $scope.party = newParty;
    }
    /**
     * Change URL hash to party
     */
    $window.location.hash = "#/" + $scope.party;
    console.log("Joined party", $scope.party);
    /**
     * Get songs of this party
     */
    getSongs();
  };

  /**
   * Get user
   */
  var getUser = function () {
    /**
     * Get user object from localStorage
     */
    if (localStorage.getItem("user")) {
      $scope.user = localStorage.getItem("user");
      console.log("Loaded user", $scope.user, "from localStorage");
    }
    /**
     * New user, create user and store to localStorage
     */
    else {
      console.log("Generating new user...");
      API.get("generate", null, null, function (data) {
        localStorage.setItem("user", data.data.user);
        console.log("Created user", data.data.user);
        getUser();
      });
      return;
    }
  };

  /**
   * Get songs of current party
   */
  var getSongs = function () {
    console.log("Getting party songs...");
    var payload = {
      key: "party",
      value: $scope.party,
      last: $scope.songs.length ? $scope.songs[0].id : 0
    };
    API.get("song", null, payload, function (data) {
      angular.forEach(data.data, function (songData) {
        $scope.songs.unshift(new Song(songData));
      });
      console.log("Loaded", $scope.songs.length, "party songs");
    });
  };

  /**
   * Init function
   */
  var init = function () {
    /**
     * Initial party
     */
    getParty();
    /**
     * Initial user
     */
    getUser();
  };

  init();

  /**
   * Add a new song to party
   */
  $scope.addSong = function (form) {
    form.loading = true;
    var payload = {
      user: $scope.user,
      party: $scope.party,
      url: form.data.url
    };
    console.log("Adding song to party...");
    API.post("song", payload, null, function (data) {
      console.log("Added song to party");
      payload.url = data.data;
      $scope.songs.unshift(new Song(payload));
      form.loading = false;
      form.data.url = null;
    });
  };

  /**
   * Play song via player
   */
  $scope.playSong = function (song) {
    $scope.currentSong = song;
  };

  /**
   * Get all users of songs in this party
   */
  $scope.getUsers = function () {
    var users = [];
    angular.forEach($scope.songs, function (song) {
      if (users.indexOf(song.user) === -1) {
        users.push(song.user);
      }
    });
    return users;
  };

  /**
   * Player video ended
   */
  $scope.$on("youtube.player.ended", function (event, player) {
    console.log("Video ended, playing next video.");
    var nextIndex = $scope.songs.indexOf($scope.currentSong) + 1;
    if (nextIndex >= $scope.songs.length) {
      nextIndex = 0;
    }
    $scope.currentSong = $scope.songs[nextIndex];
    player.playVideo();
  });

  /**
   * Party changed from URL
   */
  $scope.$watch(function () { return $window.location.hash; }, function (value) {
    getParty(value.split("/")[1]);
  });

  /**
   * Update song list
   */
  $interval(getSongs, 15000);
});
