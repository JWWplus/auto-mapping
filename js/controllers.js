/**
 * Created by jiangweiwei on 16/11/29.
 */

angular.module('WebCtr', ['ui.bootstrap']).controller('DataListCtr', function (
    $scope,$rootScope,$state,popupService,$window,DataForQuery,DataForSingle,DataForPagination,LogInfo,LogInfoInPage) {

    $scope.DataInfo = DataForQuery.get();
    $scope.curPage = $rootScope.currentPage;
    $scope.AppVersion = $rootScope.AppVersion;
    $scope.platform = $rootScope.platform;
    $scope.event = $rootScope.event;
    $scope.page = $rootScope.page;
    $scope.maxSize = 10;
    $scope.numPerPage = 15;
    $scope.curLogPage = 1;

    $scope.ClickLogPagination = function (oid) {
        $scope.loginfo = new LogInfoInPage();
        $scope.loginfo.oid = oid;
        $scope.logdatas = LogInfoInPage.save($scope.loginfo, function () {

        })
    };

    //点击提交触发的事件
    $scope.selectData =function () {
        //将数据保存到rootScope中
        $rootScope.AppVersion = $scope.AppVersion ;
        $rootScope.platform = $scope.platform;
        $rootScope.event = $scope.event;
        $rootScope.page = $scope.page;

        $scope.Datas = new DataForPagination();
        $scope.Datas.AppVersion = $scope.AppVersion;
        $scope.Datas.platform = $scope.platform;
        $scope.Datas.event = $scope.event;
        $scope.Datas.page = $scope.page;
        $scope.Datas.curPage = 1 ;
        $scope.Datas.numPerPage = $scope.numPerPage;
        $scope.datas = DataForPagination.save($scope.Datas, function () {
            var oid = [];
            for (var i=0;i<$scope.datas.resp.length; i++){
                oid.push($scope.datas.resp[i].id)
            }
            $scope.ClickLogPagination(oid);
            // 由于重定向到data页后会自动跳转到第一页   因此在返回后重新跳回原先选择页
            $scope.AppVersion = $rootScope.AppVersion;
            $scope.platform = $rootScope.platform;
            $scope.event = $rootScope.event;
            $scope.curPage = 1;
        })
    };

    //单击删除按钮触发的事件
    $scope.DeleteData = function (data) {
        if (popupService.showPopup('确定删除该记录吗?')){
            var time = new Date();
            $scope.delete_log = new LogInfo();
            $scope.delete_log.username = $rootScope.username;
            $scope.delete_log.time = time.toLocaleString();//否则返回的是GMT时间
            $scope.delete_log.logtype = '删除单条数据';
            $scope.delete_log.id = data.id;
            $scope.delete_log.$save({type:'Delete'}, function () {
                DataForSingle.delete({id:data.id}, function () {
                    $scope.ClickPagination(); //刷新数据
                    $scope.DataInfo = DataForQuery.get();
                })
            });
        }
    };
    //点击页码标签触发的事件
    $scope.ClickPagination = function () {
        //将数据保存到rootScope中
        $rootScope.currentPage = $scope.curPage;
        $rootScope.AppVersion = $scope.AppVersion ;
        $rootScope.platform = $scope.platform;
        $rootScope.event = $scope.event;
        $rootScope.page = $scope.page;

        $scope.Datas = new DataForPagination();
        $scope.Datas.curPage = $scope.curPage;
        $scope.Datas.numPerPage = $scope.numPerPage;
        $scope.Datas.AppVersion = $scope.AppVersion;
        $scope.Datas.platform = $scope.platform;
        $scope.Datas.event = $scope.event;
        $scope.Datas.page = $scope.page;

        $scope.datas = DataForPagination.save($scope.Datas, function () {
            var oid = [];
            for (var i=0;i<$scope.datas.resp.length; i++){
                oid.push($scope.datas.resp[i].id)
            }
            $scope.ClickLogPagination(oid);
            // 由于重定向到data页后会自动跳转到第一页   因此在返回后重新跳回原先选择页
            $scope.curPage = $rootScope.currentPage;
            $scope.AppVersion = $rootScope.AppVersion;
            $scope.platform = $rootScope.platform;
            $scope.event = $rootScope.event;
            $scope.page = $rootScope.page;
        });
    };

    $scope.ClickPagination();

}).controller('EditCtr', function ($scope,$rootScope,$state,$stateParams,DataForSingle,DataForQuery) {

    $scope.DataInfo = DataForQuery.get();
    $scope.updateData = function () {
        var time = new Date();
        $scope.data.username = $rootScope.username;
        $scope.data.time = time.toLocaleString();//否则返回的是GMT时间
        $scope.data.logtype = '编辑单条数据';
        $scope.data.$update(function () {
            $state.go('DataList');
        })
    };

    $scope.loadData = function () {
        $scope.data = DataForSingle.get({id: $stateParams.id});
    };

    $scope.BackToHome = function () {
        $state.go('DataList')
    };

    $scope.loadData();
}).controller('AddCtr', function ($scope,$rootScope,$state,$stateParams,DataForQuery) {

    $scope.DataInfo = DataForQuery.get();
    $scope.data = new DataForQuery();
    $scope.data.appversion = $rootScope.AppVersion;
    $scope.data.platform = $rootScope.platform;
    $scope.data.page = $rootScope.page;
    $scope.data.event = $rootScope.event;

    $scope.BackToHome = function () {
        $state.go('DataList')
    };

    $scope.addData = function () {
        var time = new Date();
        $scope.data.username = $rootScope.username;
        $scope.data.time = time.toLocaleString();//否则返回的是GMT时间
        $scope.data.logtype = '增加单条数据';
        $scope.data.$save(function () {
            $state.go('DataList')
        })
    }
}).controller('Add_version', function ($scope,$rootScope,$state,$stateParams,AddAppVersion,DataForQuery,popupService,LogInfo) {
    $scope.ver = new AddAppVersion();
    var versionlist = [];
    $scope.DataInfo = DataForQuery.get({}, function () {
        for (var i=0; i<$scope.DataInfo.appversion.length; i++ ){
            versionlist.push($scope.DataInfo.appversion[i].app_version)
        }
    });

    $scope.BackToHome = function () {
        $state.go('DataList')
    };

    $scope.Addver = function () {
        if (versionlist.indexOf($scope.ver.appversion) != -1){
            popupService.showPopup('该版本号已存在，请重新输入！')
        }
        else {
            var time = new Date();
            $scope.ver.username = $rootScope.username;
            $scope.ver.time = time.toLocaleString();//否则返回的是GMT时间
            $scope.ver.logtype = '增加新版本';
            AddAppVersion.save($scope.ver, function () {
                $state.go('DataList')
            });
        }
    }
}).controller('LoginCtr', function ($scope,$rootScope,$state,CheckPass,popupService,Base64,$cookieStore,$http) {
    $scope.username = '';
    $scope.password = '';
    $scope.userrole = '';
    $rootScope.username = '';
    //登陆按钮函数
    $scope.login =function () {
        $scope.LoginInfo = new CheckPass();
        $scope.LoginInfo.username = $scope.username;
        $scope.LoginInfo.password = $scope.password;

        //由于是异步返回    因此判定条件必须要放在func里面   不然在判定的时候result为空
        result = CheckPass.save($scope.LoginInfo, function () {
            if (result.status == -1){
                popupService.showPopup('用户名/密码不正确 请重新输入！')
            }
            else {
                $scope.SetCredentials($scope.username, $scope.password, result.role);
                $rootScope.username = $scope.username;
                $rootScope.userrole = result.role;
                $state.go('DataList')
            }
        });
    };
    //保存参数到cookies 并建立Auth
    $scope.SetCredentials = function (username, password, role) {
        var authdata = Base64.encode(username + ':' + password + ":" + role);

        $rootScope.globals = {
            currentUser: {
                username: username,
                role: role,
                authdata: authdata
            }
        };

        $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata; // jshint ignore:line
        $cookieStore.put('globals', $rootScope.globals);
    };
    //清除cookies
    $scope.ClearCredentials = function () {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
        $http.defaults.headers.common.Authorization = 'Basic ';
    };
    //跳转到登录页面自动清空
    $scope.ClearCredentials();
}).controller('LogCtr', function ($scope, $rootScope, popupService, $state, LoginfoByPage) {
    $scope.maxSize = 10;
    $scope.numPerPage = 50;
    $scope.curLogPage = 1;
    if (!$rootScope.username){
        popupService.showPopup('请先登录');
        $state.go('Login')
    }

    $scope.ClickPagination = function () {
        $scope.datas = LoginfoByPage.get({
            pagenumber:$scope.curLogPage,
            numPerPage:$scope.numPerPage
        })
    };

    $scope.BackToHome = function () {
        $state.go('DataList')
    };

    $scope.ClickPagination()
});
