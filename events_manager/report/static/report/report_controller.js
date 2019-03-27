

boleteria.controller('sellByEventController',function($scope,$http){

    $scope.init = function(initial_params){
        $scope.params = initial_params;
        $scope.filtros = {};
        $scope.graph = {
            data: [],
            labels: [],
            series: []
        }
        $scope.series = ['Vendidos']
    }

    $scope.fetchData = function(){
        $http({
            method: 'POST',
            url: '/report/sell_by_event',
            data: $scope.filtros
        }).then(function(response){
            $scope.graph = response.data;
            $scope.graph.series = ['Vendidos']
        },function(response){
            
        })
    }

    $scope.cleanFilters = function(){
        $scope.filtros = {};
    }

});

boleteria.controller('topCostumerController',function($scope,$http){

    $scope.init = function(initial_params){
        $scope.params = initial_params;
        $scope.filtros = {};
        $scope.graph = {
            data: [],
            labels: [],
            series: []
        }
        $scope.series = ['Vendidos']
        $scope.options = { legend: { display: false } };
    }

    $scope.fetchData = function(){
        $http({
            method: 'POST',
            url: '/report/top_costumers',
            data: $scope.filtros
        }).then(function(response){
            $scope.graph = response.data;
            $scope.graph.series = ['Vendidos']
            $scope.graph.options = { legend: { display: false } };
        },function(response){
            
        })
    }

    $scope.cleanFilters = function(){
        $scope.filtros = {};
    }

});

boleteria.controller('summarizeEventLocalityController',function($scope,$http){

    $scope.init = function(initial_params){
        $scope.params = initial_params;
        $scope.filtros = {};
        $scope.gridObject = {
            data: [],
            enableFiltering: true,
            showGridFooter: true,
            showColumnFooter: true,
            paginationPageSizes: [10, 20, 30],
            paginationPageSize: 10,
            columnDefs: [
                {
                    field: 'event__name',
                    displayName: 'Evento',
                    width:'15%',
                    headerCellClass:'text-center'
                },
                {
                    field: 'locality__name',
                    displayName: 'Localidad',
                    width:'15%',
                    headerCellClass:'text-center'
                },
                {
                    field: 'capacity',
                    displayName: 'Capacidad',
                    width:'15%',
                    headerCellClass:'text-center',
                    aggregationType : 2,
                    aggregationLabel : ' ',
                    cellClass : ' text-right',
                    footerCellClass : 'text-right'
                },
                {
                    field: 'availability',
                    displayName: 'Disponibilidad',
                    width:'15%',
                    headerCellClass:'text-center',
                    aggregationType : 2,
                    aggregationLabel : ' ',
                    cellClass : ' text-right',
                    footerCellClass : 'text-right'
                },
                {
                    field: 'sold',
                    displayName: 'Vendidos',
                    width:'15%',
                    headerCellClass:'text-center',
                    aggregationType : 2,
                    aggregationLabel : ' ',
                    cellClass : ' text-right',
                    footerCellClass : 'text-right'
                },
                {
                    field: 'percentage_occupation',
                    displayName: 'Porcentage De Ocupación',
                    width:'25%',
                    headerCellClass:'text-center',
                    cellClass : ' text-right',
                    cellFilter : 'number:2',
                    footerCellClass : 'text-right',
                    footerCellFilter : 'number:2'
                }
            ]    
        }
    }

    $scope.fetchData = function(){
        $http({
            method: 'POST',
            url: '/report/summerize_event_locality',
            data: $scope.filtros
        }).then(function(response){
            $scope.gridObject.data = response.data;
        },function(response){
            
        })
    }

    $scope.cleanFilters = function(){
        $scope.filtros = {};
    }

});

boleteria.controller('paretoCostumersController',function($scope,$http,$window){

    $scope.init = function(initial_params){
        $scope.params = initial_params;
        $scope.filtros = {};
        
        var ctx = document.getElementById('pareto_costumers_chart').getContext('2d');

        $window.chart_object = new Chart(ctx, {
            type: 'bar',
            data: [],
            options: {
                title: {
                    display: true,
                    text: 'Clientes Pareto'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        stacked: true,
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                }
            }
        });

    }

    $scope.fetchData = function(){
        $http({
            method: 'POST',
            url: '/report/pareto_costumers',
            data: $scope.filtros
        }).then(function(response){
            $window.chart_object.data = response.data;
            $window.chart_object.update();
        },function(response){
            
        })
    }

    $scope.cleanFilters = function(){
        $scope.filtros = {};
    }

});