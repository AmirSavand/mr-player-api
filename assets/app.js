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
app.service("Song", function (API, $http, $rootScope) {
  return function (data) {
    var self = this;
    self.id = data.id;
    self.url = data.url;
    self.title = null;
    self.thumbnail = null;
    self.isValid = false;
    self.init = function () {
      $http.get("https://noembed.com/embed?url=https://www.youtube.com/watch?v=" + self.url).then(function (data) {
        self.title = data.data.title;
        self.thumbnail = data.data.thumbnail_url.replace("hq", "mq");
        self.isValid = data.data.error ? false : true;
        $rootScope.$broadcast("mrPlayer.Song.init", self);
      });
    };
    self.delete = function (user) {
      if (!confirm("Are you sure?")) {
        return;
      }
      API.delete("song", { id: self.id, user: user }, null, function () {
        $rootScope.$broadcast("mrPlayer.Song.delete", self);
      }, function () {
        alert("You can't delete others videos.");
      });
    };
    self.init();
  };
});

/**
 * Main controller
 */
app.controller("MainController", function (API, Song, $interval, $scope, $window, $filter) {

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
      last: 0,
      limit: 100
    };
    if ($scope.songs.length > 0) {
      payload.last = $scope.songs[$scope.songs.length - 1];
    }
    API.get("song", null, payload, function (data) {
      angular.forEach(data.data, function (songData) {
        new Song(songData);
      });
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
      new Song(data.data);
      form.loading = false;
      form.data.url = null;
    });
  };

  /**
   * Play song and update variable
   */
  $scope.playSong = function (song) {
    if (song) {
      console.log("Playing selected song");
      $scope.currentSong = song;
    } else {
      console.log("Playing next song");
      var nextIndex = $scope.songs.indexOf($scope.currentSong) + 1;
      if (nextIndex >= $scope.songs.length) {
        nextIndex = 0;
      }
      $scope.currentSong = $scope.songs[nextIndex];
    }
    $scope.player.loadVideoById($scope.currentSong.url);
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
   * Video player ready
   */
  $scope.$on("youtube.player.ready", function (event, player) {
    console.log("Video player is ready");
    $scope.player = player;
    $scope.playSong();
  });

  /**
   * Video player ended
   */
  $scope.$on("youtube.player.ended", function (event, player) {
    console.log("Video player ended");
    $scope.playSong();
  });

  /**
   * Party changed from URL
   */
  $scope.$watch(function () { return $window.location.hash; }, function (value) {
    getParty(value.split("/")[1]);
  });

  /**
   * Song loaded
   */
  $scope.$on("mrPlayer.Song.init", function (event, song) {
    if (song.isValid) {
      $scope.songs.push(song);
    } else {
      song.delete($scope.user);
    }
    $scope.songs = $filter("orderBy")($scope.songs, "id");
  });

  /**
   * Song deleted
   */
  $scope.$on("mrPlayer.Song.delete", function (event, song) {
    console.log("Called");
    var index = $scope.songs.indexOf(song);
    if (index != -1) {
      $scope.songs.splice(index, 1);
    }
  });

  /**
   * Update song list
   */
  $interval(getSongs, 15000);
});
