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
	    });
    };
    $scope.putPrefName = function() {
        console.log('pub = ' + $scope.wp_publish);
	$log.info('about to put '+ pdp_name_url);
	$http.put(pdp_name_url, $scope.pn)
	.success(function(data){
		$scope.putStatus = 'Updated';
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
                msg = JSON.parse(data)
                err_message = msg.message;
                console.log(err_message);
		$scope.putPubStatus = err_message;
		$log.info($scope.putPubStatus);
	    });
    };

}]);
