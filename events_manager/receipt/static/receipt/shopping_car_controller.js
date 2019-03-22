boleteria.controller('shoppingCarController',function($scope,$controller,$http){

    $scope.init = function(receipt,pay_method_list){
        $scope.receipt = receipt;
        $scope.pay_method_list = pay_method_list;
    }

    $scope.calculateValuesItem = function(index){
        $http({
            method: 'POST',
            url: '/receipt/update_item_shopping_car',
            data: {
                id: $scope.receipt.items[index].id,
                quantity: $scope.receipt.items[index].quantity
            }
        }).then(function(response){
            $scope.receipt.items[index].subtotal = $scope.receipt.items[index].quantity * $scope.receipt.items[index].price;
            $scope.receipt.items[index].tax = $scope.receipt.items[index].subtotal * $scope.receipt.tax_percentage;
            $scope.receipt.items[index].total = $scope.receipt.items[index].subtotal + $scope.receipt.items[index].tax;
            $scope.$parent.item_quantity = $scope.calculateTotal('quantity');
        },function(response){
            
        })
        
    }

    $scope.calculateTotal = function (property) {
        let subtotal = 0;
        $scope.receipt.items.forEach(element => {
            subtotal = subtotal + element[property];
        });
        return subtotal;
    }

    $scope.deleteItem = function(index){
        $http({
            method: 'POST',
            url: '/receipt/delete_item_shopping_car',
            data: {
                id: $scope.receipt.items[index].id
            }
        }).then(function(response){
            $scope.receipt.items[index].is_active = false;
            $scope.receipt.items = $scope.receipt.items.filter((element) => element.is_active);
            $scope.$parent.item_quantity = $scope.calculateTotal('quantity');
        },function(response){
            
        })
         
    }

});