// possible js tools for the project

// these are set by page load
var pdp_name_url = 'api/name';
var pdp_pub_url = 'api/publish';

var app = angular.module('identityApp');

app.filter('invalid_chars', function () {
    return function (input, valid) {
        var ichars = [];
        for (var i = 0; i < input.length; i++) {
            if (!valid.test(input.charAt(i))) {
                if (ichars.indexOf(input.charAt(i)) == -1) {
                    ichars.push(input.charAt(i));
                }
            }
        }
        return ichars.join(', ');
    };
});

/* controller for the preferred name */

app.controller('NameCtrl', ['$http', '$log', 'ErrorSvc', 'loginStatus', function ($http, $log, ErrorSvc, loginStatus) {
    var _this = this;
    // sample valid name characters
    this.valid_chars = /^[\w !#$%&\'*+\-,.?^_`{}~]*$/;
    this.displayNameMax = 80;
    this.fieldMax = 64;
    this.displayName = '';
    this.displayCharsRemaining = this.displayNameMax;

    // display names as they are edited
    this.pn = {
        display_fname: '',
        display_mname: '',
        display_lname: ''
    };

    this.getStatus = null;
    this.putStatus = null;
    this.getPrefName = function () {
        $log.info('about to get ' + pdp_name_url);
        $http.get(pdp_name_url)
            .success(function (data, status) {
                _this.pn = data;
                _this.updateDisplayName();
                _this.getStatus = status;
            })
            .error(function (data, status) {
                $log.info('name get status returned error, status ' + status);
                _this.getStatus = status;
                ErrorSvc.handleError(data, status);
            });
    };
    this.putPrefName = function () {
        if (_this.puttingPrefName == true) return;
        _this.puttingPrefName = true;
        $log.info('about to put ' + pdp_name_url);
        $http.put(pdp_name_url, _this.pn)
            .then(function (response) {
                _this.putStatus = 'success';
                $log.info(_this.putStatus);
                $log.info(response);
                _this.form.$setPristine(); // only set pristine on success
                loginStatus.info.name = _this.getDisplayNameFromObject(response.data);
            })
            .catch(function (response) {
                _this.putStatus = 'error';
                ErrorSvc.handleError(response.data, response.status);
                $log.info(_this.putStatus);
                $log.info(response);
            })
            .finally(function(){_this.puttingPrefName = false;});
    };
    this.getDisplayNameFromObject = function (value) {
        dname = "";
        if (value.display_fname) dname += value.display_fname;
        if (value.display_mname) dname += (dname.length ? ' ' : '') + value.display_mname;
        if (value.display_lname) dname += (dname.length ? ' ' : '') + value.display_lname;
        return dname;
    };
    this.updateDisplayName = function () {
        _this.displayName = _this.getDisplayNameFromObject(_this.pn);
        _this.displayCharsRemaining = _this.displayNameMax - _this.displayName.length;
    };
    this.getFieldMaxLength = function(text) {
        var totalMax = (text ? text.length : 0) + (_this.displayCharsRemaining > 0 ? _this.displayCharsRemaining : 0);
        return Math.min(totalMax, _this.fieldMax);
    };
    this.getPrefName();
}]);


/* controller for the publish preference */

app.controller('PubCtrl', ['$http', '$log', function ($http, $log) {
    var _this = this;
    this.publish = {
        publish: 'no'
    };
    this.getStatus = null;
    this.putStatus = null;
    this.getPubPref = function () {
        $log.info('about to get ' + pdp_pub_url);
        $http.get(pdp_pub_url)
            .success(function (data, status) {
                _this.publish = data;
                _this.getStatus = status;
            })
            .error(function(data, status) {
                $log.info('get status returned ' + status);
                _this.getStatus = status;
            });
    };
    this.putPubPref = function () {
        $log.info('about to put to ' + pdp_pub_url);
        $http.put(pdp_pub_url, _this.publish)
            .success(function (data) {
                _this.putStatus = 'success';
                $log.info(_this.putStatus);
                _this.form.$setPristine();
            })
            .error(function (data, status) {
                $log.info('error trying to put, status returned is ' + status);
                _this.putStatus = 'error';
            });
    };
    this.getPubPref();

}]);

