// possible js tools for the project

// these are set by page load
var pdp_name_url = 'api/name';
var pdp_pub_url = 'api/identity/publish';
var pdp_user_has_publish = false;


var app = angular.module('pdpApp', []);

app.config(['$httpProvider', function($httpProvider) {
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}]);

/* controller for the preferred name */

app.controller('NameCtrl', ['$http', '$log', function($http, $log) {

    var _this = this;
    // sample valid name characters
    //this.valid_chars = /^[\w !\"#$%&\'()*+,.-:;<>?@\/`=]+$/

    // diaplay names as they look in the directory
    this.wp = {
        fname: null,
        mname: null,
        lname: null,
    };
    // display names as they are edited
    this.pn = {
	display_fname: null,
	display_mname: null,
	display_lname: null,
    };

    this.putStatus = null;
    this.getPrefName = function() {
	$log.info('about to get '+ pdp_name_url);
	$http.get(pdp_name_url)
	.success(function(data){
		_this.pn = data;
                _this.wp.fname = _this.pn.display_fname;
                _this.wp.mname = _this.pn.display_mname;
                _this.wp.lname = _this.pn.display_lname;
	    });
    };
    this.putPrefName = function() {
        console.log('pub = ' + _this.wp_publish);
	$log.info('about to put '+ pdp_name_url);
	$http.put(pdp_name_url, _this.pn)
	.success(function(data){
		_this.putStatus = 'Updated';
                _this.getPrefName();
		$log.info(_this.putStatus);		
	    })
	.error(function(data){
		_this.putStatus = 'Update failed';
		$log.info(_this.putStatus);
	    });
    };
    _this.getPrefName();
}]);


/* controller for the publish preference */

app.controller('PubCtrl', ['$scope', '$http', '$log', function($scope, $http, $log) {
    console.log('pubctrl, publish = ' + pdp_user_has_publish);

    // initial publish flag comes from the page load
    $scope.wp_publish = 'no';
    if (pdp_user_has_publish) $scope.wp_publish = 'yes';

    $scope.putPubStatus = null;
    $scope.getPubPref = function() {
	$log.info('about to get '+ pdp_pub_url);
	$http.get(pdp_pub_url).success(function(data){
		$scope.pn = data;
	    });
    };
    $scope.putPubPref = function() {
        console.log('pub = ' + $scope.wp_publish);
	$log.info('about to put '+ pdp_pub_url);
	$http.put(pdp_pub_url, $scope.pn)
	.success(function(data){
		$scope.putStatus = 'Successful response from put';
		$log.info($scope.putStatus);		
	    })
	.error(function(data){
                err_msg = data.error_message;
                console.log(err_msg);
                $scope.putPubStatus = err_msg;
                $log.info($scope.putPubStatus);
	    });
    };

}]);

