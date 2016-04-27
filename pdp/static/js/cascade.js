var app = angular.module('identityApp');

function ApiService($log, $http, ErrorSvc){
    var get = function(url) {
        $log.info('getting ' + url);
        return $http.get(url)
            .then(function(response){
                $log.info(response);
                return response;
            })
            .catch(function(response) {
                $log.info(response);
                if (response.status == 500 || response.status == 401) {
                    ErrorSvc.handleError(response.data, response.status);
                }
            })
    };
    return {get: get};
}

app.factory('apiService', ['$log', '$http', 'ErrorSvc', ApiService]);

function ProfileService(apiService) {
    // Service returning profile information about an authenticated user.
    var profile = {getting: false, data: {}};
    var getProfile = function(netid) {
        profile.getting = true;
        apiService.get('api/profile/')
            .then(function(response){
                for (var key in response.data){ profile.data[key] = response.data[key];}})
            .finally(function(){ profile.getting = false;});};
    return {profile: profile,
        getProfile: getProfile};
}

app.factory('profileService', ['apiService', ProfileService]);

app.controller('ProfileCtrl', ['profileService', function(profileService){
    profileService.getProfile('');

    this.data = profileService.profile.data;
}]);

//$(".modal-transparent").on('show.bs.modal', function () {
//  setTimeout( function() {
//    $(".modal-backdrop").addClass("modal-backdrop-transparent");
//  }, 0);
//});
//$(".modal-transparent").on('hidden.bs.modal', function () {
//  $(".modal-backdrop").addClass("modal-backdrop-transparent");
//});
//
//$(".modal-fullscreen").on('show.bs.modal', function () {
//  setTimeout( function() {
//    $(".modal-backdrop").addClass("modal-backdrop-fullscreen");
//  }, 0);
//});
//$(".modal-fullscreen").on('hidden.bs.modal', function () {
//  $(".modal-backdrop").addClass("modal-backdrop-fullscreen");
//});

angular.module('ui.bootstrap.demo').controller('ModalDemoCtrl', function ($scope, $uibModal, $log) {

  $scope.items = ['item1', 'item2', 'item3'];

  $scope.animationsEnabled = true;

  $scope.open = function (size) {

    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.toggleAnimation = function () {
    $scope.animationsEnabled = !$scope.animationsEnabled;
  };

});

// Please note that $uibModalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

angular.module('ui.bootstrap.demo').controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, items) {

  $scope.items = items;
  $scope.selected = {
    item: $scope.items[0]
  };

  $scope.ok = function () {
    $uibModalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});