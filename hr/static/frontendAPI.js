/**
 * Created by sam on 4/3/17.
 */
<script>
    angular.module('MyApp', [])
        .controller('MyCtrl', ['$scope', '$http', function ($scope, $http) {
            $scope.allEmployees = " ";
            $scope.postedEmployee = " ";
            $scope.singleEmployee = " ";
            $scope.deletedEmployee = " ";
            $scope.patchedEmployee = " ";


            $scope.getAllEmployees = function () {

                $http.get("employee")
                    .then(function (response) {
                        $scope.allEmployees = JSON.stringify( response.data,null,3);
                    });
            }

            $scope.getEmployee = function (eId) {
                if (eId) {
                    $http.get("employee?employee_id=" + eId)
                        .then(function (response) {
                            $scope.singleEmployee = JSON.stringify(response.data,null,3);
                        }, function (response) {
                            alert(response.data.detail)
                        });
                }

            }

            $scope.postEmployee = function (isValid) {
                if (isValid) {
                    $http({
                        url: 'employee',
                        method: "POST",
                        data: {
                            "is_active": $scope.postIsActive,
                            "name": $scope.postName,
                            "birth_date": $scope.postDOB,
                            "address": $scope.postAddress,
                            "department": $scope.postDepartment,
                            "role": $scope.postRole,
                            "team_start_date": $scope.postTeamStartDate,
                            "company_start_date": $scope.postCompanyStartDate
                        }
                    })
                        .then(function (response) {
                            $scope.postedEmployee = JSON.stringify(response.data,null,3);
                        });
                }
            }
            $scope.patchEmployee = function () {
                var data = {"employee_id": +$scope.patchEmployeeId};
                if ($scope.patchName) {
                    data["name"] = $scope.patchName;
                }
                if ($scope.patchDOB) {
                    data["birth_date"] = $scope.patchDOB;
                }
                if ($scope.patchAddress) {
                    data["address"] = $scope.patchAddress;
                }
                if ($scope.patchDepartment) {
                    data["department"] = $scope.patchDepartment;
                }
                if ($scope.patchRole) {
                    data["role"] = $scope.patchRole;
                }
                if ($scope.patchTeamStartDate) {
                    data["team_start_date"] = $scope.patchTeamStartDate;
                }
                if ($scope.patchCompanyStartDate) {
                    data["company_start_date"] = $scope.patchCompanyStartDate;
                }
                $http({
                    url: 'employee',
                    method: "PATCH",
                    data: data
                })
                    .then(function (response) {
                        $scope.patchedEmployee =JSON.stringify(response.data,null,3);
                    });
            }
            $scope.deleteEmployee = function (eId) {
                if (eId) {
                    $http.delete("employee?employee_id=" + eId)
                        .then(function (response) {
                            $scope.deletedEmployee = JSON.stringify(response.data,null,3);
                        }, function (response) {
                            alert(response.data.detail)
                        });
                }
            }
        }]);
    </script>