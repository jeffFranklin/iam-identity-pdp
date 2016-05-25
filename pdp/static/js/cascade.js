var app = angular.module('identityApp');

function ApiService($log, $http, ErrorSvc){
    var apiFunc = function(operation){ return function(url, data) {
        $log.info(operation + ' ' + url);
        return $http[operation](url, data)
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

function ProfileService(apiService, $q) {
    var profileUrl = 'api/profile/';
    var publishUrl = 'api/publish/';
    var nameUrl = 'api/name/';

    var lastProfile = {netid: null, promise: null};
    var getProfile = function(netid) {
        lastProfile.netid = netid;
        lastProfile.promise = apiService.get(profileUrl + netid)
            .then(function(response){
                return response.status == 200 ? response.data : {};
            });
        return lastProfile.promise;
    };
    var putEmployeePublish = function(netid, publishValue){
        return apiService.put(publishUrl + netid + '?value=' + publishValue).then(function(response){
            return response.status == 200 ? response.data.publish : null;
        });
    };
    var getPreferredName = function(netid) {
        promise = (lastProfile.netid == netid && lastProfile.promise) ? lastProfile.promise : getProfile(netid);
        return promise.then(function(profile){
            return profile ? profile.preferred: null;
        });
    };
    var getNetid = function() {
        if(!lastProfile.promise){return $q.when(null);}
        return lastProfile.promise.then(function(profile){return profile ? profile.netid : null}); };
    var putPreferredName = function(netid, name){
        return apiService.put(nameUrl, {first: name.first, middle: name.middle, last: name.last})
            .then(function(response){return response.status == 200 ? response.data : null});
    };

    return {getProfile: getProfile,
        putEmployeePublish: putEmployeePublish,
        getPreferredName: getPreferredName,
        putPreferredName: putPreferredName,
        getNetid: getNetid
    };
}

app.factory('profileService', ['apiService', '$q', ProfileService]);

app.controller('ProfileCtrl', ['profileService', 'loginStatus', '$log', function(profileService, loginStatus, $log){
    var _this = this;
    this.netid = null;
    this.isAdmin = null;  // set to true or false when we get it.
    loginStatus.getNetid().then(function(netid){
        _this.netid = netid;  /* null on error */
        if(netid){
            profileService.getProfile(netid).then(function(profile){
                if (_this.isAdmin == null) _this.isAdmin = profile.is_profile_admin;
                $log.info('admin mode available');
                _this.data = profile;
            });
        }
    });
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

    this.impersonate = function(netid){
        _this.clearNameChange();
        _this.clearPublishChange();
        profileService.getProfile(netid || '').then(function(profile){
            if(!netid || netid == _this.netid){
                _this.impersonationNetid = null;
            }
            else { _this.impersonationNetid = netid;}
            _this.data = profile;
        })

    }
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
