// possible js tools for the project

// these are set by page load
var pdp_name_url = '/id/api/name';
var pdp_pub_url = '/id/api/publish';
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
		$scope.putStatus = 'Successful response from put';
		$log.info($scope.putStatus);		
	    })
	.error(function(data){
		$scope.putStatus = 'Successful response from put';
		$log.info($scope.putStatus);
	    });
    };
    $scope.getPrefName();
}]);


/* controller for the publish preference */

app.controller('PubCtrl', ['$scope', '$http', '$log', function($scope, $http, $log) {
    console.log('name url = ' + pdp_name_url);
    $scope.wp_publish = 'yes';
    $scope.putStatus = null;
    $scope.getPubPref = function() {
	$log.info('about to get '+ pdp_pub_url);
	$http.get(pdp_pub_url).success(function(data){
		$scope.pn = data;
	    });
    };
    $scope.putPubPref = function() {
        console.log('pub = ' + $scope.wp_publish);
        /*
	$log.info('about to put '+ pdp_pub_url);
	$http.put(pdp_pub_url, $scope.pn)
	.success(function(data){
		$scope.putStatus = 'Successful response from put';
		$log.info($scope.putStatus);		
	    })
	.error(function(data){
		$scope.putStatus = 'Successful response from put';
		$log.info($scope.putStatus);
	    });
        */
    };

    if (pdp_user_has_publish) {
        console.log('has publish');
        $scope.getPubPref();
    } else console.log('doen not haev publish');
}]);

