var app = angular.module('identityApp');

function ApiService($log, $http, ErrorSvc){
    var apiFunc = function(operation){ return function(url) {
        $log.info(operation + ' ' + url);
        return $http[operation](url)
            .then(function(response){
                $log.info(response);
                return response;
            })
            .catch(function(response) {
                $log.info(response);
                if (response.status == 500 || response.status == 401) {
                    ErrorSvc.handleError(response.data, response.status);
                }
                return response;
            })
    }};
    var get = apiFunc('get');
    var put = apiFunc('put');
    return {get: get, put: put};
}

app.factory('apiService', ['$log', '$http', 'ErrorSvc', ApiService]);

function ProfileService(apiService) {
    var profileUrl = 'api/profile/';
    var publishUrl = 'api/publish/';
    // Service returning profile information about an authenticated user.
    var profile = {getting: false, data: {}};
    var getProfile = function(netid) {
        profile.getting = true;
        apiService.get(profileUrl)
            .then(function(response){
                for (var key in response.data){ profile.data[key] = response.data[key];}})
            .finally(function(){ profile.getting = false;});};
    var putEmployeePublish = function(netid, publishValue){
        return apiService.put(publishUrl + netid + '?value=' + publishValue).then(function(response){
            return response.status == 200 ? response.data.publish : null;
        });
    };
    return {profile: profile,
        getProfile: getProfile,
        putEmployeePublish: putEmployeePublish
    };
}

app.factory('profileService', ['apiService', ProfileService]);

app.controller('ProfileCtrl', ['profileService', 'loginStatus', function(profileService, loginStatus){
    var _this = this;
    this.netid = null;
    loginStatus.getNetid().then(function(netid){
        _this.netid = netid;  /* null on error */
        if(netid){profileService.getProfile(netid);}
    });
    this.data = profileService.profile.data;
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
        _this.employeePublishValue = _this.data.employee && _this.data.employee.publish ?
            _this.data.employee.publish : 'Y';
    };

    this.putPublish  = function(){
        profileService.putEmployeePublish(_this.netid, _this.employeePublishValue).then(function(newValue){
            if(newValue){
                _this.data.employee.publish = newValue;
                _this.clearPublishChange();
            }
        });
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

app.controller('SplashModalCtrl', ['modalService', '$cookies', function(modalService, $cookies){
    var cookieName = 'profileSplashPersistent';   /* persistent in the name keeps it around after logout */

    this.setProfileVisit = function() {
        var now = new Date();
        var inTenYears = new Date(now.getFullYear() + 10, now.getMonth(), now.getDate());
        $cookies.put(cookieName, true, {expires: inTenYears});
    };
    if(!$cookies.get(cookieName)){
        modalService.showModal('#splashModal');
    }
}]);


// This should ultimately replace the tooltip in idbase.
// Usage: <uw-tooltip>Tooltip description goes here</uw-tooltip>
app.directive('uwTooltip', ['$log', function($log){
    return {
        restrict: 'E',
        link: function(scope, element, attrs){
            $log.info('tooltip set?');
            $(element).children().tooltip();
        },
        template: function(element){
            return  $('<a href="" data-toggle="tooltip"><i class="fa fa-question-circle fa-lg icon-look" data-toggle="tooltip" /></a>')
                .attr('title', $(element).text());
        }
    };
}]);
