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

app.controller('NameCtrl', ['profileService', 'loginStatus', '$log', function (profileService, loginStatus, $log) {
    var _this = this;
    // sample valid name characters
    this.valid_chars = /^[\w !#$%&\'*+\-,.?^_`{}~]*$/;
    this.displayNameMax = 80;
    this.fieldMax = 64;
    this.displayName = '';
    this.displayCharsRemaining = this.displayNameMax;

    this.getDisplayNameFromObject = function (name) {
        return [name.first, name.middle, name.last]
            .filter(function(x){return x;})
            .join(' ');
    };
    this.updateDisplayName = function (name) {
        _this.displayName = _this.getDisplayNameFromObject(name);
        _this.displayCharsRemaining = _this.displayNameMax - _this.displayName.length;
    };
    this.getFieldMaxLength = function(text) {
        var totalMax = (text ? text.length : 0) + (_this.displayCharsRemaining > 0 ? _this.displayCharsRemaining : 0);
        return Math.min(totalMax, _this.fieldMax);
    };
}]);

