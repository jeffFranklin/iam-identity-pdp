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

app.controller('NameCtrl', ['profileService', 'loginStatus', '$log', function (profileService, loginStatus, $log) {
    var _this = this;
    // sample valid name characters
    this.valid_chars = /^[\w !#$%&\'*+\-,.?^_`{}~]*$/;
    this.displayNameMax = 80;
    this.fieldMax = 64;
    this.displayName = '';
    this.displayCharsRemaining = this.displayNameMax;

    // display names as they are edited
    this.netid = null;
    this.pn = { first: '', middle: '', last: ''};

    this.resetForm = function(netid, name){
        _this.putError = false;
        _this.netid = netid;
        _this.pn = name ? {first: name.first, middle: name.middle, last: name.last} : {};
    };
    this.getPrefName = function() {
        return profileService.getNetid().then(function (netid) {
            return profileService.getPreferredName(netid).then(function (name) {_this.resetForm(netid, name);});});
    };
    this.putPrefName = function(){
        _this.puttingPrefName = true;
        return profileService.putPreferredName(_this.netid, _this.pn)
            .then(function(name){
                if(!name){_this.putError = true}
                return name;
            })
            .finally(function(){_this.puttingPrefName = false;});
    };
    this.getDisplayNameFromObject = function (name) {
        return [name.first, name.middle, name.last]
            .filter(function(x){return x;})
            .join(' ');
    };
    this.updateDisplayName = function () {
        _this.displayName = _this.getDisplayNameFromObject(_this.pn);
        _this.displayCharsRemaining = _this.displayNameMax - _this.displayName.length;
    };
    this.getFieldMaxLength = function(text) {
        var totalMax = (text ? text.length : 0) + (_this.displayCharsRemaining > 0 ? _this.displayCharsRemaining : 0);
        return Math.min(totalMax, _this.fieldMax);
    };
    this.profilePutName = function(onPutSuccess){
        return _this.putPrefName().then(function(name){
            if(name){ onPutSuccess(name);}
        })
    };
}]);

