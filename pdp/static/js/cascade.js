var app = angular.module('identityApp');

function ApiService($log, $http, ErrorSvc){
    var get = function(url) {
        $log.info('getting ' + url);
        return $http.get(url)
            .then(function(response){
                $log.info(response);
                return response.data;
            })
            .catch(function(response) {
                $log.info(response);
                if (response.status == 500 || response.status == 401) {
                    ErrorSvc.handleError(response.data, response.status);
                }
                return null;
            })
    };
    return {get: get};
}

app.factory('apiService', ['$log', '$http', 'ErrorSvc', ApiService]);

function ProfileService(apiService, $log, $q) {
    // Service returning profile information about an authenticated user.
    var profile = {getting: false, data: {}};
    var getProfile = function(netid) {
        return apiService.get('api/profile/');};
    return {profile: profile,
        getProfile: getProfile};
}

function MockProfileService(apiService, $log, $q) {
    var getProfile = function(netid){
        response = {netid: netid, preferred_name: 'Joe Blow',
            official_name: 'JOSEPH BLOW', emails: ['j@f.u'],
            student: {official_name: 'Joey Blow', phone_numbers: ['12345'],
                clazz: 'Junior', major: 'French'},
            employee: {official_name: 'JOEY BLOW', phone_numbers: ['54321'],
                emails: ['f@j.u'], address: 'Wallaby Way', box: 'P32'}};
        return $q.when(response);
    };
    return {getProfile: getProfile};
}

app.factory('profileService', ['apiService', '$log', '$q', ProfileService]);

app.controller('ProfileCtrl', ['profileService', 'loginStatus', '$log', function(profileService, loginStatus, $log){
    this.data = {};
    var _this = this;
    loginStatus.info.promise.then(function () {
        profileService.getProfile(loginStatus.info.netid).then(function (data) {
            if (data) {
                $log.info('pfc got ');
                $log.info(data);
                for (var key in data) {
                    _this.data[key] = data[key];
                }
            }
            else {
                $log.info('pfc got no data')
            }
        });
    });
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