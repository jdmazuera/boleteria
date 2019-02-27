

boleteria.controller('sellByEventController',function($scope,$http){

    $scope.init = function(initial_params){
        $scope.params = initial_params;
        $scope.filtros = {};
        $scope.graph = {
            data: [],
            labels: [],
            series: []
        }
    }

    $scope.fetchData = function(){
        $http({
            method: 'POST',
            url: '/report/sell_by_event',
            data: $scope.filtros
        }).then(function(response){
            $scope.graph = response.data;
        },function(response){
            
        })
    }

    $scope.cleanFilters = function(){
        $scope.filtros = {};
    }

});