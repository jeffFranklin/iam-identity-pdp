// possible js tools for the project

// these are set by page load
var pdp_name_url = '/id/api/name';
var pdp_pub_url = '/id/api/identity/publish';
var pdp_user_has_publish = false;


var app = angular.module('pdpApp', []);

app.config(['$httpProvider', function($httpProvider) {
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}]);

/* controller for the preferred name */

app.controller('NameCtrl', ['$scope', '$http', '$log', function($scope, $http, $log) {

    // sample valid name characters
    $scope.valid_chars = /^[\w !"#$%&'()*+,.-:;<>?@\/`=]+$/

    // diaplay names as they look in the directory
    $scope.wp = {
        fname: null,
        mname: null,
        lname: null,
    };
    // display names as they are edited
    $scope.pn = {
	display_fname: null,
	display_mname: null,
	display_lname: null,
    };

    $scope.putStatus = null;
    $scope.getPrefName = function() {
	$log.info('about to get '+ pdp_name_url);
	$http.get(pdp_name_url).success(function(data){
		$scope.pn = data;
                $scope.wp.fname = $scope.pn.display_fname;
                $scope.wp.mname = $scope.pn.display_mname;
                $scope.wp.lname = $scope.pn.display_lname;
	    });
    };
    $scope.putPrefName = function() {
        console.log('pub = ' + $scope.wp_publish);
	$log.info('about to put '+ pdp_name_url);
	$http.put(pdp_name_url, $scope.pn)
	.success(function(data){
		$scope.putStatus = 'Updated';
                $scope.getPrefName();
		$log.info($scope.putStatus);		
	    })
	.error(function(data){
		$scope.putStatus = 'Update failed';
		$log.info($scope.putStatus);
	    });
    };
    $scope.getPrefName();
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

