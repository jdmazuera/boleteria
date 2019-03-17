boleteria.controller('shoppingCarController',function($scope,$http){

    $scope.init = function(shopping_car){
        $scope.shopping_car = shopping_car;
    }

    $scope.getTotalQuantity = function (total, item) {
        let total_quantity = 0;
        $scope.shopping_car.forEach(element => {
            total_quantity = total_quantity + element.quantity;
        });
        return total_quantity;
    }

    $scope.getSubtotal = function (total, item) {
        let subtotal = 0;
        $scope.shopping_car.forEach(element => {
            subtotal = subtotal + (element.price * element.quantity);
        });
        return subtotal;
    }

    $scope.getTax = function (total, item) {
        let tax = 0;
        $scope.shopping_car.forEach(element => {
            tax = tax + (element.price * element.quantity * element.tax);
        });
        return tax;
    }

    $scope.getTotal = function (total, item) {
        let tax = 0;
        $scope.shopping_car.forEach(element => {
            tax = tax + (element.price * element.quantity * (1 + element.tax));
        });
        return tax;
    }

    $scope.deleteItem = function(index_param){
        $http({
            method: 'POST',
            url: '/receipt/update_shopping_car',
            data: $scope.shopping_car[index_param].event_locality_id
        }).then(function(response){
            
        },function(response){
            
        })
        $scope.shopping_car = $scope.shopping_car.filter((element,index) => index_param!==index); 
    }

});