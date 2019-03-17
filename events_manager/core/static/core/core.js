var boleteria = angular.module('boleteriaApp',['ngCookies','ngSanitize'], function($interpolateProvider){
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
        $scope.shopping_car = shopping_car;
        if(shopping_car){
            $scope.item_quantity = $scope.calculateQuantity(shopping_car[1]);
        }
        
    }

    $scope.addToShoppingCar = function(event_locality){
        $http({
            method: 'POST',
            url: '/receipt/add_to_shopping_car',
            data: event_locality
        }).then(function(response){
            $scope.shopping_car = response.data;
            $scope.item_quantity = $scope.calculateQuantity($scope.shopping_car[1])
            alertify.notify('El item fue añadido al carrito')
        },function(response){
            
        })
    }

    $scope.calculateQuantity = function(shopping_car){
        var quantity = 0;
        shopping_car.forEach(function(item){
            quantity = quantity + item;
        });
        return quantity
    }

});