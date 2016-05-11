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
    var _this = this;
    this.clearNameChange = function(){
        _this.isSettingName = false;
    };
    this.showNameChange = function(){
        _this.isSettingName = true;
        _this.nameChangeSuccess = false;
    };

    this.clearPublishChange = function(){
        _this.isSettingPublish = false;
    };

    this.showPublishScreen = function(){
        _this.isSettingPublish = true;
    };

    this.isSettingPublish = false;

    this.isSettingName = false;
    this.onNameChange = function(data){
        _this.isSettingName = false;
        _this.nameChangeSuccess = true;
        _this.data.preferred = data;
        _this.data.preferred_name = data.full;
    };
}]);

app.factory('modalService', [function(){
    var _this = this;

    return {
        showModal: function(id) {
            $(id)
                .modal('show')
                .on('shown.bs.modal', function() { $(id).find('button.btn-primary').focus();
            });
        }
    };
}]);

app.controller('SplashModalCtrl', ['modalService', function(modalService){
    modalService.showModal('#splashModal');
}]);
