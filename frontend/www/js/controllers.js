angular.module('starter.controllers', [])

.controller('DashCtrl', function ($scope, $ionicPopup, $timeout, $state,
    sleepService, $ionicHistory) {
    var forecastMin = 0;
    var forecastMax = 100;

    function barChartColor(n) {
      var color = ["red", "yellow", "green"];
      var rangeColor = d3.scale.linear()
        .domain([0, 100])
        .range([0, 2]);
      var colorValue = 1;
      if (rangeColor(n) < 0.7) {
        colorValue = 0;
      } else if (rangeColor(n) > 1.5) {
        colorValue = 2;
      }
      return color[colorValue];
    }
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
        color: function (d, i) {
          return barChartColor(d.values.Q3);
        },
        x: function (d) {
          return d.label;
        },
        maxBoxWidth: 0,
        yDomain: [forecastMin, forecastMax]
      },
      title: {
        enable: false,
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
        Q3: 100
      }
    }];

    $scope.drink = function () {
      // Triggered on a button click, or some other target
      $scope.data = {};

      // An elaborate, custom popup
      var myPopup = $ionicPopup.show({
        template: '<input type="text" ng-model="data.inputValue">',
        title: 'Enter how much alky you drank',
        subTitle: 'in [ml]',
        scope: $scope,
        buttons: [{
          text: 'Cancel'
        }, {
          text: '<b>Save</b>',
          type: 'button-positive',
          onTap: function (e) {
            if (!$scope.data.inputValue) {
              e.preventDefault();
            } else {
              if (isNaN($scope.data.inputValue)) {
                $scope.data.inputValue = 0;
              }
              $scope.vm.data[0].values.Q3 = $scope.vm.data[
                0].values.Q3 - $scope.data.inputValue;
              return $scope.data.inputValue;
            }
          }
        }, ]
      });
      myPopup.then(function (res) {
        console.log('Tapped!', res);
      });
    };
    $scope.sleep = function () {

      $ionicHistory.nextViewOptions({
        disableBack: true
      });

      sleepService.startSleep();
      $state.go('tab.nextView');
    };
  })
  .controller('sleepingCtrl', function ($scope, $state, sleepService,
    $ionicHistory, $ionicViewSwitcher) {
    console.log("sleepingCtrl");
    $scope.wakingUp = function () {
      $ionicViewSwitcher.nextDirection('back');
      $ionicHistory.nextViewOptions({
        disableBack: true
      });

      sleepService.endSleep();
      $state.go('tab.dash');
    };
  })
  .controller('ChatsCtrl', function ($scope, Chats, $state) {
    // With the new view caching in Ionic, Controllers are only called
    // when they are recreated or on app start, instead of every page change.
    // To listen for when this page is active (for example, to refresh data),
    // listen for the $ionicView.enter event:
    //
    //$scope.$on('$ionicView.enter', function(e) {
    //});
    $scope.myGrade = "";
    $scope.gradeSave = function (theGrade) {
      console.log("send my grade to server ", theGrade);
      $state.go('tab.dash');
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
