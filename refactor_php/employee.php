<?php
include 'database.php';


class Employee
{
    private $db;

    public function __construct($db)
    {
        if (!$db) {
            throw new Exception("Conexión a la base de datos fallida.");
        }
        $this->db = $db;
    }

    public function getEmployeeDetails($employee_id, $company_id)
    {
        $sql_query = "SELECT * FROM employee WHERE id = ? AND company_id = ?";

        if ($prepared_statement = mysqli_prepare($this->db, $sql_query)) {
            mysqli_stmt_bind_param($prepared_statement, "ii", $employee_id, $company_id);
            mysqli_stmt_execute($prepared_statement);
            $result = mysqli_stmt_get_result($prepared_statement);

            if ($result && mysqli_num_rows($result) > 0) {
                return mysqli_fetch_assoc($result);
            } else {
                return null;
            }
        } else {
            throw new Exception("Error al preparar la consulta SQL.");
        }
    }

    public function getEmployeeSubclass($table_name, $employee_id, $company_id)
    {
        $allowed_tables = [
            'employee_position',
            'employee_salary',
            'employee_dependent',
            'employee_emergency_contact',
            'employee_education',
            'performance_review',
            'employee_status'
        ];

        if (!in_array($table_name, $allowed_tables)) {
            throw new Exception("Tabla no permitida: " . htmlspecialchars($table_name));
        }

        $sql_query = "SELECT * FROM " . mysqli_real_escape_string($this->db, $table_name) . " WHERE employee_id = ? AND company_id = ?";

        if ($prepared_statement = mysqli_prepare($this->db, $sql_query)) {
            mysqli_stmt_bind_param($prepared_statement, "ii", $employee_id, $company_id);
            mysqli_stmt_execute($prepared_statement);
            $result = mysqli_stmt_get_result($prepared_statement);

            if ($result) {
                $detail_subclass = [];
                while ($row = mysqli_fetch_assoc($result)) {
                    $detail_subclass[] = $row;
                }
                return $detail_subclass;
            } else {
                return [];
            }
        } else {
            throw new Exception("Error al preparar la consulta de salario.");
        }
    }
}

try {
    function jsonResponse($status, $message, $data = null)
        {
            header('Content-Type: application/json');
            echo json_encode([
                'status' => $status,
                'message' => $message,
                'data' => $data
            ]);
            exit();
        }

    $db_connection = (new Database())->getConnection(); 

    if (!$db_connection) {
        throw new Exception('No se pudo establecer una conexión a la base de datos.');
    }

    $employee = new Employee($db_connection);
    
    if (isset($_GET['employee_id']) && isset($_GET['company_id'])) {
        $employee_id = intval($_GET['employee_id']);
        $company_id = intval($_GET['company_id']);

        $employee_details = $employee->getEmployeeDetails($employee_id, $company_id);

        if ($employee_details) {
            $employee_details['employee_positions'] = $employee->getEmployeeSubclass('employee_position', $employee_id, $company_id);
            $employee_details['previous_salaries'] = $employee->getEmployeeSubclass('employee_salary', $employee_id, $company_id);
            $employee_details['dependents'] = $employee->getEmployeeSubclass('employee_dependent', $employee_id, $company_id);
            $employee_details['emergency_contact'] = $employee->getEmployeeSubclass('employee_emergency_contact', $employee_id, $company_id);
            $employee_details['education'] = $employee->getEmployeeSubclass('employee_education', $employee_id, $company_id);
            $employee_details['performance_reviews'] = $employee->getEmployeeSubclass('performance_review', $employee_id, $company_id);
            $employee_details['employee_status'] = $employee->getEmployeeSubclass('employee_status', $employee_id, $company_id);

            jsonResponse('éxito', 'Empleado encontrado', $employee_details);
        } else {
            jsonResponse('error', "No se encontró ningún empleado con ID: $employee_id o empresa con ID: $company_id.");
        }
    } else {
        jsonResponse('error', 'No se proporcionó el ID del empleado o el ID de la empresa.');
    }

    $db->close();
} catch (Exception $e) {
    jsonResponse('error', 'Ocurrió un error inesperado: ' . $e->getMessage());
}
