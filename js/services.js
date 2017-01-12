/**
 * Created by jiangweiwei on 16/11/29.
 */

var service = angular.module('WebService', ['ngResource']);

/**
 * 工厂类    将请求送到对应的api
 * DataForQuery  单条记录的增加  整个数据集合信息返回
 * DataForSingle 单条记录的删改查  注意id
 * DataForPagination 点击页面选择时刷新整个页面数据
*/

service.factory('DataForQuery', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/getinfo')
});

service.service('popupService',function($window){
    this.showPopup=function(message){
        return $window.confirm(message);
    }
});

service.factory('DataForSingle', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/getinfo/:id', {id: '@id'}, {
        update: {
            method: 'PUT' // this method issues a PUT request
        }
    })
});

service.factory('DataForPagination', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/getdata',
        {},
        {
            save: {
                method: 'POST',
                isArray: false
            }
        });
});

service.factory('AddAppVersion', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/add_version')
});

service.factory('CheckPass', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/login')
});

service.factory('LogInfo', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/log_server/:type',
        {},
        {
            save: {
                method: 'POST',
                isArray: false
            }
        })
});

service.factory('LogInfoInPage', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/log_server/check_for_current_page',
        {},
        {
            save: {
                method: 'POST',
                isArray: false
            }
        })
});

service.factory('LoginfoByPage', function ($resource) {
    return $resource('http://127.0.0.1:6234/api/v1/log_server/:pagenumber/:numPerPage',
        {},
        {
            save: {
                method: 'POST',
                isArray: false
            }
        })
});

service.factory('Base64', function () {
    /* jshint ignore:start */

    var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

    return {
        encode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            do {
                chr1 = input.charCodeAt(i++);
                chr2 = input.charCodeAt(i++);
                chr3 = input.charCodeAt(i++);

                enc1 = chr1 >> 2;
                enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                enc4 = chr3 & 63;

                if (isNaN(chr2)) {
                    enc3 = enc4 = 64;
                } else if (isNaN(chr3)) {
                    enc4 = 64;
                }

                output = output +
                    keyStr.charAt(enc1) +
                    keyStr.charAt(enc2) +
                    keyStr.charAt(enc3) +
                    keyStr.charAt(enc4);
                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";
            } while (i < input.length);

            return output;
        },

        decode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
            var base64test = /[^A-Za-z0-9\+\/\=]/g;
            if (base64test.exec(input)) {
                window.alert("There were invalid base64 characters in the input text.\n" +
                    "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                    "Expect errors in decoding.");
            }
            input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

            do {
                enc1 = keyStr.indexOf(input.charAt(i++));
                enc2 = keyStr.indexOf(input.charAt(i++));
                enc3 = keyStr.indexOf(input.charAt(i++));
                enc4 = keyStr.indexOf(input.charAt(i++));

                chr1 = (enc1 << 2) | (enc2 >> 4);
                chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                chr3 = ((enc3 & 3) << 6) | enc4;

                output = output + String.fromCharCode(chr1);

                if (enc3 != 64) {
                    output = output + String.fromCharCode(chr2);
                }
                if (enc4 != 64) {
                    output = output + String.fromCharCode(chr3);
                }

                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";

            } while (i < input.length);

            return output;
        }
    };

    /* jshint ignore:end */
});