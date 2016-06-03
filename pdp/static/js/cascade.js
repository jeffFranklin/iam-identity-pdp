var app = angular.module('identityApp');

function ApiService($log, $http, ErrorSvc){
    var apiFunc = function(operation){ return function(url, opts) {
        opts = opts || {};
        var data = opts.data;
        var expectedErrors = opts.expectedErrors || [];

        $log.info(operation + ' ' + url);
        return $http[operation](url, data)
            .then(function(response){
                $log.info(response);
                return response;
            })
            .catch(function(response) {
                $log.info(response);
                if (response.status >= 400 && expectedErrors.indexOf(response.status) < 0){
                    // ErrorSvc ignores everything not 401 or 500. Promote non-401s to 500s.
                    ErrorSvc.handleError(response.data, response.status == 401 ? 401 : 500);
                }
                return response;
            });
    }};
    var get = apiFunc('get');
    var put = apiFunc('put');
    return {get: get, put: put};
}

app.factory('apiService', ['$log', '$http', 'ErrorSvc', ApiService]);

function ProfileService(apiService) {
    var profileUrl = 'api/profile/';
    var publishUrl = 'api/publish/';
    var nameUrl = 'api/name/';

    var getProfile = function(netid) {
        return apiService.get(profileUrl + netid)
            .then(function(response){
                return response.status == 200 ? response.data : null;
            });
    };
    var putEmployeePublish = function(netid, publishValue){
        return apiService.put(publishUrl + netid + '?value=' + publishValue).then(function(response){
            return response.status == 200 ? response.data.publish : null;
        });
    };
    var putPreferredName = function(netid, name){
        return apiService.put(nameUrl + netid, {data: {first: name.first, middle: name.middle, last: name.last}})
            .then(function(response){return response.status == 200 ? response.data : null});
    };

    return {getProfile: getProfile,
        putEmployeePublish: putEmployeePublish,
        putPreferredName: putPreferredName
    };
}

app.factory('profileService', ['apiService', ProfileService]);

app.controller('ProfileCtrl', ['profileService', 'loginStatus', '$log', '$timeout', function(profileService, loginStatus, $log, $timeout){
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
        _this.pn = {};
        _this.nameForm.$setPristine();
        
    };


    this.showNameChange = function(){
        _this.isSettingName = true;
        _this.nameChangeSuccess = false;
        var pn = _this.data.preferred;
        _this.pn = {first: pn.first, middle: pn.middle, last: pn.last};
        // $timeout so we focus after the form's visible. this kinda smells.
        $timeout(function(){$('#nameForm').find('input')[0].focus();});

    };
    this.putPreferredName = function(name){
        _this.puttingPrefName = true;
        return profileService.putPreferredName(_this.data.netid, name).then(function(name){
            if(name){
                _this.nameChangeSuccess = true;
                _this.data.preferred = name;
                _this.data.preferred_name = name.full;
                _this.data.rollup_name = name.full;
                _this.clearNameChange();
            }
            else {_this.nameChangeError = true;}
            return name;
        }).finally(function(){_this.puttingPrefName = false;})
    };

    this.clearPublishChange = function(){
        _this.isSettingPublish = false;
    };

    this.showPublishScreen = function(){
        _this.isSettingPublish = true;
        _this.publishChangeSuccess = false;
        _this.publishForm.$setPristine();
        _this.employeePublishValue = _this.data.employee && _this.data.employee.publish ?
            _this.data.employee.publish : 'Y';
        // wrapping the focus in a $timeout lets the form become visible before
        // focusing. It feels a little like black magic, unsure if it works
        // on a slower box.
        $timeout(function(){$('#publishForm').find('input:checked').focus();});
    };

    this.putPublish  = function(){
        _this.puttingPublish = true;
        profileService.putEmployeePublish(_this.netid, _this.employeePublishValue).then(function(newValue){
            if(newValue){
                _this.data.employee.publish = newValue;
                _this.publishChangeSuccess = true;
                _this.clearPublishChange();
            }})
            .finally(function(){_this.puttingPublish = false;});
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
        $cookies.put(cookieName, true, {expires: inTenYears, path: '/'});
    };
    if(!$cookies.get(cookieName)){
        modalService.showModal('#splashModal');
    }
}]);
