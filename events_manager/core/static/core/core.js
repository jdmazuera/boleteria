var boleteria = angular.module('boleteriaApp',['ngCookies','ngSanitize','chart.js','ui.grid', 'ui.grid.resizeColumns', 'ui.grid.pagination'], function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

boleteria.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';}
]);

boleteria.controller('boleteriaController',function($scope,$http){

    $scope.init = function(shopping_car){
        if(shopping_car){
            $scope.shopping_car = shopping_car;
            $scope.item_quantity = $scope.shopping_car.receipt_items_quantity;
        }
        
    }

    $scope.addToShoppingCar = function(event_locality){
        $http({
            method: 'POST',
            url: '/receipt/add_to_shopping_car',
            data: event_locality
        }).then(function(response){
            $scope.shopping_car = response.data;
            $scope.item_quantity = $scope.shopping_car.receipt_items_quantity;
            alertify.success('El item fue añadido al carrito')
        },function(response){
            
        })
    }

});