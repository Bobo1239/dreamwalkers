angular.module('starter.controllers', [])

.controller('DashCtrl', function ($scope) {
  var forecastMin = 0;
  var forecastMax = 40;
  $scope.vm = this;
  $scope.vm.options = {
    chart: {
      type: 'boxPlotChart',
      height: 150,
      margin: {
        top: 5,
        right: 0,
        bottom: 20,
        left: 30
      },
      color: ['darkorange'],
      x: function (d) {
        return d.label;
      },
      maxBoxWidth: 10,
      yDomain: [forecastMin, forecastMax]
    },
    title: {
      enable: true,
      text: ''
    }
  };
  $scope.vm.data = [{
    label: "You",
    values: {
      Q1: 0,
      Q2: 0,
      Q3: 22
    }
  }, {
    label: "Average",
    values: {
      Q1: 0,
      Q2: 0,
      Q3: 30
    }
  }];
  console.log("dash!! ", $scope.vm);
})

.controller('ChatsCtrl', function ($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function (chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailCtrl', function ($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function ($scope) {
  $scope.settings = {
    enableFriends: true
  };
});
