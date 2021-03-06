var isDemo = true;
angular.module('starter.controllers', [])

.controller('DashCtrl', function ($scope, $ionicPopup, $timeout, $state,
    sleepService, $ionicHistory, $http) {
    var forecastMin = 0;
    var forecastMax = 100;

    function barChartColor(doc, n) {
      var color = ["red", "yellow", "green"];
      var rangeColor = d3.scale.linear()
        .domain([0, 100])
        .range([0, 2]);
      var colorValue = 1;
      console.log("doc ", doc);
      console.log("n ", n);
      if (doc.label == "You") {
        $scope.awesomeTip = "Reduce partying if you want to hold your GPA. ";
      }
      if (rangeColor(n) < 0.7) {
        colorValue = 0;
        if (doc.label == "You") {
          $scope.awesomeTip = "Stop partying and start learning.";
        }
      } else if (rangeColor(n) > 1.5) {
        colorValue = 2;
        if (doc.label == "You") {
          $scope.awesomeTip = "You are good. Keep rocking!";
        }
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
          return barChartColor(d, d.values.Q3);
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
        Q3: 77
      }
    }];

    $scope.drink = function () {
      // Triggered on a button click, or some other target
      $scope.data = {};

      // An elaborate, custom popup
      var myPopup = $ionicPopup.show({
        template: '<input type="number" ng-model="data.inputValue">',
        title: 'Enter how much alky you drank',
        subTitle: 'in [liter]',
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
              //var isDemo = false;
              var urlPOST =
                "http://dreamwalkers.cloudapp.net/add_drink/1/" +
                $scope.data.inputValue;
              if (isDemo) {
                urlPOST =
                  "http://dreamwalkers.cloudapp.net/add_drink/1/demo";
              }
              console.log(urlPOST);
              //alert(urlPOST);

              $http.post(urlPOST)
                .success(function (data) {
                  console.log("add drink ", data);
                  //alert("add drink " + data);
                  $scope.predictedGrade = (Math.round(data *
                      100) / 100)
                    .toFixed(1);
                })
                .error(function (data) {
                  console.log("drink err ", data);
                  data = 3.321;
                  $scope.predictedGrade = (Math.round(data *
                      100) / 100)
                    .toFixed(1);
                  //$scope.predictedGrade = 3.0;
                  //alert("drink err " + data);
                });



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
  .controller('ChatsCtrl', function ($scope, Chats, $state, $http) {
    // With the new view caching in Ionic, Controllers are only called
    // when they are recreated or on app start, instead of every page change.
    // To listen for when this page is active (for example, to refresh data),
    // listen for the $ionicView.enter event:
    //
    //$scope.$on('$ionicView.enter', function(e) {
    //});
    $scope.myGrade = "";
    //var isDemo = false;
    $scope.gradeSave = function (theGrade) {
      console.log(isDemo);
      var urlPOST = "http://dreamwalkers.cloudapp.net/set_grade/1/" +
        theGrade;
      if (isDemo) {
        urlPOST =
          "http://dreamwalkers.cloudapp.net/set_grade/1/demo";
      }
      console.log(urlPOST);
      //alert(urlPOST);

      $http.post(urlPOST)
        .success(function (data) {
          console.log("grade ", data);
          //alert("grade " + data);
          $scope.predictedGrade = (Math.round(data *
              100) / 100)
            .toFixed(1);
        })
        .error(function (data) {
          console.log("grade err ", data);
          data = 3.321;
          $scope.predictedGrade = (Math.round(data *
              100) / 100)
            .toFixed(1);
        });

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
